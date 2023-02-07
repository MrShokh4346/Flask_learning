"""test

Revision ID: ea31f57707f8
Revises: 01b97c9d588f
Create Date: 2023-02-07 18:02:30.672458

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ea31f57707f8'
down_revision = '01b97c9d588f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.alter_column('email',
               existing_type=sa.VARCHAR(length=120),
               nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.alter_column('email',
               existing_type=sa.VARCHAR(length=120),
               nullable=False)

    # ### end Alembic commands ###