"""Modèle ORM événement d'audit.

:spec: FEAT-002.1
"""

from datetime import datetime
from typing import Any

from sqlalchemy import JSON, DateTime, String
from sqlalchemy.orm import Mapped, mapped_column

from baobab_auth_database.models.orm.auth_orm_base import AuthOrmBase
from baobab_auth_database.naming.auth_table_naming_convention import (
    AuthTableNamingConvention,
)


class AuthAuditEventModel(AuthOrmBase):
    """Table ``auth_audit_events`` — journal d'audit immuable.

    :spec: FEAT-002.1
    """

    __tablename__ = AuthTableNamingConvention.table_name("audit_events")

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    event_type: Mapped[str] = mapped_column(String(64), nullable=False)
    severity: Mapped[str] = mapped_column(String(32), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    actor_subject: Mapped[str | None] = mapped_column(String(255))
    target_type: Mapped[str | None] = mapped_column(String(64))
    target_id: Mapped[str | None] = mapped_column(String(64))
    ip_address: Mapped[str | None] = mapped_column(String(64))
    user_agent: Mapped[str | None] = mapped_column(String(512))
    event_metadata: Mapped[dict[str, Any]] = mapped_column(
        JSON,
        nullable=False,
        insert_default=dict,
    )

    def __repr__(self) -> str:
        """Représentation lisible.

        :returns: Représentation de l'événement d'audit.
        """
        return (
            f"AuthAuditEventModel(id={self.id!r}, event_type={self.event_type!r}, "
            f"target_type={self.target_type!r}, target_id={self.target_id!r})"
        )
