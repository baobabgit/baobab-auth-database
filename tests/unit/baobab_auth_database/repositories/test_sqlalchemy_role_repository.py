"""Tests SqlAlchemyRoleRepository."""

from datetime import datetime

import pytest
from baobab_auth_core.domain.entities.permission import Permission
from baobab_auth_core.domain.entities.role import Role
from baobab_auth_core.domain.entities.user import User
from baobab_auth_core.domain.enums.user_status import UserStatus
from baobab_auth_core.domain.value_objects.auth_subject import AuthSubject
from baobab_auth_core.domain.value_objects.email import Email
from baobab_auth_core.domain.value_objects.password_hash import PasswordHash
from baobab_auth_core.domain.value_objects.permission_id import PermissionId
from baobab_auth_core.domain.value_objects.permission_name import PermissionName
from baobab_auth_core.domain.value_objects.role_id import RoleId
from baobab_auth_core.domain.value_objects.role_name import RoleName
from baobab_auth_core.domain.value_objects.user_id import UserId
from sqlalchemy.orm import Session

from baobab_auth_database.exceptions.persistence import AuthDatabasePersistenceError
from baobab_auth_database.repositories.sqlalchemy_permission_repository import (
    SqlAlchemyPermissionRepository,
)
from baobab_auth_database.repositories.sqlalchemy_role_repository import (
    SqlAlchemyRoleRepository,
)
from baobab_auth_database.repositories.sqlalchemy_user_repository import (
    SqlAlchemyUserRepository,
)


class TestSqlAlchemyRoleRepository:
    """Tests FEAT-003.1 — repository rôle."""

    def _permission(self, now_utc: datetime) -> Permission:
        return Permission(
            id=PermissionId("perm-1"),
            name=PermissionName("auth:user:read"),
            resource="user",
            action="read",
            is_system=True,
            created_at=now_utc,
        )

    def _role(self, now_utc: datetime) -> Role:
        return Role(
            id=RoleId("role-1"),
            name=RoleName("ADMIN"),
            is_system=True,
            created_at=now_utc,
            updated_at=now_utc,
            permission_names=(PermissionName("auth:user:read"),),
        )

    def test_FEAT_003_1_roundtrip_role(
        self, db_session: Session, now_utc: datetime
    ) -> None:
        SqlAlchemyPermissionRepository(db_session).save(self._permission(now_utc))
        repo = SqlAlchemyRoleRepository(db_session)
        role = self._role(now_utc)
        repo.save(role)
        restored = repo.get_by_id(role.id)
        assert restored is not None
        assert restored.name == role.name
        assert restored.permission_names == role.permission_names
        assert repo.get_by_name(role.name) == restored
        assert len(repo.list_all()) == 1

    def test_FEAT_003_1_unicite_role(
        self, db_session: Session, now_utc: datetime
    ) -> None:
        repo = SqlAlchemyRoleRepository(db_session)
        repo.save(self._role(now_utc))
        duplicate = Role(
            id=RoleId("role-2"),
            name=RoleName("ADMIN"),
            is_system=False,
            created_at=now_utc,
            updated_at=now_utc,
            permission_names=(),
        )
        with pytest.raises(AuthDatabasePersistenceError):
            repo.save(duplicate)

    def test_FEAT_003_1_count_users_with_role(
        self, db_session: Session, now_utc: datetime
    ) -> None:
        SqlAlchemyRoleRepository(db_session).save(
            Role(
                id=RoleId("role-user"),
                name=RoleName("USER"),
                is_system=True,
                created_at=now_utc,
                updated_at=now_utc,
                permission_names=(),
            )
        )
        role_repo = SqlAlchemyRoleRepository(db_session)
        user_repo = SqlAlchemyUserRepository(db_session)
        user_repo.save(
            User(
                id=UserId("user-1"),
                auth_subject=AuthSubject("sub-1"),
                email=Email("alice@example.com"),
                password_hash=PasswordHash("hash"),
                status=UserStatus.ACTIVE,
                role_names=(RoleName("USER"),),
                created_at=now_utc,
                updated_at=now_utc,
            )
        )
        assert role_repo.count_users_with_role(RoleName("USER")) == 1
