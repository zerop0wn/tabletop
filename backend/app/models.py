from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, JSON, Enum as SQLEnum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime
import enum
from app.database import Base


class GameStatus(str, enum.Enum):
    LOBBY = "lobby"
    IN_PROGRESS = "in_progress"
    PAUSED = "paused"
    FINISHED = "finished"


class PhaseState(str, enum.Enum):
    NOT_STARTED = "not_started"
    BRIEFING = "briefing"
    OPEN_FOR_DECISIONS = "open_for_decisions"
    DECISION_LOCK = "decision_lock"
    RESOLUTION = "resolution"
    COMPLETE = "complete"


class DecisionStatus(str, enum.Enum):
    DRAFT = "draft"
    SUBMITTED = "submitted"
    LOCKED = "locked"
    SCORED = "scored"


class ArtifactType(str, enum.Enum):
    LOG_SNIPPET = "log_snippet"
    SCREENSHOT = "screenshot"
    EMAIL = "email"
    TOOL_OUTPUT = "tool_output"
    INTEL_REPORT = "intel_report"


class GMUser(Base):
    __tablename__ = "gm_users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Scenario(Base):
    __tablename__ = "scenarios"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(Text)
    miro_board_url = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    phases = relationship("ScenarioPhase", back_populates="scenario", order_by="ScenarioPhase.order_index")


class ScenarioPhase(Base):
    __tablename__ = "scenario_phases"

    id = Column(Integer, primary_key=True, index=True)
    scenario_id = Column(Integer, ForeignKey("scenarios.id"), nullable=False)
    order_index = Column(Integer, nullable=False)
    name = Column(String, nullable=False)
    briefing_text = Column(Text)
    red_objective = Column(Text, nullable=True)
    blue_objective = Column(Text, nullable=True)
    default_duration_seconds = Column(Integer, nullable=True)
    miro_frame_url = Column(String, nullable=True)
    available_actions = Column(JSON, nullable=True)  # Phase-specific actions: {"red": [...], "blue": [...]}
    gm_prompt_questions = Column(JSON, nullable=True)  # List of 2 prompt questions for GM: ["question1", "question2"]

    scenario = relationship("Scenario", back_populates="phases")
    artifacts = relationship("Artifact", secondary="scenario_phase_artifacts", back_populates="phases")


class Artifact(Base):
    __tablename__ = "artifacts"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    type = Column(SQLEnum(ArtifactType), nullable=False)
    description = Column(Text)
    file_url = Column(String, nullable=True)
    embed_url = Column(String, nullable=True)
    content = Column(Text, nullable=True)  # Store text content directly in database
    notes_for_gm = Column(Text, nullable=True)

    phases = relationship("ScenarioPhase", secondary="scenario_phase_artifacts", back_populates="artifacts")


# Join table for scenario phases and artifacts
from sqlalchemy import Table

scenario_phase_artifacts = Table(
    "scenario_phase_artifacts",
    Base.metadata,
    Column("phase_id", Integer, ForeignKey("scenario_phases.id"), primary_key=True),
    Column("artifact_id", Integer, ForeignKey("artifacts.id"), primary_key=True),
    Column("team_role", String, nullable=True),  # "red", "blue", or None for both teams
)


class Game(Base):
    __tablename__ = "games"

    id = Column(Integer, primary_key=True, index=True)
    scenario_id = Column(Integer, ForeignKey("scenarios.id"), nullable=False)
    status = Column(SQLEnum(GameStatus), default=GameStatus.LOBBY)
    current_phase_id = Column(Integer, ForeignKey("scenario_phases.id"), nullable=True)
    phase_state = Column(SQLEnum(PhaseState), default=PhaseState.NOT_STARTED)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    gm_id = Column(Integer, ForeignKey("gm_users.id"), nullable=False)
    red_team_code = Column(String, unique=True, nullable=False)
    blue_team_code = Column(String, unique=True, nullable=False)
    audience_code = Column(String, unique=True, nullable=True)
    miro_session_url = Column(String, nullable=True)
    settings = Column(JSON, default={})

    scenario = relationship("Scenario")
    current_phase = relationship("ScenarioPhase", foreign_keys=[current_phase_id])
    teams = relationship("Team", back_populates="game", cascade="all, delete-orphan")
    gm = relationship("GMUser")


