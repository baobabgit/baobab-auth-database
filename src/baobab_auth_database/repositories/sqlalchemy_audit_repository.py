"""Repository SQLAlchemy des événements d'audit.

:spec: FEAT-003.1
"""

from baobab_auth_core.domain.entities.audit_event import AuditEvent
from baobab_auth_core.domain.value_objects.auth_subject import AuthSubject
from sqlalchemy import select
from sqlalchemy.orm import Session

from baobab_auth_database.mappers.auth_audit_event_orm_mapper import (
    AuthAuditEventOrmMapper,
)
from baobab_auth_database.models.orm.auth_audit_event_model import AuthAuditEventModel
from baobab_auth_database.repositories.sqlalchemy_persistence_guard import (
    SqlAlchemyPersistenceGuard,
)


class SqlAlchemyAuditRepository:
    """Implémentation synchrone du port ``AuditRepository``.

    :spec: FEAT-003.1
    """

    def __init__(
        self,
        session: Session,
        mapper: AuthAuditEventOrmMapper | None = None,
    ) -> None:
        """Injecte la session et le mapper.

        :param session: Session SQLAlchemy partagée.
        :param mapper: Mapper audit ; instance par défaut si omis.
        """
        self._session = session
        self._mapper = mapper or AuthAuditEventOrmMapper()

    def save(self, event: AuditEvent) -> None:
        """Enregistre un événement d'audit (append-only).

        :param event: Événement core.
        """
        self._session.add(self._mapper.to_model(event))
        SqlAlchemyPersistenceGuard.flush(self._session)

    def list_by_actor(self, actor_subject: AuthSubject) -> list[AuditEvent]:
        """Liste les événements d'un acteur triés par date croissante.

        :param actor_subject: Sujet de l'acteur.
        :returns: Événements correspondants.
        """
        models = self._session.scalars(
            select(AuthAuditEventModel)
            .where(AuthAuditEventModel.actor_subject == str(actor_subject))
            .order_by(AuthAuditEventModel.created_at)
        ).all()
        return [self._mapper.to_domain(model) for model in models]
