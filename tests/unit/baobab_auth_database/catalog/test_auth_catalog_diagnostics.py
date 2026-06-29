"""Tests AuthCatalogDiagnostics."""

from datetime import UTC, datetime
from pathlib import Path

import pytest
from baobab_auth_core.domain.catalogs.default_auth_catalog import DefaultAuthCatalog
from baobab_auth_core.domain.entities.permission import Permission
from baobab_auth_core.domain.value_objects.permission_id import PermissionId
from baobab_auth_core.domain.value_objects.permission_name import PermissionName
from baobab_auth_core.domain.value_objects.role_name import RoleName
from pydantic import SecretStr

from baobab_auth_database.bootstrap.auth_catalog_bootstrap import AuthCatalogBootstrap
from baobab_auth_database.catalog.auth_catalog_diagnostics import AuthCatalogDiagnostics
from baobab_auth_database.factories.sqlalchemy_session_factory import (
    SqlAlchemySessionFactory,
)
from baobab_auth_database.migrations.auth_database_migrator import AuthDatabaseMigrator
from baobab_auth_database.settings.auth_database_settings import AuthDatabaseSettings
from baobab_auth_database.unit_of_work.sqlalchemy_auth_unit_of_work import (
    SqlAlchemyAuthUnitOfWork,
)


@pytest.fixture
def migrated_session_factory(tmp_path: Path) -> SqlAlchemySessionFactory:
    db_file = tmp_path / "catalog_diag.db"
    settings = AuthDatabaseSettings(
        database_url=SecretStr(f"sqlite:///{db_file.as_posix()}"),
    )
    AuthDatabaseMigrator(settings).upgrade_head()
    return SqlAlchemySessionFactory(settings)


class TestAuthCatalogDiagnostics:
    """Tests FEAT-006.3 — diagnostics catalogue."""

    def test_FEAT_006_3_conform_after_seed(
        self, migrated_session_factory: SqlAlchemySessionFactory
    ) -> None:
        AuthCatalogBootstrap(migrated_session_factory).run()
        session = migrated_session_factory.create()
        try:
            report = AuthCatalogDiagnostics(session).run()
        finally:
            session.close()
        assert report.is_conform is True
        assert report.missing_permissions == ()
        assert report.obsolete_permissions == ()

    def test_FEAT_006_3_divergent_on_empty_base(
        self, migrated_session_factory: SqlAlchemySessionFactory
    ) -> None:
        session = migrated_session_factory.create()
        try:
            report = AuthCatalogDiagnostics(session).run()
        finally:
            session.close()
        assert report.is_conform is False
        assert report.missing_permissions

    def test_FEAT_006_3_detects_obsolete_permission(
        self, migrated_session_factory: SqlAlchemySessionFactory
    ) -> None:
        AuthCatalogBootstrap(migrated_session_factory).run()
        obsolete = Permission(
            id=PermissionId("perm-auth-permission-read"),
            name=PermissionName("auth:permission:read"),
            resource="permission",
            action="read",
            is_system=True,
            created_at=datetime(2024, 1, 1, tzinfo=UTC),
            description="Permission obsolète.",
        )
        with SqlAlchemyAuthUnitOfWork(migrated_session_factory) as uow:
            uow.permissions.save(obsolete)
            uow.commit()

        session = migrated_session_factory.create()
        try:
            report = AuthCatalogDiagnostics(session).run()
        finally:
            session.close()
        assert "auth:permission:read" in report.obsolete_permissions
        assert report.is_conform is False

    def test_FEAT_006_3_service_has_no_permissions(
        self, migrated_session_factory: SqlAlchemySessionFactory
    ) -> None:
        AuthCatalogBootstrap(migrated_session_factory).run()
        with SqlAlchemyAuthUnitOfWork(migrated_session_factory) as uow:
            service = uow.roles.get_by_name(RoleName("SERVICE"))
            assert service is not None
            assert service.permission_names == ()

    def test_FEAT_006_3_super_admin_has_all_permissions(
        self, migrated_session_factory: SqlAlchemySessionFactory
    ) -> None:
        AuthCatalogBootstrap(migrated_session_factory).run()
        catalog = DefaultAuthCatalog()
        expected = {str(permission.name) for permission in catalog.permissions()}
        with SqlAlchemyAuthUnitOfWork(migrated_session_factory) as uow:
            super_admin = uow.roles.get_by_name(RoleName("SUPER_ADMIN"))
            assert super_admin is not None
            actual = {str(name) for name in super_admin.permission_names}
            assert actual == expected
