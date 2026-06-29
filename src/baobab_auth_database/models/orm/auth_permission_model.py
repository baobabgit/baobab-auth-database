"""Modèle ORM permission.

:spec: FEAT-002.1
"""

from datetime import datetime

from sqlalchemy import Boolean, DateTime, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from baobab_auth_database.models.orm.auth_orm_base import AuthOrmBase
from baobab_auth_database.naming.auth_table_naming_convention import (
    AuthTableNamingConvention,
)


class AuthPermissionModel(AuthOrmBase):
    """Table ``auth_permissions`` — permission atomique RBAC.

    :spec: FEAT-002.1
    """

    __tablename__ = AuthTableNamingConvention.table_name("permissions")
    __table_args__ = (UniqueConstraint("name", name="uq_auth_permissions_name"),)

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    name: Mapped[str] = mapped_column(String(128), nullable=False)
    resource: Mapped[str] = mapped_column(String(64), nullable=False)
    action: Mapped[str] = mapped_column(String(64), nullable=False)
    is_system: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    description: Mapped[str | None] = mapped_column(String(512))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )

    def __repr__(self) -> str:
        """Représentation lisible.

        :returns: Représentation de la permission.
        """
        return (
            f"AuthPermissionModel(id={self.id!r}, name={self.name!r}, "
            f"resource={self.resource!r}, action={self.action!r})"
        )
