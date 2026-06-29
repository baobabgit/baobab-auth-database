"""Repository SQLAlchemy des rôles.

:spec: FEAT-003.1
"""

from baobab_auth_core.domain.entities.role import Role
from baobab_auth_core.domain.value_objects.permission_name import PermissionName
from baobab_auth_core.domain.value_objects.role_id import RoleId
from baobab_auth_core.domain.value_objects.role_name import RoleName
from sqlalchemy import delete, func, select
from sqlalchemy.orm import Session

from baobab_auth_database.mappers.auth_role_orm_mapper import AuthRoleOrmMapper
from baobab_auth_database.models.orm.auth_permission_model import AuthPermissionModel
from baobab_auth_database.models.orm.auth_role_model import AuthRoleModel
from baobab_auth_database.models.orm.auth_role_permission_model import (
    AuthRolePermissionModel,
)
from baobab_auth_database.models.orm.auth_user_role_model import AuthUserRoleModel
from baobab_auth_database.repositories.sqlalchemy_persistence_guard import (
    SqlAlchemyPersistenceGuard,
)


class SqlAlchemyRoleRepository:
    """Implémentation synchrone du port ``RoleRepository``.

    :spec: FEAT-003.1
    """

    def __init__(
        self, session: Session, mapper: AuthRoleOrmMapper | None = None
    ) -> None:
        """Injecte la session et le mapper.

        :param session: Session SQLAlchemy partagée.
        :param mapper: Mapper rôle ; instance par défaut si omis.
        """
        self._session = session
        self._mapper = mapper or AuthRoleOrmMapper()

    def get_by_id(self, role_id: RoleId) -> Role | None:
        """Récupère un rôle par identifiant.

        :param role_id: Identifiant core.
        :returns: Entité ou ``None``.
        """
        model = self._session.get(AuthRoleModel, str(role_id))
        if model is None:
            return None
        permission_names = self._load_permission_names(model.id)
        return self._mapper.to_domain(model, permission_names=permission_names)

    def get_by_name(self, name: RoleName) -> Role | None:
        """Récupère un rôle par nom.

        :param name: Nom du rôle.
        :returns: Entité ou ``None``.
        """
        model = self._session.scalars(
            select(AuthRoleModel).where(AuthRoleModel.name == str(name))
        ).first()
        if model is None:
            return None
        permission_names = self._load_permission_names(model.id)
        return self._mapper.to_domain(model, permission_names=permission_names)

    def save(self, role: Role) -> None:
        """Crée ou met à jour un rôle et ses permissions associées.

        :param role: Entité core.
        """
        self._session.merge(self._mapper.to_model(role))
        self._sync_permissions(str(role.id), role.permission_names)
        SqlAlchemyPersistenceGuard.flush(self._session)

    def list_all(self) -> list[Role]:
        """Liste tous les rôles.

        :returns: Liste des rôles.
        """
        return list(self.list_roles())

    def list_roles(self) -> tuple[Role, ...]:
        """Liste tous les rôles.

        :returns: Tuple des rôles.
        """
        models = self._session.scalars(
            select(AuthRoleModel).order_by(AuthRoleModel.name)
        ).all()
        return tuple(
            self._mapper.to_domain(
                model, permission_names=self._load_permission_names(model.id)
            )
            for model in models
        )

    def count_users_with_role(self, name: RoleName) -> int:
        """Compte les utilisateurs assignés à un rôle.

        :param name: Nom du rôle.
        :returns: Nombre d'utilisateurs.
        """
        stmt = (
            select(func.count())
            .select_from(AuthUserRoleModel)
            .join(AuthRoleModel, AuthUserRoleModel.role_id == AuthRoleModel.id)
            .where(AuthRoleModel.name == str(name))
        )
        return int(self._session.scalar(stmt) or 0)

    def _load_permission_names(self, role_id: str) -> tuple[str, ...]:
        stmt = (
            select(AuthPermissionModel.name)
            .join(
                AuthRolePermissionModel,
                AuthRolePermissionModel.permission_id == AuthPermissionModel.id,
            )
            .where(AuthRolePermissionModel.role_id == role_id)
            .order_by(AuthPermissionModel.name)
        )
        return tuple(self._session.scalars(stmt).all())

    def _sync_permissions(
        self, role_id: str, permission_names: tuple[PermissionName, ...]
    ) -> None:
        self._session.execute(
            delete(AuthRolePermissionModel).where(
                AuthRolePermissionModel.role_id == role_id
            )
        )
        for permission_name in permission_names:
            permission = self._session.scalars(
                select(AuthPermissionModel).where(
                    AuthPermissionModel.name == str(permission_name)
                )
            ).first()
            if permission is None:
                continue
            self._session.add(
                AuthRolePermissionModel(
                    role_id=role_id,
                    permission_id=permission.id,
                )
            )
