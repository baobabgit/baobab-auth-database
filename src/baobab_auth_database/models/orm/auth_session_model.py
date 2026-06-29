"""Modèle ORM session utilisateur.

:spec: FEAT-002.1
"""

from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from baobab_auth_database.models.orm.auth_orm_base import AuthOrmBase
from baobab_auth_database.naming.auth_table_naming_convention import (
    AuthTableNamingConvention,
)


class AuthSessionModel(AuthOrmBase):
    """Table ``auth_sessions`` — session persistée.

    ``repr()`` n'expose jamais ``refresh_token_hash``.

    :spec: FEAT-002.1
    """

    __tablename__ = AuthTableNamingConvention.table_name("sessions")
    __table_args__ = (
        UniqueConstraint("id", name="uq_auth_sessions_session_id"),
        UniqueConstraint(
            "refresh_token_hash", name="uq_auth_sessions_refresh_token_hash"
        ),
    )

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    user_id: Mapped[str] = mapped_column(
        String(64),
        ForeignKey(f"{AuthTableNamingConvention.table_name('users')}.id"),
        nullable=False,
    )
    refresh_token_hash: Mapped[str] = mapped_column(String(512), nullable=False)
    status: Mapped[str] = mapped_column(String(32), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    expires_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    revoked_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    last_used_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    user_agent: Mapped[str | None] = mapped_column(String(512))
    ip_address: Mapped[str | None] = mapped_column(String(64))
    device_label: Mapped[str | None] = mapped_column(String(255))

    def __repr__(self) -> str:
        """Représentation sans refresh token.

        :returns: Représentation sûre de la session.
        """
        return (
            f"AuthSessionModel(id={self.id!r}, user_id={self.user_id!r}, "
            f"status={self.status!r})"
        )
