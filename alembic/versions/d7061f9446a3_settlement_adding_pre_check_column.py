"""settlement adding pre_check column

Revision ID: d7061f9446a3
Revises: 025fcaab1377
Create Date: 2025-11-03 13:10:14.885855

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd7061f9446a3'
down_revision: Union[str, Sequence[str], None] = '025fcaab1377'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("settlement", sa.Column(
        "pre_check", sa.DECIMAL(10, 2), nullable=False, server_default="0.00"), schema="serv")


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('settlement', 'pre_check', schema='serv')
