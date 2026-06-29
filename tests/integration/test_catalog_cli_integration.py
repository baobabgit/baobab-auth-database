"""Tests intégration catalogue v0.2.0."""

import json
from pathlib import Path

import pytest
from pydantic import SecretStr

from baobab_auth_database.cli.auth_database_cli import AuthDatabaseCli
from baobab_auth_database.migrations.auth_database_migrator import AuthDatabaseMigrator
from baobab_auth_database.settings.auth_database_settings import AuthDatabaseSettings


class TestCatalogCliIntegration:
    """Intégration FEAT-006.5 — CLI catalogue sur SQLite migré."""

    def test_FEAT_006_5_catalog_workflow(
        self, tmp_path: Path, capsys: pytest.CaptureFixture[str]
    ) -> None:
        db_file = tmp_path / "catalog_cli.db"
        settings = AuthDatabaseSettings(
            database_url=SecretStr(f"sqlite:///{db_file.as_posix()}"),
        )
        AuthDatabaseMigrator(settings).upgrade_head()
        cli = AuthDatabaseCli(settings=settings)

        assert cli.run(["catalog", "check"]) == 1
        capsys.readouterr()

        assert cli.run(["catalog", "seed"]) == 0
        capsys.readouterr()
        assert cli.run(["catalog", "check"]) == 0
        capsys.readouterr()

        assert cli.run(["catalog", "report", "--format", "json"]) == 0
        payload = json.loads(capsys.readouterr().out.strip())
        assert payload["conform"] is True

        assert cli.run(["catalog", "seed", "--dry-run"]) == 0
