"""Tests AlembicConfigFactory."""

from baobab_auth_database.migrations.alembic_config_factory import AlembicConfigFactory
from baobab_auth_database.settings.auth_database_settings import AuthDatabaseSettings


class TestAlembicConfigFactory:
    """Tests FEAT-002.2 — factory Alembic."""

    def test_FEAT_002_2_create_config(self) -> None:
        settings = AuthDatabaseSettings()
        factory = AlembicConfigFactory(settings)
        config = factory.create()
        assert config.get_main_option("script_location") == str(factory.migrations_dir)
        assert (
            config.get_main_option("sqlalchemy.url") == settings.resolved_database_url()
        )

    def test_FEAT_002_2_migrations_dir(self) -> None:
        factory = AlembicConfigFactory(AuthDatabaseSettings())
        assert factory.migrations_dir.name == "migrations"
        assert (factory.migrations_dir / "env.py").is_file()
