"""add_scenario_templates

Revision ID: 7f8g9h0i1j2k3
Revises: f30de78a2c19
Create Date: 2025-01-27 12:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = '7f8g9h0i1j2k3'
down_revision: Union[str, None] = 'f30de78a2c19'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Scenario Templates - check if table exists first
    from sqlalchemy import inspect
    conn = op.get_bind()
    inspector = inspect(conn)
    tables = inspector.get_table_names()
    
    if 'scenario_templates' not in tables:
        op.create_table(
            'scenario_templates',
            sa.Column('id', sa.Integer(), nullable=False),
            sa.Column('name', sa.String(), nullable=False),
            sa.Column('description', sa.Text(), nullable=True),
            sa.Column('template_data', postgresql.JSON(astext_type=sa.Text()), nullable=False),
            sa.Column('created_by_gm_id', sa.Integer(), nullable=True),
            sa.Column('is_public', sa.Boolean(), server_default='false', nullable=False),
            sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()')),
            sa.ForeignKeyConstraint(['created_by_gm_id'], ['gm_users.id'], ),
            sa.PrimaryKeyConstraint('id')
        )
        op.create_index(op.f('ix_scenario_templates_id'), 'scenario_templates', ['id'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_scenario_templates_id'), table_name='scenario_templates')
    op.drop_table('scenario_templates')

