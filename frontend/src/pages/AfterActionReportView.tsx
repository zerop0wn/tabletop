import { useEffect, useState } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import apiClient from '../api/client'

interface PhaseAnalysis {
  phase_id: number
  phase_name: string
  phase_order: number
  average_rating?: number
  risk_rating: string
  total_responses: number
  comments: Array<{
    player_name: string
    team_role: string
    rating?: number
    comments: string
  }>
  gm_notes?: string
}

interface AfterActionReport {
  game_id: number
  scenario_name: string
  generated_at: string
  overall_risk_rating: string
  overall_risk_score: number
  phase_analyses: PhaseAnalysis[]
}

const getRiskColor = (risk: string) => {
  switch (risk) {
    case 'Critical':
      return 'bg-red-600 text-white'
    case 'High':
      return 'bg-orange-600 text-white'
    case 'Medium':
      return 'bg-yellow-500 text-white'
    case 'Low':
      return 'bg-green-500 text-white'
    case 'Very Low':
      return 'bg-blue-500 text-white'
    default:
      return 'bg-gray-500 text-white'
  }
}

export default function AfterActionReportView() {
  const { id } = useParams<{ id: string }>()
  const navigate = useNavigate()
  const [report, setReport] = useState<AfterActionReport | null>(null)
  const [loading, setLoading] = useState(true)
  const [generating, setGenerating] = useState(false)

  useEffect(() => {
    if (id) {
      fetchReport()
    }
  }, [id])

  const fetchReport = async () => {
    try {
      const response = await apiClient.get<AfterActionReport>(`/games/${id}/after-action-report`)
      setReport(response.data)
      setLoading(false)
    } catch (err: any) {
      if (err.response?.status === 404) {
        // Report doesn't exist yet, show generate button
        setLoading(false)
      } else {
        console.error('Failed to fetch report:', err)
        setLoading(false)
      }
    }
  }

  const generateReport = async () => {
    setGenerating(true)
    try {
      const response = await apiClient.get<AfterActionReport>(`/games/${id}/after-action-report`)
      setReport(response.data)
    } catch (err) {
      console.error('Failed to generate report:', err)
      alert('Failed to generate report')
    } finally {
      setGenerating(false)
    }
  }

  if (loading) {
    return <div className="p-8">Loading...</div>
  }

  if (!report) {
    return (
      <div className="min-h-screen bg-gray-50 p-8">
        <div className="max-w-4xl mx-auto">
          <div className="bg-white rounded-lg shadow-md p-6">
            <h1 className="text-2xl font-bold mb-4">After Action Report</h1>
            <p className="text-gray-600 mb-6">No report has been generated yet.</p>
            <button
              onClick={generateReport}
              disabled={generating}
              className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:bg-gray-400"
            >
              {generating ? 'Generating...' : 'Generate Report'}
            </button>
            <button
              onClick={() => navigate(`/gm/games/${id}`)}
              className="ml-4 px-4 py-2 bg-gray-600 text-white rounded-md hover:bg-gray-700"
            >
              Back to Game
            </button>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-50 p-8">
      <div className="max-w-6xl mx-auto">
        <div className="bg-white rounded-lg shadow-md p-6 mb-6">
          <div className="flex flex-col sm:flex-row sm:justify-between sm:items-center mb-6 gap-4">
            <div>
              <h1 className="text-2xl sm:text-3xl font-bold mb-2">After Action Report</h1>
              <p className="text-sm sm:text-base text-gray-600">
                {report.scenario_name} - Generated {new Date(report.generated_at).toLocaleString()}
              </p>
            </div>
            <div className="flex flex-wrap gap-2">
              <button
                onClick={async () => {
                  try {
                    const response = await apiClient.get(`/games/${id}/after-action-report/export/word`, {
                      responseType: 'blob'
                    })
                    const url = window.URL.createObjectURL(new Blob([response.data]))
                    const link = document.createElement('a')
                    link.href = url
                    link.setAttribute('download', `AAR_${report.scenario_name.replace(/[^a-z0-9]/gi, '_')}_${id}_${new Date().toISOString().split('T')[0]}.docx`)
                    document.body.appendChild(link)
                    link.click()
                    link.remove()
                    window.URL.revokeObjectURL(url)
                  } catch (err) {
                    console.error('Failed to export Word document:', err)
                    alert('Failed to export Word document')
                  }
                }}
                className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 font-medium text-sm sm:text-base"
              >
                Export Word
              </button>
              <button
                onClick={async () => {
                  try {
                    const response = await apiClient.get(`/games/${id}/after-action-report/export/pdf`, {
                      responseType: 'blob'
                    })
                    const url = window.URL.createObjectURL(new Blob([response.data]))
                    const link = document.createElement('a')
                    link.href = url
                    link.setAttribute('download', `AAR_${report.scenario_name.replace(/[^a-z0-9]/gi, '_')}_${id}_${new Date().toISOString().split('T')[0]}.pdf`)
                    document.body.appendChild(link)
                    link.click()
                    link.remove()
                    window.URL.revokeObjectURL(url)
                  } catch (err) {
                    console.error('Failed to export PDF document:', err)
                    alert('Failed to export PDF document')
                  }
                }}
                className="px-4 py-2 bg-red-600 text-white rounded-md hover:bg-red-700 font-medium text-sm sm:text-base"
              >
                Export PDF
              </button>
              <button
                onClick={() => navigate(`/gm/games/${id}`)}
                className="px-4 py-2 bg-gray-600 text-white rounded-md hover:bg-gray-700 font-medium text-sm sm:text-base"
              >
                Back to Game
              </button>
            </div>
          </div>

          {/* Overall Risk Summary */}
          <div className="bg-gradient-to-r from-blue-50 to-purple-50 rounded-lg p-6 mb-6">
            <h2 className="text-xl font-bold mb-4">Overall Risk Assessment</h2>
            <div className="flex items-center space-x-4">
              <div className={`px-6 py-3 rounded-lg ${getRiskColor(report.overall_risk_rating)}`}>
                <div className="text-sm font-semibold">Overall Risk Rating</div>
                <div className="text-3xl font-bold">{report.overall_risk_rating}</div>
              </div>
              <div className="flex-1">
                <div className="text-sm text-gray-600 mb-1">Average Effectiveness Score</div>
                <div className="text-2xl font-bold text-gray-800">
                  {report.overall_risk_score.toFixed(2)}/10
                </div>
                <div className="text-xs text-gray-500 mt-1">
                  Lower scores indicate higher risk
                </div>
              </div>
            </div>
          </div>

          {/* Risk Rating Legend */}
          <div className="mb-6 p-4 bg-gray-50 rounded-lg">
            <h3 className="font-semibold mb-2">Risk Rating Scale (Industry Standard - NIST/FIRST)</h3>
            <div className="grid grid-cols-5 gap-2 text-sm">
              <div className="text-center">
                <div className="bg-red-600 text-white px-2 py-1 rounded mb-1">Critical (1-2)</div>
                <div className="text-xs text-gray-600">Immediate action required</div>
              </div>
              <div className="text-center">
                <div className="bg-orange-600 text-white px-2 py-1 rounded mb-1">High (3-4)</div>
                <div className="text-xs text-gray-600">Address within 24-48 hours</div>
              </div>
              <div className="text-center">
                <div className="bg-yellow-500 text-white px-2 py-1 rounded mb-1">Medium (5-6)</div>
                <div className="text-xs text-gray-600">Address within 1 week</div>
              </div>
              <div className="text-center">
                <div className="bg-green-500 text-white px-2 py-1 rounded mb-1">Low (7-8)</div>
                <div className="text-xs text-gray-600">Address within 1 month</div>
              </div>
              <div className="text-center">
                <div className="bg-blue-500 text-white px-2 py-1 rounded mb-1">Very Low (9-10)</div>
                <div className="text-xs text-gray-600">Monitor and address as resources allow</div>
              </div>
            </div>
          </div>

          {/* Phase-by-Phase Analysis */}
          <div className="space-y-6">
            <h2 className="text-2xl font-bold mb-4">Phase-by-Phase Analysis</h2>
            {report.phase_analyses.map((phase) => (
              <div key={phase.phase_id} className="border border-gray-200 rounded-lg p-6">
                <div className="flex justify-between items-start mb-4">
                  <div>
                    <h3 className="text-xl font-bold">
                      Phase {phase.phase_order + 1}: {phase.phase_name}
                    </h3>
                    <p className="text-sm text-gray-500 mt-1">
                      {phase.total_responses} response{phase.total_responses !== 1 ? 's' : ''}
                    </p>
                  </div>
                  <div className="text-right">
                    {phase.average_rating !== null && phase.average_rating !== undefined ? (
                      <>
                        <div className={`px-4 py-2 rounded-lg ${getRiskColor(phase.risk_rating)}`}>
                          <div className="text-sm font-semibold">Risk Rating</div>
                          <div className="text-xl font-bold">{phase.risk_rating}</div>
                        </div>
                        <div className="text-sm text-gray-600 mt-2">
                          Avg: {phase.average_rating.toFixed(2)}/10
                        </div>
                      </>
                    ) : (
                      <div className="px-4 py-2 rounded-lg bg-gray-500 text-white">
                        <div className="text-sm font-semibold">Not Rated</div>
                      </div>
                    )}
                  </div>
                </div>

                {/* GM Notes */}
                {phase.gm_notes && (
                  <div className="mb-4 p-4 bg-yellow-50 border-l-4 border-yellow-400 rounded">
                    <h4 className="font-semibold mb-2">GM Notes & Takeaways</h4>
                    <p className="text-sm text-gray-700 whitespace-pre-wrap">{phase.gm_notes}</p>
                  </div>
                )}

                {!phase.gm_notes && (
                  <p className="text-sm text-gray-500 italic">No GM notes for this phase.</p>
                )}
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  )
}

