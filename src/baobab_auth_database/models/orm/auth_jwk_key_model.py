"""Modèle ORM clé JWK persistée.

:spec: FEAT-002.1
"""

from datetime import datetime

from sqlalchemy import Boolean, DateTime, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from baobab_auth_database.models.orm.auth_orm_base import AuthOrmBase
from baobab_auth_database.naming.auth_table_naming_convention import (
    AuthTableNamingConvention,
)


class AuthJwkKeyModel(AuthOrmBase):
    """Table ``auth_jwk_keys`` — stockage des clés JWK (privée chiffrée).

    ``repr()`` n'expose jamais ``private_key_encrypted``.

    :spec: FEAT-002.1
    """

    __tablename__ = AuthTableNamingConvention.table_name("jwk_keys")
    __table_args__ = (UniqueConstraint("kid", name="uq_auth_jwk_keys_kid"),)

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    kid: Mapped[str] = mapped_column(String(128), nullable=False)
    algorithm: Mapped[str] = mapped_column(String(32), nullable=False)
    public_key: Mapped[str] = mapped_column(Text, nullable=False)
    private_key_encrypted: Mapped[str] = mapped_column(Text, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    expires_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    revoked_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    def __repr__(self) -> str:
        """Représentation sans clé privée.

        :returns: Représentation sûre de la clé JWK.
        """
        return (
            f"AuthJwkKeyModel(id={self.id!r}, kid={self.kid!r}, "
            f"algorithm={self.algorithm!r}, is_active={self.is_active!r})"
        )
