"""adding postal code col to address

Revision ID: 952f6a0954e9
Revises: 350de7252f96
Create Date: 2025-09-24 13:34:11.610697

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '952f6a0954e9'
down_revision: Union[str, Sequence[str], None] = '350de7252f96'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('address', sa.Column('postal_code', sa.String(length=15), nullable=False),
                  schema='refer')

def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('address', 'postal_code', schema='refer')
