"""create role column for user table

Revision ID: 7752e3e53272
Revises: bbfa4fe5fd34
Create Date: 2019-12-21 22:04:05.334543

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7752e3e53272'
down_revision = 'bbfa4fe5fd34'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        'user',
        sa.Column('role', sa.String(length=36), nullable=True)
    )


def downgrade():
    op.drop_column('user', 'role')
