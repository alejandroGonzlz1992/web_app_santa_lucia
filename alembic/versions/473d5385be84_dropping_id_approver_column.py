"""dropping id_approver column

Revision ID: 473d5385be84
Revises: 191113c0aa42
Create Date: 2025-09-16 15:24:24.116985

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '473d5385be84'
down_revision: Union[str, Sequence[str], None] = '191113c0aa42'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

# FK_SCHEMA
FK_SCHEMA = [
    ("serv", "bonus", "id_subject"),
    ("serv", "extra_hour", "id_subject"),
    ("serv", "inability", "id_subject"),
    ("serv", "request_extra_hour", "id_subject"),
    ("serv", "request_vacation", "id_subject"),
    ("serv", "settlement", "id_subject"),
    ("serv", "vacation", "id_subject"),
]


def upgrade() -> None:
    """Upgrade schema."""
    for schema, table, _ in FK_SCHEMA:
        op.drop_column(table, 'id_approver', schema=schema)


def downgrade() -> None:
    """Downgrade schema."""
    for schema, table, subject in FK_SCHEMA:
        # re-add column, backfill, make not null, re-add FK
        op.add_column(table, sa.Column('id_approver', sa.Integer(), nullable=True), schema=schema)

        # backfill using subject's current approver
        op.execute(f'UPDATE "{schema}"."{table}" AS t SET id_approver = ur.approver FROM "entity"."user_role AS ur WHERE ur.id_record = t.{subject} AND t.id_approver IS NULL"')

        # alter column
        op.alter_column(table, 'id_approver', existing_type=sa.Integer(), nullable=False, schema=schema)

        # recreate fk with original names
        fk_name = f'{table}_id_approver_fkey'
        op.create_foreign_key(fk_name, source_table=table, referent_table='user_role', local_cols=['id_approver'], remote_cols=['id_record'], source_schema=schema, referent_schema='entity', ondelete=None)
