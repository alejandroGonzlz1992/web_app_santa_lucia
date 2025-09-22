"""adding log_date column to checkin_tracker

Revision ID: 350de7252f96
Revises: e0e2fabb6152
Create Date: 2025-09-22 15:16:35.915506

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '350de7252f96'
down_revision: Union[str, Sequence[str], None] = 'e0e2fabb6152'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        'checkin_tracker',
        sa.Column(
            'log_date', sa.DateTime(), nullable=False, server_default=sa.text('now()')),
        schema='serv')

def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('checkin_tracker', 'log_date', schema='serv')
