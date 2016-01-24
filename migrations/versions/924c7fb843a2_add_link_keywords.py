"""add link keywords

Revision ID: 924c7fb843a2
Revises: 81b71df9b10f
Create Date: 2016-01-24 22:04:25.293796

"""

# revision identifiers, used by Alembic.
revision = '924c7fb843a2'
down_revision = '81b71df9b10f'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column(
        'link',
        sa.Column('keywords',
                  sa.dialects.postgresql.ARRAY(sa.String(32)),
                  server_default='{}')
    )


def downgrade():
    op.drop_column('link', 'keywords')
