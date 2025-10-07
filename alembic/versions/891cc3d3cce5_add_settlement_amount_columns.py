"""add settlement amount columns

Revision ID: 891cc3d3cce5
Revises: 37f6bd437642
Create Date: 2025-10-07 22:45:39.371090

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '891cc3d3cce5'
down_revision: Union[str, Sequence[str], None] = '37f6bd437642'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("settlement", sa.Column(
        "cesantia", sa.DECIMAL(10, 2), nullable=False, server_default="0.00"), schema="serv")
    op.add_column("settlement", sa.Column(
        "vacations", sa.DECIMAL(10, 2), nullable=False, server_default="0.00"), schema="serv")
    op.add_column("settlement", sa.Column(
        "bonus", sa.DECIMAL(10, 2), nullable=False, server_default="0.00"), schema="serv")
    op.add_column("settlement", sa.Column(
        "payroll", sa.DECIMAL(10, 2), nullable=False, server_default="0.00"), schema="serv")


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('settlement', 'cesantia', schema='serv')
    op.drop_column('settlement', 'vacations', schema='serv')
    op.drop_column('settlement', 'bonus', schema='serv')
    op.drop_column('settlement', 'payroll', schema='serv')
