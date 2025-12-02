from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import and_
from typing import List
from app.database import get_db
from app.auth import get_current_gm
from app.models import Scenario, ScenarioPhase, Artifact, scenario_phase_artifacts, ScenarioTemplate
from app.schemas import (
    ScenarioResponse, ScenarioCreate, ScenarioUpdate,
    ScenarioPhaseCreate, PhaseArtifactLink,
    ScenarioTemplateCreate, ScenarioTemplateResponse
)

router = APIRouter()


@router.get("", response_model=List[ScenarioResponse])
def list_scenarios(db: Session = Depends(get_db), current_gm: dict = Depends(get_current_gm)):
    scenarios = db.query(Scenario).all()
    return scenarios


@router.get("/{scenario_id}", response_model=ScenarioResponse)
def get_scenario(scenario_id: int, db: Session = Depends(get_db), current_gm: dict = Depends(get_current_gm)):
    scenario = db.query(Scenario).filter(Scenario.id == scenario_id).first()
    if not scenario:
        raise HTTPException(status_code=404, detail="Scenario not found")
    return scenario


@router.post("", response_model=ScenarioResponse)
def create_scenario(
    scenario_data: ScenarioCreate,
    db: Session = Depends(get_db),
    current_gm: dict = Depends(get_current_gm)
):
    """Create a new scenario with phases and artifacts"""
    try:
        # Create scenario
        scenario = Scenario(
            name=scenario_data.name,
            description=scenario_data.description,
            miro_board_url=scenario_data.miro_board_url
        )
        db.add(scenario)
        db.flush()
        
        # Create phases
        for phase_data in scenario_data.phases:
            phase = ScenarioPhase(
                scenario_id=scenario.id,
                order_index=phase_data.order_index,
                name=phase_data.name,
                briefing_text=phase_data.briefing_text,
                red_objective=phase_data.red_objective,
                blue_objective=phase_data.blue_objective,
                default_duration_seconds=phase_data.default_duration_seconds,
                miro_frame_url=phase_data.miro_frame_url,
                available_actions=phase_data.available_actions,
                gm_prompt_questions=phase_data.gm_prompt_questions
            )
            db.add(phase)
            db.flush()
            
            # Handle artifacts for this phase
            for artifact_link in phase_data.artifacts:
                artifact = None
                
                # Create new artifact if provided
                if artifact_link.artifact:
                    artifact = Artifact(
                        name=artifact_link.artifact.name,
                        type=artifact_link.artifact.type,
                        description=artifact_link.artifact.description,
                        file_url=artifact_link.artifact.file_url,
                        embed_url=artifact_link.artifact.embed_url,
                        content=artifact_link.artifact.content,
                        notes_for_gm=getattr(artifact_link.artifact, 'notes_for_gm', None)
                    )
                    db.add(artifact)
                    db.flush()
                # Or use existing artifact
                elif artifact_link.artifact_id:
                    artifact = db.query(Artifact).filter(Artifact.id == artifact_link.artifact_id).first()
                    if not artifact:
                        raise HTTPException(
                            status_code=404,
                            detail=f"Artifact with id {artifact_link.artifact_id} not found"
                        )
                
                if artifact:
                    # Link artifact to phase
                    db.execute(
                        scenario_phase_artifacts.insert().values(
                            phase_id=phase.id,
                            artifact_id=artifact.id,
                            team_role=artifact_link.team_role
                        )
                    )
        
        db.commit()
        db.refresh(scenario)
        return scenario
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Failed to create scenario: {str(e)}")


