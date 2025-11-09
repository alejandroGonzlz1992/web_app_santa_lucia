"""adding payment_period and dropping fk column from payroll_user

Revision ID: 38241f3997f8
Revises: d7061f9446a3
Create Date: 2025-11-08 19:21:45.477611

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '38241f3997f8'
down_revision: Union[str, Sequence[str], None] = 'd7061f9446a3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    with op.batch_alter_table('payroll_user', schema='serv') as batch_op:
        # add column
        batch_op.add_column(
            sa.Column('payment_period', sa.Date(), nullable=False))

        # drop fk constraint
        batch_op.drop_constraint('payroll_user_id_payment_date_fkey', type_='foreignkey')

        # drop column
        batch_op.drop_column('id_payment_date')

def downgrade() -> None:
    """Downgrade schema."""
    with op.batch_alter_table('payroll_user', schema='serv') as batch_op:
        # recreate column and fk constraint
        batch_op.add_column(
            sa.Column('id_payment_date', sa.Integer(), nullable=False))

        batch_op.create_foreign_key(
            'payroll_user_id_payment_date_fkey', 'payment_date',
            ['id_payment_date'], ['id_record'])