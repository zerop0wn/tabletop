"""add_player_votes

Revision ID: f30de78a2c19
Revises: 001_initial
Create Date: 2025-11-25 21:45:58.670264

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f30de78a2c19'
down_revision: Union[str, None] = '001_initial'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Player Votes - check if table exists first
    from sqlalchemy import inspect
    conn = op.get_bind()
    inspector = inspect(conn)
    tables = inspector.get_table_names()
    
    if 'player_votes' not in tables:
        op.create_table(
            'player_votes',
            sa.Column('id', sa.Integer(), nullable=False),
            sa.Column('game_id', sa.Integer(), nullable=False),
            sa.Column('team_id', sa.Integer(), nullable=False),
            sa.Column('phase_id', sa.Integer(), nullable=False),
            sa.Column('player_id', sa.Integer(), nullable=False),
            sa.Column('selected_action', sa.String(), nullable=False),
            sa.Column('justification', sa.Text(), nullable=True),
            sa.Column('voted_at', sa.DateTime(timezone=True), server_default=sa.text('now()')),
            sa.ForeignKeyConstraint(['game_id'], ['games.id'], ),
            sa.ForeignKeyConstraint(['team_id'], ['teams.id'], ),
            sa.ForeignKeyConstraint(['phase_id'], ['scenario_phases.id'], ),
            sa.ForeignKeyConstraint(['player_id'], ['players.id'], ),
            sa.PrimaryKeyConstraint('id'),
            sa.UniqueConstraint('player_id', 'phase_id', name='uq_player_phase_vote')  # One vote per player per phase
        )
        op.create_index(op.f('ix_player_votes_id'), 'player_votes', ['id'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_player_votes_id'), table_name='player_votes')
    op.drop_table('player_votes')

