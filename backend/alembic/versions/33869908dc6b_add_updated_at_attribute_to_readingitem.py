"""Add updated_at attribute to ReadingItem

Revision ID: 33869908dc6b
Revises: 3ac7da654ec8
Create Date: 2025-03-23 12:48:31.835722

"""
from datetime import datetime
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '33869908dc6b'
down_revision: Union[str, None] = '3ac7da654ec8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('reading_item', sa.Column('updated_at', sa.DateTime(), nullable=True))
    op.execute(f"UPDATE reading_item SET updated_at = '{datetime.now()}'")
    op.alter_column('reading_item', 'updated_at', nullable=False)

def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('reading_item', 'updated_at')
