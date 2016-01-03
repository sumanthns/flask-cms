"""empty message

Revision ID: 107c7ef8171a
Revises: 585003100816
Create Date: 2016-01-03 00:23:31.583273

"""

# revision identifiers, used by Alembic.
revision = '107c7ef8171a'
down_revision = '585003100816'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('confirmed_at', sa.DateTime(), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'confirmed_at')
    ### end Alembic commands ###
