import { useEffect, useState } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import apiClient from '../api/client'
import { PlayerReportCard } from '../types'

export default function PlayerReportCardView() {
  const { gameId, playerId } = useParams<{ gameId: string; playerId: string }>()
  const navigate = useNavigate()
  const [reportCard, setReportCard] = useState<PlayerReportCard | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    if (!gameId || !playerId) return
    fetchReportCard()
  }, [gameId, playerId])

  const fetchReportCard = async () => {
    try {
      setLoading(true)
      const response = await apiClient.get<PlayerReportCard>(
        `/players/games/${gameId}/player/${playerId}/report-card`
      )
      setReportCard(response.data)
    } catch (err) {
      console.error('Failed to fetch report card:', err)
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 p-8">
        <div className="max-w-4xl mx-auto">
          <div className="bg-white rounded-lg shadow-md p-6">
            <p className="text-gray-600">Loading your report card...</p>
          </div>
        </div>
      </div>
    )
  }

  if (!reportCard) {
    return (
      <div className="min-h-screen bg-gray-50 p-8">
        <div className="max-w-4xl mx-auto">
          <div className="bg-white rounded-lg shadow-md p-6">
            <p className="text-gray-600">Unable to load report card.</p>
          </div>
        </div>
      </div>
    )
  }

  const teamBgColor = reportCard.team_role === 'red' ? 'bg-red-50 border-red-200' : 'bg-blue-50 border-blue-200'
  const teamTextColor = reportCard.team_role === 'red' ? 'text-red-800' : 'text-blue-800'
  const teamBadgeColor = reportCard.team_role === 'red' ? 'bg-red-600' : 'bg-blue-600'
  const teamBorderColor = reportCard.team_role === 'red' ? 'border-red-300' : 'border-blue-300'

  // Calculate performance grade
  const getPerformanceGrade = (score: number, maxScore: number) => {
    const percentage = (score / maxScore) * 100
    if (percentage >= 90) return { grade: 'A+', color: 'text-green-600', bg: 'bg-green-50' }
    if (percentage >= 80) return { grade: 'A', color: 'text-green-600', bg: 'bg-green-50' }
    if (percentage >= 70) return { grade: 'B', color: 'text-blue-600', bg: 'bg-blue-50' }
    if (percentage >= 60) return { grade: 'C', color: 'text-yellow-600', bg: 'bg-yellow-50' }
    if (percentage >= 50) return { grade: 'D', color: 'text-orange-600', bg: 'bg-orange-50' }
    return { grade: 'F', color: 'text-red-600', bg: 'bg-red-50' }
  }

  const maxPossibleScore = reportCard.phases.reduce((sum, phase) => sum + (phase.max_possible_score || 10), 0)
  const performance = getPerformanceGrade(reportCard.total_score, maxPossibleScore)

  return (
    <div className="min-h-screen bg-gray-50 p-8">
      <div className="max-w-4xl mx-auto">
        {/* Header */}
        <div className="bg-white rounded-lg shadow-md p-6 mb-6">
          <div className="flex items-center justify-between mb-4">
            <h1 className="text-3xl font-bold">Your Performance Report Card</h1>
            <div className="flex items-center gap-3">
              <button
                onClick={() => navigate('/play/join')}
                className="px-4 py-2 bg-gray-600 text-white rounded-md hover:bg-gray-700 font-medium text-sm"
              >
                Join New Game
              </button>
              <div className={`px-4 py-2 rounded-lg ${teamBadgeColor} text-white font-semibold`}>
                {reportCard.team_role === 'red' ? 'Red Team' : 'Blue Team'}
              </div>
            </div>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <p className="text-sm text-gray-600">Player</p>
              <p className="text-lg font-semibold">{reportCard.player_name}</p>
            </div>
            <div>
              <p className="text-sm text-gray-600">Scenario</p>
              <p className="text-lg font-semibold">{reportCard.scenario_name}</p>
            </div>
            <div>
              <p className="text-sm text-gray-600">Team</p>
              <p className="text-lg font-semibold">{reportCard.team_name}</p>
            </div>
            {reportCard.game_completed_at && (
              <div>
                <p className="text-sm text-gray-600">Completed</p>
                <p className="text-lg font-semibold">
                  {new Date(reportCard.game_completed_at).toLocaleString()}
                </p>
              </div>
            )}
          </div>
        </div>

        {/* Overall Performance */}
        <div className="bg-white rounded-lg shadow-md p-6 mb-6">
          <h2 className="text-2xl font-bold mb-4">Overall Performance</h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className={`p-4 rounded-lg ${performance.bg} border-2 ${teamBorderColor}`}>
              <p className="text-sm text-gray-600 mb-1">Performance Grade</p>
              <p className={`text-4xl font-bold ${performance.color}`}>{performance.grade}</p>
            </div>
            <div className={`p-4 rounded-lg ${teamBgColor} border-2 ${teamBorderColor}`}>
              <p className="text-sm text-gray-600 mb-1">Total Score</p>
              <p className={`text-4xl font-bold ${teamTextColor}`}>{reportCard.total_score}</p>
              <p className="text-sm text-gray-500">out of {maxPossibleScore}</p>
            </div>
            {reportCard.average_effectiveness_rating !== null && reportCard.average_effectiveness_rating !== undefined && (
              <div className={`p-4 rounded-lg ${teamBgColor} border-2 ${teamBorderColor}`}>
                <p className="text-sm text-gray-600 mb-1">Avg. Effectiveness Rating</p>
                <p className={`text-4xl font-bold ${teamTextColor}`}>
                  {reportCard.average_effectiveness_rating.toFixed(1)}
                </p>
                <p className="text-sm text-gray-500">out of 10</p>
              </div>
            )}
          </div>
        </div>

        {/* Phase-by-Phase Breakdown */}
        <div className="bg-white rounded-lg shadow-md p-6">
          <h2 className="text-2xl font-bold mb-4">Phase-by-Phase Breakdown</h2>
          <div className="space-y-4">
            {reportCard.phases.map((phase, index) => (
              <div
                key={phase.phase_id}
                className={`p-4 rounded-lg border-2 ${teamBorderColor} ${teamBgColor}`}
              >
                <div className="flex items-start justify-between mb-3">
                  <div>
                    <h3 className={`text-lg font-bold ${teamTextColor}`}>
                      Phase {phase.phase_order + 1}: {phase.phase_name}
                    </h3>
                  </div>
                  <div className="text-right">
                    <p className={`text-2xl font-bold ${teamTextColor}`}>{phase.score_received}</p>
                    <p className="text-xs text-gray-500">/ {phase.max_possible_score || 10}</p>
                  </div>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mt-3">
                  <div className="bg-white rounded p-3">
                    <p className="text-sm font-semibold text-gray-700 mb-1">Your Vote</p>
                    <p className="text-gray-800">
                      {phase.player_vote || <span className="text-gray-400 italic">No vote submitted</span>}
                    </p>
                    {phase.player_effectiveness_rating !== null && phase.player_effectiveness_rating !== undefined && (
                      <p className="text-sm text-gray-600 mt-2">
                        Effectiveness Rating: {phase.player_effectiveness_rating}/10
                      </p>
                    )}
                    {phase.player_comments && (
                      <p className="text-sm text-gray-600 mt-2 italic">"{phase.player_comments}"</p>
                    )}
                  </div>
                  <div className="bg-white rounded p-3">
                    <p className="text-sm font-semibold text-gray-700 mb-1">Team Decision</p>
                    <p className="text-gray-800">
                      {phase.team_decision || <span className="text-gray-400 italic">No decision made</span>}
                    </p>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Summary */}
        <div className="mt-6 bg-white rounded-lg shadow-md p-6">
          <h2 className="text-xl font-bold mb-3">Summary</h2>
          <p className="text-gray-700">
            You participated in <strong>{reportCard.phases.length}</strong> phase{reportCard.phases.length !== 1 ? 's' : ''} of the{' '}
            <strong>{reportCard.scenario_name}</strong> scenario as part of{' '}
            <strong>{reportCard.team_name}</strong>.
            {reportCard.total_score > 0 && (
              <>
                {' '}Your team earned a total of <strong>{reportCard.total_score}</strong> points across all phases,
                achieving a performance grade of <strong className={performance.color}>{performance.grade}</strong>.
              </>
            )}
            {reportCard.average_effectiveness_rating !== null && reportCard.average_effectiveness_rating !== undefined && (
              <>
                {' '}Your average effectiveness rating was{' '}
                <strong>{reportCard.average_effectiveness_rating.toFixed(1)}/10</strong>.
              </>
            )}
          </p>
        </div>
      </div>
    </div>
  )
}

