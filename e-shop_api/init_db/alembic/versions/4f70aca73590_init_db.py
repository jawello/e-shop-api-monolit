"""init db

Revision ID: 4f70aca73590
Revises: 
Create Date: 2019-11-09 20:36:38.779724

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '4f70aca73590'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('uua',
                    sa.Column('id', sa.Integer, primary_key=True),
                    sa.Column('name', sa.String, nullable=False),
                    sa.Column('login', sa.String, nullable=False),
                    sa.Column('password', sa.String, nullable=False)
                    )
    op.create_unique_constraint('uq_uua_login', 'uua', ['login'])

    op.create_table('product',
                    sa.Column('id', sa.Integer, primary_key=True),
                    sa.Column('name', sa.String, nullable=False),
                    sa.Column('description', sa.String))

    op.create_table('shop',
                    sa.Column('id', sa.Integer, primary_key=True),
                    sa.Column('name', sa.String, nullable=False),
                    sa.Column('description', sa.String),
                    sa.Column('site', sa.String))

    op.create_table('product_shop',
                    sa.Column('id', sa.Integer, primary_key=True),
                    sa.Column('product_id', sa.Integer, sa.ForeignKey('product.id'), nullable=False),
                    sa.Column('shop_id', sa.Integer, sa.ForeignKey('shop.id'), nullable=False),
                    sa.Column('price', sa.Float),
                    sa.Column('quantity', sa.Integer),
                    sa.UniqueConstraint('product_id', 'shop_id', name='uix_product_shop'))
    op.create_unique_constraint('uq_product_shop', 'product_shop', ['product_id', 'shop_id'])
    op.create_check_constraint('ck_quantity_shop', 'product_shop', 'quantity > -1')

    op.create_table('basket',
                    sa.Column('id', sa.Integer, primary_key=True),
                    sa.Column('user_id', sa.Integer, nullable=False),
                    )

    op.create_table('product_in_basket',
                    sa.Column('id', sa.Integer, primary_key=True),
                    sa.Column('basket_id', sa.Integer, sa.ForeignKey('basket.id'), nullable=False),
                    sa.Column('product_shop_ids', sa.Integer, nullable=True),
                    sa.Column('quantity', sa.Integer, default=1)
                    )
    op.create_unique_constraint('uq_product_basket_id', 'product_in_basket', ['basket_id'])
    op.create_check_constraint('ck_quantity_basket', 'product_in_basket', 'quantity > 0')

    order_status_table = op.create_table('order_status',
                                         sa.Column('id', sa.String, primary_key=True))
    op.bulk_insert(
        order_status_table,
        [
            {"id": "check availability"},
            {"id": "awaiting payment"},
            {"id": "paid"},
        ]
    )

    op.create_table('order',
                    sa.Column('id', sa.Integer, primary_key=True),
                    sa.Column('user_id', sa.Integer, nullable=False),
                    sa.Column('basket_id', sa.Integer, nullable=False),
                    sa.Column('date', sa.DateTime, nullable=False),
                    sa.Column('status', sa.String, sa.ForeignKey('order_status.id'), nullable=False),
                    )
    op.create_unique_constraint('uq_order_basket_id', 'order', ['basket_id'])


def downgrade():
    op.drop_constraint('uq_order_basket_id', 'order')
    op.drop_table('order')
    op.drop_table('order_status')

    op.drop_constraint('uq_product_basket_id', 'product_in_basket')
    op.drop_constraint('ck_quantity_basket', 'product_in_basket')
    op.drop_table('product_in_basket')
    op.drop_table('basket')

    op.drop_constraint('uq_product_shop', 'product_shop')
    op.drop_constraint('ck_quantity_shop', 'product_shop')
    op.drop_table('product_shop')
    op.drop_table('shop')
    op.drop_table('product')

    op.drop_constraint('uq_uua_login', 'uua')
    op.drop_table('uua')
