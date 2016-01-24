"""add link ad

Revision ID: 81b71df9b10f
Revises: f687ca65d4ca
Create Date: 2016-01-24 20:29:22.163156

"""

# revision identifiers, used by Alembic.
revision = '81b71df9b10f'
down_revision = 'f687ca65d4ca'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table(
        'ad',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('asin', sa.String(20), nullable=False),
        sa.Column('title', sa.String(128), nullable=False),
        sa.Column('description', sa.String(256), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('asin', name='ux_ad_asin'),
    )
    op.create_table(
        'link_ad',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('issue_id', sa.Integer(), nullable=False),
        sa.Column('link_id', sa.Integer(), nullable=False),
        sa.Column('ad_id', sa.Integer(), nullable=False),
        sa.Column('weight', sa.Numeric(5, 2), nullable=False, server_default='0'),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('link_id', 'ad_id', name='ux_link_ad'),
    )
    op.create_index('ix_link_weight', 'link_ad', ['link_id', 'weight'], unique=False)
    op.create_index('ix_issue_weight', 'link_ad', ['issue_id', 'weight'], unique=False)


def downgrade():
    op.drop_index('ix_issue_weight', table_name='link_ad')
    op.drop_index('ix_link_weight', table_name='link_ad')
    op.drop_table('link_ad')
    op.drop_table('ad')
