"""add_team_role_to_artifacts

Revision ID: 2a098de1cf00
Revises: f30de78a2c19
Create Date: 2025-11-26 13:38:31.760128

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2a098de1cf00'
down_revision: Union[str, None] = 'f30de78a2c19'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add team_role column to scenario_phase_artifacts
    op.add_column('scenario_phase_artifacts', sa.Column('team_role', sa.String(), nullable=True))


def downgrade() -> None:
    op.drop_column('scenario_phase_artifacts', 'team_role')

