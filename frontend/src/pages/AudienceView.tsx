import { useEffect, useState, useRef } from 'react'
import { useParams } from 'react-router-dom'
import apiClient from '../api/client'
import { Scoreboard, TeamScore } from '../types'

interface AnimatedScore {
  value: number
  previousValue: number
  isAnimating: boolean
}

export default function AudienceView() {
  const { gameIdentifier } = useParams<{ gameIdentifier: string }>()
  const [scoreboard, setScoreboard] = useState<Scoreboard | null>(null)
  const [loading, setLoading] = useState(true)
  const [previousPhase, setPreviousPhase] = useState<string | undefined>(undefined)
  const [phaseTransition, setPhaseTransition] = useState(false)
  const [animatedScores, setAnimatedScores] = useState<Record<number, AnimatedScore>>({})
  const [seenEventIds, setSeenEventIds] = useState<Set<string>>(new Set())
  const previousScoresRef = useRef<Record<number, number>>({})

  useEffect(() => {
    if (!gameIdentifier) return
    fetchScoreboard()
    const interval = setInterval(fetchScoreboard, 3000) // Poll every 3 seconds for more real-time feel
    return () => clearInterval(interval)
  }, [gameIdentifier])

  useEffect(() => {
    if (!scoreboard) return

    // Detect phase transitions
    if (previousPhase && previousPhase !== scoreboard.current_phase_name) {
      setPhaseTransition(true)
      setTimeout(() => setPhaseTransition(false), 2000)
    }
    setPreviousPhase(scoreboard.current_phase_name)

    // Animate score changes
    scoreboard.teams.forEach(team => {
      const prevScore = previousScoresRef.current[team.team_id] || 0
      if (team.total_score !== prevScore) {
        setAnimatedScores(prev => ({
          ...prev,
          [team.team_id]: {
            value: team.total_score,
            previousValue: prevScore,
            isAnimating: true
          }
        }))
        setTimeout(() => {
          setAnimatedScores(prev => ({
            ...prev,
            [team.team_id]: { ...prev[team.team_id], isAnimating: false }
          }))
        }, 1000)
        previousScoresRef.current[team.team_id] = team.total_score
      }
    })

    // Track new events
    scoreboard.recent_events.forEach(event => {
      const eventId = `${event.team_id}-${event.created_at}-${event.delta}`
      if (!seenEventIds.has(eventId)) {
        setSeenEventIds(prev => new Set([...prev, eventId]))
      }
    })
  }, [scoreboard, previousPhase, seenEventIds])

  const fetchScoreboard = async () => {
    try {
      const response = await apiClient.get<Scoreboard>(
        `/games/${gameIdentifier}/scoreboard`
      )
      // Debug: log score history
      response.data.teams.forEach(team => {
        console.log(`Team ${team.team_name} score_history:`, team.score_history)
        if (team.score_history) {
          team.score_history.forEach((entry, idx) => {
            console.log(`  Phase ${idx + 1}:`, entry)
          })
        }
      })
      setScoreboard(response.data)
      setLoading(false)
    } catch (err) {
      console.error('Failed to fetch scoreboard:', err)
      setLoading(false)
    }
  }

  if (loading || !scoreboard) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900 text-white">
        <div className="text-2xl animate-pulse">Loading...</div>
      </div>
    )
  }

  const maxScore = Math.max(...scoreboard.teams.map((t) => t.total_score), 1)
  const leadingTeam = scoreboard.teams.reduce((prev, current) => 
    (current.total_score > prev.total_score) ? current : prev
  )

  const getTeamColor = (team: TeamScore) => {
    return team.team_role === 'red' 
      ? 'from-red-600 via-red-500 to-red-600' 
      : 'from-blue-600 via-blue-500 to-blue-600'
  }

  const getTeamBgColor = (team: TeamScore) => {
    return team.team_role === 'red' 
      ? 'bg-red-900/30 border-red-500/50' 
      : 'bg-blue-900/30 border-blue-500/50'
  }

  const formatTimeAgo = (dateString?: string) => {
    if (!dateString) return 'Just now'
    const date = new Date(dateString)
    const now = new Date()
    const seconds = Math.floor((now.getTime() - date.getTime()) / 1000)
    if (seconds < 60) return `${seconds}s ago`
    const minutes = Math.floor(seconds / 60)
    if (minutes < 60) return `${minutes}m ago`
    const hours = Math.floor(minutes / 60)
    return `${hours}h ago`
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900 text-white p-4 md:p-8">
      {/* Phase Transition Animation */}
      {phaseTransition && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/80 animate-fadeIn">
          <div className="text-4xl md:text-6xl font-bold animate-bounce">
            <div className="bg-gradient-to-r from-yellow-400 to-orange-500 bg-clip-text text-transparent">
              PHASE TRANSITION
            </div>
          </div>
        </div>
      )}

      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-4xl md:text-6xl font-bold mb-4 bg-gradient-to-r from-blue-400 via-purple-500 to-pink-500 bg-clip-text text-transparent">
            {scoreboard.scenario_name}
          </h1>
          {scoreboard.current_phase_name && (
            <div className="mt-4">
              <div className="inline-block px-6 py-3 bg-gray-800/50 rounded-full border border-gray-700">
                <p className="text-xl md:text-2xl text-gray-200 font-semibold">
                  {scoreboard.current_phase_name}
                </p>
                <p className="text-sm text-gray-400 mt-1 capitalize">
                  {scoreboard.phase_state.replace('_', ' ')}
                </p>
              </div>
            </div>
          )}
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-6">
          {/* Team Score Cards */}
          <div className="lg:col-span-2 grid grid-cols-1 md:grid-cols-2 gap-6">
            {scoreboard.teams.map((team) => {
              const percentage = (team.total_score / maxScore) * 100
              const isLeader = team.team_id === leadingTeam.team_id && team.total_score > 0
              const animatedScore = animatedScores[team.team_id]
              const scoreValue = animatedScore?.value ?? team.total_score
              const isAnimating = animatedScore?.isAnimating ?? false
              const scoreChange = animatedScore ? scoreValue - animatedScore.previousValue : 0

              return (
                <div
                  key={team.team_id}
                  className={`relative rounded-xl p-6 border-2 transition-all duration-500 ${
                    isLeader
                      ? `${getTeamBgColor(team)} border-opacity-100 shadow-2xl scale-105 ring-4 ring-opacity-50 ${
                          team.team_role === 'red' ? 'ring-red-500' : 'ring-blue-500'
                        }`
                      : `${getTeamBgColor(team)} border-opacity-50`
                  }`}
                >
                  {/* Leader Badge */}
                  {isLeader && (
                    <div className="absolute -top-4 -right-4 bg-gradient-to-r from-yellow-400 to-orange-500 text-gray-900 px-4 py-2 rounded-full font-bold text-sm animate-pulse shadow-lg">
                      🏆 LEADER
                    </div>
                  )}

                  <div className="text-center mb-4">
                    <h2 className={`text-2xl font-bold mb-2 ${
                      team.team_role === 'red' ? 'text-red-300' : 'text-blue-300'
                    }`}>
                      {team.team_name} Team
                    </h2>
                    {/* Team Members */}
                    {team.team_members && team.team_members.length > 0 && (
                      <div className="mt-3">
                        <div className="text-xs text-gray-400 mb-1">Team Members</div>
                        <div className="flex flex-wrap justify-center gap-2">
                          {team.team_members.map((member, idx) => (
                            <span
                              key={idx}
                              className="px-2 py-1 bg-gray-700/50 rounded-md text-sm text-gray-300"
                            >
                              {member}
                            </span>
                          ))}
                        </div>
                      </div>
                    )}
                  </div>

                  {/* Score Display with Animation */}
                  <div className="text-center mb-6 relative">
                    <div
                      className={`text-7xl font-bold transition-all duration-500 ${
                        isAnimating
                          ? 'scale-125 text-yellow-400'
                          : team.team_role === 'red'
                          ? 'text-red-400'
                          : 'text-blue-400'
                      }`}
                    >
                      {scoreValue}
                    </div>
                    {isAnimating && scoreChange > 0 && (
                      <div className="absolute top-0 right-0 text-green-400 font-bold text-2xl animate-bounce">
                        +{scoreChange}
                      </div>
                    )}
                    {isAnimating && scoreChange < 0 && (
                      <div className="absolute top-0 right-0 text-red-400 font-bold text-2xl animate-bounce">
                        {scoreChange}
                      </div>
                    )}
                    <div className="text-sm text-gray-400 mt-2">points</div>
                  </div>

                  {/* Progress Bar */}
                  <div className="w-full bg-gray-700/50 rounded-full h-4 mb-4 overflow-hidden">
                    <div
                      className={`h-4 rounded-full bg-gradient-to-r ${getTeamColor(team)} transition-all duration-1000 ease-out shadow-lg`}
                      style={{ width: `${percentage}%` }}
                    ></div>
                  </div>

                  {/* Voting Status */}
                  {team.voting_status && (
                    <div className="mt-4 p-3 bg-gray-800/50 rounded-lg">
                      <div className="flex items-center justify-between text-sm mb-2">
                        <span className="text-gray-400">Voting Progress</span>
                        <span className="font-semibold">
                          {team.voting_status.votes_submitted}/{team.voting_status.total_players}
                        </span>
                      </div>
                      <div className="w-full bg-gray-700 rounded-full h-2">
                        <div
                          className={`h-2 rounded-full transition-all duration-500 ${
                            team.voting_status.all_voted
                              ? 'bg-green-500'
                              : team.team_role === 'red'
                              ? 'bg-red-500'
                              : 'bg-blue-500'
                          }`}
                          style={{
                            width: `${(team.voting_status.votes_submitted / team.voting_status.total_players) * 100}%`
                          }}
                        ></div>
                      </div>
                      {team.voting_status.all_voted && (
                        <div className="text-xs text-green-400 mt-1">✓ All votes submitted</div>
                      )}
                    </div>
                  )}

                  {/* Recent Decision */}
                  {team.recent_decision?.action && (
                    <div className="mt-4 p-3 bg-gray-800/50 rounded-lg">
                      <div className="text-xs text-gray-400 mb-1">Last Action</div>
                      <div className="font-semibold text-sm">{team.recent_decision.action}</div>
                      {team.recent_decision.score_awarded !== null && (
                        <div className={`text-xs mt-1 ${
                          team.recent_decision.score_awarded >= 7
                            ? 'text-green-400'
                            : team.recent_decision.score_awarded >= 4
                            ? 'text-yellow-400'
                            : 'text-red-400'
                        }`}>
                          Scored: {team.recent_decision.score_awarded}/10
                        </div>
                      )}
                    </div>
                  )}

                  {/* Score History Mini Chart */}
                  <div className="mt-4 p-3 bg-gray-800/50 rounded-lg">
                    <div className="text-xs text-gray-400 mb-2">Score by Phase</div>
                    {team.score_history && team.score_history.length > 0 ? (
                      <div className="flex items-end justify-between h-16 gap-1">
                        {team.score_history.map((entry, idx) => {
                          const allScores = team.score_history.map(e => e.score)
                          const maxPhaseScore = Math.max(...allScores, 1)
                          // Ensure minimum height of 10% so bars are always visible, even with 0 scores
                          const height = maxPhaseScore > 0 
                            ? Math.max((entry.score / maxPhaseScore) * 90, entry.score > 0 ? 10 : 5)
                            : 5
                          return (
                            <div key={`${team.team_id}-${entry.phase_order}-${idx}`} className="flex-1 flex flex-col items-center min-w-0">
                              <div
                                className={`w-full rounded-t transition-all duration-500 ${
                                  team.team_role === 'red' ? 'bg-red-500' : 'bg-blue-500'
                                } ${entry.score === 0 ? 'opacity-30' : 'opacity-100'}`}
                                style={{ height: `${height}%`, minHeight: '4px' }}
                                title={`Phase ${entry.phase_order + 1}: ${entry.score} pts`}
                              ></div>
                              <div className="text-[8px] text-gray-500 mt-1 truncate w-full text-center">
                                P{entry.phase_order + 1}
                              </div>
                              {entry.score > 0 && (
                                <div className="text-[8px] text-gray-400 mt-0.5">
                                  {entry.score}
                                </div>
                              )}
                            </div>
                          )
                        })}
                      </div>
                    ) : (
                      <div className="text-xs text-gray-500 text-center py-4">
                        {team.score_history === undefined 
                          ? 'Loading phase data...' 
                          : 'No phase scores yet'}
                      </div>
                    )}
                  </div>
                </div>
              )
            })}
          </div>

          {/* Live Event Feed */}
          <div className="lg:col-span-1">
            <div className="bg-gray-800/50 rounded-xl p-4 border border-gray-700 h-full">
              <h3 className="text-xl font-bold mb-4 flex items-center">
                <span className="w-3 h-3 bg-green-500 rounded-full mr-2 animate-pulse"></span>
                Live Events
              </h3>
              <div className="space-y-3 max-h-[600px] overflow-y-auto">
                {scoreboard.recent_events.length === 0 ? (
                  <div className="text-gray-400 text-sm text-center py-8">
                    No events yet. Waiting for scoring...
                  </div>
                ) : (
                  scoreboard.recent_events.map((event, idx) => {
                    const isNew = idx < 3 // Highlight first 3 events
                    return (
                      <div
                        key={`${event.team_id}-${event.created_at}-${idx}`}
                        className={`p-3 rounded-lg border transition-all duration-300 ${
                          isNew
                            ? 'bg-gray-700/50 border-opacity-100 scale-105'
                            : 'bg-gray-800/30 border-opacity-50'
                        } ${
                          event.team_role === 'red' ? 'border-red-500/50' : 'border-blue-500/50'
                        }`}
                      >
                        <div className="flex items-start justify-between mb-2">
                          <div className="flex items-center">
                            <div
                              className={`w-2 h-2 rounded-full mr-2 ${
                                event.team_role === 'red' ? 'bg-red-500' : 'bg-blue-500'
                              }`}
                            ></div>
                            <span className="font-semibold text-sm">{event.team_name}</span>
                          </div>
                          <span
                            className={`text-lg font-bold ${
                              event.delta > 0 ? 'text-green-400' : 'text-red-400'
                            }`}
                          >
                            {event.delta > 0 ? '+' : ''}{event.delta}
                          </span>
                        </div>
                        <div className="text-xs text-gray-400 mb-1">{event.reason}</div>
                        <div className="text-xs text-gray-500">{formatTimeAgo(event.created_at)}</div>
                      </div>
                    )
                  })
                )}
              </div>
            </div>
          </div>
        </div>

        {scoreboard.teams.length === 0 && (
          <div className="text-center text-gray-400 py-12">
            <p className="text-xl">No teams yet. Waiting for game to start...</p>
          </div>
        )}
      </div>
    </div>
  )
}
