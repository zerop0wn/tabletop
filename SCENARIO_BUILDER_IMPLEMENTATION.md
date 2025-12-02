# Scenario Builder Implementation Summary

## Overview
A comprehensive modular scenario creation system has been implemented, allowing GMs to create, edit, and save scenarios through a user-friendly interface with template support.

## Backend Implementation

### 1. Database Models
- **ScenarioTemplate** model added (`backend/app/models.py`)
  - Stores reusable scenario templates
  - Supports public/private templates
  - Links to GM users for ownership

### 2. API Schemas (`backend/app/schemas.py`)
- **ArtifactCreate**: Schema for creating new artifacts
- **ArtifactUpdate**: Schema for updating existing artifacts
- **PhaseArtifactLink**: Schema for linking artifacts to phases (supports both new and existing artifacts)
- **ScenarioPhaseCreate**: Schema for creating phases with all fields
- **ScenarioCreate**: Schema for creating complete scenarios
- **ScenarioUpdate**: Schema for updating scenarios
- **ScenarioTemplateCreate/Response**: Schemas for template management

### 3. API Endpoints (`backend/app/routers/scenarios.py`)
- `POST /scenarios` - Create a new scenario with phases and artifacts
- `PUT /scenarios/{id}` - Update an existing scenario
- `DELETE /scenarios/{id}` - Delete a scenario (with validation for games using it)
- `POST /scenarios/templates` - Save a scenario as a template
- `GET /scenarios/templates` - List all accessible templates (public + user's own)
- `GET /scenarios/templates/{id}` - Get a specific template
- `DELETE /scenarios/templates/{id}` - Delete a template (owner only)

### 4. Database Migration
- Migration file: `backend/alembic/versions/7f8g9h0i1j2k3_add_scenario_templates.py`
- Creates `scenario_templates` table with all necessary fields

## Frontend Implementation

### 1. Types (`frontend/src/types.ts`)
- Added comprehensive types for scenario creation:
  - `ArtifactCreate`, `ArtifactType`
  - `PhaseArtifactLink`, `ScenarioPhaseCreate`
  - `ScenarioCreate`, `ScenarioUpdate`
  - `ScenarioTemplate`, `ScenarioTemplateCreate`

### 2. Scenario Builder Page (`frontend/src/pages/GMScenarioBuilder.tsx`)
A multi-step wizard interface with 4 steps:

#### Step 1: Scenario Metadata
- Scenario name, description, Miro board URL

#### Step 2: Phases
- Add/edit/delete phases
- Configure phase details:
  - Name, briefing text
  - Red/Blue objectives
  - Duration, Miro frame URL
  - GM prompt questions (2 questions)
  - Team-specific actions (Red/Blue)
- Phase ordering

#### Step 3: Artifacts
- Global artifact library
- Create/edit/delete artifacts
- Artifact types: log_snippet, screenshot, email, tool_output, intel_report
- Link artifacts to phases with team role assignment (Red/Blue/Both)
- Artifact fields: name, type, description, content, file_url, notes_for_gm

#### Step 4: Review
- Summary of scenario, phases, and artifacts
- Save scenario or save as template

### 3. Template Library Component (`frontend/src/components/TemplateLibrary.tsx`)
- Browse available templates (public + user's own)
- Load templates into scenario builder
- Save current scenario as template
- Delete templates (owner only)
- Template metadata: name, description, public/private flag

### 4. Navigation & Routing
- Added route: `/gm/scenarios/new` for scenario builder
- Added "Create Scenario" button to GM Games List page
- Integrated template library into scenario builder

## Key Features

### Modular Template System
- GMs can save scenarios as reusable templates
- Templates can be public (shared) or private
- Templates store complete scenario structure (phases, artifacts, metadata)
- Easy template loading into builder for modification

### Flexible Artifact Management
- Global artifact library - create once, use in multiple phases
- Artifacts can be linked to phases with team-specific visibility
- Support for multiple artifact types
- Rich content support (text, URLs, embedded content)

### Comprehensive Phase Configuration
- Full control over phase structure
- Team-specific objectives and actions
- GM prompt questions for engagement
- Configurable durations and Miro integration

### Validation & Safety
- Scenario deletion checks for active games
- Template access control (public vs private)
- Form validation at each step
- Error handling with user-friendly messages

## Usage Flow

1. **Create Scenario**:
   - Navigate to "Create Scenario" from GM dashboard
   - Fill in scenario metadata
   - Add phases with all details
   - Create artifacts and link to phases
   - Review and save

2. **Use Templates**:
   - Click "Template Library" in scenario builder
   - Browse available templates
   - Load a template to use as starting point
   - Modify as needed and save as new scenario

3. **Save as Template**:
   - Complete scenario creation
   - On review step, click "Save as Template"
   - Provide template name and description
   - Choose public/private visibility
   - Template saved for future use

## Technical Notes

### Artifact Linking Strategy
- Artifacts can be created inline when linking to phases
- Or linked from the global artifact library
- Team role assignment (red/blue/both) at link time
- Artifacts are copied when linking to avoid reference issues

### Data Structure
- Scenarios contain phases
- Phases contain artifact links (not direct artifacts)
- Artifacts are stored separately and referenced
- Templates store complete scenario structure as JSON

### API Design
- RESTful endpoints
- Proper error handling
- Validation at API level
- Support for partial updates (PUT endpoints)

## Future Enhancements (Potential)

1. **Scenario Editing UI**: Add ability to edit existing scenarios
2. **Template Marketplace**: Enhanced sharing and discovery
3. **Import/Export**: JSON import/export for scenarios
4. **Version Control**: Track scenario versions
5. **Bulk Operations**: Duplicate/clone scenarios
6. **Advanced Artifact Types**: Support for more artifact formats
7. **Phase Templates**: Reusable phase structures
8. **Validation Rules**: Advanced validation for scenario completeness

## Testing Recommendations

1. Test scenario creation with various configurations
2. Test template save/load functionality
3. Test artifact linking with different team roles
4. Test scenario deletion with/without active games
5. Test template access control (public/private)
6. Test form validation at each step
7. Test error handling for API failures

## Migration Instructions

To apply the database migration:
```bash
cd backend
alembic upgrade head
```

This will create the `scenario_templates` table.

## Conclusion

The scenario builder provides a complete, user-friendly solution for creating and managing cyber tabletop scenarios. The modular template system enables reuse and sharing, while the comprehensive phase and artifact management gives GMs full control over scenario structure.

