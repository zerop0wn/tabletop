import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import apiClient from '../api/client'
import { Game } from '../types'

export default function GMGamesList() {
  const [games, setGames] = useState<Game[]>([])
  const [loading, setLoading] = useState(true)
  const [showPasswordModal, setShowPasswordModal] = useState(false)
  const [currentPassword, setCurrentPassword] = useState('')
  const [newPassword, setNewPassword] = useState('')
  const [confirmPassword, setConfirmPassword] = useState('')
  const [passwordError, setPasswordError] = useState('')
  const [passwordSuccess, setPasswordSuccess] = useState(false)
  const navigate = useNavigate()

  useEffect(() => {
    const token = localStorage.getItem('gm_token')
    if (!token) {
      navigate('/gm/login')
      return
    }

    fetchGames()
    const interval = setInterval(fetchGames, 10000) // Poll every 10 seconds
    return () => clearInterval(interval)
  }, [navigate])

  const fetchGames = async () => {
    try {
      const response = await apiClient.get<Game[]>('/games')
      setGames(response.data)
      setLoading(false)
    } catch (err) {
      console.error('Failed to fetch games:', err)
      setLoading(false)
    }
  }

  const handleChangePassword = async () => {
    setPasswordError('')
    setPasswordSuccess(false)

    if (!currentPassword || !newPassword || !confirmPassword) {
      setPasswordError('All fields are required')
      return
    }

    if (newPassword.length < 6) {
      setPasswordError('New password must be at least 6 characters long')
      return
    }

    if (newPassword !== confirmPassword) {
      setPasswordError('New passwords do not match')
      return
    }

    try {
      await apiClient.post('/auth/change-password', {
        current_password: currentPassword,
        new_password: newPassword,
      })
      setPasswordSuccess(true)
      setCurrentPassword('')
      setNewPassword('')
      setConfirmPassword('')
      setTimeout(() => {
        setShowPasswordModal(false)
        setPasswordSuccess(false)
      }, 2000)
    } catch (err: any) {
      setPasswordError(err.response?.data?.detail || 'Failed to change password')
    }
  }

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'in_progress':
        return 'bg-green-100 text-green-800'
      case 'finished':
        return 'bg-gray-100 text-gray-800'
      case 'paused':
        return 'bg-yellow-100 text-yellow-800'
      default:
        return 'bg-blue-100 text-blue-800'
    }
  }

  if (loading) {
    return <div className="p-8">Loading...</div>
  }

  return (
    <div className="min-h-screen bg-gray-50 p-4 sm:p-6 lg:p-8">
      <div className="max-w-6xl mx-auto">
        {/* Header - Mobile responsive */}
        <div className="flex flex-col sm:flex-row sm:justify-between sm:items-center mb-6 gap-4">
          <h1 className="text-2xl sm:text-3xl font-bold">Game Manager Console</h1>
          <div className="flex flex-wrap gap-2">
            <button
              onClick={() => navigate('/gm/scenarios/new')}
              className="flex-1 sm:flex-none px-4 py-2.5 bg-purple-600 text-white rounded-md hover:bg-purple-700 text-sm sm:text-base font-medium"
            >
              Create Scenario
            </button>
            <button
              onClick={() => navigate('/gm/games/new')}
              className="flex-1 sm:flex-none px-4 py-2.5 bg-blue-600 text-white rounded-md hover:bg-blue-700 text-sm sm:text-base font-medium"
            >
              New Game
            </button>
            <button
              onClick={() => setShowPasswordModal(true)}
              className="flex-1 sm:flex-none px-4 py-2.5 bg-indigo-600 text-white rounded-md hover:bg-indigo-700 text-sm sm:text-base font-medium"
            >
              Change Password
            </button>
            <button
              onClick={() => navigate('/gm/login')}
              className="flex-1 sm:flex-none px-4 py-2.5 bg-gray-600 text-white rounded-md hover:bg-gray-700 text-sm sm:text-base font-medium"
            >
              Logout
            </button>
          </div>
        </div>

        {/* Create Scenario Card - Prominent */}
        <div className="mb-6 bg-gradient-to-r from-purple-500 to-purple-600 rounded-lg shadow-lg p-6 text-white">
          <div className="flex flex-col sm:flex-row justify-between items-center gap-4">
            <div>
              <h2 className="text-2xl font-bold mb-2">Create a New Scenario</h2>
              <p className="text-purple-100">Build custom cyber incident response scenarios with phases, artifacts, and team objectives</p>
            </div>
            <button
              onClick={() => navigate('/gm/scenarios/new')}
              className="px-6 py-3 bg-white text-purple-600 rounded-md hover:bg-purple-50 font-semibold text-lg shadow-md transition-all"
            >
              Create Scenario →
            </button>
          </div>
        </div>

        {/* Desktop Table View */}
        <div className="hidden md:block bg-white rounded-lg shadow-md overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">ID</th>
                <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Scenario</th>
                <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Status</th>
                <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Phase</th>
                <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Created</th>
                <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase min-w-[200px]">Actions</th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {games.map((game) => (
                <tr key={game.id}>
                  <td className="px-4 py-4 whitespace-nowrap text-sm font-medium">{game.id}</td>
                  <td className="px-4 py-4 text-sm max-w-xs truncate">
                    {game.scenario?.name || 'Unknown'}
                  </td>
                  <td className="px-4 py-4 whitespace-nowrap">
                    <span className={`px-2 py-1 text-xs font-semibold rounded-full ${getStatusColor(game.status)}`}>
                      {game.status}
                    </span>
                  </td>
                  <td className="px-4 py-4 text-sm max-w-xs truncate">
                    {game.current_phase?.name || 'N/A'}
                  </td>
                  <td className="px-4 py-4 whitespace-nowrap text-sm text-gray-500">
                    {new Date(game.created_at).toLocaleDateString()}
                  </td>
                  <td className="px-4 py-4 whitespace-nowrap text-sm">
                    <div className="flex gap-2 flex-nowrap">
                      <button
                        onClick={() => navigate(`/gm/games/${game.id}`)}
                        className="px-3 py-1.5 text-blue-600 hover:text-blue-800 hover:bg-blue-50 rounded text-sm font-medium whitespace-nowrap flex-shrink-0"
                      >
                        Open
                      </button>
                      {(game.status === 'in_progress' || game.status === 'finished') && (
                        <button
                          onClick={() => navigate(`/gm/games/${game.id}/after-action-report`)}
                          className="px-3 py-1.5 text-purple-600 hover:text-purple-800 hover:bg-purple-50 rounded text-sm font-medium whitespace-nowrap flex-shrink-0"
                        >
                          AAR
                        </button>
                      )}
                      <button
                        onClick={async () => {
                          if (confirm(`Are you sure you want to delete game ${game.id}? This action cannot be undone.`)) {
                            try {
                              await apiClient.delete(`/games/${game.id}`)
                              fetchGames()
                            } catch (err: any) {
                              alert(err.response?.data?.detail || 'Failed to delete game')
                            }
                          }
                        }}
                        className="px-3 py-1.5 text-red-600 hover:text-red-800 hover:bg-red-50 rounded text-sm font-medium whitespace-nowrap flex-shrink-0"
                      >
                        Delete
                      </button>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        {/* Mobile Card View */}
        <div className="md:hidden space-y-4">
          {games.map((game) => (
            <div key={game.id} className="bg-white rounded-lg shadow-md p-4">
              <div className="flex justify-between items-start mb-3">
                <div className="flex-1">
                  <div className="flex items-center gap-2 mb-1">
                    <span className="text-sm font-medium text-gray-500">ID:</span>
                    <span className="text-sm font-semibold">{game.id}</span>
                  </div>
                  <h3 className="text-lg font-semibold text-gray-900 mb-2">
                    {game.scenario?.name || 'Unknown'}
                  </h3>
                  <div className="flex items-center gap-2 mb-2">
                    <span className={`px-2 py-1 text-xs font-semibold rounded-full ${getStatusColor(game.status)}`}>
                      {game.status}
                    </span>
                  </div>
                </div>
              </div>
              
              <div className="space-y-2 mb-4 text-sm">
                <div className="flex items-center gap-2">
                  <span className="text-gray-500">Phase:</span>
                  <span className="font-medium">{game.current_phase?.name || 'N/A'}</span>
                </div>
                <div className="flex items-center gap-2">
                  <span className="text-gray-500">Created:</span>
                  <span className="font-medium">{new Date(game.created_at).toLocaleDateString()}</span>
                </div>
              </div>

              {/* Action Buttons - Always visible on mobile */}
              <div className="flex gap-2 pt-3 border-t border-gray-200">
                <button
                  onClick={() => navigate(`/gm/games/${game.id}`)}
                  className="flex-1 px-4 py-3 bg-blue-600 text-white rounded-md hover:bg-blue-700 font-medium text-sm"
                >
                  Open Game
                </button>
                {(game.status === 'in_progress' || game.status === 'finished') && (
                  <button
                    onClick={() => navigate(`/gm/games/${game.id}/after-action-report`)}
                    className="flex-1 px-4 py-3 bg-purple-600 text-white rounded-md hover:bg-purple-700 font-medium text-sm"
                  >
                    AAR
                  </button>
                )}
                <button
                  onClick={async () => {
                    if (confirm(`Are you sure you want to delete game ${game.id}? This action cannot be undone.`)) {
                      try {
                        await apiClient.delete(`/games/${game.id}`)
                        fetchGames()
                      } catch (err: any) {
                        alert(err.response?.data?.detail || 'Failed to delete game')
                      }
                    }
                  }}
                  className="flex-1 px-4 py-3 bg-red-600 text-white rounded-md hover:bg-red-700 font-medium text-sm"
                >
                  Delete
                </button>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Password Change Modal */}
      {showPasswordModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg shadow-xl p-6 max-w-md w-full mx-4">
            <h2 className="text-2xl font-bold mb-4">Change Password</h2>
            
            {passwordSuccess && (
              <div className="mb-4 p-3 bg-green-100 border border-green-400 text-green-700 rounded">
                Password changed successfully!
              </div>
            )}

            {passwordError && (
              <div className="mb-4 p-3 bg-red-100 border border-red-400 text-red-700 rounded">
                {passwordError}
              </div>
            )}

            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium mb-1">Current Password</label>
                <input
                  type="password"
                  value={currentPassword}
                  onChange={(e) => setCurrentPassword(e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md"
                  placeholder="Enter current password"
                />
              </div>
              <div>
                <label className="block text-sm font-medium mb-1">New Password</label>
                <input
                  type="password"
                  value={newPassword}
                  onChange={(e) => setNewPassword(e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md"
                  placeholder="Enter new password (min 6 characters)"
                />
              </div>
              <div>
                <label className="block text-sm font-medium mb-1">Confirm New Password</label>
                <input
                  type="password"
                  value={confirmPassword}
                  onChange={(e) => setConfirmPassword(e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md"
                  placeholder="Confirm new password"
                />
              </div>
            </div>

            <div className="flex gap-2 mt-6">
              <button
                onClick={handleChangePassword}
                className="flex-1 px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700"
              >
                Change Password
              </button>
              <button
                onClick={() => {
                  setShowPasswordModal(false)
                  setPasswordError('')
                  setPasswordSuccess(false)
                  setCurrentPassword('')
                  setNewPassword('')
                  setConfirmPassword('')
                }}
                className="flex-1 px-4 py-2 bg-gray-600 text-white rounded-md hover:bg-gray-700"
              >
                Cancel
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

