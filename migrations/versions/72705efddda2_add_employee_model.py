"""Add Employee model

Revision ID: 72705efddda2
Revises: 5288abe42cb8
Create Date: 2021-06-17 14:22:55.123456

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '72705efddda2'
down_revision = '5288abe42cb8'
branch_labels = None
depends_on = None

def upgrade():
    # Add a temporary default value for the new column 'manager_id' to avoid NOT NULL constraint violation
    op.add_column('employee', sa.Column('manager_id', sa.Integer(), nullable=True))

    # Update the existing rows to set 'manager_id' to a default value, assuming 1 is a valid user_id
    op.execute('UPDATE employee SET manager_id = 1 WHERE manager_id IS NULL')

    # Alter column to set NOT NULL constraint
    op.alter_column('employee', 'manager_id', nullable=False)
    op.create_foreign_key(None, 'employee', 'user', ['manager_id'], ['id'])

def downgrade():
    # Remove the foreign key constraint and drop the column
    op.drop_constraint(None, 'employee', type_='foreignkey')
    op.drop_column('employee', 'manager_id')
