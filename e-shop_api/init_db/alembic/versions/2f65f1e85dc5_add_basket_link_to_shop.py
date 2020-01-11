"""add basket link to shop

Revision ID: 2f65f1e85dc5
Revises: 4f70aca73590
Create Date: 2020-01-11 16:50:09.823000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '2f65f1e85dc5'
down_revision = '4f70aca73590'
branch_labels = None
depends_on = None


def upgrade():
    connection = op.get_bind()
    connection.execute('DELETE from "order"')
    connection.execute('DELETE from product_in_basket')
    connection.execute('DELETE from basket')
    op.add_column('basket', sa.Column('shop_id', sa.Integer, sa.ForeignKey('shop.id'), nullable=False))


def downgrade():
    op.drop_column('basket', 'shop_id')
