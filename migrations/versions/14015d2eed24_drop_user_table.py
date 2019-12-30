"""drop user table

Revision ID: 14015d2eed24
Revises: 7752e3e53272
Create Date: 2019-12-30 22:39:06.958697

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '14015d2eed24'
down_revision = '7752e3e53272'
branch_labels = None
depends_on = None


def upgrade():
    op.drop_table('user')


def downgrade():
    pass
