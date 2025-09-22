"""create checkin_tracker table

Revision ID: e0e2fabb6152
Revises: d027f366571a
Create Date: 2025-09-22 13:40:55.749655

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e0e2fabb6152'
down_revision: Union[str, Sequence[str], None] = 'd027f366571a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "checkin_tracker",
        sa.Column(
            "id_record", sa.Integer(),
            sa.Identity(start=330, increment=1, cycle=False), primary_key=True),
        sa.Column("start_hour", sa.Time(), nullable=False),
        sa.Column("end_hour", sa.Time(), nullable=False),
        sa.Column("hours", sa.Integer(), nullable=False, server_default=sa.text("0")),
        sa.Column("status", sa.String(length=25), nullable=False, server_default=sa.text("'Completado'")),
        sa.Column(
            "id_subject", sa.Integer(),
            sa.ForeignKey("entity.user_role.id_record", ondelete=None)),
        schema="serv"
    )

def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("checkin_tracker", schema="serv")
