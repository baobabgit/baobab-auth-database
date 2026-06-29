"""Exécution programmatique des migrations Alembic.

:spec: FEAT-002.2
"""

from alembic import command
from alembic.config import Config
from alembic.runtime.migration import MigrationContext
from alembic.script import ScriptDirectory
from sqlalchemy.engine import Engine

from baobab_auth_database.factories.sqlalchemy_engine_factory import (
    SqlAlchemyEngineFactory,
)
from baobab_auth_database.migrations.alembic_config_factory import AlembicConfigFactory
from baobab_auth_database.settings.auth_database_settings import AuthDatabaseSettings


class AuthDatabaseMigrator:
    """Applique ou annule les migrations sur une base cible.

    :param settings: Configuration injectée.
    :param config: Configuration Alembic optionnelle (sinon créée depuis settings).
    :spec: FEAT-002.2
    """

    def __init__(
        self,
        settings: AuthDatabaseSettings,
        config: Config | None = None,
    ) -> None:
        """Initialise le migrateur.

        :param settings: Paramètres de connexion.
        :param config: Configuration Alembic pré-construite.
        """
        self._settings = settings
        self._config = config or AlembicConfigFactory(settings).create()
        self._engine_factory = SqlAlchemyEngineFactory(settings)

    @property
    def config(self) -> Config:
        """Configuration Alembic active.

        :returns: Instance ``Config``.
        """
        return self._config

    def upgrade_head(self) -> None:
        """Applique toutes les migrations jusqu'à ``head``.

        :raises Exception: En cas d'échec Alembic.
        """
        command.upgrade(self._config, "head")

    def downgrade_base(self) -> None:
        """Annule toutes les migrations (retour à ``base``).

        :raises Exception: En cas d'échec Alembic.
        """
        command.downgrade(self._config, "base")

    def current_revision(self) -> str | None:
        """Retourne la révision courante de la base.

        :returns: Identifiant de révision ou ``None`` si base vierge.
        """
        engine = self._engine_factory.create()
        try:
            with engine.connect() as connection:
                context = MigrationContext.configure(connection)
                return context.get_current_revision()
        finally:
            engine.dispose()

    def history_ids(self) -> tuple[str, ...]:
        """Liste les identifiants de révision dans l'ordre Alembic.

        :returns: Tuple des revision IDs connus.
        """
        script = ScriptDirectory.from_config(self._config)
        revisions = script.walk_revisions(base="base", head="head")
        return tuple(rev.revision for rev in reversed(list(revisions)))

    def create_engine(self) -> Engine:
        """Crée l'engine SQLAlchemy pour la base configurée.

        :returns: Engine SQLAlchemy.
        """
        return self._engine_factory.create()
