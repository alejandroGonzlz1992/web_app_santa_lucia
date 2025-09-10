"""updating temp_password column in user model

Revision ID: ef80823f38fb
Revises: 
Create Date: 2025-09-10 17:31:47.615387

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ef80823f38fb'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.alter_column("user", "temp_password", schema="entity",
                    existing_type=sa.String(length=275), existing_nullable=False, nullable=True)

def downgrade() -> None:
    """Downgrade schema."""
    op.alter_column("user", "temp_password", schema="entity",
                    existing_type=sa.String(length=275), existing_nullable=True, nullable=False)
