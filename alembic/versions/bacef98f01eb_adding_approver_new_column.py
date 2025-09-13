"""adding approver new column

Revision ID: bacef98f01eb
Revises: ef80823f38fb
Create Date: 2025-09-13 14:25:14.258541

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'bacef98f01eb'
down_revision: Union[str, Sequence[str], None] = 'ef80823f38fb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('user_role', sa.Column("approver", sa.Integer(), nullable=True),
                  schema="entity")

    op.execute("UPDATE entity.user_role SET approver = 0 WHERE approver IS NULL")

    op.alter_column("user_role", "approver", existing_type=sa.Integer(), nullable=False,
                    schema="entity")

def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('user_role', 'approver', schema="entity")
