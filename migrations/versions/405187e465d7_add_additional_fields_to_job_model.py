"""Add additional fields to Job model

Revision ID: 405187e465d7
Revises: 9512480d2672
Create Date: 2024-11-09 11:43:57.207436

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '405187e465d7'
down_revision = '9512480d2672'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('jobs', schema=None) as batch_op:
        batch_op.add_column(sa.Column('company', sa.String(length=150), nullable=True))
        batch_op.add_column(sa.Column('location', sa.String(length=150), nullable=True))
        batch_op.add_column(sa.Column('company_size', sa.String(length=50), nullable=True))
        batch_op.add_column(sa.Column('description', sa.String(length=500), nullable=True))
        batch_op.add_column(sa.Column('photo', sa.LargeBinary(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('jobs', schema=None) as batch_op:
        batch_op.drop_column('photo')
        batch_op.drop_column('description')
        batch_op.drop_column('company_size')
        batch_op.drop_column('location')
        batch_op.drop_column('company')

    # ### end Alembic commands ###