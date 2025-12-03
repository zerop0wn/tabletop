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
        <div className="flex justify-between items-center mb-6">
          <h1 className="text-3xl font-bold">Create New Game</h1>
          <button
            onClick={() => navigate('/gm/scenarios/new')}
            className="px-4 py-2 bg-purple-600 text-white rounded-md hover:bg-purple-700"
          >
            Create Scenario
          </button>
        </div>
        <div className="bg-white rounded-lg shadow-md p-6">
          <div className="mb-4">
            <div className="flex justify-between items-center mb-2">
              <label className="block text-sm font-medium">Select Scenario</label>
              {scenarios.length === 0 && (
                <span className="text-sm text-gray-500">No scenarios available</span>
              )}
            </div>
            {scenarios.length === 0 ? (
              <div className="border-2 border-dashed border-gray-300 rounded-md p-8 text-center">
                <p className="text-gray-600 mb-4">No scenarios found. Create one to get started!</p>
                <button
                  onClick={() => navigate('/gm/scenarios/new')}
                  className="px-6 py-2 bg-purple-600 text-white rounded-md hover:bg-purple-700"
                >
                  Create Your First Scenario
                </button>
              </div>
            ) : (
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
            )}
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

