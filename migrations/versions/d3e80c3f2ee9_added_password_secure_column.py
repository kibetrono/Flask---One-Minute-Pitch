"""added password secure column

Revision ID: d3e80c3f2ee9
Revises: 28de81bc4c7c
Create Date: 2022-02-05 11:27:24.329179

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd3e80c3f2ee9'
down_revision = '28de81bc4c7c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('password_secure', sa.String(length=255), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'password_secure')
    # ### end Alembic commands ###