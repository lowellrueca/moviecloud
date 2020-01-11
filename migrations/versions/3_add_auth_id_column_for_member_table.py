"""add auth_id column for member table

Revision ID: 3
Revises: 2
Create Date: 2020-01-11 08:28:59.305526

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3'
down_revision = '2'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('member',
        sa.Column('auth_id', sa.String(length=256), nullable=True)
    )


def downgrade():
    op.drop_column('member', 'auth_id')
