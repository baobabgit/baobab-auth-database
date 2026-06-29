"""Factory de configuration Alembic embarquée.

:spec: FEAT-002.2
"""

from pathlib import Path

from alembic.config import Config

from baobab_auth_database.settings.auth_database_settings import AuthDatabaseSettings


class AlembicConfigFactory:
    """Construit un ``alembic.config.Config`` pour ce package.

    :param settings: Paramètres de connexion injectés.
    :spec: FEAT-002.2
    """

    def __init__(self, settings: AuthDatabaseSettings) -> None:
        """Initialise la factory.

        :param settings: Configuration de la base de données.
        """
        self._settings = settings
        self._migrations_dir = Path(__file__).resolve().parent

    def create(self) -> Config:
        """Produit la configuration Alembic prête à l'emploi.

        :returns: Instance ``Config`` pointant vers ``migrations/``.
        """
        config = Config()
        config.set_main_option("script_location", str(self._migrations_dir))
        config.set_main_option(
            "sqlalchemy.url",
            self._settings.resolved_database_url(),
        )
        return config

    @property
    def migrations_dir(self) -> Path:
        """Répertoire des scripts de migration.

        :returns: Chemin absolu du dossier ``migrations/``.
        """
        return self._migrations_dir
