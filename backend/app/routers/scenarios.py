from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.auth import get_current_gm
from app.models import Scenario
from app.schemas import ScenarioResponse

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

