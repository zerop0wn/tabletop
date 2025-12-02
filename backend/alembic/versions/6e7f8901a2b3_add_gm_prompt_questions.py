"""add_gm_prompt_questions

Revision ID: 6e7f8901a2b3
Revises: 5d6e7f8901a2
Create Date: 2025-01-15 14:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = '6e7f8901a2b3'
down_revision: Union[str, None] = '5d6e7f8901a2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add gm_prompt_questions JSON field to scenario_phases
    # This will store 2 prompt questions for the GM to ask players
    op.add_column('scenario_phases', sa.Column('gm_prompt_questions', postgresql.JSON(astext_type=sa.Text()), nullable=True))


def downgrade() -> None:
    op.drop_column('scenario_phases', 'gm_prompt_questions')

