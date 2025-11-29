"""add_phase_specific_actions

Revision ID: 4c5d6e7f8901
Revises: 3b4c5d6e7f80
Create Date: 2025-01-15 12:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = '4c5d6e7f8901'
down_revision: Union[str, None] = '3b4c5d6e7f80'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add available_actions JSON field to scenario_phases
    # This will store phase-specific actions for red and blue teams
    op.add_column('scenario_phases', sa.Column('available_actions', postgresql.JSON(astext_type=sa.Text()), nullable=True))


def downgrade() -> None:
    op.drop_column('scenario_phases', 'available_actions')

