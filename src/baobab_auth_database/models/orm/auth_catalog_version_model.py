"""Modèle ORM version de catalogue RBAC.

:spec: FEAT-006.1
"""

from datetime import datetime

from sqlalchemy import DateTime, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from baobab_auth_database.models.orm.auth_orm_base import AuthOrmBase
from baobab_auth_database.naming.auth_table_naming_convention import (
    AuthTableNamingConvention,
)


class AuthCatalogVersionModel(AuthOrmBase):
    """Table ``auth_catalog_versions`` — trace d'application du catalogue.

    :spec: FEAT-006.1
    """

    __tablename__ = AuthTableNamingConvention.table_name("catalog_versions")

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    core_version: Mapped[str] = mapped_column(String(32), nullable=False)
    compat_profile: Mapped[str] = mapped_column(String(32), nullable=False)
    catalog_checksum: Mapped[str] = mapped_column(String(64), nullable=False)
    applied_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    applied_by: Mapped[str | None] = mapped_column(String(128))
    metadata_json: Mapped[str | None] = mapped_column(Text)

    def __repr__(self) -> str:
        """Représentation lisible.

        :returns: Représentation de la version catalogue.
        """
        return (
            f"AuthCatalogVersionModel(id={self.id!r}, "
            f"checksum={self.catalog_checksum!r})"
        )
