"""Repository SQLAlchemy des profils utilisateur.

:spec: FEAT-003.1
"""

from baobab_auth_core.domain.entities.user_profile import UserProfile
from baobab_auth_core.domain.value_objects.user_id import UserId
from sqlalchemy import select
from sqlalchemy.orm import Session

from baobab_auth_database.mappers.auth_user_profile_orm_mapper import (
    AuthUserProfileOrmMapper,
)
from baobab_auth_database.models.orm.auth_user_profile_model import (
    AuthUserProfileModel,
)
from baobab_auth_database.repositories.sqlalchemy_persistence_guard import (
    SqlAlchemyPersistenceGuard,
)


class SqlAlchemyUserProfileRepository:
    """Persistance des profils ``auth_profiles`` (pas de port core dédié).

    :spec: FEAT-003.1
    """

    def __init__(
        self,
        session: Session,
        mapper: AuthUserProfileOrmMapper | None = None,
    ) -> None:
        """Injecte la session et le mapper.

        :param session: Session SQLAlchemy partagée.
        :param mapper: Mapper profil ; instance par défaut si omis.
        """
        self._session = session
        self._mapper = mapper or AuthUserProfileOrmMapper()

    def get_by_user_id(self, user_id: UserId) -> UserProfile | None:
        """Récupère le profil d'un utilisateur.

        :param user_id: Identifiant utilisateur.
        :returns: Profil ou ``None``.
        """
        model = self._session.get(AuthUserProfileModel, str(user_id))
        if model is None:
            return None
        return self._mapper.to_domain(model)

    def save(self, profile: UserProfile) -> None:
        """Crée ou met à jour un profil.

        :param profile: Entité core.
        """
        self._session.merge(self._mapper.to_model(profile))
        SqlAlchemyPersistenceGuard.flush(self._session)

    def delete(self, user_id: UserId) -> None:
        """Supprime le profil d'un utilisateur.

        :param user_id: Identifiant utilisateur.
        """
        model = self._session.get(AuthUserProfileModel, str(user_id))
        if model is not None:
            self._session.delete(model)
            SqlAlchemyPersistenceGuard.flush(self._session)

    def exists_by_user_id(self, user_id: UserId) -> bool:
        """Indique si un profil existe pour l'utilisateur.

        :param user_id: Identifiant utilisateur.
        :returns: ``True`` si le profil existe.
        """
        stmt = select(AuthUserProfileModel.user_id).where(
            AuthUserProfileModel.user_id == str(user_id)
        )
        return self._session.scalars(stmt).first() is not None
