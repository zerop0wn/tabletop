"""Initial migration

Revision ID: 001_initial
Revises: 
Create Date: 2024-01-01 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '001_initial'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create enum types (if they don't exist)
    op.execute("DO $$ BEGIN CREATE TYPE gamestatus AS ENUM ('lobby', 'in_progress', 'paused', 'finished'); EXCEPTION WHEN duplicate_object THEN null; END $$;")
    op.execute("DO $$ BEGIN CREATE TYPE phasestate AS ENUM ('not_started', 'briefing', 'open_for_decisions', 'decision_lock', 'resolution', 'complete'); EXCEPTION WHEN duplicate_object THEN null; END $$;")
    op.execute("DO $$ BEGIN CREATE TYPE decisionstatus AS ENUM ('draft', 'submitted', 'locked', 'scored'); EXCEPTION WHEN duplicate_object THEN null; END $$;")
    op.execute("DO $$ BEGIN CREATE TYPE artifacttype AS ENUM ('log_snippet', 'screenshot', 'email', 'tool_output', 'intel_report'); EXCEPTION WHEN duplicate_object THEN null; END $$;")

    # GM Users
    op.create_table(
        'gm_users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('username', sa.String(), nullable=False),
        sa.Column('password_hash', sa.String(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()')),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_gm_users_id'), 'gm_users', ['id'], unique=False)
    op.create_index(op.f('ix_gm_users_username'), 'gm_users', ['username'], unique=True)

    # Scenarios
    op.create_table(
        'scenarios',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('miro_board_url', sa.String(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()')),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_scenarios_id'), 'scenarios', ['id'], unique=False)

    # Scenario Phases
    op.create_table(
        'scenario_phases',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('scenario_id', sa.Integer(), nullable=False),
        sa.Column('order_index', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('briefing_text', sa.Text(), nullable=True),
        sa.Column('red_objective', sa.Text(), nullable=True),
        sa.Column('blue_objective', sa.Text(), nullable=True),
        sa.Column('default_duration_seconds', sa.Integer(), nullable=True),
        sa.Column('miro_frame_url', sa.String(), nullable=True),
        sa.ForeignKeyConstraint(['scenario_id'], ['scenarios.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_scenario_phases_id'), 'scenario_phases', ['id'], unique=False)

    # Artifacts
    op.create_table(
        'artifacts',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('type', postgresql.ENUM('log_snippet', 'screenshot', 'email', 'tool_output', 'intel_report', name='artifacttype'), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('file_url', sa.String(), nullable=True),
        sa.Column('embed_url', sa.String(), nullable=True),
        sa.Column('notes_for_gm', sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_artifacts_id'), 'artifacts', ['id'], unique=False)

    # Scenario Phase Artifacts (join table)
    op.create_table(
        'scenario_phase_artifacts',
        sa.Column('phase_id', sa.Integer(), nullable=False),
        sa.Column('artifact_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['artifact_id'], ['artifacts.id'], ),
        sa.ForeignKeyConstraint(['phase_id'], ['scenario_phases.id'], ),
        sa.PrimaryKeyConstraint('phase_id', 'artifact_id')
    )

    # Games
    op.create_table(
        'games',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('scenario_id', sa.Integer(), nullable=False),
        sa.Column('status', postgresql.ENUM('lobby', 'in_progress', 'paused', 'finished', name='gamestatus'), nullable=True),
        sa.Column('current_phase_id', sa.Integer(), nullable=True),
        sa.Column('phase_state', postgresql.ENUM('not_started', 'briefing', 'open_for_decisions', 'decision_lock', 'resolution', 'complete', name='phasestate'), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()')),
        sa.Column('gm_id', sa.Integer(), nullable=False),
        sa.Column('red_team_code', sa.String(), nullable=False),
        sa.Column('blue_team_code', sa.String(), nullable=False),
        sa.Column('audience_code', sa.String(), nullable=True),
        sa.Column('miro_session_url', sa.String(), nullable=True),
        sa.Column('settings', sa.JSON(), nullable=True),
        sa.ForeignKeyConstraint(['current_phase_id'], ['scenario_phases.id'], ),
        sa.ForeignKeyConstraint(['gm_id'], ['gm_users.id'], ),
        sa.ForeignKeyConstraint(['scenario_id'], ['scenarios.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_games_id'), 'games', ['id'], unique=False)
    op.create_index(op.f('ix_games_red_team_code'), 'games', ['red_team_code'], unique=True)
    op.create_index(op.f('ix_games_blue_team_code'), 'games', ['blue_team_code'], unique=True)
    op.create_index(op.f('ix_games_audience_code'), 'games', ['audience_code'], unique=True)

    # Teams
    op.create_table(
        'teams',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('game_id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('code', sa.String(), nullable=False),
        sa.Column('role', sa.String(), nullable=False),
        sa.ForeignKeyConstraint(['game_id'], ['games.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_teams_id'), 'teams', ['id'], unique=False)

    # Players
    op.create_table(
        'players',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('game_id', sa.Integer(), nullable=False),
        sa.Column('team_id', sa.Integer(), nullable=False),
        sa.Column('display_name', sa.String(), nullable=False),
        sa.Column('joined_at', sa.DateTime(timezone=True), server_default=sa.text('now()')),
        sa.ForeignKeyConstraint(['game_id'], ['games.id'], ),
        sa.ForeignKeyConstraint(['team_id'], ['teams.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_players_id'), 'players', ['id'], unique=False)

    # Phase Decisions
    op.create_table(
        'phase_decisions',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('game_id', sa.Integer(), nullable=False),
        sa.Column('team_id', sa.Integer(), nullable=False),
        sa.Column('phase_id', sa.Integer(), nullable=False),
        sa.Column('submitted_at', sa.DateTime(timezone=True), server_default=sa.text('now()')),
        sa.Column('actions', sa.JSON(), nullable=False),
        sa.Column('free_text_justification', sa.Text(), nullable=True),
        sa.Column('status', postgresql.ENUM('draft', 'submitted', 'locked', 'scored', name='decisionstatus'), nullable=True),
        sa.Column('score_awarded', sa.Integer(), nullable=True),
        sa.Column('gm_notes', sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(['game_id'], ['games.id'], ),
        sa.ForeignKeyConstraint(['phase_id'], ['scenario_phases.id'], ),
        sa.ForeignKeyConstraint(['team_id'], ['teams.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_phase_decisions_id'), 'phase_decisions', ['id'], unique=False)

    # Score Events
    op.create_table(
        'score_events',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('game_id', sa.Integer(), nullable=False),
        sa.Column('team_id', sa.Integer(), nullable=False),
        sa.Column('phase_id', sa.Integer(), nullable=False),
        sa.Column('delta', sa.Integer(), nullable=False),
        sa.Column('reason', sa.String(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()')),
        sa.ForeignKeyConstraint(['game_id'], ['games.id'], ),
        sa.ForeignKeyConstraint(['phase_id'], ['scenario_phases.id'], ),
        sa.ForeignKeyConstraint(['team_id'], ['teams.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_score_events_id'), 'score_events', ['id'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_score_events_id'), table_name='score_events')
    op.drop_table('score_events')
    op.drop_index(op.f('ix_phase_decisions_id'), table_name='phase_decisions')
    op.drop_table('phase_decisions')
    op.drop_index(op.f('ix_players_id'), table_name='players')
    op.drop_table('players')
    op.drop_index(op.f('ix_teams_id'), table_name='teams')
    op.drop_table('teams')
    op.drop_index(op.f('ix_games_audience_code'), table_name='games')
    op.drop_index(op.f('ix_games_blue_team_code'), table_name='games')
    op.drop_index(op.f('ix_games_red_team_code'), table_name='games')
    op.drop_index(op.f('ix_games_id'), table_name='games')
    op.drop_table('games')
    op.drop_table('scenario_phase_artifacts')
    op.drop_index(op.f('ix_artifacts_id'), table_name='artifacts')
    op.drop_table('artifacts')
    op.drop_index(op.f('ix_scenario_phases_id'), table_name='scenario_phases')
    op.drop_table('scenario_phases')
    op.drop_index(op.f('ix_scenarios_id'), table_name='scenarios')
    op.drop_table('scenarios')
    op.drop_index(op.f('ix_gm_users_username'), table_name='gm_users')
    op.drop_index(op.f('ix_gm_users_id'), table_name='gm_users')
    op.drop_table('gm_users')

    # Drop enum types
    op.execute("DROP TYPE IF EXISTS artifacttype")
    op.execute("DROP TYPE IF EXISTS decisionstatus")
    op.execute("DROP TYPE IF EXISTS phasestate")
    op.execute("DROP TYPE IF EXISTS gamestatus")

