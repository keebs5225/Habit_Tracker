"""Add status column to habits table

Revision ID: 17380fbb8fc2
Revises: 4844e5728150
Create Date: 2024-11-13 13:31:21.804626

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '17380fbb8fc2'
down_revision = '4844e5728150'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('habitlist', schema=None) as batch_op:
        batch_op.drop_column('status')

    with op.batch_alter_table('habits', schema=None) as batch_op:
        batch_op.add_column(sa.Column('status', sa.Boolean(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('habits', schema=None) as batch_op:
        batch_op.drop_column('status')

    with op.batch_alter_table('habitlist', schema=None) as batch_op:
        batch_op.add_column(sa.Column('status', sa.VARCHAR(length=50), nullable=True))

    # ### end Alembic commands ###