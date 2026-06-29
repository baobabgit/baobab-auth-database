"""Tests SqlAlchemyPersistenceGuard."""

import pytest
from baobab_auth_core.domain.entities.permission import Permission
from baobab_auth_core.domain.value_objects.permission_id import PermissionId
from baobab_auth_core.domain.value_objects.permission_name import PermissionName
from sqlalchemy.orm import Session

from baobab_auth_database.exceptions.persistence import AuthDatabasePersistenceError
from baobab_auth_database.repositories.sqlalchemy_permission_repository import (
    SqlAlchemyPermissionRepository,
)
from baobab_auth_database.repositories.sqlalchemy_persistence_guard import (
    SqlAlchemyPersistenceGuard,
)


class TestSqlAlchemyPersistenceGuard:
    """Tests FEAT-003.1 — garde d'intégrité."""

    def _permission(self, now_utc, *, perm_id: str = "p1") -> Permission:
        return Permission(
            id=PermissionId(perm_id),
            name=PermissionName("auth:user:read"),
            resource="user",
            action="read",
            is_system=True,
            created_at=now_utc,
        )

    def test_FEAT_003_1_flush_ok(self, db_session: Session, now_utc) -> None:
        SqlAlchemyPermissionRepository(db_session).save(self._permission(now_utc))
        SqlAlchemyPersistenceGuard.flush(db_session)

    def test_FEAT_003_1_integrity_encapsule(self, db_session: Session, now_utc) -> None:
        repo = SqlAlchemyPermissionRepository(db_session)
        repo.save(self._permission(now_utc))
        with pytest.raises(AuthDatabasePersistenceError) as exc_info:
            repo.save(self._permission(now_utc, perm_id="p2"))
        assert exc_info.value.cause is not None
