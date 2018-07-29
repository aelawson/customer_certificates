"""initial schema

Revision ID: ccf25419dd1d
Revises: 
Create Date: 2018-07-29 00:06:59.380559

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ccf25419dd1d'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('certificates',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('private_key', sa.String(), nullable=True),
    sa.Column('active', sa.SmallInteger(), nullable=True),
    sa.Column('body', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('email', sa.String(), nullable=True),
    sa.Column('password', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users')
    op.drop_table('certificates')
    # ### end Alembic commands ###
