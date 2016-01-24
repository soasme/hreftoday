"""add issue title

Revision ID: f687ca65d4ca
Revises: 262183b1809c
Create Date: 2016-01-24 14:50:48.136326

"""

# revision identifiers, used by Alembic.
revision = 'f687ca65d4ca'
down_revision = '262183b1809c'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column(
        'issue',
        sa.Column('title', sa.String(128), nullable=False, server_default='')
    )


def downgrade():
    op.drop_column('issue', 'title')
