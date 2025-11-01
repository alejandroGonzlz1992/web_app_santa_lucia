"""add payroll extra columns

Revision ID: 025fcaab1377
Revises: 56e20f4d57cd
Create Date: 2025-11-01 04:55:21.517687

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '025fcaab1377'
down_revision: Union[str, Sequence[str], None] = '56e20f4d57cd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("payroll_user", sa.Column(
        "payroll_amount", sa.DECIMAL(10, 2), nullable=False, server_default="0.00"),
                  schema="serv")
    op.add_column("payroll_user", sa.Column(
        "extra_hour_amount", sa.DECIMAL(10, 2), nullable=False, server_default="0.00"),
                  schema="serv")
    op.add_column("payroll_user", sa.Column(
        "vacations_amount", sa.DECIMAL(10, 2), nullable=False, server_default="0.00"),
                  schema="serv")
    op.add_column("payroll_user", sa.Column(
        "holiday_amount", sa.DECIMAL(10, 2), nullable=False, server_default="0.00"),
                  schema="serv")
    op.add_column("payroll_user", sa.Column(
        "total_gross_amount", sa.DECIMAL(10, 2), nullable=False, server_default="0.00"),
                  schema="serv")


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('payroll_user', 'payroll_amount', schema='serv')
    op.drop_column('payroll_user', 'extra_hour_amount', schema='serv')
    op.drop_column('payroll_user', 'vacations_amount', schema='serv')
    op.drop_column('payroll_user', 'holiday_amount', schema='serv')
    op.drop_column('payroll_user', 'total_gross_amount', schema='serv')
