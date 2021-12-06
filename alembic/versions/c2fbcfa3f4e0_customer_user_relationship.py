"""customer-user relationship

Revision ID: c2fbcfa3f4e0
Revises: 9f2fcef54373
Create Date: 2021-12-06 16:41:23.058899

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c2fbcfa3f4e0'
down_revision = '9f2fcef54373'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('customers', sa.Column('user_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'customers', 'users', ['user_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'customers', type_='foreignkey')
    op.drop_column('customers', 'user_id')
    # ### end Alembic commands ###