@router.put("/{scenario_id}", response_model=ScenarioResponse)
def update_scenario(
    scenario_id: int,
    scenario_data: ScenarioUpdate,
    db: Session = Depends(get_db),
    current_gm: dict = Depends(get_current_gm)
):
    """Update an existing scenario"""
    scenario = db.query(Scenario).filter(Scenario.id == scenario_id).first()
    if not scenario:
        raise HTTPException(status_code=404, detail="Scenario not found")
    
    try:
        # Update scenario fields
        if scenario_data.name is not None:
            scenario.name = scenario_data.name
        if scenario_data.description is not None:
            scenario.description = scenario_data.description
        if scenario_data.miro_board_url is not None:
            scenario.miro_board_url = scenario_data.miro_board_url
        
        # If phases are provided, replace all phases
        if scenario_data.phases is not None:
            # Delete existing phases (cascade will handle artifacts)
            db.query(ScenarioPhase).filter(ScenarioPhase.scenario_id == scenario.id).delete()
            db.flush()
            
            # Create new phases
            for phase_data in scenario_data.phases:
                phase = ScenarioPhase(
                    scenario_id=scenario.id,
                    order_index=phase_data.order_index,
                    name=phase_data.name,
                    briefing_text=phase_data.briefing_text,
                    red_objective=phase_data.red_objective,
                    blue_objective=phase_data.blue_objective,
                    default_duration_seconds=phase_data.default_duration_seconds,
                    miro_frame_url=phase_data.miro_frame_url,
                    available_actions=phase_data.available_actions,
                    gm_prompt_questions=phase_data.gm_prompt_questions
                )
                db.add(phase)
                db.flush()
                
                # Handle artifacts for this phase
                for artifact_link in phase_data.artifacts:
                    artifact = None
                    
                    if artifact_link.artifact:
                        artifact = Artifact(
                            name=artifact_link.artifact.name,
                            type=artifact_link.artifact.type,
                            description=artifact_link.artifact.description,
                            file_url=artifact_link.artifact.file_url,
                            embed_url=artifact_link.artifact.embed_url,
                            content=artifact_link.artifact.content,
                            notes_for_gm=getattr(artifact_link.artifact, 'notes_for_gm', None)
                        )
                        db.add(artifact)
                        db.flush()
                    elif artifact_link.artifact_id:
                        artifact = db.query(Artifact).filter(Artifact.id == artifact_link.artifact_id).first()
                        if not artifact:
                            raise HTTPException(
                                status_code=404,
                                detail=f"Artifact with id {artifact_link.artifact_id} not found"
                            )
                    
                    if artifact:
                        db.execute(
                            scenario_phase_artifacts.insert().values(
                                phase_id=phase.id,
                                artifact_id=artifact.id,
                                team_role=artifact_link.team_role
                            )
                        )
        
        db.commit()
        db.refresh(scenario)
        return scenario
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Failed to update scenario: {str(e)}")


@router.delete("/{scenario_id}")
def delete_scenario(
    scenario_id: int,
    db: Session = Depends(get_db),
    current_gm: dict = Depends(get_current_gm)
):
    """Delete a scenario"""
    scenario = db.query(Scenario).filter(Scenario.id == scenario_id).first()
    if not scenario:
        raise HTTPException(status_code=404, detail="Scenario not found")
    
    # Check if scenario is used in any games
    from app.models import Game
    games_using_scenario = db.query(Game).filter(Game.scenario_id == scenario_id).count()
    if games_using_scenario > 0:
        raise HTTPException(
            status_code=400,
            detail=f"Cannot delete scenario: {games_using_scenario} game(s) are using this scenario"
        )
    
    try:
        db.delete(scenario)
        db.commit()
        return {"message": "Scenario deleted successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Failed to delete scenario: {str(e)}")


# Template endpoints
@router.post("/templates", response_model=ScenarioTemplateResponse)
def create_template(
    template_data: ScenarioTemplateCreate,
    db: Session = Depends(get_db),
    current_gm: dict = Depends(get_current_gm)
):
    """Create a new scenario template"""
    try:
        template = ScenarioTemplate(
            name=template_data.name,
            description=template_data.description,
            template_data=template_data.template_data,
            created_by_gm_id=current_gm.get("id"),
            is_public=template_data.is_public
        )
        db.add(template)
        db.commit()
        db.refresh(template)
        return template
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Failed to create template: {str(e)}")


@router.get("/templates", response_model=List[ScenarioTemplateResponse])
def list_templates(
    db: Session = Depends(get_db),
    current_gm: dict = Depends(get_current_gm)
):
    """List all templates (public and user's own)"""
    templates = db.query(ScenarioTemplate).filter(
        (ScenarioTemplate.is_public == True) |
        (ScenarioTemplate.created_by_gm_id == current_gm.get("id"))
    ).all()
    return templates


@router.get("/templates/{template_id}", response_model=ScenarioTemplateResponse)
def get_template(
    template_id: int,
    db: Session = Depends(get_db),
    current_gm: dict = Depends(get_current_gm)
):
    """Get a specific template"""
    template = db.query(ScenarioTemplate).filter(ScenarioTemplate.id == template_id).first()
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")
    
    # Check access
    if not template.is_public and template.created_by_gm_id != current_gm.get("id"):
        raise HTTPException(status_code=403, detail="Access denied")
    
    return template


@router.delete("/templates/{template_id}")
def delete_template(
    template_id: int,
    db: Session = Depends(get_db),
    current_gm: dict = Depends(get_current_gm)
):
    """Delete a template (only by owner)"""
    template = db.query(ScenarioTemplate).filter(ScenarioTemplate.id == template_id).first()
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")
    
    if template.created_by_gm_id != current_gm.get("id"):
        raise HTTPException(status_code=403, detail="Only template owner can delete")
    
    try:
        db.delete(template)
        db.commit()
        return {"message": "Template deleted successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Failed to delete template: {str(e)}")

