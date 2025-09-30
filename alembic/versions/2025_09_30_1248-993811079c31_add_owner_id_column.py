"""add owner_id column

Revision ID: 993811079c31
Revises: 3a537f3e05eb
Create Date: 2025-09-30 12:48:36.579307

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "993811079c31"
down_revision: Union[str, Sequence[str], None] = "3a537f3e05eb"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("photos", sa.Column("owner_id", sa.Integer(), nullable=False))
    op.create_foreign_key(
        op.f("fk_photos_owner_id_users"),
        "photos",
        "users",
        ["owner_id"],
        ["id"],
        ondelete="RESTRICT",
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint(op.f("fk_photos_owner_id_users"), "photos", type_="foreignkey")
    op.drop_column("photos", "owner_id")
