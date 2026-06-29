"""Unit of Work SQLAlchemy pour la persistance auth.

:spec: FEAT-003.2
"""

from types import TracebackType
from typing import Self

from sqlalchemy.orm import Session

from baobab_auth_database.factories.sqlalchemy_session_factory import (
    SqlAlchemySessionFactory,
)
from baobab_auth_database.repositories.sqlalchemy_audit_repository import (
    SqlAlchemyAuditRepository,
)
from baobab_auth_database.repositories.sqlalchemy_jwk_key_repository import (
    SqlAlchemyJwkKeyRepository,
)
from baobab_auth_database.repositories.sqlalchemy_permission_repository import (
    SqlAlchemyPermissionRepository,
)
from baobab_auth_database.repositories.sqlalchemy_role_repository import (
    SqlAlchemyRoleRepository,
)
from baobab_auth_database.repositories.sqlalchemy_session_repository import (
    SqlAlchemySessionRepository,
)
from baobab_auth_database.repositories.sqlalchemy_user_profile_repository import (
    SqlAlchemyUserProfileRepository,
)
from baobab_auth_database.repositories.sqlalchemy_user_repository import (
    SqlAlchemyUserRepository,
)


class SqlAlchemyAuthUnitOfWork:
    """Unité de travail synchrone exposant les repositories auth.

    :spec: FEAT-003.2
    """

    def __init__(self, session_factory: SqlAlchemySessionFactory) -> None:
        """Injecte la factory de sessions SQLAlchemy.

        :param session_factory: Factory partagée pour ouvrir la session UoW.
        """
        self._session_factory = session_factory
        self._session: Session | None = None
        self._users: SqlAlchemyUserRepository | None = None
        self._profiles: SqlAlchemyUserProfileRepository | None = None
        self._roles: SqlAlchemyRoleRepository | None = None
        self._permissions: SqlAlchemyPermissionRepository | None = None
        self._sessions: SqlAlchemySessionRepository | None = None
        self._audit: SqlAlchemyAuditRepository | None = None
        self._jwk_keys: SqlAlchemyJwkKeyRepository | None = None

    def __enter__(self) -> Self:
        """Ouvre une session SQLAlchemy dédiée à l'unité de travail.

        :returns: L'unité de travail active.
        """
        self._session = self._session_factory.create()
        self._reset_repositories()
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        """Ferme la session ; rollback automatique si une exception est propagée.

        :param exc_type: Type de l'exception (ou ``None``).
        :param exc_val: Valeur de l'exception (ou ``None``).
        :param exc_tb: Traceback de l'exception (ou ``None``).
        """
        try:
            if exc_type is not None:
                self.rollback()
        finally:
            if self._session is not None:
                self._session.close()
            self._session = None
            self._reset_repositories()

    def commit(self) -> None:
        """Valide la transaction courante sur la session active.

        :raises RuntimeError: Si la session n'est pas ouverte.
        """
        self._require_session().commit()

    def rollback(self) -> None:
        """Annule la transaction courante sur la session active.

        :raises RuntimeError: Si la session n'est pas ouverte.
        """
        self._require_session().rollback()

    @property
    def users(self) -> SqlAlchemyUserRepository:
        """Repository utilisateurs partageant la session UoW.

        :returns: Implémentation SQLAlchemy du port ``UserRepository``.
        :raises RuntimeError: Si la session n'est pas ouverte.
        """
        if self._users is None:
            self._users = SqlAlchemyUserRepository(self._require_session())
        return self._users

    @property
    def profiles(self) -> SqlAlchemyUserProfileRepository:
        """Repository profils utilisateur.

        :returns: Repository profils lié à la session UoW.
        :raises RuntimeError: Si la session n'est pas ouverte.
        """
        if self._profiles is None:
            self._profiles = SqlAlchemyUserProfileRepository(self._require_session())
        return self._profiles

    @property
    def roles(self) -> SqlAlchemyRoleRepository:
        """Repository rôles.

        :returns: Implémentation SQLAlchemy du port ``RoleRepository``.
        :raises RuntimeError: Si la session n'est pas ouverte.
        """
        if self._roles is None:
            self._roles = SqlAlchemyRoleRepository(self._require_session())
        return self._roles

    @property
    def permissions(self) -> SqlAlchemyPermissionRepository:
        """Repository permissions.

        :returns: Implémentation SQLAlchemy du port ``PermissionRepository``.
        :raises RuntimeError: Si la session n'est pas ouverte.
        """
        if self._permissions is None:
            self._permissions = SqlAlchemyPermissionRepository(self._require_session())
        return self._permissions

    @property
    def sessions(self) -> SqlAlchemySessionRepository:
        """Repository sessions auth.

        :returns: Implémentation SQLAlchemy du port ``SessionRepository``.
        :raises RuntimeError: Si la session n'est pas ouverte.
        """
        if self._sessions is None:
            self._sessions = SqlAlchemySessionRepository(self._require_session())
        return self._sessions

    @property
    def audit(self) -> SqlAlchemyAuditRepository:
        """Repository événements d'audit.

        :returns: Implémentation SQLAlchemy du port ``AuditRepository``.
        :raises RuntimeError: Si la session n'est pas ouverte.
        """
        if self._audit is None:
            self._audit = SqlAlchemyAuditRepository(self._require_session())
        return self._audit

    @property
    def jwk_keys(self) -> SqlAlchemyJwkKeyRepository:
        """Repository clés JWK (snapshot local).

        :returns: Repository JWK lié à la session UoW.
        :raises RuntimeError: Si la session n'est pas ouverte.
        """
        if self._jwk_keys is None:
            self._jwk_keys = SqlAlchemyJwkKeyRepository(self._require_session())
        return self._jwk_keys

    def _require_session(self) -> Session:
        """Retourne la session active ou lève une erreur explicite.

        :returns: Session SQLAlchemy ouverte par ``__enter__``.
        :raises RuntimeError: Si le gestionnaire de contexte n'est pas actif.
        """
        if self._session is None:
            msg = (
                "SqlAlchemyAuthUnitOfWork session is not active; "
                "use the unit of work as a context manager."
            )
            raise RuntimeError(msg)
        return self._session

    def _reset_repositories(self) -> None:
        """Réinitialise les repositories lazy après changement de session."""
        self._users = None
        self._profiles = None
        self._roles = None
        self._permissions = None
        self._sessions = None
        self._audit = None
        self._jwk_keys = None
