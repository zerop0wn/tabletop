"""add_rating_comments_and_reports

Revision ID: 3b4c5d6e7f80
Revises: 2a098de1cf00
Create Date: 2025-01-15 10:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3b4c5d6e7f80'
down_revision: Union[str, None] = '2a098de1cf00'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add effectiveness_rating and comments to player_votes
    op.add_column('player_votes', sa.Column('effectiveness_rating', sa.Integer(), nullable=True))
    op.add_column('player_votes', sa.Column('comments', sa.String(length=500), nullable=True))
    
    # Create phase_gm_notes table
    op.create_table(
        'phase_gm_notes',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('game_id', sa.Integer(), nullable=False),
        sa.Column('phase_id', sa.Integer(), nullable=False),
        sa.Column('gm_id', sa.Integer(), nullable=False),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['game_id'], ['games.id'], ),
        sa.ForeignKeyConstraint(['gm_id'], ['gm_users.id'], ),
        sa.ForeignKeyConstraint(['phase_id'], ['scenario_phases.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_phase_gm_notes_id'), 'phase_gm_notes', ['id'], unique=False)
    op.create_index('ix_phase_gm_notes_game_phase', 'phase_gm_notes', ['game_id', 'phase_id'], unique=True)
    
    # Create after_action_reports table
    op.create_table(
        'after_action_reports',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('game_id', sa.Integer(), nullable=False),
        sa.Column('generated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('overall_risk_rating', sa.String(), nullable=False),
        sa.Column('overall_risk_score', sa.Float(), nullable=False),
        sa.Column('report_data', sa.JSON(), nullable=False),
        sa.Column('gm_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['game_id'], ['games.id'], ),
        sa.ForeignKeyConstraint(['gm_id'], ['gm_users.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('game_id')
    )
    op.create_index(op.f('ix_after_action_reports_id'), 'after_action_reports', ['id'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_after_action_reports_id'), table_name='after_action_reports')
    op.drop_table('after_action_reports')
    op.drop_index('ix_phase_gm_notes_game_phase', table_name='phase_gm_notes')
    op.drop_index(op.f('ix_phase_gm_notes_id'), table_name='phase_gm_notes')
    op.drop_table('phase_gm_notes')
    op.drop_column('player_votes', 'comments')
    op.drop_column('player_votes', 'effectiveness_rating')

