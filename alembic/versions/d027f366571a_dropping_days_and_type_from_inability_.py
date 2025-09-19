"""dropping days and type from inability model

Revision ID: d027f366571a
Revises: 800a3c09f5b9
Create Date: 2025-09-19 14:02:34.107557

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd027f366571a'
down_revision: Union[str, Sequence[str], None] = '800a3c09f5b9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.drop_column('inability', 'days', schema='serv')
    op.drop_column('inability', 'type', schema='serv')


def downgrade() -> None:
    """Downgrade schema."""
    op.add_column('inability', sa.Column(
        'days', sa.Integer(), nullable=False, server_default="0"), schema='serv')
    op.add_column('inability', sa.Column(
        'type', sa.String(length=75), nullable=False), schema='serv')
