"""create delete driver procedure

Revision ID: f58a3c67a070
Revises: 146f718907e6
Create Date: 2026-10-23 15:00:03.911267

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f58a3c67a070'
down_revision: Union[str, Sequence[str], None] = '146f718907e6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
