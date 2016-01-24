"""add user invitation

Revision ID: 262183b1809c
Revises: 355dbcd8fd5d
Create Date: 2016-01-24 14:00:24.079679

"""

# revision identifiers, used by Alembic.
revision = '262183b1809c'
down_revision = '355dbcd8fd5d'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table('user_invitation',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=255), nullable=False),
    sa.Column('invited_by_user_id', sa.Integer(), nullable=False),
    sa.Column('token', sa.String(length=100), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('token', name='ux_user_invitation_token'),
    sa.UniqueConstraint('email', name='ux_user_invitation_email'),
    )


def downgrade():
    op.drop_table('user_invitation'),
