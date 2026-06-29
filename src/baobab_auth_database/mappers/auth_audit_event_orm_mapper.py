"""Mapper ORM audit ↔ entité ``AuditEvent`` du core.

:spec: FEAT-004.1
"""

from baobab_auth_core.domain.entities.audit_event import AuditEvent
from baobab_auth_core.domain.enums.audit_event_type import AuditEventType
from baobab_auth_core.domain.enums.audit_severity import AuditSeverity
from baobab_auth_core.domain.value_objects.audit_event_id import AuditEventId
from baobab_auth_core.domain.value_objects.auth_subject import AuthSubject
from baobab_auth_core.exceptions.validation import ValidationError

from baobab_auth_database.exceptions.mapping.auth_database_mapping_error import (
    AuthDatabaseMappingError,
)
from baobab_auth_database.mappers.auth_orm_value_converter import AuthOrmValueConverter
from baobab_auth_database.models.orm.auth_audit_event_model import AuthAuditEventModel


class AuthAuditEventOrmMapper:
    """Convertit ``AuthAuditEventModel`` en :class:`AuditEvent` et inversement.

    :spec: FEAT-004.1
    """

    def to_domain(self, model: AuthAuditEventModel) -> AuditEvent:
        """Construit une entité ``AuditEvent`` depuis le modèle ORM.

        :param model: Ligne ``auth_audit_events``.
        :returns: Entité core immuable.
        :raises AuthDatabaseMappingError: Si la conversion échoue.
        """
        try:
            actor = (
                AuthSubject(model.actor_subject)
                if model.actor_subject is not None
                else None
            )
            return AuditEvent(
                id=AuditEventId(model.id),
                event_type=AuthOrmValueConverter.to_enum(
                    AuditEventType, model.event_type, "event_type"
                ),
                severity=AuthOrmValueConverter.to_enum(
                    AuditSeverity, model.severity, "severity"
                ),
                created_at=model.created_at,
                actor_subject=actor,
                target_type=model.target_type,
                target_id=model.target_id,
                ip_address=model.ip_address,
                user_agent=model.user_agent,
                metadata=dict(model.event_metadata),
            )
        except (ValidationError, ValueError) as exc:
            msg = "Impossible de mapper AuthAuditEventModel vers AuditEvent."
            raise AuthDatabaseMappingError(msg, cause=exc) from exc

    def to_model(self, event: AuditEvent) -> AuthAuditEventModel:
        """Construit un modèle ORM depuis une entité ``AuditEvent``.

        :param event: Entité core.
        :returns: Modèle SQLAlchemy.
        """
        return AuthAuditEventModel(
            id=str(event.id),
            event_type=event.event_type.value,
            severity=event.severity.value,
            created_at=event.created_at,
            actor_subject=str(event.actor_subject) if event.actor_subject else None,
            target_type=event.target_type,
            target_id=event.target_id,
            ip_address=event.ip_address,
            user_agent=event.user_agent,
            event_metadata=dict(event.metadata),
        )
