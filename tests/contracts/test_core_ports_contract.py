"""Harness contrat — ports core et API publique.

:spec: FEAT-006.1
"""

from pathlib import Path

import pytest
from baobab_auth_core.domain.catalogs.default_auth_catalog import DefaultAuthCatalog
from baobab_auth_core.ports.audit_repository import AuditRepository
from baobab_auth_core.ports.permission_repository import PermissionRepository
from baobab_auth_core.ports.role_repository import RoleRepository
from baobab_auth_core.ports.session_repository import SessionRepository
from baobab_auth_core.ports.unit_of_work import UnitOfWork
from baobab_auth_core.ports.user_repository import UserRepository
from pydantic import SecretStr

from baobab_auth_database.bootstrap.auth_catalog_bootstrap import AuthCatalogBootstrap
from baobab_auth_database.factories.sqlalchemy_session_factory import (
    SqlAlchemySessionFactory,
)
from baobab_auth_database.migrations.auth_database_migrator import AuthDatabaseMigrator
from baobab_auth_database.repositories.sqlalchemy_audit_repository import (
    SqlAlchemyAuditRepository,
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
from baobab_auth_database.repositories.sqlalchemy_user_repository import (
    SqlAlchemyUserRepository,
)
from baobab_auth_database.settings.auth_database_settings import AuthDatabaseSettings
from baobab_auth_database.unit_of_work.sqlalchemy_auth_unit_of_work import (
    SqlAlchemyAuthUnitOfWork,
)


@pytest.fixture
def migrated_session_factory(tmp_path: Path) -> SqlAlchemySessionFactory:
    """Factory SQLite migrée pour les tests contrat.

    :param tmp_path: Répertoire temporaire pytest.
    :returns: Factory prête pour UoW et bootstrap.
    """
    db_file = tmp_path / "contract.db"
    settings = AuthDatabaseSettings(
        database_url=SecretStr(f"sqlite:///{db_file.as_posix()}"),
    )
    AuthDatabaseMigrator(settings).upgrade_head()
    return SqlAlchemySessionFactory(settings)


class TestCorePortsContract:
    """Tests FEAT-006.1 — conformité aux ports ``baobab-auth-core`` 0.5.1."""

    def test_FEAT_006_1_repository_instances_satisfy_core_protocols(
        self, migrated_session_factory: SqlAlchemySessionFactory
    ) -> None:
        """Les instances repository satisfont les protocoles runtime du core."""
        session = migrated_session_factory.create()
        try:
            assert isinstance(SqlAlchemyUserRepository(session), UserRepository)
            assert isinstance(SqlAlchemyRoleRepository(session), RoleRepository)
            assert isinstance(
                SqlAlchemyPermissionRepository(session), PermissionRepository
            )
            assert isinstance(SqlAlchemySessionRepository(session), SessionRepository)
            assert isinstance(SqlAlchemyAuditRepository(session), AuditRepository)
        finally:
            session.close()

    def test_FEAT_006_1_uow_exposes_typed_repositories(
        self, migrated_session_factory: SqlAlchemySessionFactory
    ) -> None:
        """L'UoW expose des repositories conformes via le gestionnaire de contexte."""
        uow = SqlAlchemyAuthUnitOfWork(migrated_session_factory)
        assert isinstance(uow, UnitOfWork)
        with uow:
            assert isinstance(uow.users, UserRepository)
            assert isinstance(uow.roles, RoleRepository)
            assert isinstance(uow.permissions, PermissionRepository)
            assert isinstance(uow.sessions, SessionRepository)
            assert isinstance(uow.audit, AuditRepository)

    def test_FEAT_006_1_bootstrap_matches_default_auth_catalog(
        self, migrated_session_factory: SqlAlchemySessionFactory
    ) -> None:
        """Le bootstrap persiste le catalogue core sans doublon."""
        catalog = DefaultAuthCatalog()
        AuthCatalogBootstrap(migrated_session_factory, catalog=catalog).run()
        AuthCatalogBootstrap(migrated_session_factory, catalog=catalog).run()

        with SqlAlchemyAuthUnitOfWork(migrated_session_factory) as uow:
            assert len(uow.permissions.list_all()) == len(catalog.permissions())
            assert len(uow.roles.list_all()) == len(catalog.roles())
