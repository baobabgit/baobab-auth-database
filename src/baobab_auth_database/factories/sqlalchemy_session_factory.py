"""Factory SQLAlchemy session.

:spec: FEAT-001.2
"""

from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker

from baobab_auth_database.factories.sqlalchemy_engine_factory import (
    SqlAlchemyEngineFactory,
)
from baobab_auth_database.settings.auth_database_settings import AuthDatabaseSettings


class SqlAlchemySessionFactory:
    """Produit des sessions SQLAlchemy liées à un engine.

    :param settings: Configuration injectée (utilisée si aucun engine n'est fourni).
    :param engine: Engine existant (optionnel).
    :spec: FEAT-001.2
    """

    def __init__(
        self,
        settings: AuthDatabaseSettings,
        engine: Engine | None = None,
    ) -> None:
        """Initialise la factory de sessions.

        :param settings: Paramètres de connexion.
        :param engine: Engine SQLAlchemy optionnel.
        """
        self._settings = settings
        self._engine = engine or SqlAlchemyEngineFactory(settings).create()
        self._session_maker = sessionmaker(
            bind=self._engine,
            autocommit=False,
            autoflush=False,
            expire_on_commit=False,
        )

    @property
    def engine(self) -> Engine:
        """Engine sous-jacent.

        :returns: Engine SQLAlchemy.
        """
        return self._engine

    def create(self) -> Session:
        """Ouvre une nouvelle session.

        :returns: Session SQLAlchemy.
        """
        return self._session_maker()
