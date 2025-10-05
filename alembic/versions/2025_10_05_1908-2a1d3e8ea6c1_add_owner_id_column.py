"""add owner_id column

Revision ID: 2a1d3e8ea6c1
Revises: d18cb987294a
Create Date: 2025-10-05 19:08:23.801080

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "2a1d3e8ea6c1"
down_revision: Union[str, Sequence[str], None] = "d18cb987294a"
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
