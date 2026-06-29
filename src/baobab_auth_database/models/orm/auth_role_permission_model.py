"""Modèle ORM association rôle-permission.

:spec: FEAT-002.1
"""

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from baobab_auth_database.models.orm.auth_orm_base import AuthOrmBase
from baobab_auth_database.naming.auth_table_naming_convention import (
    AuthTableNamingConvention,
)

_PERMISSIONS = AuthTableNamingConvention.table_name("permissions")
_ROLES = AuthTableNamingConvention.table_name("roles")


class AuthRolePermissionModel(AuthOrmBase):
    """Table ``auth_role_permissions`` — assignation permission ↔ rôle.

    :spec: FEAT-002.1
    """

    __tablename__ = AuthTableNamingConvention.table_name("role_permissions")

    role_id: Mapped[str] = mapped_column(
        String(64),
        ForeignKey(f"{_ROLES}.id"),
        primary_key=True,
    )
    permission_id: Mapped[str] = mapped_column(
        String(64),
        ForeignKey(f"{_PERMISSIONS}.id"),
        primary_key=True,
    )

    def __repr__(self) -> str:
        """Représentation lisible.

        :returns: Représentation de l'association.
        """
        return (
            f"AuthRolePermissionModel(role_id={self.role_id!r}, "
            f"permission_id={self.permission_id!r})"
        )
