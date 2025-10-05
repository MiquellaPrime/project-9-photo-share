"""add comments table

Revision ID: 7a6e664f0503
Revises: 2a1d3e8ea6c1
Create Date: 2025-10-05 19:48:23.888424

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "7a6e664f0503"
down_revision: Union[str, Sequence[str], None] = "2a1d3e8ea6c1"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "comments",
        sa.Column("uuid", sa.Uuid(), nullable=False),
        sa.Column("photo_uuid", sa.Uuid(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("text", sa.Text(), nullable=False),
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text("TIMEZONE('utc', now())"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text("TIMEZONE('utc', now())"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["photo_uuid"],
            ["photos.uuid"],
            name=op.f("fk_comments_photo_uuid_photos"),
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
            name=op.f("fk_comments_user_id_users"),
            ondelete="RESTRICT",
        ),
        sa.PrimaryKeyConstraint("uuid", name=op.f("pk_comments")),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("comments")
