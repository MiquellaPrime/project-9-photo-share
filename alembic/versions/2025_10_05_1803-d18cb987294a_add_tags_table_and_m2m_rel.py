"""add tags table and m2m rel

Revision ID: d18cb987294a
Revises: 37973af9fab2
Create Date: 2025-10-05 18:03:47.506158

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "d18cb987294a"
down_revision: Union[str, Sequence[str], None] = "37973af9fab2"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "tags",
        sa.Column("uuid", sa.Uuid(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text("TIMEZONE('utc', now())"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("uuid", name=op.f("pk_tags")),
    )
    op.create_table(
        "photo_tags",
        sa.Column("photo_uuid", sa.Uuid(), nullable=False),
        sa.Column("tag_uuid", sa.Uuid(), nullable=False),
        sa.ForeignKeyConstraint(
            ["photo_uuid"],
            ["photos.uuid"],
            name=op.f("fk_photo_tags_photo_uuid_photos"),
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["tag_uuid"],
            ["tags.uuid"],
            name=op.f("fk_photo_tags_tag_uuid_tags"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("photo_uuid", "tag_uuid", name=op.f("pk_photo_tags")),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("photo_tags")
    op.drop_table("tags")
