"""add link created_at

Revision ID: be2ad59aef79
Revises: 545777b0a0a1
Create Date: 2016-01-23 14:20:24.311883

"""

# revision identifiers, used by Alembic.
revision = 'be2ad59aef79'
down_revision = '545777b0a0a1'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column(
        'link',
        sa.Column('created_at', sa.DateTime(), nullable=True),
    )


def downgrade():
    op.drop_column(
        'link',
        'created_at',
    )
