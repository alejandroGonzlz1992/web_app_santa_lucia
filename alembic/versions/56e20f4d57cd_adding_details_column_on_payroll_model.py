"""adding details column on payroll model

Revision ID: 56e20f4d57cd
Revises: a4a09311b1fa
Create Date: 2025-10-14 22:26:17.181178

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '56e20f4d57cd'
down_revision: Union[str, Sequence[str], None] = 'a4a09311b1fa'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        "payroll_user",
        sa.Column('details', sa.String(length=250), nullable=False,
                  server_default='Periodo regular de planilla'),
        schema="serv"
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('payroll_user', 'details', schema='serv')
