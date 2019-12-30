"""create member table

Revision ID: 1
Revises: 0
Create Date: 2019-12-30 23:41:32.730261

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1'
down_revision = '0'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'member',
        sa.Column('id', sa.Integer, primary_key=True, nullable=False),
        sa.Column('first_name', sa.String(length=64), nullable=False),
        sa.Column('last_name', sa.String(length=64), nullable=False),
        sa.Column('email', sa.String(length=64), nullable=False, unique=True),
        sa.Column('password', sa.String(length=128), nullable=False),
        sa.Column('role', sa.String(length=32), nullable=True),
        sa.Column('session_id', sa.String(length=256))
    )


def downgrade():
    op.drop_table('member')
