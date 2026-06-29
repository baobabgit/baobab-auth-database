"""Tests SqlAlchemyPermissionRepository."""

import pytest
from baobab_auth_core.domain.entities.permission import Permission
from baobab_auth_core.domain.value_objects.permission_id import PermissionId
from baobab_auth_core.domain.value_objects.permission_name import PermissionName
from sqlalchemy.orm import Session

from baobab_auth_database.exceptions.persistence import AuthDatabasePersistenceError
from baobab_auth_database.repositories.sqlalchemy_permission_repository import (
    SqlAlchemyPermissionRepository,
)


class TestSqlAlchemyPermissionRepository:
    """Tests FEAT-003.1 — repository permission."""

    def _permission(self, now_utc, *, perm_id: str = "p1") -> Permission:
        return Permission(
            id=PermissionId(perm_id),
            name=PermissionName("auth:user:read"),
            resource="user",
            action="read",
            is_system=True,
            created_at=now_utc,
        )

    def test_FEAT_003_1_roundtrip_permission(
        self, db_session: Session, now_utc
    ) -> None:
        repo = SqlAlchemyPermissionRepository(db_session)
        perm = self._permission(now_utc)
        repo.save(perm)
        restored = repo.get_by_id(perm.id)
        assert restored is not None
        assert restored.name == perm.name
        assert restored.resource == perm.resource
        assert repo.get_by_name(perm.name) == restored
        assert len(repo.list_permissions()) == 1

    def test_FEAT_003_1_unicite_permission(self, db_session: Session, now_utc) -> None:
        repo = SqlAlchemyPermissionRepository(db_session)
        repo.save(self._permission(now_utc))
        duplicate = self._permission(now_utc, perm_id="p2")
        with pytest.raises(AuthDatabasePersistenceError):
            repo.save(duplicate)
