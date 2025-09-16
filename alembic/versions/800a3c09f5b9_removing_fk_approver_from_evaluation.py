"""removing fk_approver from evaluation

Revision ID: 800a3c09f5b9
Revises: 473d5385be84
Create Date: 2025-09-16 19:39:37.961967

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '800a3c09f5b9'
down_revision: Union[str, Sequence[str], None] = '473d5385be84'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Drop FK constraint if present
    op.execute('ALTER TABLE "serv"."evaluation" DROP CONSTRAINT IF EXISTS "evaluation_id_approver_fkey"')
    # Drop the column
    op.drop_column("evaluation", "id_approver", schema="serv")


def downgrade() -> None:
    """Downgrade schema."""
    # Add FK constraint
    op.add_column("evaluation",
                  sa.Column("id_approver", sa.Integer(), nullable=True), schema="serv")

    op.alter_column( "evaluation", "id_approver", existing_type=sa.Integer(),
        nullable=False, schema="serv", server_default=sa.text("0"))

    op.create_foreign_key(
        "evaluation_id_approver_fkey", source_table="evaluation",
        referent_table="user_role", local_cols=["id_approver"], remote_cols=["id_record"], source_schema="serv",
        referent_schema="entity", ondelete=None
    )
