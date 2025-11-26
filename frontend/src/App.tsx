import { BrowserRouter, Routes, Route } from 'react-router-dom'
import GMLogin from './pages/GMLogin'
import GMGamesList from './pages/GMGamesList'
import GMGameDashboard from './pages/GMGameDashboard'
import GMCreateGame from './pages/GMCreateGame'
import PlayerJoin from './pages/PlayerJoin'
import PlayerView from './pages/PlayerView'
import AudienceView from './pages/AudienceView'

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={
          <div className="min-h-screen bg-gray-50 p-8">
            <div className="max-w-4xl mx-auto text-center">
              <h1 className="text-4xl font-bold mb-6">Cyber Tabletop</h1>
              <p className="text-xl text-gray-600 mb-8">Turn-Based Incident Response Training Platform</p>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <a href="/gm/login" className="p-6 bg-blue-600 text-white rounded-lg hover:bg-blue-700">
                  <h2 className="text-xl font-semibold mb-2">Game Master</h2>
                  <p className="text-sm">Manage scenarios and games</p>
                </a>
                <a href="/play/join" className="p-6 bg-green-600 text-white rounded-lg hover:bg-green-700">
                  <h2 className="text-xl font-semibold mb-2">Join Game</h2>
                  <p className="text-sm">Enter with team code</p>
                </a>
                <a href="/audience/demo" className="p-6 bg-purple-600 text-white rounded-lg hover:bg-purple-700">
                  <h2 className="text-xl font-semibold mb-2">Audience View</h2>
                  <p className="text-sm">Watch game progress</p>
                </a>
              </div>
            </div>
          </div>
        } />
        <Route path="/gm/login" element={<GMLogin />} />
        <Route path="/gm" element={<GMGamesList />} />
        <Route path="/gm/games/new" element={<GMCreateGame />} />
        <Route path="/gm/games/:id" element={<GMGameDashboard />} />
        <Route path="/play/join" element={<PlayerJoin />} />
        <Route path="/play/game/:gameId/player/:playerId" element={<PlayerView />} />
        <Route path="/audience/:gameIdentifier" element={<AudienceView />} />
      </Routes>
    </BrowserRouter>
  )
}

export default App

