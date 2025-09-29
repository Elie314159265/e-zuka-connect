"""fix_is_active_default_values

Revision ID: 144f09c861db
Revises: b4c4a58fcac3
Create Date: 2025-09-29 03:45:46.827602

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '144f09c861db'
down_revision: Union[str, Sequence[str], None] = 'b4c4a58fcac3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Fix is_active columns to have proper default values and NOT NULL constraint

    # First, update any NULL values to True (active by default)
    op.execute("UPDATE product_categories SET is_active = TRUE WHERE is_active IS NULL")
    op.execute("UPDATE products SET is_active = TRUE WHERE is_active IS NULL")
    op.execute("UPDATE products SET is_featured = FALSE WHERE is_featured IS NULL")
    op.execute("UPDATE products SET is_seasonal = FALSE WHERE is_seasonal IS NULL")
    op.execute("UPDATE products SET is_stock_managed = TRUE WHERE is_stock_managed IS NULL")

    # Add default values to columns
    op.alter_column('product_categories', 'is_active',
                   server_default=sa.text('TRUE'), nullable=False)
    op.alter_column('product_categories', 'sort_order',
                   server_default=sa.text('0'), nullable=False)

    op.alter_column('products', 'is_active',
                   server_default=sa.text('TRUE'), nullable=False)
    op.alter_column('products', 'is_featured',
                   server_default=sa.text('FALSE'), nullable=False)
    op.alter_column('products', 'is_seasonal',
                   server_default=sa.text('FALSE'), nullable=False)
    op.alter_column('products', 'is_stock_managed',
                   server_default=sa.text('TRUE'), nullable=False)
    op.alter_column('products', 'stock_quantity',
                   server_default=sa.text('0'), nullable=False)
    op.alter_column('products', 'low_stock_threshold',
                   server_default=sa.text('10'), nullable=False)
    op.alter_column('products', 'tax_rate',
                   server_default=sa.text('0.10'), nullable=False)
    op.alter_column('products', 'unit',
                   server_default=sa.text("'個'"), nullable=False)


def downgrade() -> None:
    """Downgrade schema."""
    # Revert columns to nullable with no defaults
    op.alter_column('product_categories', 'is_active',
                   server_default=None, nullable=True)
    op.alter_column('product_categories', 'sort_order',
                   server_default=None, nullable=True)

    op.alter_column('products', 'is_active',
                   server_default=None, nullable=True)
    op.alter_column('products', 'is_featured',
                   server_default=None, nullable=True)
    op.alter_column('products', 'is_seasonal',
                   server_default=None, nullable=True)
    op.alter_column('products', 'is_stock_managed',
                   server_default=None, nullable=True)
    op.alter_column('products', 'stock_quantity',
                   server_default=None, nullable=True)
    op.alter_column('products', 'low_stock_threshold',
                   server_default=None, nullable=True)
    op.alter_column('products', 'tax_rate',
                   server_default=None, nullable=True)
    op.alter_column('products', 'unit',
                   server_default=None, nullable=True)
