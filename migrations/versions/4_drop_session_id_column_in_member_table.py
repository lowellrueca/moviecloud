"""drop session id column in member table

Revision ID: 4
Revises: 3
Create Date: 2020-01-11 08:34:45.892642

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4'
down_revision = '3'
branch_labels = None
depends_on = None


def upgrade():
    op.drop_column('member', 'session_id')


def downgrade():
    op.add_column('member',
        sa.Column('session_id', sa.String(length=256), nullable=True)
    )
