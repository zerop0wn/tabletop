import { useEffect, useState } from 'react'
import { useParams } from 'react-router-dom'
import apiClient from '../api/client'
import { Scoreboard } from '../types'

export default function AudienceView() {
  const { gameIdentifier } = useParams<{ gameIdentifier: string }>()
  const [scoreboard, setScoreboard] = useState<Scoreboard | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    if (!gameIdentifier) return
    fetchScoreboard()
    const interval = setInterval(fetchScoreboard, 8000) // Poll every 8 seconds
    return () => clearInterval(interval)
  }, [gameIdentifier])

  const fetchScoreboard = async () => {
    try {
      const response = await apiClient.get<Scoreboard>(
        `/games/${gameIdentifier}/scoreboard`
      )
      setScoreboard(response.data)
      setLoading(false)
    } catch (err) {
      console.error('Failed to fetch scoreboard:', err)
      setLoading(false)
    }
  }

  if (loading || !scoreboard) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-900 text-white">
        <div className="text-2xl">Loading...</div>
      </div>
    )
  }

  const maxScore = Math.max(...scoreboard.teams.map((t) => t.total_score), 1)

  return (
    <div className="min-h-screen bg-gray-900 text-white p-8">
      <div className="max-w-6xl mx-auto">
        <div className="text-center mb-12">
          <h1 className="text-5xl font-bold mb-4">{scoreboard.scenario_name}</h1>
          {scoreboard.current_phase_name && (
            <div>
              <p className="text-2xl text-gray-300">Current Phase: {scoreboard.current_phase_name}</p>
              <p className="text-lg text-gray-400 mt-2">Status: {scoreboard.phase_state}</p>
            </div>
          )}
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-8 mb-12">
          {scoreboard.teams.map((team) => {
            const percentage = (team.total_score / maxScore) * 100
            return (
              <div key={team.team_id} className="bg-gray-800 rounded-lg p-8">
                <h2 className="text-3xl font-bold mb-4 text-center">{team.team_name}</h2>
                <div className="text-center mb-6">
                  <div className="text-6xl font-bold text-blue-400">{team.total_score}</div>
                  <div className="text-sm text-gray-400 mt-2">points</div>
                </div>
                <div className="w-full bg-gray-700 rounded-full h-8">
                  <div
                    className={`h-8 rounded-full ${
                      team.team_role === 'red' ? 'bg-red-600' : 'bg-blue-600'
                    }`}
                    style={{ width: `${percentage}%` }}
                  ></div>
                </div>
              </div>
            )
          })}
        </div>

        {scoreboard.teams.length === 0 && (
          <div className="text-center text-gray-400">
            <p>No teams yet. Waiting for game to start...</p>
          </div>
        )}
      </div>
    </div>
  )
}

