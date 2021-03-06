"""Create oui_vendor table

Revision ID: e5e016a16fac
Revises: 346fb8b8d447
Create Date: 2019-04-02 08:50:47.990492

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e5e016a16fac'
down_revision = '346fb8b8d447'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('oui_vendor',
    sa.Column('assignment', sa.Text(), nullable=False),
    sa.Column('orgname', sa.Text(), nullable=False),
    sa.Column('orgaddr', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('assignment', name=op.f('pk_oui_vendor'))
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('oui_vendor')
    # ### end Alembic commands ###
