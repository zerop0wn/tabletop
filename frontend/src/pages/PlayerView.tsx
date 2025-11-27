import { useEffect, useState, useRef } from 'react'
import { useParams } from 'react-router-dom'
import apiClient from '../api/client'
import { PlayerState } from '../types'

interface ActionInfo {
  name: string
  description: string
}

const BLUE_TEAM_ACTIONS: ActionInfo[] = [
  {
    name: 'Isolate host',
    description: 'Disconnect the compromised host from the network to prevent further spread of the attack. This stops lateral movement but may alert the attacker.'
  },
  {
    name: 'Block IP address',
    description: 'Block the attacker\'s IP address at the firewall or network perimeter. Effective for known malicious IPs but may be bypassed if attacker changes IPs.'
  },
  {
    name: 'Collect forensic evidence',
    description: 'Gather logs, memory dumps, and system artifacts for analysis. Critical for understanding the attack but takes time and may not stop immediate threats.'
  },
  {
    name: 'Deploy countermeasures',
    description: 'Implement security controls like patches, endpoint protection, or network segmentation. Proactive defense but may impact system availability.'
  },
  {
    name: 'Escalate to management',
    description: 'Notify leadership and activate incident response procedures. Ensures proper coordination but may slow immediate response actions.'
  },
]

const RED_TEAM_ACTIONS: ActionInfo[] = [
  {
    name: 'Establish persistence',
    description: 'Create backdoors, scheduled tasks, or service accounts to maintain access even if initial entry point is discovered. High risk if detected.'
  },
  {
    name: 'Escalate privileges',
    description: 'Gain administrator or root-level access through privilege escalation exploits. Unlocks more system capabilities but increases detection risk.'
  },
  {
    name: 'Move laterally',
    description: 'Spread from the initial compromised system to other systems on the network. Expands attack surface but creates more forensic evidence.'
  },
  {
    name: 'Exfiltrate data',
    description: 'Steal sensitive data from compromised systems. High-value objective but network monitoring may detect large data transfers.'
  },
  {
    name: 'Cover tracks',
    description: 'Delete logs, clear command history, and remove forensic artifacts. Reduces detection but suspicious log gaps may be noticed.'
  },
]

