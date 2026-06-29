"""Modèle ORM association utilisateur-rôle.

:spec: FEAT-002.1
"""

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from baobab_auth_database.models.orm.auth_orm_base import AuthOrmBase
from baobab_auth_database.naming.auth_table_naming_convention import (
    AuthTableNamingConvention,
)

_USERS = AuthTableNamingConvention.table_name("users")
_ROLES = AuthTableNamingConvention.table_name("roles")


class AuthUserRoleModel(AuthOrmBase):
    """Table ``auth_user_roles`` — assignation rôle ↔ utilisateur.

    :spec: FEAT-002.1
    """

    __tablename__ = AuthTableNamingConvention.table_name("user_roles")

    user_id: Mapped[str] = mapped_column(
        String(64),
        ForeignKey(f"{_USERS}.id"),
        primary_key=True,
    )
    role_id: Mapped[str] = mapped_column(
        String(64),
        ForeignKey(f"{_ROLES}.id"),
        primary_key=True,
    )

    def __repr__(self) -> str:
        """Représentation lisible.

        :returns: Représentation de l'association.
        """
        return f"AuthUserRoleModel(user_id={self.user_id!r}, role_id={self.role_id!r})"
