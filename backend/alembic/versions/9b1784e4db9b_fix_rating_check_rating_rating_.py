"""Fix rating.check_rating_rating constraint

Revision ID: 9b1784e4db9b
Revises: 7b4e40279e98
Create Date: 2025-03-21 19:27:01.337363

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9b1784e4db9b'
down_revision: Union[str, None] = '7b4e40279e98'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_check_constraint(
        'check_rating_rating',
        'rating',
        sa.text('rating >= 1 AND rating <= 5')
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint(
        'check_rating_rating',
        'rating',
        type_='check'
    )
