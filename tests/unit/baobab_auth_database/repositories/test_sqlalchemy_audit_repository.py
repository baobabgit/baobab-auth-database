"""Tests SqlAlchemyAuditRepository."""

from baobab_auth_core.domain.entities.audit_event import AuditEvent
from baobab_auth_core.domain.enums.audit_event_type import AuditEventType
from baobab_auth_core.domain.enums.audit_severity import AuditSeverity
from baobab_auth_core.domain.value_objects.audit_event_id import AuditEventId
from baobab_auth_core.domain.value_objects.auth_subject import AuthSubject
from sqlalchemy.orm import Session

from baobab_auth_database.repositories.sqlalchemy_audit_repository import (
    SqlAlchemyAuditRepository,
)


class TestSqlAlchemyAuditRepository:
    """Tests FEAT-003.1 — repository audit."""

    def test_FEAT_003_1_save_et_list_by_actor(
        self, db_session: Session, now_utc
    ) -> None:
        actor = AuthSubject("sub-1")
        first = AuditEvent(
            id=AuditEventId("a1"),
            event_type=AuditEventType.LOGIN_SUCCESS,
            severity=AuditSeverity.INFO,
            created_at=now_utc,
            actor_subject=actor,
        )
        second = AuditEvent(
            id=AuditEventId("a2"),
            event_type=AuditEventType.LOGOUT,
            severity=AuditSeverity.INFO,
            created_at=now_utc,
            actor_subject=actor,
        )
        repo = SqlAlchemyAuditRepository(db_session)
        repo.save(first)
        repo.save(second)
        events = repo.list_by_actor(actor)
        assert [event.id for event in events] == [first.id, second.id]
