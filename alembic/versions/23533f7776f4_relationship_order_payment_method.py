"""relationship order-payment-method

Revision ID: 23533f7776f4
Revises: 923722242a59
Create Date: 2021-12-08 11:11:39.627289

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '23533f7776f4'
down_revision = '923722242a59'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_foreign_key(None, 'orders', 'payment_methods', ['payment_form_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'orders', type_='foreignkey')
    # ### end Alembic commands ###
