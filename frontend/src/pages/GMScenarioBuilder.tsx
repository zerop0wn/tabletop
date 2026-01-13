import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import apiClient from '../api/client'
import TemplateLibrary from '../components/TemplateLibrary'
import {
  ScenarioCreate,
  ScenarioPhaseCreate,
  ArtifactCreate,
  PhaseArtifactLink,
  ArtifactType
} from '../types'

type Step = 'scenario' | 'phases' | 'artifacts' | 'review'

export default function GMScenarioBuilder() {
  const navigate = useNavigate()
  const [currentStep, setCurrentStep] = useState<Step>('scenario')
  const [loading, setLoading] = useState(false)
  
  // Scenario data
  const [scenarioName, setScenarioName] = useState('')
  const [scenarioDescription, setScenarioDescription] = useState('')
  const [miroBoardUrl, setMiroBoardUrl] = useState('')
  
  // Phases data
  const [phases, setPhases] = useState<ScenarioPhaseCreate[]>([])
  const [editingPhaseIndex, setEditingPhaseIndex] = useState<number | null>(null)
  
  // Artifacts data (global artifact library)
  const [artifacts, setArtifacts] = useState<ArtifactCreate[]>([])
  const [editingArtifactIndex, setEditingArtifactIndex] = useState<number | null>(null)
  const [showTemplateLibrary, setShowTemplateLibrary] = useState(false)

  const handleNext = () => {
    if (currentStep === 'scenario') {
      if (!scenarioName.trim()) {
        alert('Please enter a scenario name')
        return
      }
      setCurrentStep('phases')
    } else if (currentStep === 'phases') {
      if (phases.length === 0) {
        alert('Please add at least one phase')
        return
      }
      setCurrentStep('artifacts')
    } else if (currentStep === 'artifacts') {
      setCurrentStep('review')
    }
  }

  const handleBack = () => {
    if (currentStep === 'phases') {
      setCurrentStep('scenario')
    } else if (currentStep === 'artifacts') {
      setCurrentStep('phases')
    } else if (currentStep === 'review') {
      setCurrentStep('artifacts')
    }
  }

  const handleAddPhase = () => {
    const newPhase: ScenarioPhaseCreate = {
      order_index: phases.length,
      name: `Phase ${phases.length + 1}`,
      briefing_text: '',
      red_objective: '',
      blue_objective: '',
      default_duration_seconds: 900,
      available_actions: {
        red: [],
        blue: []
      },
      gm_prompt_questions: [],
      artifacts: []
    }
    setPhases([...phases, newPhase])
    setEditingPhaseIndex(phases.length)
  }

  const handleUpdatePhase = (index: number, updates: Partial<ScenarioPhaseCreate>) => {
    const updated = [...phases]
    updated[index] = { ...updated[index], ...updates }
    setPhases(updated)
  }

  const handleDeletePhase = (index: number) => {
    const updated = phases.filter((_, i) => i !== index)
    // Reorder indices
    updated.forEach((phase, i) => {
      phase.order_index = i
    })
    setPhases(updated)
  }

  const handleAddArtifact = () => {
    const newArtifact: ArtifactCreate = {
      name: `Artifact ${artifacts.length + 1}`,
      type: 'log_snippet',
      description: '',
      content: ''
    }
    setArtifacts([...artifacts, newArtifact])
    setEditingArtifactIndex(artifacts.length)
  }

  const handleUpdateArtifact = (index: number, updates: Partial<ArtifactCreate>) => {
    const updated = [...artifacts]
    updated[index] = { ...updated[index], ...updates }
    setArtifacts(updated)
  }

  const handleDeleteArtifact = (index: number) => {
    setArtifacts(artifacts.filter((_, i) => i !== index))
    // Remove from phases
    const updatedPhases = phases.map(phase => ({
      ...phase,
      artifacts: phase.artifacts.filter(link => 
        link.artifact_id !== undefined || 
        (link.artifact && artifacts.indexOf(link.artifact as ArtifactCreate) !== index)
      )
    }))
    setPhases(updatedPhases)
  }

  const handleLinkArtifactToPhase = (phaseIndex: number, artifactIndex: number, teamRole?: 'red' | 'blue') => {
    const updated = [...phases]
    const artifact = artifacts[artifactIndex]
    // Create a copy of the artifact to avoid reference issues
    const artifactCopy: ArtifactCreate = {
      name: artifact.name,
      type: artifact.type,
      description: artifact.description,
      file_url: artifact.file_url,
      embed_url: artifact.embed_url,
      content: artifact.content,
      notes_for_gm: artifact.notes_for_gm
    }
    const link: PhaseArtifactLink = {
      artifact: artifactCopy,
      team_role: teamRole || null
    }
    updated[phaseIndex].artifacts = [...updated[phaseIndex].artifacts, link]
    setPhases(updated)
  }

  const handleUnlinkArtifact = (phaseIndex: number, linkIndex: number) => {
    const updated = [...phases]
    updated[phaseIndex].artifacts = updated[phaseIndex].artifacts.filter((_, i) => i !== linkIndex)
    setPhases(updated)
  }

  const handleSave = async () => {
    if (!scenarioName.trim()) {
      alert('Please enter a scenario name')
      return
    }
    if (phases.length === 0) {
      alert('Please add at least one phase')
      return
    }

    setLoading(true)
    try {
      const scenarioData: ScenarioCreate = {
        name: scenarioName,
        description: scenarioDescription || undefined,
        miro_board_url: miroBoardUrl || undefined,
        phases: phases
      }
      
      await apiClient.post('/scenarios', scenarioData)
      navigate('/gm')
    } catch (err: any) {
      console.error('Failed to create scenario:', err)
      alert(err.response?.data?.detail || 'Failed to create scenario')
      setLoading(false)
    }
  }

  const handleSaveAsTemplate = async () => {
    const templateName = prompt('Enter template name:')
    if (!templateName) return

    const templateDescription = prompt('Enter template description (optional):') || ''
    const isPublic = confirm('Make this template public?')

    try {
      const templateData = {
        name: scenarioName,
        description: scenarioDescription,
        miro_board_url: miroBoardUrl,
        phases: phases,
        artifacts: artifacts
      }

      await apiClient.post('/scenarios/templates', {
        name: templateName,
        description: templateDescription || undefined,
        template_data: templateData,
        is_public: isPublic
      })
      alert('Template saved successfully!')
    } catch (err: any) {
      console.error('Failed to save template:', err)
      alert(err.response?.data?.detail || 'Failed to save template')
    }
  }

  const renderScenarioStep = () => (
    <div className="space-y-4">
      <div>
        <label className="block text-sm font-medium mb-2">Scenario Name *</label>
        <input
          type="text"
          value={scenarioName}
          onChange={(e) => setScenarioName(e.target.value)}
          className="w-full px-3 py-2 border border-gray-300 rounded-md"
          placeholder="e.g., Ransomware Attack: Corporate Network Compromise"
        />
      </div>
      <div>
        <label className="block text-sm font-medium mb-2">Description</label>
        <textarea
          value={scenarioDescription}
          onChange={(e) => setScenarioDescription(e.target.value)}
          className="w-full px-3 py-2 border border-gray-300 rounded-md"
          rows={5}
          placeholder="Describe the scenario..."
        />
      </div>
      <div>
        <label className="block text-sm font-medium mb-2">Miro Board URL</label>
        <input
          type="url"
          value={miroBoardUrl}
          onChange={(e) => setMiroBoardUrl(e.target.value)}
          className="w-full px-3 py-2 border border-gray-300 rounded-md"
          placeholder="https://miro.com/app/board/..."
        />
      </div>
    </div>
  )

  const renderPhasesStep = () => (
    <div className="space-y-4">
      <div className="flex justify-between items-center">
        <h3 className="text-lg font-semibold">Phases</h3>
        <button
          onClick={handleAddPhase}
          className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700"
        >
          Add Phase
        </button>
      </div>
      
      {phases.map((phase, index) => (
        <div key={index} className="border border-gray-300 rounded-lg p-4">
          {editingPhaseIndex === index ? (
            <PhaseEditor
              phase={phase}
              onUpdate={(updates) => handleUpdatePhase(index, updates)}
              onSave={() => setEditingPhaseIndex(null)}
              onCancel={() => setEditingPhaseIndex(null)}
              onDelete={() => {
                handleDeletePhase(index)
                setEditingPhaseIndex(null)
              }}
            />
          ) : (
            <div className="flex justify-between items-start">
              <div>
                <h4 className="font-semibold">{phase.name}</h4>
                <p className="text-sm text-gray-600">Order: {phase.order_index + 1}</p>
                {phase.briefing_text && (
                  <p className="text-sm text-gray-500 mt-1 line-clamp-2">
                    {phase.briefing_text.substring(0, 100)}...
                  </p>
                )}
              </div>
              <button
                onClick={() => setEditingPhaseIndex(index)}
                className="px-3 py-1 bg-gray-600 text-white rounded-md hover:bg-gray-700"
              >
                Edit
              </button>
            </div>
          )}
        </div>
      ))}
      
      {phases.length === 0 && (
        <p className="text-gray-500 text-center py-8">No phases added yet. Click "Add Phase" to get started.</p>
      )}
    </div>
  )

  const renderArtifactsStep = () => (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h3 className="text-lg font-semibold">Artifacts Library</h3>
        <button
          onClick={handleAddArtifact}
          className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700"
        >
          Add Artifact
        </button>
      </div>
      
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {artifacts.map((artifact, index) => (
          <div key={index} className="border border-gray-300 rounded-lg p-4">
            {editingArtifactIndex === index ? (
              <ArtifactEditor
                artifact={artifact}
                onUpdate={(updates) => handleUpdateArtifact(index, updates)}
                onSave={() => setEditingArtifactIndex(null)}
                onCancel={() => setEditingArtifactIndex(null)}
                onDelete={() => {
                  handleDeleteArtifact(index)
                  setEditingArtifactIndex(null)
                }}
              />
            ) : (
              <div>
                <div className="flex justify-between items-start mb-2">
                  <div>
                    <h4 className="font-semibold">{artifact.name}</h4>
                    <p className="text-xs text-gray-500">{artifact.type}</p>
                  </div>
                  <button
                    onClick={() => setEditingArtifactIndex(index)}
                    className="px-2 py-1 text-sm bg-gray-600 text-white rounded hover:bg-gray-700"
                  >
                    Edit
                  </button>
                </div>
                {artifact.description && (
                  <p className="text-sm text-gray-600 line-clamp-2">{artifact.description}</p>
                )}
              </div>
            )}
          </div>
        ))}
      </div>
      
      {artifacts.length === 0 && (
        <p className="text-gray-500 text-center py-8">No artifacts added yet. Click "Add Artifact" to create one.</p>
      )}
      
      {/* Phase-Artifact Linking */}
      <div className="mt-8 border-t pt-6">
        <h3 className="text-lg font-semibold mb-4">Link Artifacts to Phases</h3>
        {phases.map((phase, phaseIndex) => (
          <div key={phaseIndex} className="mb-4 border border-gray-200 rounded p-4">
            <h4 className="font-semibold mb-2">{phase.name}</h4>
            <div className="space-y-2">
              {artifacts.map((artifact, artifactIndex) => {
                const isLinked = phase.artifacts.some(link => 
                  link.artifact?.name === artifact.name
                )
                return (
                  <div key={artifactIndex} className="flex items-center gap-2">
                    <input
                      type="checkbox"
                      checked={isLinked}
                      onChange={(e) => {
                        if (e.target.checked) {
                          handleLinkArtifactToPhase(phaseIndex, artifactIndex)
                        } else {
                          const linkIndex = phase.artifacts.findIndex(link => 
                            link.artifact?.name === artifact.name
                          )
                          if (linkIndex !== -1) {
                            handleUnlinkArtifact(phaseIndex, linkIndex)
                          }
                        }
                      }}
                      className="rounded"
                    />
                    <label className="text-sm">{artifact.name}</label>
                    {isLinked && (
                      <select
                        value={phase.artifacts.find(link => link.artifact?.name === artifact.name)?.team_role || ''}
                        onChange={(e) => {
                          const linkIndex = phase.artifacts.findIndex(link => 
                            link.artifact?.name === artifact.name
                          )
                          if (linkIndex !== -1) {
                            const updated = [...phases]
                            updated[phaseIndex].artifacts[linkIndex].team_role = 
                              e.target.value === '' ? null : (e.target.value as 'red' | 'blue')
                            setPhases(updated)
                          }
                        }}
                        className="ml-auto text-xs border rounded px-2 py-1"
                      >
                        <option value="">Both Teams</option>
                        <option value="red">Red Team Only</option>
                        <option value="blue">Blue Team Only</option>
                      </select>
                    )}
                  </div>
                )
              })}
            </div>
          </div>
        ))}
      </div>
    </div>
  )

  const renderReviewStep = () => (
    <div className="space-y-6">
      <div>
        <h3 className="text-lg font-semibold mb-2">Scenario: {scenarioName}</h3>
        {scenarioDescription && <p className="text-gray-600">{scenarioDescription}</p>}
      </div>
      
      <div>
        <h3 className="text-lg font-semibold mb-2">Phases ({phases.length})</h3>
        {phases.map((phase, index) => (
          <div key={index} className="border border-gray-300 rounded p-4 mb-2">
            <h4 className="font-semibold">{phase.name}</h4>
            <p className="text-sm text-gray-600">Artifacts: {phase.artifacts.length}</p>
          </div>
        ))}
      </div>
      
      <div>
        <h3 className="text-lg font-semibold mb-2">Total Artifacts: {artifacts.length}</h3>
      </div>
    </div>
  )

  return (
    <div className="min-h-screen bg-gray-50 p-8">
      <div className="max-w-4xl mx-auto">
        <div className="flex justify-between items-center mb-6">
          <h1 className="text-3xl font-bold">Create Scenario</h1>
          <button
            onClick={() => setShowTemplateLibrary(true)}
            className="px-4 py-2 bg-purple-600 text-white rounded-md hover:bg-purple-700"
          >
            Template Library
          </button>
        </div>
        
        {showTemplateLibrary && (
          <TemplateLibrary
            onLoadTemplate={(template) => {
              // Load template data into form
              if (template.template_data) {
                const data = template.template_data
                if (data.name) setScenarioName(data.name)
                if (data.description) setScenarioDescription(data.description)
                if (data.miro_board_url) setMiroBoardUrl(data.miro_board_url)
                if (data.phases) {
                  // Ensure phases have proper structure
                  const loadedPhases = data.phases.map((p: any) => ({
                    ...p,
                    artifacts: p.artifacts || []
                  }))
                  setPhases(loadedPhases)
                }
                if (data.artifacts) {
                  setArtifacts(data.artifacts)
                }
              }
              setShowTemplateLibrary(false)
            }}
            onClose={() => setShowTemplateLibrary(false)}
          />
        )}
        
        {/* Progress Steps */}
        <div className="mb-8">
          <div className="flex items-center justify-between">
            {(['scenario', 'phases', 'artifacts', 'review'] as Step[]).map((step, index) => (
              <div key={step} className="flex items-center flex-1">
                <div className={`flex items-center justify-center w-10 h-10 rounded-full ${
                  currentStep === step ? 'bg-blue-600 text-white' :
                  ['scenario', 'phases', 'artifacts', 'review'].indexOf(currentStep) > index ? 'bg-green-600 text-white' :
                  'bg-gray-300 text-gray-600'
                }`}>
                  {index + 1}
                </div>
                <div className="ml-2 text-sm font-medium capitalize">{step}</div>
                {index < 3 && (
                  <div className={`flex-1 h-1 mx-4 ${
                    ['scenario', 'phases', 'artifacts', 'review'].indexOf(currentStep) > index ? 'bg-green-600' : 'bg-gray-300'
                  }`} />
                )}
              </div>
            ))}
          </div>
        </div>
        
        {/* Step Content */}
        <div className="bg-white rounded-lg shadow-md p-6 mb-6">
          {currentStep === 'scenario' && renderScenarioStep()}
          {currentStep === 'phases' && renderPhasesStep()}
          {currentStep === 'artifacts' && renderArtifactsStep()}
          {currentStep === 'review' && renderReviewStep()}
        </div>
        
        {/* Navigation */}
        <div className="flex justify-between">
          <button
            onClick={handleBack}
            disabled={currentStep === 'scenario'}
            className="px-6 py-2 bg-gray-600 text-white rounded-md hover:bg-gray-700 disabled:bg-gray-400"
          >
            Back
          </button>
          <div className="flex gap-4">
            <button
              onClick={() => navigate('/gm')}
              className="px-6 py-2 bg-gray-600 text-white rounded-md hover:bg-gray-700"
            >
              Cancel
            </button>
            {currentStep === 'review' ? (
              <div className="flex gap-2">
                <button
                  onClick={handleSaveAsTemplate}
                  className="px-6 py-2 bg-purple-600 text-white rounded-md hover:bg-purple-700"
                >
                  Save as Template
                </button>
                <button
                  onClick={handleSave}
                  disabled={loading}
                  className="px-6 py-2 bg-green-600 text-white rounded-md hover:bg-green-700 disabled:bg-gray-400"
                >
                  {loading ? 'Saving...' : 'Save Scenario'}
              </button>
              </div>
            ) : (
              <button
                onClick={handleNext}
                className="px-6 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700"
              >
                Next
              </button>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}

// Phase Editor Component
function PhaseEditor({
  phase,
  onUpdate,
  onSave,
  onCancel,
  onDelete
}: {
  phase: ScenarioPhaseCreate
  onUpdate: (updates: Partial<ScenarioPhaseCreate>) => void
  onSave: () => void
  onCancel: () => void
  onDelete: () => void
}) {
  const [redActions, setRedActions] = useState(phase.available_actions?.red || [])
  const [blueActions, setBlueActions] = useState(phase.available_actions?.blue || [])
  const [gmQuestions, setGmQuestions] = useState(phase.gm_prompt_questions || ['', ''])

  const handleSave = () => {
    onUpdate({
      available_actions: {
        red: redActions,
        blue: blueActions
      },
      gm_prompt_questions: gmQuestions.filter(q => q.trim() !== '')
    })
    onSave()
  }

  return (
    <div className="space-y-4">
      <div>
        <label className="block text-sm font-medium mb-1">Phase Name *</label>
        <input
          type="text"
          value={phase.name}
          onChange={(e) => onUpdate({ name: e.target.value })}
          className="w-full px-3 py-2 border border-gray-300 rounded-md"
        />
      </div>
      <div>
        <label className="block text-sm font-medium mb-1">Briefing Text</label>
        <textarea
          value={phase.briefing_text || ''}
          onChange={(e) => onUpdate({ briefing_text: e.target.value })}
          className="w-full px-3 py-2 border border-gray-300 rounded-md"
          rows={4}
        />
      </div>
      <div className="grid grid-cols-2 gap-4">
        <div>
          <label className="block text-sm font-medium mb-1">Red Objective</label>
          <textarea
            value={phase.red_objective || ''}
            onChange={(e) => onUpdate({ red_objective: e.target.value })}
            className="w-full px-3 py-2 border border-gray-300 rounded-md"
            rows={3}
          />
        </div>
        <div>
          <label className="block text-sm font-medium mb-1">Blue Objective</label>
          <textarea
            value={phase.blue_objective || ''}
            onChange={(e) => onUpdate({ blue_objective: e.target.value })}
            className="w-full px-3 py-2 border border-gray-300 rounded-md"
            rows={3}
          />
        </div>
      </div>
      <div>
        <label className="block text-sm font-medium mb-1">Duration (seconds)</label>
        <input
          type="number"
          value={phase.default_duration_seconds || 900}
          onChange={(e) => onUpdate({ default_duration_seconds: parseInt(e.target.value) || 900 })}
          className="w-full px-3 py-2 border border-gray-300 rounded-md"
        />
      </div>
      <div>
        <label className="block text-sm font-medium mb-1">Miro Frame URL</label>
        <input
          type="url"
          value={phase.miro_frame_url || ''}
          onChange={(e) => onUpdate({ miro_frame_url: e.target.value })}
          className="w-full px-3 py-2 border border-gray-300 rounded-md"
        />
      </div>
      <div>
        <label className="block text-sm font-medium mb-1">GM Prompt Questions</label>
        <input
          type="text"
          value={gmQuestions[0] || ''}
          onChange={(e) => setGmQuestions([e.target.value, gmQuestions[1] || ''])}
          placeholder="Question 1"
          className="w-full px-3 py-2 border border-gray-300 rounded-md mb-2"
        />
        <input
          type="text"
          value={gmQuestions[1] || ''}
          onChange={(e) => setGmQuestions([gmQuestions[0] || '', e.target.value])}
          placeholder="Question 2"
          className="w-full px-3 py-2 border border-gray-300 rounded-md"
        />
      </div>
      <div className="grid grid-cols-2 gap-4">
        <div>
          <label className="block text-sm font-medium mb-1">Red Team Actions</label>
          <ActionListEditor
            actions={redActions}
            onChange={(actions) => setRedActions(actions)}
          />
        </div>
        <div>
          <label className="block text-sm font-medium mb-1">Blue Team Actions</label>
          <ActionListEditor
            actions={blueActions}
            onChange={(actions) => setBlueActions(actions)}
          />
        </div>
      </div>
      <div className="flex gap-2">
        <button
          onClick={handleSave}
          className="px-4 py-2 bg-green-600 text-white rounded-md hover:bg-green-700"
        >
          Save
        </button>
        <button
          onClick={onCancel}
          className="px-4 py-2 bg-gray-600 text-white rounded-md hover:bg-gray-700"
        >
          Cancel
        </button>
        <button
          onClick={onDelete}
          className="px-4 py-2 bg-red-600 text-white rounded-md hover:bg-red-700"
        >
          Delete
        </button>
      </div>
    </div>
  )
}

// Action List Editor Component
function ActionListEditor({
  actions,
  onChange
}: {
  actions: Array<{ name: string; description: string }>
  onChange: (actions: Array<{ name: string; description: string }>) => void
}) {
  const handleAdd = () => {
    onChange([...actions, { name: '', description: '' }])
  }

  const handleUpdate = (index: number, updates: Partial<{ name: string; description: string }>) => {
    const updated = [...actions]
    updated[index] = { ...updated[index], ...updates }
    onChange(updated)
  }

  const handleDelete = (index: number) => {
    onChange(actions.filter((_, i) => i !== index))
  }

  return (
    <div className="space-y-2">
      {actions.map((action, index) => (
        <div key={index} className="border border-gray-200 rounded p-2">
          <input
            type="text"
            value={action.name}
            onChange={(e) => handleUpdate(index, { name: e.target.value })}
            placeholder="Action name"
            className="w-full px-2 py-1 border border-gray-300 rounded mb-1 text-sm"
          />
          <textarea
            value={action.description}
            onChange={(e) => handleUpdate(index, { description: e.target.value })}
            placeholder="Action description"
            className="w-full px-2 py-1 border border-gray-300 rounded text-sm"
            rows={2}
          />
          <button
            onClick={() => handleDelete(index)}
            className="mt-1 text-xs text-red-600 hover:text-red-800"
          >
            Delete
          </button>
        </div>
      ))}
      <button
        onClick={handleAdd}
        className="text-sm text-blue-600 hover:text-blue-800"
      >
        + Add Action
      </button>
    </div>
  )
}

// Artifact Editor Component
function ArtifactEditor({
  artifact,
  onUpdate,
  onSave,
  onCancel,
  onDelete
}: {
  artifact: ArtifactCreate
  onUpdate: (updates: Partial<ArtifactCreate>) => void
  onSave: () => void
  onCancel: () => void
  onDelete: () => void
}) {
  return (
    <div className="space-y-3">
      <div>
        <label className="block text-xs font-medium mb-1">Name *</label>
        <input
          type="text"
          value={artifact.name}
          onChange={(e) => onUpdate({ name: e.target.value })}
          className="w-full px-2 py-1 border border-gray-300 rounded text-sm"
        />
      </div>
      <div>
        <label className="block text-xs font-medium mb-1">Type *</label>
        <select
          value={artifact.type}
          onChange={(e) => onUpdate({ type: e.target.value as ArtifactType })}
          className="w-full px-2 py-1 border border-gray-300 rounded text-sm"
        >
          <option value="log_snippet">Log Snippet</option>
          <option value="screenshot">Screenshot</option>
          <option value="email">Email</option>
          <option value="tool_output">Tool Output</option>
          <option value="intel_report">Intel Report</option>
        </select>
      </div>
      <div>
        <label className="block text-xs font-medium mb-1">Description</label>
        <textarea
          value={artifact.description || ''}
          onChange={(e) => onUpdate({ description: e.target.value })}
          className="w-full px-2 py-1 border border-gray-300 rounded text-sm"
          rows={2}
        />
      </div>
      <div>
        <label className="block text-xs font-medium mb-1">Content</label>
        <textarea
          value={artifact.content || ''}
          onChange={(e) => onUpdate({ content: e.target.value })}
          className="w-full px-2 py-1 border border-gray-300 rounded text-sm font-mono"
          rows={6}
        />
      </div>
      <div>
        <label className="block text-xs font-medium mb-1">File URL</label>
        <input
          type="url"
          value={artifact.file_url || ''}
          onChange={(e) => onUpdate({ file_url: e.target.value })}
          className="w-full px-2 py-1 border border-gray-300 rounded text-sm"
        />
      </div>
      <div>
        <label className="block text-xs font-medium mb-1">Notes for GM</label>
        <textarea
          value={artifact.notes_for_gm || ''}
          onChange={(e) => onUpdate({ notes_for_gm: e.target.value })}
          className="w-full px-2 py-1 border border-gray-300 rounded text-sm"
          rows={2}
        />
      </div>
      <div className="flex gap-2">
        <button
          onClick={onSave}
          className="px-3 py-1 bg-green-600 text-white rounded text-sm hover:bg-green-700"
        >
          Save
        </button>
        <button
          onClick={onCancel}
          className="px-3 py-1 bg-gray-600 text-white rounded text-sm hover:bg-gray-700"
        >
          Cancel
        </button>
        <button
          onClick={onDelete}
          className="px-3 py-1 bg-red-600 text-white rounded text-sm hover:bg-red-700"
        >
          Delete
        </button>
      </div>
    </div>
  )
}