class Team(Base):
    __tablename__ = "teams"

    id = Column(Integer, primary_key=True, index=True)
    game_id = Column(Integer, ForeignKey("games.id"), nullable=False)
    name = Column(String, nullable=False)
    code = Column(String, nullable=False)
    role = Column(String, nullable=False)  # "red" or "blue"

    game = relationship("Game", back_populates="teams")
    players = relationship("Player", back_populates="team", cascade="all, delete-orphan")


class Player(Base):
    __tablename__ = "players"

    id = Column(Integer, primary_key=True, index=True)
    game_id = Column(Integer, ForeignKey("games.id"), nullable=False)
    team_id = Column(Integer, ForeignKey("teams.id"), nullable=False)
    display_name = Column(String, nullable=False)
    joined_at = Column(DateTime(timezone=True), server_default=func.now())

    game = relationship("Game")
    team = relationship("Team", back_populates="players")


class PhaseDecision(Base):
    __tablename__ = "phase_decisions"

    id = Column(Integer, primary_key=True, index=True)
    game_id = Column(Integer, ForeignKey("games.id"), nullable=False)
    team_id = Column(Integer, ForeignKey("teams.id"), nullable=False)
    phase_id = Column(Integer, ForeignKey("scenario_phases.id"), nullable=False)
    submitted_at = Column(DateTime(timezone=True), server_default=func.now())
    actions = Column(JSON, nullable=False)
    free_text_justification = Column(Text)
    status = Column(SQLEnum(DecisionStatus), default=DecisionStatus.DRAFT)
    score_awarded = Column(Integer, nullable=True)
    gm_notes = Column(Text, nullable=True)

    game = relationship("Game")
    team = relationship("Team")
    phase = relationship("ScenarioPhase")


class PlayerVote(Base):
    __tablename__ = "player_votes"

    id = Column(Integer, primary_key=True, index=True)
    game_id = Column(Integer, ForeignKey("games.id"), nullable=False)
    team_id = Column(Integer, ForeignKey("teams.id"), nullable=False)
    phase_id = Column(Integer, ForeignKey("scenario_phases.id"), nullable=False)
    player_id = Column(Integer, ForeignKey("players.id"), nullable=False)
    selected_action = Column(String, nullable=False)  # Single action voted for
    justification = Column(Text, nullable=True)  # Kept for backward compatibility
    effectiveness_rating = Column(Integer, nullable=True)  # 1-10 rating
    comments = Column(String(500), nullable=True)  # Max 500 characters
    voted_at = Column(DateTime(timezone=True), server_default=func.now())

    game = relationship("Game")
    team = relationship("Team")
    phase = relationship("ScenarioPhase")
    player = relationship("Player")


class ScoreEvent(Base):
    __tablename__ = "score_events"

    id = Column(Integer, primary_key=True, index=True)
    game_id = Column(Integer, ForeignKey("games.id"), nullable=False)
    team_id = Column(Integer, ForeignKey("teams.id"), nullable=False)
    phase_id = Column(Integer, ForeignKey("scenario_phases.id"), nullable=False)
    delta = Column(Integer, nullable=False)
    reason = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    game = relationship("Game")


class PhaseGMNotes(Base):
    __tablename__ = "phase_gm_notes"

    id = Column(Integer, primary_key=True, index=True)
    game_id = Column(Integer, ForeignKey("games.id"), nullable=False)
    phase_id = Column(Integer, ForeignKey("scenario_phases.id"), nullable=False)
    gm_id = Column(Integer, ForeignKey("gm_users.id"), nullable=False)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), nullable=True, onupdate=func.now())

    game = relationship("Game")
    phase = relationship("ScenarioPhase")
    gm = relationship("GMUser")


class AfterActionReport(Base):
    __tablename__ = "after_action_reports"

    id = Column(Integer, primary_key=True, index=True)
    game_id = Column(Integer, ForeignKey("games.id"), nullable=False, unique=True)
    generated_at = Column(DateTime(timezone=True), server_default=func.now())
    overall_risk_rating = Column(String, nullable=False)  # "Critical", "High", "Medium", "Low", "Very Low"
    overall_risk_score = Column(Integer, nullable=False)  # Average of all phase ratings (1-10)
    report_data = Column(JSON, nullable=False)  # Full report data as JSON
    gm_id = Column(Integer, ForeignKey("gm_users.id"), nullable=False)

    game = relationship("Game")
    gm = relationship("GMUser")

