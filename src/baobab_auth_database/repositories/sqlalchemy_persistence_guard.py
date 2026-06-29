"""Exécution sécurisée des opérations SQLAlchemy.

:spec: FEAT-003.1
"""

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from baobab_auth_database.exceptions.persistence import AuthDatabasePersistenceError


class SqlAlchemyPersistenceGuard:
    """Transforme les ``IntegrityError`` en erreurs database contrôlées.

    :spec: FEAT-003.1
    """

    @staticmethod
    def flush(session: Session) -> None:
        """Exécute ``session.flush()`` en encapsulant les violations d'intégrité.

        :param session: Session SQLAlchemy active.
        :raises AuthDatabasePersistenceError: Si une contrainte est violée.
        """
        try:
            session.flush()
        except IntegrityError as exc:
            msg = "Contrainte de persistance violée."
            raise AuthDatabasePersistenceError(msg, cause=exc) from exc
