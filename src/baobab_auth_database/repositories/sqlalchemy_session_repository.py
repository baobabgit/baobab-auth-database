"""Repository SQLAlchemy des sessions.

:spec: FEAT-003.1
"""

from baobab_auth_core.domain.entities.session import Session as AuthSession
from baobab_auth_core.domain.enums.session_status import SessionStatus
from baobab_auth_core.domain.value_objects.session_id import SessionId
from baobab_auth_core.domain.value_objects.token_id import TokenId
from baobab_auth_core.domain.value_objects.user_id import UserId
from sqlalchemy import select
from sqlalchemy.orm import Session

from baobab_auth_database.mappers.auth_session_orm_mapper import AuthSessionOrmMapper
from baobab_auth_database.models.orm.auth_session_model import AuthSessionModel
from baobab_auth_database.repositories.sqlalchemy_persistence_guard import (
    SqlAlchemyPersistenceGuard,
)


class SqlAlchemySessionRepository:
    """Implémentation synchrone du port ``SessionRepository``.

    :spec: FEAT-003.1
    """

    def __init__(
        self,
        session: Session,
        mapper: AuthSessionOrmMapper | None = None,
    ) -> None:
        """Injecte la session et le mapper.

        :param session: Session SQLAlchemy partagée.
        :param mapper: Mapper session ; instance par défaut si omis.
        """
        self._session = session
        self._mapper = mapper or AuthSessionOrmMapper()

    def get_by_id(self, session_id: SessionId) -> AuthSession | None:
        """Récupère une session par identifiant.

        :param session_id: Identifiant core.
        :returns: Entité ou ``None``.
        """
        model = self._session.get(AuthSessionModel, str(session_id))
        if model is None:
            return None
        return self._mapper.to_domain(model)

    def get_by_refresh_token_id(self, refresh_token_id: TokenId) -> AuthSession | None:
        """Récupère une session par hash de refresh token.

        :param refresh_token_id: Identifiant token core.
        :returns: Entité ou ``None``.
        """
        model = self._session.scalars(
            select(AuthSessionModel).where(
                AuthSessionModel.refresh_token_hash == str(refresh_token_id)
            )
        ).first()
        if model is None:
            return None
        return self._mapper.to_domain(model)

    def get_active_by_user(self, user_id: UserId) -> list[AuthSession]:
        """Liste les sessions actives d'un utilisateur.

        :param user_id: Identifiant utilisateur.
        :returns: Sessions au statut ``ACTIVE``.
        """
        models = self._session.scalars(
            select(AuthSessionModel)
            .where(AuthSessionModel.user_id == str(user_id))
            .where(AuthSessionModel.status == SessionStatus.ACTIVE.value)
            .order_by(AuthSessionModel.created_at)
        ).all()
        return [self._mapper.to_domain(model) for model in models]

    def save(self, auth_session: AuthSession) -> None:
        """Crée ou met à jour une session.

        :param auth_session: Entité core.
        """
        self._session.merge(self._mapper.to_model(auth_session))
        SqlAlchemyPersistenceGuard.flush(self._session)

    def delete(self, session_id: SessionId) -> None:
        """Supprime une session.

        :param session_id: Identifiant à supprimer.
        """
        model = self._session.get(AuthSessionModel, str(session_id))
        if model is not None:
            self._session.delete(model)
            SqlAlchemyPersistenceGuard.flush(self._session)
