import { useEffect, useState } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import apiClient from '../api/client'
import { Game, Decision, VotingStatus } from '../types'

export default function GMGameDashboard() {
  const { id } = useParams<{ id: string }>()
  const navigate = useNavigate()
  const [game, setGame] = useState<Game | null>(null)
  const [decisions, setDecisions] = useState<Decision[]>([])
  const [votingStatus, setVotingStatus] = useState<VotingStatus[]>([])
  const [loading, setLoading] = useState(true)
  const [scoring, setScoring] = useState<Record<number, { score: string; notes: string }>>({})
  const [phaseComments, setPhaseComments] = useState<any[]>([])
  const [gmNotes, setGmNotes] = useState<Record<number, string>>({})
  const [gmNotesLoading, setGmNotesLoading] = useState<Record<number, boolean>>({})

  useEffect(() => {
    if (!id) return
    fetchGame()
    const interval = setInterval(() => {
      fetchGame()
    }, 5000) // Poll every 5 seconds
    return () => clearInterval(interval)
  }, [id])

  useEffect(() => {
    if (game?.current_phase_id) {
      fetchDecisions()
      fetchVotingStatus()
      fetchPhaseComments()
      fetchGMNotes()
      const interval = setInterval(() => {
        fetchDecisions()
        fetchVotingStatus()
        fetchPhaseComments()
      }, 3000) // Poll every 3 seconds for real-time comments
      return () => clearInterval(interval)
    }
  }, [game?.current_phase_id])

  const fetchGame = async () => {
    try {
      const response = await apiClient.get<Game>(`/games/${id}`)
      setGame(response.data)
      setLoading(false)
    } catch (err) {
      console.error('Failed to fetch game:', err)
      setLoading(false)
    }
  }

  const fetchDecisions = async () => {
    if (!game?.current_phase_id) return
    try {
      const response = await apiClient.get<Decision[]>(`/games/${id}/phases/${game.current_phase_id}/decisions`)
      setDecisions(response.data)
    } catch (err) {
      console.error('Failed to fetch decisions:', err)
    }
  }

  const fetchPhaseComments = async () => {
    if (!game?.current_phase_id) return
    try {
      const response = await apiClient.get(`/games/${id}/phases/${game.current_phase_id}/comments`)
      setPhaseComments(response.data.comments || [])
    } catch (err) {
      console.error('Failed to fetch comments:', err)
    }
  }

  const fetchGMNotes = async () => {
    if (!game?.current_phase_id) return
    try {
      const response = await apiClient.get(`/games/${id}/phases/${game.current_phase_id}/gm-notes`)
      setGmNotes(prev => ({ ...prev, [game.current_phase_id!]: response.data.notes || '' }))
    } catch (err) {
      console.error('Failed to fetch GM notes:', err)
    }
  }

  const handleGMNotesUpdate = async (phaseId: number, notes: string) => {
    setGmNotesLoading(prev => ({ ...prev, [phaseId]: true }))
    try {
      await apiClient.post(`/games/${id}/phases/${phaseId}/gm-notes`, { notes })
      setGmNotes(prev => ({ ...prev, [phaseId]: notes }))
    } catch (err) {
      console.error('Failed to update GM notes:', err)
      alert('Failed to save notes')
    } finally {
      setGmNotesLoading(prev => ({ ...prev, [phaseId]: false }))
    }
  }

  const fetchVotingStatus = async () => {
    if (!game?.current_phase_id) return
    try {
      const response = await apiClient.get<VotingStatus[]>(`/games/${id}/phases/${game.current_phase_id}/voting-status`)
      setVotingStatus(response.data)
    } catch (err) {
      console.error('Failed to fetch voting status:', err)
    }
  }

  const handlePhaseAction = async (action: string) => {
    // Check voting status before locking decisions or moving to next phase
    if ((action === 'phase/lock_decisions' || action === 'phase/resolve' || action === 'phase/complete_and_next') && game?.current_phase_id) {
      const notAllVoted = votingStatus.some(status => !status.all_voted && status.total_players > 0)
      if (notAllVoted) {
        const message = action === 'phase/complete_and_next' 
          ? 'Not all players have voted. Are you sure you want to proceed to the next phase?'
          : 'Not all players have voted. Are you sure you want to proceed?'
        if (!confirm(message)) {
          return
        }
      }
    }

    try {
      await apiClient.post(`/games/${id}/${action}`)
      fetchGame()
    } catch (err) {
      console.error(`Failed to ${action}:`, err)
      alert(`Failed to ${action}`)
    }
  }

  const handleScoreDecision = async (decisionId: number) => {
    const scoreData = scoring[decisionId]
    if (!scoreData || !scoreData.score) {
      alert('Please enter a score')
      return
    }

    try {
      await apiClient.post(
        `/games/${id}/phases/${game?.current_phase_id}/decisions/${decisionId}/score`,
        {
          score_awarded: parseInt(scoreData.score),
          gm_notes: scoreData.notes || undefined,
        }
      )
      setScoring({ ...scoring, [decisionId]: { score: '', notes: '' } })
      fetchDecisions()
      fetchGame()
    } catch (err) {
      console.error('Failed to score decision:', err)
      alert('Failed to score decision')
    }
  }

  const copyToClipboard = (text: string) => {
    navigator.clipboard.writeText(text)
    alert('Copied to clipboard!')
  }

  if (loading || !game) {
    return <div className="p-8">Loading...</div>
  }

  const audienceUrl = `${window.location.origin}/audience/${game.audience_code || game.id}`

  return (
    <div className="min-h-screen bg-gray-50 p-8">
      <div className="max-w-7xl mx-auto">
        <div className="flex justify-between items-center mb-6">
          <div>
            <h1 className="text-3xl font-bold">{game.scenario?.name || 'Game'}</h1>
            <p className="text-gray-600">Game ID: {game.id}</p>
          </div>
          <div className="flex gap-2">
            <button
              onClick={async () => {
                if (confirm(`Are you sure you want to delete this game? This action cannot be undone.`)) {
                  try {
                    await apiClient.delete(`/games/${id}`)
                    navigate('/gm')
                  } catch (err: any) {
                    alert(err.response?.data?.detail || 'Failed to delete game')
                  }
                }
              }}
              className="px-4 py-2 bg-red-600 text-white rounded-md hover:bg-red-700"
            >
              Delete Game
            </button>
            <button
              onClick={() => navigate('/gm')}
              className="px-4 py-2 bg-gray-600 text-white rounded-md hover:bg-gray-700"
            >
              Back to Games
            </button>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-6">
          {/* Phase Control */}
          <div className="lg:col-span-2 bg-white rounded-lg shadow-md p-6">
            <h2 className="text-xl font-bold mb-4">Phase Control</h2>
            <div className="mb-4">
              <p className="text-sm text-gray-600">Current Phase:</p>
              <p className="text-lg font-semibold">{game.current_phase?.name || 'Not started'}</p>
              <p className="text-sm text-gray-500">State: {game.phase_state}</p>
            </div>

            <div className="flex flex-wrap gap-2">
              {game.status === 'lobby' && (
                <button
                  onClick={() => handlePhaseAction('start')}
                  className="px-4 py-2 bg-green-600 text-white rounded-md hover:bg-green-700"
                >
                  Start Game
                </button>
              )}
              {game.phase_state === 'briefing' && (
                <button
                  onClick={() => handlePhaseAction('phase/open_for_decisions')}
                  className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700"
                >
                  Open for Decisions
                </button>
              )}
              {game.phase_state === 'open_for_decisions' && (
                <>
                  {votingStatus.some(status => !status.all_voted && status.total_players > 0) && (
                    <div className="w-full mb-2 p-3 bg-yellow-50 border border-yellow-200 rounded-md">
                      <p className="text-sm text-yellow-800">
                        ⚠️ Warning: Not all players have voted. Some teams still have pending votes.
                      </p>
                    </div>
                  )}
                  <button
                    onClick={() => handlePhaseAction('phase/lock_decisions')}
                    className="px-4 py-2 bg-yellow-600 text-white rounded-md hover:bg-yellow-700"
                  >
                    Lock Decisions
                  </button>
                </>
              )}
              {game.phase_state === 'decision_lock' && (
                <button
                  onClick={() => handlePhaseAction('phase/resolve')}
                  className="px-4 py-2 bg-purple-600 text-white rounded-md hover:bg-purple-700"
                >
                  Resolve Phase
                </button>
              )}
              {game.phase_state === 'resolution' && (
                <>
                  {votingStatus.some(status => !status.all_voted && status.total_players > 0) && (
                    <div className="w-full mb-2 p-3 bg-yellow-50 border border-yellow-200 rounded-md">
                      <p className="text-sm text-yellow-800">
                        ⚠️ Warning: Not all players voted in this phase. Proceeding may affect scoring.
                      </p>
                    </div>
                  )}
                  <button
                    onClick={() => handlePhaseAction('phase/complete_and_next')}
                    className="px-4 py-2 bg-indigo-600 text-white rounded-md hover:bg-indigo-700"
                  >
                    Complete & Next Phase
                  </button>
                </>
              )}
              {game.status === 'in_progress' && (
                <>
                  <button
                    onClick={() => handlePhaseAction('end')}
                    className="px-4 py-2 bg-red-600 text-white rounded-md hover:bg-red-700"
                  >
                    End Game
                  </button>
                  <button
                    onClick={() => navigate(`/gm/games/${id}/after-action-report`)}
                    className="px-4 py-2 bg-purple-600 text-white rounded-md hover:bg-purple-700"
                  >
                    View After Action Report
                  </button>
                </>
              )}
            </div>

            {game.current_phase && (
              <div className="mt-6 p-4 bg-gray-50 rounded-md">
                <h3 className="font-semibold mb-2">Briefing:</h3>
                <p className="text-sm text-gray-700">{game.current_phase.briefing_text}</p>
              </div>
            )}
          </div>

          {/* Join Info */}
          <div className="bg-white rounded-lg shadow-md p-6">
            <h2 className="text-xl font-bold mb-4">Join Codes</h2>
            <div className="space-y-4">
              <div>
                <label className="text-sm font-medium text-gray-600">Red Team Code</label>
                <div className="flex gap-2 mt-1">
                  <input
                    type="text"
                    value={game.red_team_code}
                    readOnly
                    className="flex-1 px-3 py-2 border border-gray-300 rounded-md bg-gray-50"
                  />
                  <button
                    onClick={() => copyToClipboard(game.red_team_code)}
                    className="px-3 py-2 bg-gray-200 rounded-md hover:bg-gray-300"
                  >
                    Copy
                  </button>
                </div>
              </div>
              <div>
                <label className="text-sm font-medium text-gray-600">Blue Team Code</label>
                <div className="flex gap-2 mt-1">
                  <input
                    type="text"
                    value={game.blue_team_code}
                    readOnly
                    className="flex-1 px-3 py-2 border border-gray-300 rounded-md bg-gray-50"
                  />
                  <button
                    onClick={() => copyToClipboard(game.blue_team_code)}
                    className="px-3 py-2 bg-gray-200 rounded-md hover:bg-gray-300"
                  >
                    Copy
                  </button>
                </div>
              </div>
              <div>
                <label className="text-sm font-medium text-gray-600">Audience URL</label>
                <div className="flex gap-2 mt-1">
                  <input
                    type="text"
                    value={audienceUrl}
                    readOnly
                    className="flex-1 px-3 py-2 border border-gray-300 rounded-md bg-gray-50 text-xs"
                  />
                  <button
                    onClick={() => copyToClipboard(audienceUrl)}
                    className="px-3 py-2 bg-gray-200 rounded-md hover:bg-gray-300"
                  >
                    Copy
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Voting Status */}
        {game.current_phase_id && game.phase_state === 'open_for_decisions' && votingStatus.length > 0 && (
          <div className="bg-white rounded-lg shadow-md p-6 mb-6">
            <h2 className="text-xl font-bold mb-4">Voting Status</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {votingStatus.map((status) => (
                <div key={status.team_id} className="border border-gray-200 rounded-md p-4">
                  <div className="flex justify-between items-center mb-2">
                    <h3 className="font-semibold">{status.team_name}</h3>
                    <span className={`px-2 py-1 rounded text-sm ${status.all_voted ? 'bg-green-100 text-green-800' : 'bg-yellow-100 text-yellow-800'}`}>
                      {status.votes_submitted}/{status.total_players} voted
                    </span>
                  </div>
                  {status.votes.length > 0 && (
                    <div className="mt-3 space-y-2">
                      {status.votes.map((vote) => (
                        <div key={vote.id} className="text-sm bg-gray-50 p-2 rounded">
                          <span className="font-medium">{vote.player_name}</span>: {vote.selected_action}
                        </div>
                      ))}
                    </div>
                  )}
                  {status.votes.length === 0 && (
                    <p className="text-sm text-gray-500 mt-2">No votes yet</p>
                  )}
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Player Comments (Real-time) */}
        {game.current_phase_id && game.phase_state === 'open_for_decisions' && phaseComments.length > 0 && (
          <div className="bg-white rounded-lg shadow-md p-6 mb-6">
            <h2 className="text-xl font-bold mb-4">Player Comments (Real-time)</h2>
            <div className="space-y-3 max-h-96 overflow-y-auto">
              {phaseComments.map((comment, idx) => (
                <div key={idx} className="border-l-4 border-blue-500 pl-4 py-2 bg-gray-50 rounded">
                  <div className="flex justify-between items-start mb-1">
                    <div>
                      <span className="font-semibold">{comment.player_name}</span>
                      <span className={`ml-2 px-2 py-1 rounded text-xs ${comment.team_role === 'red' ? 'bg-red-100 text-red-800' : 'bg-blue-100 text-blue-800'}`}>
                        {comment.team_name} ({comment.team_role.toUpperCase()})
                      </span>
                    </div>
                    {comment.effectiveness_rating && (
                      <span className="text-sm font-bold text-blue-600">
                        Rating: {comment.effectiveness_rating}/10
                      </span>
                    )}
                  </div>
                  <p className="text-sm text-gray-700 mt-1">{comment.comments}</p>
                  <span className="text-xs text-gray-400">
                    {new Date(comment.voted_at).toLocaleString()}
                  </span>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* GM Notes & Takeaways */}
        {game.current_phase_id && (
          <div className="bg-white rounded-lg shadow-md p-6 mb-6">
            <h2 className="text-xl font-bold mb-4">Phase Notes & Takeaways</h2>
            <textarea
              value={gmNotes[game.current_phase_id] || ''}
              onChange={(e) => {
                setGmNotes(prev => ({ ...prev, [game.current_phase_id!]: e.target.value }))
              }}
              onBlur={() => {
                if (game.current_phase_id) {
                  handleGMNotesUpdate(game.current_phase_id, gmNotes[game.current_phase_id] || '')
                }
              }}
              className="w-full px-3 py-2 border border-gray-300 rounded-md"
              rows={6}
              placeholder="Add your notes and takeaways for this phase..."
              disabled={gmNotesLoading[game.current_phase_id]}
            />
            {gmNotesLoading[game.current_phase_id] && (
              <p className="text-sm text-gray-500 mt-2">Saving...</p>
            )}
          </div>
        )}

        {/* Decisions */}
        {game.current_phase_id && game.phase_state !== 'not_started' && (
          <div className="bg-white rounded-lg shadow-md p-6">
            <h2 className="text-xl font-bold mb-4">Team Decisions</h2>
            {decisions.length === 0 ? (
              <p className="text-gray-500">No decisions submitted yet.</p>
            ) : (
              <div className="space-y-4">
                {decisions.map((decision) => (
                  <div key={decision.id} className="border border-gray-200 rounded-md p-4">
                    <div className="flex justify-between items-start mb-2">
                      <div>
                        <h3 className="font-semibold">{decision.team?.name || 'Unknown Team'}</h3>
                        <p className="text-sm text-gray-500">
                          Submitted: {new Date(decision.submitted_at).toLocaleString()}
                        </p>
                      </div>
                      {decision.score_awarded !== null && (
                        <span className="px-3 py-1 bg-green-100 text-green-800 rounded-full text-sm font-semibold">
                          Score: {decision.score_awarded}
                        </span>
                      )}
                    </div>

                    <div className="mb-3">
                      <p className="text-sm font-medium mb-1">Actions:</p>
                      <pre className="text-xs bg-gray-50 p-2 rounded overflow-auto">
                        {JSON.stringify(decision.actions, null, 2)}
                      </pre>
                    </div>

                    <div className="mb-3">
                      <p className="text-sm font-medium mb-1">Justification:</p>
                      <p className="text-sm text-gray-700">{decision.free_text_justification}</p>
                    </div>

                    {decision.gm_notes && (
                      <div className="mb-3">
                        <p className="text-sm font-medium mb-1">GM Notes:</p>
                        <p className="text-sm text-gray-700">{decision.gm_notes}</p>
                      </div>
                    )}

                    {decision.status !== 'scored' && game.phase_state === 'resolution' && (
                      <div className="mt-4 pt-4 border-t border-gray-200">
                        <div className="grid grid-cols-2 gap-4">
                          <div>
                            <label className="block text-sm font-medium mb-1">Score</label>
                            <input
                              type="number"
                              value={scoring[decision.id]?.score || ''}
                              onChange={(e) =>
                                setScoring({
                                  ...scoring,
                                  [decision.id]: { ...scoring[decision.id], score: e.target.value },
                                })
                              }
                              className="w-full px-3 py-2 border border-gray-300 rounded-md"
                              placeholder="0"
                            />
                          </div>
                          <div>
                            <label className="block text-sm font-medium mb-1">Notes</label>
                            <input
                              type="text"
                              value={scoring[decision.id]?.notes || ''}
                              onChange={(e) =>
                                setScoring({
                                  ...scoring,
                                  [decision.id]: { ...scoring[decision.id], notes: e.target.value },
                                })
                              }
                              className="w-full px-3 py-2 border border-gray-300 rounded-md"
                              placeholder="Optional notes"
                            />
                          </div>
                        </div>
                        <button
                          onClick={() => handleScoreDecision(decision.id)}
                          className="mt-2 px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700"
                        >
                          Save Score
                        </button>
                      </div>
                    )}
                  </div>
                ))}
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  )
}

