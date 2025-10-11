"""adding year column to bonus table

Revision ID: f9840d8eccc4
Revises: 891cc3d3cce5
Create Date: 2025-10-11 15:17:02.065143

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f9840d8eccc4'
down_revision: Union[str, Sequence[str], None] = '891cc3d3cce5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('bonus', sa.Column('year', sa.Integer(), nullable=False, server_default="1900"),
                  schema='serv')


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('bonus', 'year', schema='serv')
