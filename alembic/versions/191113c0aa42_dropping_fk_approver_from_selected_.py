"""dropping fk_approver from selected models

Revision ID: 191113c0aa42
Revises: bacef98f01eb
Create Date: 2025-09-16 14:59:09.696016

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '191113c0aa42'
down_revision: Union[str, Sequence[str], None] = 'bacef98f01eb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

# FK_SCHEMA
FK_SCHEMA = [
    ("serv", "bonus", "bonus_id_approver_fkey"),
    ("serv", "extra_hour", "extra_hour_id_approver_fkey"),
    ("serv", "inability", "inability_id_approver_fkey"),
    ("serv", "request_extra_hour", "request_extra_hour_id_approver_fkey"),
    ("serv", "request_vacation", "request_vacation_id_approver_fkey"),
    ("serv", "settlement", "settlement_id_approver_fkey"),
    ("serv", "vacation", "vacation_id_approver_fkey"),
]

def upgrade() -> None:
    """Upgrade schema."""
    for schema, table, fk in FK_SCHEMA:
        op.execute(f'ALTER TABLE "{schema}"."{table}" DROP CONSTRAINT IF EXISTS "{fk}"')


def downgrade() -> None:
    """Downgrade schema."""
    # recreate simple fk: id_approver
    for schema, table, fk in FK_SCHEMA:
        op.create_foreign_key(
            fk,
            source_table=table,
            referent_table="user_role",
            local_cols=["id_approver"],
            remote_cols=["id_record"],
            source_schema=schema,
            referent_schema="entity",
            ondelete=None
        )

