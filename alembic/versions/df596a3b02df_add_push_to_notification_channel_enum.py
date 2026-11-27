"""add push to notification channel enum

Revision ID: df596a3b02df
Revises: 28c127f0c8f1
Create Date: 2026-11-27 06:56:21.516756

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'df596a3b02df'
down_revision: Union[str, Sequence[str], None] = '28c127f0c8f1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(
        "ALTER TYPE notification_channel "
        "ADD VALUE IF NOT EXISTS 'push'"
    )


def downgrade() -> None:
    raise NotImplementedError(
        "Removing an ENUM value requires recreating the type"
    )