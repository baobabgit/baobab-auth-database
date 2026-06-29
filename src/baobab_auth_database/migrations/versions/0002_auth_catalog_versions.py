"""auth catalog versions table

Revision ID: 0002
Revises: 0001
Create Date: 2026-06-28 20:00:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0002"
down_revision: str | Sequence[str] | None = "0001"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "auth_catalog_versions",
        sa.Column("id", sa.String(length=64), nullable=False),
        sa.Column("core_version", sa.String(length=32), nullable=False),
        sa.Column("compat_profile", sa.String(length=32), nullable=False),
        sa.Column("catalog_checksum", sa.String(length=64), nullable=False),
        sa.Column("applied_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("applied_by", sa.String(length=128), nullable=True),
        sa.Column("metadata_json", sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_auth_catalog_versions")),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("auth_catalog_versions")
