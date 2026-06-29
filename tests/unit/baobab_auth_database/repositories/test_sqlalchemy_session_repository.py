"""Tests SqlAlchemySessionRepository."""

import pytest
from baobab_auth_core.domain.entities.session import Session
from baobab_auth_core.domain.enums.session_status import SessionStatus
from baobab_auth_core.domain.value_objects.session_id import SessionId
from baobab_auth_core.domain.value_objects.token_id import TokenId
from baobab_auth_core.domain.value_objects.user_id import UserId
from sqlalchemy.orm import Session as OrmSession

from baobab_auth_database.exceptions.persistence import AuthDatabasePersistenceError
from baobab_auth_database.repositories.sqlalchemy_session_repository import (
    SqlAlchemySessionRepository,
)


class TestSqlAlchemySessionRepository:
    """Tests FEAT-003.1 — repository session."""

    def _session(
        self, now_utc, *, session_id: str = "sess-1", token: str = "rt-1"
    ) -> Session:
        return Session(
            id=SessionId(session_id),
            user_id=UserId("user-1"),
            refresh_token_id=TokenId(token),
            status=SessionStatus.ACTIVE,
            created_at=now_utc,
            expires_at=now_utc,
        )

    def test_FEAT_003_1_roundtrip_session(
        self, db_session: OrmSession, now_utc
    ) -> None:
        repo = SqlAlchemySessionRepository(db_session)
        auth_session = self._session(now_utc)
        repo.save(auth_session)
        restored = repo.get_by_id(auth_session.id)
        assert restored is not None
        assert restored.refresh_token_id == auth_session.refresh_token_id
        assert restored.status == auth_session.status
        assert (
            repo.get_by_refresh_token_id(auth_session.refresh_token_id) == restored
        )
        assert repo.get_active_by_user(auth_session.user_id) == [restored]

    def test_FEAT_003_1_get_absent(self, db_session: OrmSession, now_utc) -> None:
        repo = SqlAlchemySessionRepository(db_session)
        assert repo.get_by_id(SessionId("missing")) is None
        assert repo.get_by_refresh_token_id(TokenId("missing")) is None
        assert repo.get_active_by_user(UserId("user-1")) == []

    def test_FEAT_003_1_active_exclut_revoked(
        self, db_session: OrmSession, now_utc
    ) -> None:
        repo = SqlAlchemySessionRepository(db_session)
        revoked = Session(
            id=SessionId("sess-revoked"),
            user_id=UserId("user-1"),
            refresh_token_id=TokenId("rt-revoked"),
            status=SessionStatus.REVOKED,
            created_at=now_utc,
            expires_at=now_utc,
        )
        repo.save(revoked)
        assert repo.get_active_by_user(UserId("user-1")) == []

    def test_FEAT_003_1_unicite_refresh_token(
        self, db_session: OrmSession, now_utc
    ) -> None:
        repo = SqlAlchemySessionRepository(db_session)
        repo.save(self._session(now_utc))
        duplicate = self._session(now_utc, session_id="sess-2", token="rt-1")
        with pytest.raises(AuthDatabasePersistenceError):
            repo.save(duplicate)

    def test_FEAT_003_1_delete_session(self, db_session: OrmSession, now_utc) -> None:
        repo = SqlAlchemySessionRepository(db_session)
        auth_session = self._session(now_utc)
        repo.save(auth_session)
        repo.delete(auth_session.id)
        assert repo.get_by_id(auth_session.id) is None
