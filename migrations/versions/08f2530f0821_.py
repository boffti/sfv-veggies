"""empty message

Revision ID: 08f2530f0821
Revises: 
Create Date: 2020-04-13 13:02:05.100168

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '08f2530f0821'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('apartment',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('categories',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('stock',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('in_stock', sa.Boolean(), nullable=True),
    sa.Column('stock', sa.Float(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('testimonials',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('testimonial', sa.String(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(), nullable=True),
    sa.Column('phone', sa.String(), nullable=True),
    sa.Column('password', sa.String(), nullable=True),
    sa.Column('fname', sa.String(), nullable=True),
    sa.Column('apt', sa.String(), nullable=True),
    sa.Column('apt_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['apt_id'], ['apartment.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('vegetables',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('k_name', sa.String(), nullable=True),
    sa.Column('price', sa.Float(), nullable=True),
    sa.Column('image', sa.String(length=120), nullable=True),
    sa.Column('unit', sa.String(), nullable=True),
    sa.Column('onSale', sa.Boolean(), nullable=True),
    sa.Column('category_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['category_id'], ['categories.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('orders',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('customer_id', sa.Integer(), nullable=False),
    sa.Column('order_number', sa.String(), nullable=True),
    sa.Column('order_date', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['customer_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('order_details',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('product_id', sa.Integer(), nullable=True),
    sa.Column('order_id', sa.Integer(), nullable=True),
    sa.Column('price', sa.String(), nullable=True),
    sa.Column('qty', sa.String(), nullable=True),
    sa.Column('total', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['order_id'], ['orders.id'], ),
    sa.ForeignKeyConstraint(['product_id'], ['vegetables.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('order_details')
    op.drop_table('orders')
    op.drop_table('vegetables')
    op.drop_table('users')
    op.drop_table('testimonials')
    op.drop_table('stock')
    op.drop_table('categories')
    op.drop_table('apartment')
    # ### end Alembic commands ###