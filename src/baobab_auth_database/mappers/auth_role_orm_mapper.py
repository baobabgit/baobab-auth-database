"""Mapper ORM rôle ↔ entité ``Role`` du core.

:spec: FEAT-004.1
"""

from baobab_auth_core.domain.entities.role import Role
from baobab_auth_core.domain.value_objects.permission_name import PermissionName
from baobab_auth_core.domain.value_objects.role_id import RoleId
from baobab_auth_core.domain.value_objects.role_name import RoleName
from baobab_auth_core.exceptions.validation import ValidationError

from baobab_auth_database.exceptions.mapping.auth_database_mapping_error import (
    AuthDatabaseMappingError,
)
from baobab_auth_database.models.orm.auth_role_model import AuthRoleModel


class AuthRoleOrmMapper:
    """Convertit ``AuthRoleModel`` en :class:`Role` et inversement.

    :spec: FEAT-004.1
    """

    def to_domain(
        self, model: AuthRoleModel, permission_names: tuple[str, ...]
    ) -> Role:
        """Construit une entité ``Role`` depuis le modèle ORM.

        :param model: Ligne ``auth_roles``.
        :param permission_names: Permissions associées (``auth_role_permissions``).
        :returns: Entité core.
        :raises AuthDatabaseMappingError: Si la conversion échoue.
        """
        try:
            return Role(
                id=RoleId(model.id),
                name=RoleName(model.name),
                is_system=model.is_system,
                created_at=model.created_at,
                updated_at=model.updated_at,
                description=model.description,
                permission_names=tuple(
                    PermissionName(name) for name in permission_names
                ),
            )
        except (ValidationError, ValueError) as exc:
            msg = "Impossible de mapper AuthRoleModel vers Role."
            raise AuthDatabaseMappingError(msg, cause=exc) from exc

    def to_model(self, role: Role) -> AuthRoleModel:
        """Construit un modèle ORM depuis une entité ``Role``.

        :param role: Entité core.
        :returns: Modèle SQLAlchemy (sans les permissions).
        """
        return AuthRoleModel(
            id=str(role.id),
            name=str(role.name),
            is_system=role.is_system,
            description=role.description,
            created_at=role.created_at,
            updated_at=role.updated_at,
        )
