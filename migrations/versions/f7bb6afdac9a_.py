"""empty message

Revision ID: f7bb6afdac9a
Revises: 660c5b2dc806
Create Date: 2018-07-02 02:30:47.807159

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f7bb6afdac9a'
down_revision = '660c5b2dc806'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('total_monthly', sa.Column('index', sa.Integer(), nullable=False))
    op.drop_column('total_monthly', 'id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('total_monthly', sa.Column('id', sa.INTEGER(), nullable=False))
    op.drop_column('total_monthly', 'index')
    # ### end Alembic commands ###
