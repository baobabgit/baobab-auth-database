"""Tests SqlAlchemyAuthUnitOfWork."""

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
from baobab_auth_core.ports.unit_of_work import UnitOfWork
from sqlalchemy.engine import Engine

from baobab_auth_database.factories.sqlalchemy_session_factory import (
    SqlAlchemySessionFactory,
)
from baobab_auth_database.repositories.sqlalchemy_audit_repository import (
    SqlAlchemyAuditRepository,
)
from baobab_auth_database.repositories.sqlalchemy_jwk_key_repository import (
    SqlAlchemyJwkKeyRepository,
)
from baobab_auth_database.repositories.sqlalchemy_permission_repository import (
    SqlAlchemyPermissionRepository,
)
from baobab_auth_database.repositories.sqlalchemy_role_repository import (
    SqlAlchemyRoleRepository,
)
from baobab_auth_database.repositories.sqlalchemy_session_repository import (
    SqlAlchemySessionRepository,
)
from baobab_auth_database.repositories.sqlalchemy_user_profile_repository import (
    SqlAlchemyUserProfileRepository,
)
from baobab_auth_database.repositories.sqlalchemy_user_repository import (
    SqlAlchemyUserRepository,
)
from baobab_auth_database.settings.auth_database_settings import AuthDatabaseSettings
from baobab_auth_database.unit_of_work.sqlalchemy_auth_unit_of_work import (
    SqlAlchemyAuthUnitOfWork,
)


@pytest.fixture
def session_factory(sqlite_engine: Engine) -> SqlAlchemySessionFactory:
    """Factory de sessions SQLite mémoire pour les tests UoW.

    :param sqlite_engine: Engine avec schéma auth créé.
    :returns: Factory prête pour ``SqlAlchemyAuthUnitOfWork``.
    """
    settings = AuthDatabaseSettings()
    return SqlAlchemySessionFactory(settings, engine=sqlite_engine)


class TestSqlAlchemyAuthUnitOfWork:
    """Tests FEAT-003.2 — unit of work synchrone."""

    def _role(self, now_utc: datetime) -> Role:
        return Role(
            id=RoleId("role-user"),
            name=RoleName("USER"),
            is_system=True,
            created_at=now_utc,
            updated_at=now_utc,
            permission_names=(),
        )

    def _user(self, now_utc: datetime) -> User:
        return User(
            id=UserId("user-uow-1"),
            auth_subject=AuthSubject("sub-uow-1"),
            email=Email("uow@example.com"),
            password_hash=PasswordHash("hash"),
            status=UserStatus.ACTIVE,
            role_names=(RoleName("USER"),),
            created_at=now_utc,
            updated_at=now_utc,
        )

    def test_FEAT_003_2_satisfies_unit_of_work_protocol(
        self, session_factory: SqlAlchemySessionFactory
    ) -> None:
        """La classe implémente le protocole ``UnitOfWork`` du core."""
        uow = SqlAlchemyAuthUnitOfWork(session_factory)
        with uow:
            assert isinstance(uow, UnitOfWork)

    def test_FEAT_003_2_exposes_all_repositories(
        self, session_factory: SqlAlchemySessionFactory
    ) -> None:
        """Expose users, profiles, roles, permissions, sessions, audit, jwk_keys."""
        with SqlAlchemyAuthUnitOfWork(session_factory) as uow:
            assert isinstance(uow.users, SqlAlchemyUserRepository)
            assert isinstance(uow.profiles, SqlAlchemyUserProfileRepository)
            assert isinstance(uow.roles, SqlAlchemyRoleRepository)
            assert isinstance(uow.permissions, SqlAlchemyPermissionRepository)
            assert isinstance(uow.sessions, SqlAlchemySessionRepository)
            assert isinstance(uow.audit, SqlAlchemyAuditRepository)
            assert isinstance(uow.jwk_keys, SqlAlchemyJwkKeyRepository)

    def test_FEAT_003_2_repositories_share_session(
        self, session_factory: SqlAlchemySessionFactory
    ) -> None:
        """Les repositories lazy partagent la même session SQLAlchemy."""
        with SqlAlchemyAuthUnitOfWork(session_factory) as uow:
            assert uow.users._session is uow.roles._session
            assert uow.users._session is uow.profiles._session

    def test_FEAT_003_2_commit_persists_changes(
        self, session_factory: SqlAlchemySessionFactory, now_utc: datetime
    ) -> None:
        """``commit`` valide les écritures pour une nouvelle unité de travail."""
        role = self._role(now_utc)
        user = self._user(now_utc)

        with SqlAlchemyAuthUnitOfWork(session_factory) as uow:
            uow.roles.save(role)
            uow.users.save(user)
            uow.commit()

        with SqlAlchemyAuthUnitOfWork(session_factory) as uow:
            loaded = uow.users.get_by_id(user.id)
            assert loaded is not None
            assert loaded.email.value == user.email.value

    def test_FEAT_003_2_rollback_discards_uncommitted_changes(
        self, session_factory: SqlAlchemySessionFactory, now_utc: datetime
    ) -> None:
        """``rollback`` annule les écritures non validées."""
        role = self._role(now_utc)
        user = self._user(now_utc)

        with SqlAlchemyAuthUnitOfWork(session_factory) as uow:
            uow.roles.save(role)
            uow.users.save(user)
            uow.rollback()

        with SqlAlchemyAuthUnitOfWork(session_factory) as uow:
            assert uow.users.get_by_id(user.id) is None

    def test_FEAT_003_2_exit_on_exception_rolls_back(
        self, session_factory: SqlAlchemySessionFactory, now_utc: datetime
    ) -> None:
        """Une exception dans le contexte déclenche un rollback implicite."""
        role = self._role(now_utc)
        user = self._user(now_utc)

        with pytest.raises(RuntimeError, match="boom"):
            with SqlAlchemyAuthUnitOfWork(session_factory) as uow:
                uow.roles.save(role)
                uow.users.save(user)
                raise RuntimeError("boom")

        with SqlAlchemyAuthUnitOfWork(session_factory) as uow:
            assert uow.users.get_by_id(user.id) is None

    def test_FEAT_003_2_requires_active_context_for_repositories(
        self, session_factory: SqlAlchemySessionFactory
    ) -> None:
        """Accéder aux repositories hors contexte lève ``RuntimeError``."""
        uow = SqlAlchemyAuthUnitOfWork(session_factory)
        with pytest.raises(RuntimeError, match="not active"):
            _ = uow.users
