"""add photo transformed table

Revision ID: 699cc73d87e0
Revises: 7a6e664f0503
Create Date: 2025-10-07 12:39:08.489907

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "699cc73d87e0"
down_revision: Union[str, Sequence[str], None] = "7a6e664f0503"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "photo_transformed",
        sa.Column("uuid", sa.Uuid(), nullable=False),
        sa.Column("original_uuid", sa.Uuid(), nullable=False),
        sa.Column("transformed_url", sa.Text(), nullable=False),
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text("TIMEZONE('utc', now())"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["original_uuid"],
            ["photos.uuid"],
            name=op.f("fk_photo_transformed_original_uuid_photos"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("uuid", name=op.f("pk_photo_transformed")),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("photo_transformed")
