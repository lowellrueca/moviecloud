"""create user table

Revision ID: bbfa4fe5fd34
Revises: f32ae1a460b5
Create Date: 2019-12-21 12:45:11.894626

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bbfa4fe5fd34'
down_revision = 'f32ae1a460b5'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'user',
        sa.Column('id', sa.Integer, primary_key=True, nullable=False),
        sa.Column('first_name', sa.String(length=64), nullable=False),
        sa.Column('last_name', sa.String(length=64), nullable=False),
        sa.Column('email', sa.String(length=64), nullable=False, unique=True),
        sa.Column('password', sa.String(length=128), nullable=False),
        sa.Column('session_token', sa.String(length=256))
    )


def downgrade():
    op.drop_table('user')
