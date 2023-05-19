"""empty message

Revision ID: 5296fd21d08b
Revises: 1e86a014a8d5
Create Date: 2023-05-19 05:05:53.973168

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5296fd21d08b'
down_revision = '1e86a014a8d5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('username', sa.String(length=100), nullable=False))
        batch_op.create_unique_constraint(None, ['username'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='unique')
        batch_op.drop_column('username')

    # ### end Alembic commands ###
