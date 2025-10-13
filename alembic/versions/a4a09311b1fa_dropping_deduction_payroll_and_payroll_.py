"""dropping deduction_payroll and payroll models

Revision ID: a4a09311b1fa
Revises: f9840d8eccc4
Create Date: 2025-10-13 22:25:54.604372

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a4a09311b1fa'
down_revision: Union[str, Sequence[str], None] = 'f9840d8eccc4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.drop_table('payroll', schema='serv')
    op.drop_table('deduction_payroll', schema='serv')

def downgrade() -> None:
    """Downgrade schema."""
    op.create_table(
        "deduction_payroll",
        sa.Column(
            "id_record", sa.Integer(), sa.Identity(start=210, increment=1, cycle=True), primary_key=True),
        sa.Column(
            "amount", sa.Numeric(10, 2), nullable=False, server_default=sa.text("'0.00'")),
        sa.Column(
            "id_user", sa.Integer(), sa.ForeignKey("entity.user_role.id_record"), nullable=False),
        sa.Column(
            "id_deduction", sa.Integer(), sa.ForeignKey("serv.deduction.id_record"), nullable=False),
        sa.Column(
            "log_date", sa.DateTime(), nullable=False, server_default=sa.text("now()")), schema="serv",
    )

    # Then recreate 'serv.payroll'
    op.create_table(
        "payroll",
        sa.Column(
            "id_record", sa.Integer(), sa.Identity(start=230, increment=1, cycle=True),
            primary_key=True),
        sa.Column(
            "net_amount", sa.Numeric(10, 2), nullable=False, server_default=sa.text("'0.00'")),
        sa.Column(
            "details", sa.String(250), nullable=False),
        sa.Column(
            "id_deduction_payroll", sa.Integer(), sa.ForeignKey("serv.deduction_payroll.id_record"),
            nullable=False),
        sa.Column(
            "id_payment_date", sa.Integer(), sa.ForeignKey("serv.payment_date.id_record"),
            nullable=False),
        sa.Column(
            "log_date", sa.DateTime(), nullable=False, server_default=sa.text("now()")),
        schema="serv",
    )
