from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from app.models import GameStatus, PhaseState, DecisionStatus, ArtifactType


# Auth schemas
class Token(BaseModel):
    access_token: str
    token_type: str


class LoginRequest(BaseModel):
    username: str
    password: str


# Scenario schemas
class ArtifactBase(BaseModel):
    name: str
    type: ArtifactType
    description: Optional[str] = None
    file_url: Optional[str] = None
    embed_url: Optional[str] = None


class ArtifactResponse(ArtifactBase):
    id: int

    class Config:
        from_attributes = True


class ScenarioPhaseBase(BaseModel):
    order_index: int
    name: str
    briefing_text: Optional[str] = None
    red_objective: Optional[str] = None
    blue_objective: Optional[str] = None
    default_duration_seconds: Optional[int] = None
    miro_frame_url: Optional[str] = None


class ScenarioPhaseResponse(ScenarioPhaseBase):
    id: int
    scenario_id: int
    artifacts: List[ArtifactResponse] = []

    class Config:
        from_attributes = True


class ScenarioBase(BaseModel):
    name: str
    description: Optional[str] = None
    miro_board_url: Optional[str] = None


class ScenarioResponse(ScenarioBase):
    id: int
    created_at: datetime
    phases: List[ScenarioPhaseResponse] = []

    class Config:
        from_attributes = True


# Game schemas
class GameCreate(BaseModel):
    scenario_id: int
    settings: Optional[Dict[str, Any]] = {}


class GameResponse(BaseModel):
    id: int
    scenario_id: int
    status: GameStatus
    current_phase_id: Optional[int] = None
    phase_state: PhaseState
    created_at: datetime
    gm_id: int
    red_team_code: str
    blue_team_code: str
    audience_code: Optional[str] = None
    miro_session_url: Optional[str] = None
    settings: Dict[str, Any] = {}
    scenario: Optional[ScenarioResponse] = None
    current_phase: Optional[ScenarioPhaseResponse] = None

    class Config:
        from_attributes = True


# Team schemas
class TeamResponse(BaseModel):
    id: int
    game_id: int
    name: str
    code: str
    role: str

    class Config:
        from_attributes = True


# Player schemas
class JoinRequest(BaseModel):
    team_code: str
    display_name: str


class JoinResponse(BaseModel):
    player_id: int
    team_id: int
    game_id: int
    team_role: str
    game_basic_info: Dict[str, Any]


class PlayerStateResponse(BaseModel):
    current_phase: Optional[ScenarioPhaseResponse] = None
    phase_state: PhaseState
    phase_briefing_text: Optional[str] = None
    team_objective: Optional[str] = None
    artifacts: List[ArtifactResponse] = []
    decision: Optional["DecisionResponse"] = None
    game_status: GameStatus
    team_role: Optional[str] = None
    team_name: Optional[str] = None
    has_voted: bool = False
    team_voting_status: Optional["VotingStatusResponse"] = None


# Decision schemas
class VoteSubmit(BaseModel):
    player_id: int
    selected_action: str  # Single action voted for
    effectiveness_rating: int = Field(..., ge=1, le=10, description="Rating 1-10: How effective would your organization be at detecting and responding to this phase")
    comments: Optional[str] = Field(None, max_length=500, description="Optional comments (max 500 characters)")
    justification: Optional[str] = None  # Kept for backward compatibility


class DecisionSubmit(BaseModel):
    player_id: int
    actions: Dict[str, Any]
    free_text_justification: str


class DecisionResponse(BaseModel):
    id: int
    game_id: int
    team_id: int
    phase_id: int
    submitted_at: datetime
    actions: Dict[str, Any]
    free_text_justification: Optional[str] = None
    status: DecisionStatus
    score_awarded: Optional[int] = None
    gm_notes: Optional[str] = None
    team: Optional[TeamResponse] = None

    class Config:
        from_attributes = True


class DecisionScore(BaseModel):
    score_awarded: int
    gm_notes: Optional[str] = None


class PlayerVoteResponse(BaseModel):
    id: int
    player_id: int
    player_name: str
    selected_action: str
    effectiveness_rating: Optional[int] = None
    comments: Optional[str] = None
    justification: Optional[str] = None  # Kept for backward compatibility
    voted_at: datetime

    class Config:
        from_attributes = True


class VotingStatusResponse(BaseModel):
    team_id: int
    team_name: str
    total_players: int
    votes_submitted: int
    votes: List[PlayerVoteResponse] = []
    all_voted: bool


# Scoreboard schemas
class ScoreHistoryEntry(BaseModel):
    phase_name: str
    phase_order: int
    score: int


class RecentEvent(BaseModel):
    delta: int
    reason: str
    created_at: Optional[str] = None


class GlobalEvent(BaseModel):
    team_id: int
    team_name: str
    team_role: str
    delta: int
    reason: str
    created_at: Optional[str] = None


class RecentDecision(BaseModel):
    action: Optional[str] = None
    score_awarded: Optional[int] = None
    submitted_at: Optional[str] = None


class VotingStatus(BaseModel):
    total_players: int
    votes_submitted: int
    all_voted: bool


class TeamScore(BaseModel):
    team_id: int
    team_name: str
    team_role: str
    total_score: int
    team_members: List[str] = []  # List of player display names
    recent_events: List[RecentEvent] = []
    score_history: List[ScoreHistoryEntry] = []
    recent_decision: Optional[RecentDecision] = None
    voting_status: Optional[VotingStatus] = None


class ScoreboardResponse(BaseModel):
    game_id: int
    scenario_name: str
    current_phase_name: Optional[str] = None
    phase_state: PhaseState
    teams: List[TeamScore] = []
    recent_events: List[GlobalEvent] = []


# New schemas for rating and comments system
class PhaseCommentResponse(BaseModel):
    player_id: int
    player_name: str
    team_name: str
    team_role: str
    effectiveness_rating: Optional[int] = None
    comments: Optional[str] = None
    voted_at: datetime


class PhaseCommentsResponse(BaseModel):
    comments: List[PhaseCommentResponse]


class GMNotesUpdate(BaseModel):
    notes: str


class PhaseAnalysis(BaseModel):
    phase_id: int
    phase_name: str
    phase_order: int
    average_rating: Optional[float] = None
    risk_rating: str
    total_responses: int
    comments: List[Dict[str, Any]]
    gm_notes: Optional[str] = None


class AfterActionReportResponse(BaseModel):
    game_id: int
    scenario_name: str
    generated_at: str
    overall_risk_rating: str
    overall_risk_score: float
    phase_analyses: List[PhaseAnalysis]


# Update forward references
PlayerStateResponse.model_rebuild()
VotingStatusResponse.model_rebuild()

