"""Mapper ORM utilisateur ↔ entité ``User`` du core.

:spec: FEAT-004.1
"""

from baobab_auth_core.domain.entities.user import User
from baobab_auth_core.domain.enums.user_status import UserStatus
from baobab_auth_core.domain.value_objects.auth_subject import AuthSubject
from baobab_auth_core.domain.value_objects.email import Email
from baobab_auth_core.domain.value_objects.password_hash import PasswordHash
from baobab_auth_core.domain.value_objects.role_name import RoleName
from baobab_auth_core.domain.value_objects.user_id import UserId
from baobab_auth_core.exceptions.validation import ValidationError

from baobab_auth_database.exceptions.mapping.auth_database_mapping_error import (
    AuthDatabaseMappingError,
)
from baobab_auth_database.mappers.auth_orm_value_converter import AuthOrmValueConverter
from baobab_auth_database.models.orm.auth_user_model import AuthUserModel


class AuthUserOrmMapper:
    """Convertit ``AuthUserModel`` en :class:`User` et inversement.

    Les rôles sont portés par la table ``auth_user_roles`` ; ils sont passés
    explicitement à :meth:`to_domain`.

    :spec: FEAT-004.1
    """

    def to_domain(self, model: AuthUserModel, role_names: tuple[str, ...]) -> User:
        """Construit une entité ``User`` depuis le modèle ORM.

        :param model: Ligne ``auth_users``.
        :param role_names: Noms de rôles associés (table ``auth_user_roles``).
        :returns: Entité core validée.
        :raises AuthDatabaseMappingError: Si la conversion échoue.
        """
        try:
            return User(
                id=UserId(model.id),
                auth_subject=AuthSubject(model.auth_subject),
                email=Email(model.normalized_email),
                password_hash=PasswordHash(model.password_hash),
                status=AuthOrmValueConverter.to_enum(
                    UserStatus, model.status, "status"
                ),
                role_names=tuple(RoleName(name) for name in role_names),
                created_at=model.created_at,
                updated_at=model.updated_at,
                last_login_at=model.last_login_at,
                failed_login_count=model.failed_login_count,
                locked_until=model.locked_until,
            )
        except (ValidationError, ValueError) as exc:
            msg = "Impossible de mapper AuthUserModel vers User."
            raise AuthDatabaseMappingError(msg, cause=exc) from exc

    def to_model(self, user: User) -> AuthUserModel:
        """Construit un modèle ORM depuis une entité ``User``.

        :param user: Entité core.
        :returns: Modèle SQLAlchemy prêt à persister (sans les rôles).
        """
        return AuthUserModel(
            id=str(user.id),
            auth_subject=str(user.auth_subject),
            normalized_email=str(user.email),
            password_hash=user.password_hash.value,
            status=user.status.value,
            failed_login_count=user.failed_login_count,
            locked_until=user.locked_until,
            last_login_at=user.last_login_at,
            created_at=user.created_at,
            updated_at=user.updated_at,
        )
