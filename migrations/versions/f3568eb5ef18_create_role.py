"""create role

Revision ID: f3568eb5ef18
Revises: 924c7fb843a2
Create Date: 2016-01-27 22:14:10.209184

"""

# revision identifiers, used by Alembic.
revision = 'f3568eb5ef18'
down_revision = '924c7fb843a2'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table(
        'role',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=50)),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name', name='ux_role_name'),
    )

    op.create_table(
        'user_roles',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('user.id', ondelete='CASCADE')),
        sa.Column('role_id', sa.Integer(), sa.ForeignKey('role.id', ondelete='CASCADE')),
        sa.PrimaryKeyConstraint('id'),
    )


def downgrade():
    op.drop_table('user_roles')
    op.drop_table('role')
