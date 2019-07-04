"""empty message

Revision ID: fd72ad297dac
Revises: af5553f0c404
Create Date: 2019-07-04 17:53:39.428696

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fd72ad297dac'
down_revision = 'af5553f0c404'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('login_info', sa.Column('last_login_time', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('login_info', 'last_login_time')
    # ### end Alembic commands ###
