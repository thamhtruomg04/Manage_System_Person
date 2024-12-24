"""Add department field to Employee model

Revision ID: 32d592a7e9da
Revises: 72705efddda2
Create Date: 2024-12-21 01:39:10.027511

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '32d592a7e9da'
down_revision = '72705efddda2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('employee', schema=None) as batch_op:
        batch_op.add_column(sa.Column('department', sa.String(length=100), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('employee', schema=None) as batch_op:
        batch_op.drop_column('department')

    # ### end Alembic commands ###