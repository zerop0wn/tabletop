import { useEffect, useState } from 'react'
import apiClient from '../api/client'
import { ScenarioTemplate, ScenarioTemplateCreate } from '../types'

interface TemplateLibraryProps {
  onLoadTemplate: (template: ScenarioTemplate) => void
  onClose: () => void
}

export default function TemplateLibrary({ onLoadTemplate, onClose }: TemplateLibraryProps) {
  const [templates, setTemplates] = useState<ScenarioTemplate[]>([])
  const [loading, setLoading] = useState(true)
  const [showCreateForm, setShowCreateForm] = useState(false)
  const [newTemplateName, setNewTemplateName] = useState('')
  const [newTemplateDescription, setNewTemplateDescription] = useState('')
  const [isPublic, setIsPublic] = useState(false)

  useEffect(() => {
    fetchTemplates()
  }, [])

  const fetchTemplates = async () => {
    try {
      const response = await apiClient.get<ScenarioTemplate[]>('/scenarios/templates')
      setTemplates(response.data)
    } catch (err) {
      console.error('Failed to fetch templates:', err)
    } finally {
      setLoading(false)
    }
  }

  const handleDelete = async (templateId: number) => {
    if (!confirm('Are you sure you want to delete this template?')) return
    
    try {
      await apiClient.delete(`/scenarios/templates/${templateId}`)
      fetchTemplates()
    } catch (err: any) {
      console.error('Failed to delete template:', err)
      alert(err.response?.data?.detail || 'Failed to delete template')
    }
  }

  const _handleSaveCurrentAsTemplate = async (scenarioData: any) => {
    if (!newTemplateName.trim()) {
      alert('Please enter a template name')
      return
    }

    try {
      const templateData: ScenarioTemplateCreate = {
        name: newTemplateName,
        description: newTemplateDescription || undefined,
        template_data: scenarioData,
        is_public: isPublic
      }
      
      await apiClient.post('/scenarios/templates', templateData)
      setShowCreateForm(false)
      setNewTemplateName('')
      setNewTemplateDescription('')
      setIsPublic(false)
      fetchTemplates()
      alert('Template saved successfully!')
    } catch (err: any) {
      console.error('Failed to save template:', err)
      alert(err.response?.data?.detail || 'Failed to save template')
    }
  }

  if (loading) {
    return (
      <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
        <div className="bg-white rounded-lg p-6">
          <p>Loading templates...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white rounded-lg shadow-xl max-w-4xl w-full max-h-[90vh] overflow-y-auto m-4">
        <div className="p-6">
          <div className="flex justify-between items-center mb-4">
            <h2 className="text-2xl font-bold">Template Library</h2>
            <div className="flex gap-2">
              <button
                onClick={() => setShowCreateForm(!showCreateForm)}
                className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700"
              >
                {showCreateForm ? 'Cancel' : 'Save Current as Template'}
              </button>
              <button
                onClick={onClose}
                className="px-4 py-2 bg-gray-600 text-white rounded-md hover:bg-gray-700"
              >
                Close
              </button>
            </div>
          </div>

          {showCreateForm && (
            <div className="mb-6 p-4 border border-gray-300 rounded-lg bg-gray-50">
              <h3 className="font-semibold mb-3">Save Current Scenario as Template</h3>
              <div className="space-y-3">
                <div>
                  <label className="block text-sm font-medium mb-1">Template Name *</label>
                  <input
                    type="text"
                    value={newTemplateName}
                    onChange={(e) => setNewTemplateName(e.target.value)}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md"
                    placeholder="e.g., Ransomware Attack Template"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium mb-1">Description</label>
                  <textarea
                    value={newTemplateDescription}
                    onChange={(e) => setNewTemplateDescription(e.target.value)}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md"
                    rows={3}
                    placeholder="Describe this template..."
                  />
                </div>
                <div className="flex items-center">
                  <input
                    type="checkbox"
                    id="isPublic"
                    checked={isPublic}
                    onChange={(e) => setIsPublic(e.target.checked)}
                    className="mr-2"
                  />
                  <label htmlFor="isPublic" className="text-sm">Make this template public</label>
                </div>
                <p className="text-xs text-gray-500">
                  Note: You'll need to provide the scenario data when saving. This form is for template metadata.
                </p>
              </div>
            </div>
          )}

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {templates.map((template) => (
              <div key={template.id} className="border border-gray-300 rounded-lg p-4">
                <div className="flex justify-between items-start mb-2">
                  <div>
                    <h3 className="font-semibold">{template.name}</h3>
                    {template.is_public && (
                      <span className="text-xs bg-green-100 text-green-800 px-2 py-1 rounded">
                        Public
                      </span>
                    )}
                  </div>
                  {template.created_by_gm_id && (
                    <button
                      onClick={() => handleDelete(template.id)}
                      className="text-red-600 hover:text-red-800 text-sm"
                    >
                      Delete
                    </button>
                  )}
                </div>
                {template.description && (
                  <p className="text-sm text-gray-600 mb-2">{template.description}</p>
                )}
                <p className="text-xs text-gray-500 mb-3">
                  Created: {new Date(template.created_at).toLocaleDateString()}
                </p>
                <button
                  onClick={() => onLoadTemplate(template)}
                  className="w-full px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700"
                >
                  Load Template
                </button>
              </div>
            ))}
          </div>

          {templates.length === 0 && (
            <p className="text-center text-gray-500 py-8">No templates available. Create one to get started!</p>
          )}
        </div>
      </div>
    </div>
  )
}

