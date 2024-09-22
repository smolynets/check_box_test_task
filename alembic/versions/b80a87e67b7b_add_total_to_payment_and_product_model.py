"""add_total_to_payment_and_product_model

Revision ID: b80a87e67b7b
Revises: b825d4a49c1f
Create Date: 2024-09-22 10:17:09.065114

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b80a87e67b7b'
down_revision: Union[str, None] = 'b825d4a49c1f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('payments', sa.Column('payment_total', sa.Numeric(precision=10, scale=2), nullable=True))
    op.add_column('payments', sa.Column('rest', sa.Numeric(precision=10, scale=2), nullable=True))
    op.add_column('products', sa.Column('product_total', sa.Numeric(precision=10, scale=2), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('products', 'product_total')
    op.drop_column('payments', 'rest')
    op.drop_column('payments', 'payment_total')
    # ### end Alembic commands ###
