"""Add content field to artifacts

Revision ID: 5d6e7f8901a2
Revises: 4c5d6e7f8901
Create Date: 2025-01-15 12:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5d6e7f8901a2'
down_revision: Union[str, None] = '4c5d6e7f8901'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add content column to artifacts table
    op.add_column('artifacts', sa.Column('content', sa.Text(), nullable=True))


def downgrade() -> None:
    # Remove content column from artifacts table
    op.drop_column('artifacts', 'content')

