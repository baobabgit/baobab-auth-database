"""Factory SQLAlchemy engine.

:spec: FEAT-001.2
"""

from sqlalchemy import Engine, create_engine
from sqlalchemy.pool import StaticPool

from baobab_auth_database.settings.auth_database_settings import AuthDatabaseSettings


class SqlAlchemyEngineFactory:
    """Crée un engine SQLAlchemy à partir de ``AuthDatabaseSettings``.

    :param settings: Configuration injectée.
    :spec: FEAT-001.2
    """

    def __init__(self, settings: AuthDatabaseSettings) -> None:
        """Initialise la factory.

        :param settings: Paramètres de connexion.
        """
        self._settings = settings

    def create(self) -> Engine:
        """Construit l'engine SQLAlchemy.

        :returns: Engine configuré selon les settings.
        """
        url = self._settings.resolved_database_url()
        kwargs: dict[str, object] = {
            "echo": self._settings.echo_sql,
        }
        if url.startswith("sqlite"):
            kwargs["connect_args"] = {"check_same_thread": False}
            if ":memory:" in url:
                kwargs["poolclass"] = StaticPool
        else:
            kwargs["pool_size"] = self._settings.pool_size
            kwargs["max_overflow"] = self._settings.max_overflow
        return create_engine(url, **kwargs)
