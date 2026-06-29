"""Mapper ORM permission ↔ entité ``Permission`` du core.

:spec: FEAT-004.1
"""

from baobab_auth_core.domain.entities.permission import Permission
from baobab_auth_core.domain.value_objects.permission_id import PermissionId
from baobab_auth_core.domain.value_objects.permission_name import PermissionName
from baobab_auth_core.exceptions.validation import ValidationError

from baobab_auth_database.exceptions.mapping.auth_database_mapping_error import (
    AuthDatabaseMappingError,
)
from baobab_auth_database.models.orm.auth_permission_model import AuthPermissionModel


class AuthPermissionOrmMapper:
    """Convertit ``AuthPermissionModel`` en :class:`Permission` et inversement.

    :spec: FEAT-004.1
    """

    def to_domain(self, model: AuthPermissionModel) -> Permission:
        """Construit une entité ``Permission`` depuis le modèle ORM.

        :param model: Ligne ``auth_permissions``.
        :returns: Entité core.
        :raises AuthDatabaseMappingError: Si la conversion échoue.
        """
        try:
            return Permission(
                id=PermissionId(model.id),
                name=PermissionName(model.name),
                resource=model.resource,
                action=model.action,
                is_system=model.is_system,
                created_at=model.created_at,
                description=model.description,
            )
        except (ValidationError, ValueError) as exc:
            msg = "Impossible de mapper AuthPermissionModel vers Permission."
            raise AuthDatabaseMappingError(msg, cause=exc) from exc

    def to_model(self, permission: Permission) -> AuthPermissionModel:
        """Construit un modèle ORM depuis une entité ``Permission``.

        :param permission: Entité core.
        :returns: Modèle SQLAlchemy.
        """
        return AuthPermissionModel(
            id=str(permission.id),
            name=str(permission.name),
            resource=permission.resource,
            action=permission.action,
            is_system=permission.is_system,
            description=permission.description,
            created_at=permission.created_at,
        )
