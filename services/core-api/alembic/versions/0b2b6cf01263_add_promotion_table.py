"""add_promotion_table

Revision ID: 0b2b6cf01263
Revises: 144f09c861db
Create Date: 2025-10-06 05:08:11.119293

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0b2b6cf01263'
down_revision: Union[str, Sequence[str], None] = '144f09c861db'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Create promotions table
    op.create_table('promotions',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('store_id', sa.Integer(), nullable=False),
        sa.Column('product_id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('promotion_text', sa.Text(), nullable=True),
        sa.Column('promotion_image_urls', sa.JSON(), nullable=True),
        sa.Column('start_date', sa.DateTime(timezone=True), nullable=False),
        sa.Column('end_date', sa.DateTime(timezone=True), nullable=False),
        sa.Column('status', sa.String(), nullable=True),
        sa.Column('is_auto_published', sa.Boolean(), nullable=True),
        sa.Column('published_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('display_priority', sa.Integer(), nullable=True),
        sa.Column('target_audience', sa.JSON(), nullable=True),
        sa.Column('max_views', sa.Integer(), nullable=True),
        sa.Column('current_views', sa.Integer(), nullable=True),
        sa.Column('tags', sa.JSON(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['product_id'], ['products.id'], ),
        sa.ForeignKeyConstraint(['store_id'], ['stores.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_promotions_id'), 'promotions', ['id'], unique=False)
    op.create_index(op.f('ix_promotions_title'), 'promotions', ['title'], unique=False)
    op.create_index(op.f('ix_promotions_start_date'), 'promotions', ['start_date'], unique=False)
    op.create_index(op.f('ix_promotions_end_date'), 'promotions', ['end_date'], unique=False)
    op.create_index(op.f('ix_promotions_status'), 'promotions', ['status'], unique=False)


def downgrade() -> None:
    """Downgrade schema."""
    # Drop promotions table
    op.drop_index(op.f('ix_promotions_status'), table_name='promotions')
    op.drop_index(op.f('ix_promotions_end_date'), table_name='promotions')
    op.drop_index(op.f('ix_promotions_start_date'), table_name='promotions')
    op.drop_index(op.f('ix_promotions_title'), table_name='promotions')
    op.drop_index(op.f('ix_promotions_id'), table_name='promotions')
    op.drop_table('promotions')
