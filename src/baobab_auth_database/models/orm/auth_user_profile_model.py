"""Modèle ORM profil utilisateur.

:spec: FEAT-002.1
"""

from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from baobab_auth_database.models.orm.auth_orm_base import AuthOrmBase
from baobab_auth_database.naming.auth_table_naming_convention import (
    AuthTableNamingConvention,
)


class AuthUserProfileModel(AuthOrmBase):
    """Table ``auth_profiles`` — profil public sans secret.

    :spec: FEAT-002.1
    """

    __tablename__ = AuthTableNamingConvention.table_name("profiles")

    user_id: Mapped[str] = mapped_column(
        String(64),
        ForeignKey(f"{AuthTableNamingConvention.table_name('users')}.id"),
        primary_key=True,
    )
    display_name: Mapped[str | None] = mapped_column(String(255))
    locale: Mapped[str | None] = mapped_column(String(32))
    timezone: Mapped[str | None] = mapped_column(String(64))
    avatar_url: Mapped[str | None] = mapped_column(String(2048))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )

    def __repr__(self) -> str:
        """Représentation lisible.

        :returns: Représentation du profil.
        """
        return f"AuthUserProfileModel(user_id={self.user_id!r})"
