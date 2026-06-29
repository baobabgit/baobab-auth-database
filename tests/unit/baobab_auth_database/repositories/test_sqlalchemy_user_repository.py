"""Tests SqlAlchemyUserRepository."""

from datetime import datetime

import pytest
from baobab_auth_core.domain.entities.role import Role
from baobab_auth_core.domain.entities.user import User
from baobab_auth_core.domain.enums.user_status import UserStatus
from baobab_auth_core.domain.value_objects.auth_subject import AuthSubject
from baobab_auth_core.domain.value_objects.email import Email
from baobab_auth_core.domain.value_objects.password_hash import PasswordHash
from baobab_auth_core.domain.value_objects.role_id import RoleId
from baobab_auth_core.domain.value_objects.role_name import RoleName
from baobab_auth_core.domain.value_objects.user_id import UserId
from sqlalchemy.orm import Session

from baobab_auth_database.exceptions.persistence import AuthDatabasePersistenceError
from baobab_auth_database.repositories.sqlalchemy_role_repository import (
    SqlAlchemyRoleRepository,
)
from baobab_auth_database.repositories.sqlalchemy_user_repository import (
    SqlAlchemyUserRepository,
)


class TestSqlAlchemyUserRepository:
    """Tests FEAT-003.1 — repository utilisateur."""

    def _role(self, now_utc: datetime) -> Role:
        return Role(
            id=RoleId("role-user"),
            name=RoleName("USER"),
            is_system=True,
            created_at=now_utc,
            updated_at=now_utc,
            permission_names=(),
        )

    def _user(
        self,
        now_utc: datetime,
        *,
        user_id: str = "user-1",
        email: str = "alice@example.com",
        subject: str = "sub-1",
    ) -> User:
        return User(
            id=UserId(user_id),
            auth_subject=AuthSubject(subject),
            email=Email(email),
            password_hash=PasswordHash("hash"),
            status=UserStatus.ACTIVE,
            role_names=(RoleName("USER"),),
            created_at=now_utc,
            updated_at=now_utc,
        )

    def test_FEAT_003_1_roundtrip_user(
        self, db_session: Session, now_utc: datetime
    ) -> None:
        SqlAlchemyRoleRepository(db_session).save(self._role(now_utc))
        repo = SqlAlchemyUserRepository(db_session)
        user = self._user(now_utc)
        repo.save(user)
        restored = repo.get_by_id(user.id)
        assert restored is not None
        assert restored.id == user.id
        assert restored.email == user.email
        assert restored.auth_subject == user.auth_subject
        assert restored.role_names == user.role_names
        assert repo.get_by_email(user.email) == restored
        assert repo.get_by_auth_subject(user.auth_subject) == restored
        assert repo.exists_by_email(user.email) is True

    def test_FEAT_003_1_unicite_email(
        self, db_session: Session, now_utc: datetime
    ) -> None:
        SqlAlchemyRoleRepository(db_session).save(self._role(now_utc))
        repo = SqlAlchemyUserRepository(db_session)
        repo.save(self._user(now_utc))
        duplicate = self._user(
            now_utc,
            user_id="user-2",
            email="alice@example.com",
            subject="sub-2",
        )
        with pytest.raises(AuthDatabasePersistenceError):
            repo.save(duplicate)

    def test_FEAT_003_1_unicite_subject(
        self, db_session: Session, now_utc: datetime
    ) -> None:
        SqlAlchemyRoleRepository(db_session).save(self._role(now_utc))
        repo = SqlAlchemyUserRepository(db_session)
        repo.save(self._user(now_utc))
        duplicate = self._user(
            now_utc,
            user_id="user-2",
            email="bob@example.com",
            subject="sub-1",
        )
        with pytest.raises(AuthDatabasePersistenceError):
            repo.save(duplicate)

    def test_FEAT_003_1_delete_user(
        self, db_session: Session, now_utc: datetime
    ) -> None:
        SqlAlchemyRoleRepository(db_session).save(self._role(now_utc))
        repo = SqlAlchemyUserRepository(db_session)
        user = self._user(now_utc)
        repo.save(user)
        repo.delete(user.id)
        assert repo.get_by_id(user.id) is None
