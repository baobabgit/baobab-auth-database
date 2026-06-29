"""Modèle ORM utilisateur.

:spec: FEAT-002.1
"""

from datetime import datetime

from sqlalchemy import DateTime, Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from baobab_auth_database.models.orm.auth_orm_base import AuthOrmBase
from baobab_auth_database.naming.auth_table_naming_convention import (
    AuthTableNamingConvention,
)


class AuthUserModel(AuthOrmBase):
    """Table ``auth_users`` — compte utilisateur persisté.

    ``repr()`` n'expose jamais ``password_hash``.

    :spec: FEAT-002.1
    """

    __tablename__ = AuthTableNamingConvention.table_name("users")
    __table_args__ = (
        UniqueConstraint("auth_subject", name="uq_auth_users_auth_subject"),
        UniqueConstraint("normalized_email", name="uq_auth_users_normalized_email"),
    )

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    auth_subject: Mapped[str] = mapped_column(String(255), nullable=False)
    normalized_email: Mapped[str] = mapped_column(String(320), nullable=False)
    password_hash: Mapped[str] = mapped_column(String(512), nullable=False)
    status: Mapped[str] = mapped_column(String(32), nullable=False)
    failed_login_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    locked_until: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    last_login_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )

    def __repr__(self) -> str:
        """Représentation sans mot de passe.

        :returns: Représentation sûre du modèle.
        """
        return (
            f"AuthUserModel(id={self.id!r}, auth_subject={self.auth_subject!r}, "
            f"normalized_email={self.normalized_email!r}, status={self.status!r})"
        )
