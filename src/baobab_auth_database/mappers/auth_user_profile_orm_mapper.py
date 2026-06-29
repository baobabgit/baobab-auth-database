"""Mapper ORM profil utilisateur ↔ entité ``UserProfile`` du core.

:spec: FEAT-004.1
"""

from baobab_auth_core.domain.entities.user_profile import UserProfile
from baobab_auth_core.domain.value_objects.user_id import UserId
from baobab_auth_core.exceptions.validation import ValidationError

from baobab_auth_database.exceptions.mapping.auth_database_mapping_error import (
    AuthDatabaseMappingError,
)
from baobab_auth_database.models.orm.auth_user_profile_model import AuthUserProfileModel


class AuthUserProfileOrmMapper:
    """Convertit ``AuthUserProfileModel`` en :class:`UserProfile` et inversement.

    :spec: FEAT-004.1
    """

    def to_domain(self, model: AuthUserProfileModel) -> UserProfile:
        """Construit une entité ``UserProfile`` depuis le modèle ORM.

        :param model: Ligne ``auth_profiles``.
        :returns: Entité core.
        :raises AuthDatabaseMappingError: Si la conversion échoue.
        """
        try:
            return UserProfile(
                user_id=UserId(model.user_id),
                created_at=model.created_at,
                updated_at=model.updated_at,
                display_name=model.display_name,
                locale=model.locale,
                timezone=model.timezone,
                avatar_url=model.avatar_url,
            )
        except (ValidationError, ValueError) as exc:
            msg = "Impossible de mapper AuthUserProfileModel vers UserProfile."
            raise AuthDatabaseMappingError(msg, cause=exc) from exc

    def to_model(self, profile: UserProfile) -> AuthUserProfileModel:
        """Construit un modèle ORM depuis une entité ``UserProfile``.

        :param profile: Entité core.
        :returns: Modèle SQLAlchemy.
        """
        return AuthUserProfileModel(
            user_id=str(profile.user_id),
            display_name=profile.display_name,
            locale=profile.locale,
            timezone=profile.timezone,
            avatar_url=profile.avatar_url,
            created_at=profile.created_at,
            updated_at=profile.updated_at,
        )
