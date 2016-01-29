"""remove ad issue_id

Revision ID: 5bd1e81210f9
Revises: f3568eb5ef18
Create Date: 2016-01-28 18:00:13.273207

"""

# revision identifiers, used by Alembic.
revision = '5bd1e81210f9'
down_revision = 'f3568eb5ef18'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.drop_index('ix_issue', table_name='link_ad')
    op.drop_column('link_ad', 'issue_id')


def downgrade():
    op.add_column(
        'link_ad',
        sa.Column('issue_id', sa.Integer(), nullable=False)
    )
    op.create_index('ix_issue', 'link_ad', ['issue_id'], unique=False)