export default function PlayerView() {
  const { gameId, playerId } = useParams<{ gameId: string; playerId: string }>()
  const [state, setState] = useState<PlayerState | null>(null)
  const [selectedAction, setSelectedAction] = useState<string>('')
  const [effectivenessRating, setEffectivenessRating] = useState<number | null>(null)
  const [comments, setComments] = useState('')
  const [submitting, setSubmitting] = useState(false)
  const [submitted, setSubmitted] = useState(false)

  useEffect(() => {
    if (!gameId || !playerId) return
    fetchState()
    const interval = setInterval(fetchState, 8000) // Poll every 8 seconds
    return () => clearInterval(interval)
  }, [gameId, playerId])

  // Track previous phase ID to detect phase changes
  const prevPhaseIdRef = useRef<number | null>(null)
  const prevHasVotedRef = useRef<boolean>(false)

  useEffect(() => {
    if (!state) return

    const currentPhaseId = state.current_phase?.id || null
    const hasVoted = state.has_voted || false
    const phaseChanged = prevPhaseIdRef.current !== currentPhaseId
    const voteStatusChanged = prevHasVotedRef.current !== hasVoted

    // Only reset form if phase changed or vote status changed
    if (phaseChanged || voteStatusChanged) {
      if (hasVoted) {
        // Get the player's vote from voting status
        const myVote = state.team_voting_status?.votes.find(v => v.player_id === parseInt(playerId || '0'))
        if (myVote) {
          setSelectedAction(myVote.selected_action)
          setEffectivenessRating(myVote.effectiveness_rating || 5)
          setComments(myVote.comments || '')
        }
        setSubmitted(true)
      } else if (state.decision) {
        // Legacy: if decision exists, show it
        setSelectedAction(state.decision.actions?.selected?.[0] || '')
        setEffectivenessRating(null)
        setComments('')
        setSubmitted(true)
      } else if (state.phase_state === 'open_for_decisions') {
        // Only reset if phase changed and we're in voting state
        if (phaseChanged) {
          setSubmitted(false)
          setSelectedAction('')
          setEffectivenessRating(null)
          setComments('')
        }
        // Don't reset if phase didn't change - preserve user's input
      } else {
        // Phase is not open for decisions
        setSubmitted(false)
        setSelectedAction('')
        setEffectivenessRating(null)
        setComments('')
      }

      // Update refs
      prevPhaseIdRef.current = currentPhaseId
      prevHasVotedRef.current = hasVoted
    } else if (hasVoted) {
      // If we have a vote, make sure we're showing it (in case vote data updated)
      const myVote = state.team_voting_status?.votes.find(v => v.player_id === parseInt(playerId || '0'))
      if (myVote) {
        setSelectedAction(myVote.selected_action)
        setEffectivenessRating(myVote.effectiveness_rating || 5)
        setComments(myVote.comments || '')
      }
    }
  }, [state, playerId])

  const fetchState = async () => {
    try {
      const response = await apiClient.get<PlayerState>(
        `/games/${gameId}/player/${playerId}/state`
      )
      setState(response.data)
    } catch (err) {
      console.error('Failed to fetch state:', err)
    }
  }

  const handleSubmit = async () => {
    if (!gameId || !playerId || !state?.current_phase) return
    if (!selectedAction) {
      alert('Please select an action to vote for')
      return
    }
    if (!effectivenessRating || effectivenessRating < 1 || effectivenessRating > 10) {
      alert('Please select an effectiveness rating (1-10) before submitting your vote')
      return
    }

    setSubmitting(true)
    try {
      await apiClient.post(`/games/${gameId}/phases/${state.current_phase.id}/votes`, {
        player_id: parseInt(playerId),
        selected_action: selectedAction,
        effectiveness_rating: effectivenessRating,
        comments: comments || null,
      })
      setSubmitted(true)
      fetchState()
    } catch (err: any) {
      alert(err.response?.data?.detail || 'Failed to submit vote')
    } finally {
      setSubmitting(false)
    }
  }

  if (!state) {
    return <div className="p-8">Loading...</div>
  }

  const canSubmit = state.phase_state === 'open_for_decisions' && !submitted

  // Get team-specific actions
  const availableActions = state.team_role === 'red' ? RED_TEAM_ACTIONS : BLUE_TEAM_ACTIONS

  const teamBgColor = state.team_role === 'red' ? 'bg-red-50 border-red-200' : 'bg-blue-50 border-blue-200'
  const teamTextColor = state.team_role === 'red' ? 'text-red-800' : 'text-blue-800'
  const teamBadgeColor = state.team_role === 'red' ? 'bg-red-600' : 'bg-blue-600'

  return (
    <div className="min-h-screen bg-gray-50 p-8">
      <div className="max-w-4xl mx-auto">
        <div className="flex items-center justify-between mb-6">
          <h1 className="text-3xl font-bold">Team Decision Pad</h1>
          {state.team_name && state.team_role && (
            <div className={`px-4 py-2 rounded-lg ${teamBadgeColor} text-white font-semibold`}>
              {state.team_name} Team ({state.team_role.toUpperCase()})
            </div>
          )}
        </div>

        {/* Phase Info */}
        {state.current_phase && (
          <div className="bg-white rounded-lg shadow-md p-6 mb-6">
            <h2 className="text-2xl font-bold mb-2">{state.current_phase.name}</h2>
            <p className="text-sm text-gray-500 mb-4">Status: {state.phase_state}</p>
            {state.phase_briefing_text && (
              <div className="mb-4">
                <h3 className="font-semibold mb-2">Briefing:</h3>
                <p className="text-gray-700">{state.phase_briefing_text}</p>
              </div>
            )}
            {state.team_objective && (
              <div className={`mb-4 p-4 ${teamBgColor} border-2 rounded-md`}>
                <h3 className={`font-semibold mb-2 ${teamTextColor}`}>Your Objective ({state.team_name || state.team_role?.toUpperCase()} Team):</h3>
                <p className="text-gray-700">{state.team_objective}</p>
              </div>
            )}
          </div>
        )}

        {/* Artifacts */}
        {state.artifacts.length > 0 && (
          <div className="bg-white rounded-lg shadow-md p-6 mb-6">
            <h2 className="text-xl font-bold mb-4">Artifacts</h2>
            <div className="space-y-4">
              {state.artifacts.map((artifact) => {
                const isImage = artifact.type === 'screenshot' || artifact.file_url?.match(/\.(jpg|jpeg|png|gif|webp)$/i)
                // Use the file_url as-is, the proxy will handle /api/artifacts/files/ requests
                const artifactUrl = artifact.file_url || ''
                
                return (
                  <div key={artifact.id} className="border border-gray-200 rounded-md p-4">
                    <div className="flex items-start justify-between mb-2">
                      <div>
                        <h3 className="font-semibold mb-1">{artifact.name}</h3>
                        <span className="text-xs text-gray-500 bg-gray-100 px-2 py-1 rounded">{artifact.type}</span>
                      </div>
                    </div>
                    {artifact.description && (
                      <p className="text-sm text-gray-600 mb-3">{artifact.description}</p>
                    )}
                    {artifact.file_url && (
                      <div className="mt-3">
                        {isImage ? (
                          <div>
                            <img
                              src={artifactUrl}
                              alt={artifact.name}
                              className="max-w-full h-auto rounded-md border border-gray-300 mb-2"
                              onError={(e) => {
                                // Fallback if image fails to load
                                const target = e.target as HTMLImageElement
                                target.style.display = 'none'
                                const parent = target.parentElement
                                if (parent && artifactUrl) {
                                  const link = document.createElement('a')
                                  link.href = artifactUrl
                                  link.target = '_blank'
                                  link.className = 'text-blue-600 hover:text-blue-800 text-sm'
                                  link.textContent = 'View Artifact →'
                                  parent.appendChild(link)
                                }
                              }}
                            />
                            <a
                              href={artifactUrl}
                              target="_blank"
                              rel="noopener noreferrer"
                              className="text-blue-600 hover:text-blue-800 text-sm"
                            >
                              Open in new tab →
                            </a>
                          </div>
                        ) : (
                          <a
                            href={artifactUrl}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="text-blue-600 hover:text-blue-800 text-sm inline-flex items-center"
                          >
                            <span>View Artifact</span>
                            <svg className="w-4 h-4 ml-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
                            </svg>
                          </a>
                        )}
                      </div>
                    )}
                  </div>
                )
              })}
            </div>
          </div>
        )}

        {/* Decision Form */}
        {state.phase_state === 'briefing' && (
          <div className="bg-yellow-50 border border-yellow-200 rounded-md p-4">
            <p className="text-yellow-800">Waiting for GM to open decisions...</p>
          </div>
        )}

        {canSubmit && (
          <div className="bg-white rounded-lg shadow-md p-6">
            <h2 className="text-xl font-bold mb-4">Cast Your Vote</h2>

            {/* Voting Status */}
            {state.team_voting_status && (
              <div className="mb-6 p-4 bg-gray-50 rounded-md">
                <h3 className="font-semibold mb-2">Team Voting Status</h3>
                <p className="text-sm text-gray-600">
                  {state.team_voting_status.votes_submitted} of {state.team_voting_status.total_players} players have voted
                  {state.team_voting_status.all_voted && (
                    <span className="ml-2 text-green-600 font-semibold">✓ All votes submitted!</span>
                  )}
                </p>
                {state.team_voting_status.votes.length > 0 && (
                  <div className="mt-3 space-y-1">
                    {state.team_voting_status.votes.map((vote) => (
                      <div key={vote.id} className="text-xs text-gray-500">
                        <span className="font-medium">{vote.player_name}</span>: {vote.selected_action}
                      </div>
                    ))}
                  </div>
                )}
              </div>
            )}

            <div className="mb-6">
              <h3 className="font-semibold mb-3">
                Select Action ({state.team_role === 'red' ? 'Red Team' : 'Blue Team'}):
              </h3>
              <div className="space-y-3">
                {availableActions.map((action) => (
                  <label key={action.name} className="flex items-start space-x-3 cursor-pointer p-3 border border-gray-200 rounded-lg hover:bg-gray-50 hover:border-gray-300 transition-colors">
                    <input
                      type="radio"
                      name="action"
                      value={action.name}
                      checked={selectedAction === action.name}
                      onChange={(e) => setSelectedAction(e.target.value)}
                      className={`mt-1 w-4 h-4 ${state.team_role === 'red' ? 'text-red-600' : 'text-blue-600'}`}
                    />
                    <div className="flex-1">
                      <div className="font-medium text-gray-900">{action.name}</div>
                      <div className="text-sm text-gray-600 mt-1">{action.description}</div>
                    </div>
                  </label>
                ))}
              </div>
            </div>

            <div className="mb-6">
              <label className="block font-semibold mb-3">
                How effective do you believe your organization would be at detecting and responding to this phase? <span className="text-red-500">*</span>
              </label>
              <div className="grid grid-cols-5 gap-2">
                {[1, 2, 3, 4, 5, 6, 7, 8, 9, 10].map((rating) => (
                  <label
                    key={rating}
                    className={`flex flex-col items-center justify-center p-3 border-2 rounded-lg cursor-pointer transition-all ${
                      effectivenessRating === rating
                        ? 'border-blue-600 bg-blue-50 text-blue-700'
                        : 'border-gray-200 hover:border-gray-300 hover:bg-gray-50'
                    }`}
                  >
                    <input
                      type="radio"
                      name="effectivenessRating"
                      value={rating}
                      checked={effectivenessRating === rating}
                      onChange={() => setEffectivenessRating(rating)}
                      className="sr-only"
                      required
                    />
                    <span className="text-xl font-bold">{rating}</span>
                    <span className="text-xs text-gray-600 mt-1">
                      {rating === 1 && 'Least'}
                      {rating === 10 && 'Most'}
                    </span>
                  </label>
                ))}
              </div>
              <div className="flex justify-between mt-2 text-xs text-gray-500">
                <span>1 = Least Likely</span>
                <span>10 = Highly Likely</span>
              </div>
              {effectivenessRating === null && (
                <p className="text-sm text-red-500 mt-2">Please select a rating before submitting</p>
              )}
            </div>

            <div className="mb-6">
              <label className="block font-semibold mb-2">
                Comments (Optional, max 500 characters)
              </label>
              <textarea
                value={comments}
                onChange={(e) => {
                  if (e.target.value.length <= 500) {
                    setComments(e.target.value)
                  }
                }}
                className="w-full px-3 py-2 border border-gray-300 rounded-md"
                rows={4}
                maxLength={500}
                placeholder="Add your comments here..."
              />
              <div className="text-sm text-gray-500 mt-1">
                {comments.length}/500 characters
              </div>
            </div>

            <button
              onClick={handleSubmit}
              disabled={submitting || !selectedAction || !effectivenessRating || effectivenessRating < 1 || effectivenessRating > 10}
              className="w-full bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700 disabled:bg-gray-400"
            >
              {submitting ? 'Submitting...' : submitted ? 'Update Vote' : 'Submit Vote'}
            </button>
          </div>
        )}

        {submitted && state.phase_state !== 'open_for_decisions' && (
          <div className="bg-white rounded-lg shadow-md p-6">
            <h2 className="text-xl font-bold mb-4">Your Vote</h2>
            <div className="mb-4">
              <h3 className="font-semibold mb-2">Selected Action:</h3>
              <p className="text-gray-700">{selectedAction}</p>
            </div>
            <div className="mb-4">
              <h3 className="font-semibold mb-2">Effectiveness Rating:</h3>
              <p className="text-gray-700">{effectivenessRating !== null ? `${effectivenessRating}/10` : 'Not rated'}</p>
            </div>
            {comments && (
              <div>
                <h3 className="font-semibold mb-2">Comments:</h3>
                <p className="text-gray-700">{comments}</p>
              </div>
            )}
            {state.phase_state === 'decision_lock' && (
              <p className="mt-4 text-gray-600">Voting closed. Waiting for resolution...</p>
            )}
            {state.decision && (
              <div className="mt-4 p-4 bg-blue-50 rounded-md">
                <h3 className="font-semibold mb-2">Team Decision:</h3>
                <p className="text-gray-700">{state.decision.actions?.selected?.[0] || 'N/A'}</p>
                {state.decision.actions?.vote_counts && (
                  <div className="mt-2 text-sm text-gray-600">
                    <p>Vote breakdown:</p>
                    <ul className="list-disc list-inside ml-2">
                      {Object.entries(state.decision.actions.vote_counts).map(([action, count]) => (
                        <li key={action}>{action}: {count as number} vote{(count as number) !== 1 ? 's' : ''}</li>
                      ))}
                    </ul>
                  </div>
                )}
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  )
}

