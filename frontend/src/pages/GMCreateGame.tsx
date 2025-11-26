import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import apiClient from '../api/client'
import { Scenario, Game } from '../types'

export default function GMCreateGame() {
  const [scenarios, setScenarios] = useState<Scenario[]>([])
  const [selectedScenarioId, setSelectedScenarioId] = useState<number | null>(null)
  const [loading, setLoading] = useState(false)
  const navigate = useNavigate()

  useEffect(() => {
    fetchScenarios()
  }, [])

  const fetchScenarios = async () => {
    try {
      const response = await apiClient.get<Scenario[]>('/scenarios')
      setScenarios(response.data)
      if (response.data.length > 0) {
        setSelectedScenarioId(response.data[0].id)
      }
    } catch (err) {
      console.error('Failed to fetch scenarios:', err)
    }
  }

  const handleCreate = async () => {
    if (!selectedScenarioId) return

    setLoading(true)
    try {
      const response = await apiClient.post<Game>('/games', {
        scenario_id: selectedScenarioId,
      })
      navigate(`/gm/games/${response.data.id}`)
    } catch (err) {
      console.error('Failed to create game:', err)
      alert('Failed to create game')
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-gray-50 p-8">
      <div className="max-w-2xl mx-auto">
        <h1 className="text-3xl font-bold mb-6">Create New Game</h1>
        <div className="bg-white rounded-lg shadow-md p-6">
          <div className="mb-4">
            <label className="block text-sm font-medium mb-2">Select Scenario</label>
            <select
              value={selectedScenarioId || ''}
              onChange={(e) => setSelectedScenarioId(parseInt(e.target.value))}
              className="w-full px-3 py-2 border border-gray-300 rounded-md"
            >
              {scenarios.map((scenario) => (
                <option key={scenario.id} value={scenario.id}>
                  {scenario.name}
                </option>
              ))}
            </select>
          </div>
          <div className="flex gap-4">
            <button
              onClick={handleCreate}
              disabled={loading || !selectedScenarioId}
              className="px-6 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:bg-gray-400"
            >
              {loading ? 'Creating...' : 'Create Game'}
            </button>
            <button
              onClick={() => navigate('/gm')}
              className="px-6 py-2 bg-gray-600 text-white rounded-md hover:bg-gray-700"
            >
              Cancel
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}

