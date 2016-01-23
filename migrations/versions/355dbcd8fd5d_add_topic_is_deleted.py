"""add topic is_deleted

Revision ID: 355dbcd8fd5d
Revises: be2ad59aef79
Create Date: 2016-01-24 01:23:47.996960

"""

# revision identifiers, used by Alembic.
revision = '355dbcd8fd5d'
down_revision = 'be2ad59aef79'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column(
        'topic',
        sa.Column('is_deleted', sa.Boolean(), server_default='0', nullable=False),
    )


def downgrade():
    op.drop_column('topic', 'is_deleted')
