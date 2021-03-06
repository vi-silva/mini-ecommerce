"""update address table

Revision ID: 973ded0f3826
Revises: 1630c2c7a54d
Create Date: 2021-12-03 17:44:50.177963

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '973ded0f3826'
down_revision = '1630c2c7a54d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('addresses', sa.Column('address', sa.String(length=255), nullable=True))
    op.drop_column('addresses', 'addresses')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('addresses', sa.Column('addresses', sa.VARCHAR(length=255), nullable=True))
    op.drop_column('addresses', 'address')
    # ### end Alembic commands ###
