"""amend session_id column name to auth_id in member table

Revision ID: 2
Revises: 1
Create Date: 2020-01-11 04:45:50.570400

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2'
down_revision = '1'
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column(table_name='member', column_name='session_id', new_column_name='auth_id')


def downgrade():
    op.alter_column(table_name='member', column_name='auth_id', new_column_name='session_id')
