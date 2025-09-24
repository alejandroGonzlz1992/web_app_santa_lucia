"""adding log_date col to address and drop create and update date

Revision ID: 37f6bd437642
Revises: 952f6a0954e9
Create Date: 2025-09-24 13:57:20.081902

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '37f6bd437642'
down_revision: Union[str, Sequence[str], None] = '952f6a0954e9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('address', sa.Column('log_date', sa.DateTime(),
                                               nullable=False, server_default=sa.text('now()')),
        schema='refer')
    op.drop_column('address', 'date_create', schema='refer')
    op.drop_column('address', 'date_update', schema='refer')


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('address', 'log_date', schema='refer')
    op.add_column('address', sa.Column('date_create', sa.Date(),
                                       nullable=False),
                  schema='refer')
    op.add_column('address', sa.Column('date_update', sa.Date(),
                                       nullable=False),
                  schema='refer')
