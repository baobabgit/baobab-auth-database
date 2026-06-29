"""Tests AuthDatabaseCli."""

from pathlib import Path

import pytest
from pydantic import SecretStr

from baobab_auth_database.catalog.auth_catalog_seed_result import AuthCatalogSeedResult
from baobab_auth_database.cli.auth_database_cli import AuthDatabaseCli
from baobab_auth_database.settings.auth_database_settings import AuthDatabaseSettings


class _RecordingMigrator:
    """Migrateur factice enregistrant les appels."""

    def __init__(self) -> None:
        self.upgraded = False
        self.downgraded = False
        self.current: str | None = "0001"
        self.history: tuple[str, ...] = ("0001",)

    def upgrade_head(self) -> None:
        self.upgraded = True

    def downgrade_base(self) -> None:
        self.downgraded = True

    def current_revision(self) -> str | None:
        return self.current

    def history_ids(self) -> tuple[str, ...]:
        return self.history


class _RecordingBootstrap:
    """Bootstrap factice enregistrant les exécutions."""

    def __init__(self) -> None:
        self.runs = 0

    def run(self, *, dry_run: bool = False) -> AuthCatalogSeedResult:
        self.runs += 1
        return AuthCatalogSeedResult(
            permissions_added=0,
            roles_added=0,
            roles_resynced=0,
            dry_run=dry_run,
            version_recorded=not dry_run,
        )


class TestAuthDatabaseCli:
    """Tests FEAT-005.1 — CLI migrations et bootstrap."""

    @pytest.fixture
    def sqlite_settings(self, tmp_path: Path) -> AuthDatabaseSettings:
        db_file = tmp_path / "cli.db"
        return AuthDatabaseSettings(
            database_url=SecretStr(f"sqlite:///{db_file.as_posix()}"),
        )

    def test_FEAT_005_1_upgrade_command(
        self, sqlite_settings: AuthDatabaseSettings
    ) -> None:
        migrator = _RecordingMigrator()
        cli = AuthDatabaseCli(
            settings=sqlite_settings,
            migrator_factory=lambda _settings: migrator,
        )
        assert cli.run(["upgrade"]) == 0
        assert migrator.upgraded is True

    def test_FEAT_005_1_downgrade_command(
        self, sqlite_settings: AuthDatabaseSettings
    ) -> None:
        migrator = _RecordingMigrator()
        cli = AuthDatabaseCli(
            settings=sqlite_settings,
            migrator_factory=lambda _settings: migrator,
        )
        assert cli.run(["downgrade"]) == 0
        assert migrator.downgraded is True

    def test_FEAT_005_1_current_command(
        self, sqlite_settings: AuthDatabaseSettings, capsys: pytest.CaptureFixture[str]
    ) -> None:
        migrator = _RecordingMigrator()
        cli = AuthDatabaseCli(
            settings=sqlite_settings,
            migrator_factory=lambda _settings: migrator,
        )
        assert cli.run(["current"]) == 0
        assert capsys.readouterr().out.strip() == "0001"

    def test_FEAT_005_1_current_base_when_empty(
        self, sqlite_settings: AuthDatabaseSettings, capsys: pytest.CaptureFixture[str]
    ) -> None:
        migrator = _RecordingMigrator()
        migrator.current = None
        cli = AuthDatabaseCli(
            settings=sqlite_settings,
            migrator_factory=lambda _settings: migrator,
        )
        assert cli.run(["current"]) == 0
        assert capsys.readouterr().out.strip() == "base"

    def test_FEAT_005_1_history_command(
        self, sqlite_settings: AuthDatabaseSettings, capsys: pytest.CaptureFixture[str]
    ) -> None:
        migrator = _RecordingMigrator()
        cli = AuthDatabaseCli(
            settings=sqlite_settings,
            migrator_factory=lambda _settings: migrator,
        )
        assert cli.run(["history"]) == 0
        assert capsys.readouterr().out.strip() == "0001"

    def test_FEAT_005_1_bootstrap_command(
        self, sqlite_settings: AuthDatabaseSettings
    ) -> None:
        bootstrap = _RecordingBootstrap()
        cli = AuthDatabaseCli(
            settings=sqlite_settings,
            bootstrap_factory=lambda _settings: bootstrap,
        )
        assert cli.run(["bootstrap"]) == 0
        assert bootstrap.runs == 1

    def test_FEAT_006_5_catalog_check_exit_codes(
        self, sqlite_settings: AuthDatabaseSettings
    ) -> None:
        from baobab_auth_database.migrations.auth_database_migrator import (
            AuthDatabaseMigrator,
        )

        AuthDatabaseMigrator(sqlite_settings).upgrade_head()
        cli = AuthDatabaseCli(settings=sqlite_settings)
        assert cli.run(["catalog", "check"]) == 1

    def test_FEAT_006_5_unknown_profile_raises(
        self, sqlite_settings: AuthDatabaseSettings
    ) -> None:
        cli = AuthDatabaseCli(settings=sqlite_settings)
        with pytest.raises(ValueError, match="Profil inconnu"):
            cli.run(["catalog", "check", "--profile", "core_999"])

    def test_FEAT_005_1_no_command_returns_error(
        self, sqlite_settings: AuthDatabaseSettings
    ) -> None:
        cli = AuthDatabaseCli(settings=sqlite_settings)
        assert cli.run([]) == 1
