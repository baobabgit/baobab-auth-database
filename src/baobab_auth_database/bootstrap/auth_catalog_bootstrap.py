"""Seed idempotent des rôles et permissions système.

:spec: FEAT-005.2
"""

from baobab_auth_core.domain.catalogs.default_auth_catalog import DefaultAuthCatalog

from baobab_auth_database.factories.sqlalchemy_session_factory import (
    SqlAlchemySessionFactory,
)
from baobab_auth_database.unit_of_work.sqlalchemy_auth_unit_of_work import (
    SqlAlchemyAuthUnitOfWork,
)


class AuthCatalogBootstrap:
    """Insère le catalogue ``DefaultAuthCatalog`` sans doublon.

    :param session_factory: Factory SQLAlchemy pour ouvrir l'UoW.
    :param catalog: Catalogue core injectable (tests) ; défaut si omis.
    :spec: FEAT-005.2
    """

    def __init__(
        self,
        session_factory: SqlAlchemySessionFactory,
        catalog: DefaultAuthCatalog | None = None,
    ) -> None:
        """Initialise le bootstrap catalogue.

        :param session_factory: Factory de sessions partagée avec l'UoW.
        :param catalog: Instance ``DefaultAuthCatalog`` ; créée si omise.
        """
        self._session_factory = session_factory
        self._catalog = catalog or DefaultAuthCatalog()

    def run(self) -> None:
        """Persiste permissions et rôles système de façon idempotente.

        :raises AuthDatabasePersistenceError: En cas de violation d'intégrité.
        """
        with SqlAlchemyAuthUnitOfWork(self._session_factory) as uow:
            for permission in self._catalog.permissions():
                if uow.permissions.get_by_name(permission.name) is None:
                    uow.permissions.save(permission)
            for role in self._catalog.roles():
                if uow.roles.get_by_name(role.name) is None:
                    uow.roles.save(role)
            uow.commit()
