"""Tests mappers profil, rôle, permission."""

from datetime import datetime

import pytest
from baobab_auth_core.domain.entities.permission import Permission
from baobab_auth_core.domain.entities.role import Role
from baobab_auth_core.domain.entities.user_profile import UserProfile
from baobab_auth_core.domain.value_objects.permission_id import PermissionId
from baobab_auth_core.domain.value_objects.permission_name import PermissionName
from baobab_auth_core.domain.value_objects.role_id import RoleId
from baobab_auth_core.domain.value_objects.role_name import RoleName
from baobab_auth_core.domain.value_objects.user_id import UserId

from baobab_auth_database.exceptions.mapping.auth_database_mapping_error import (
    AuthDatabaseMappingError,
)
from baobab_auth_database.mappers.auth_permission_orm_mapper import (
    AuthPermissionOrmMapper,
)
from baobab_auth_database.mappers.auth_role_orm_mapper import AuthRoleOrmMapper
from baobab_auth_database.mappers.auth_user_profile_orm_mapper import (
    AuthUserProfileOrmMapper,
)
from baobab_auth_database.models.orm.auth_permission_model import AuthPermissionModel
from baobab_auth_database.models.orm.auth_role_model import AuthRoleModel
from baobab_auth_database.models.orm.auth_user_profile_model import (
    AuthUserProfileModel,
)


class TestAuthUserProfileOrmMapper:
    """Tests mapper UserProfile."""

    def test_FEAT_004_1_roundtrip_profile(self, now_utc: datetime) -> None:
        profile = UserProfile(
            user_id=UserId("u1"),
            created_at=now_utc,
            updated_at=now_utc,
            display_name="Alice",
        )
        mapper = AuthUserProfileOrmMapper()
        restored = mapper.to_domain(mapper.to_model(profile))
        assert restored.display_name == "Alice"
        assert restored.user_id == profile.user_id

    def test_FEAT_004_1_profil_user_id_vide(self, now_utc: datetime) -> None:
        model = AuthUserProfileModel(
            user_id="",
            created_at=now_utc,
            updated_at=now_utc,
        )
        with pytest.raises(
            AuthDatabaseMappingError, match="AuthUserProfileModel vers UserProfile"
        ):
            AuthUserProfileOrmMapper().to_domain(model)


class TestAuthRoleOrmMapper:
    """Tests mapper Role."""

    def test_FEAT_004_1_roundtrip_role(self, now_utc: datetime) -> None:
        role = Role(
            id=RoleId("role-1"),
            name=RoleName("ADMIN"),
            is_system=True,
            created_at=now_utc,
            updated_at=now_utc,
            permission_names=(PermissionName("auth:user:read"),),
        )
        mapper = AuthRoleOrmMapper()
        model = mapper.to_model(role)
        restored = mapper.to_domain(model, permission_names=("auth:user:read",))
        assert restored.name == role.name
        assert restored.permission_names == role.permission_names

    def test_FEAT_004_1_role_nom_invalide(self, now_utc: datetime) -> None:
        model = AuthRoleModel(
            id="role-1",
            name="invalid role name",
            is_system=False,
            created_at=now_utc,
            updated_at=now_utc,
        )
        with pytest.raises(AuthDatabaseMappingError, match="AuthRoleModel vers Role"):
            AuthRoleOrmMapper().to_domain(model, permission_names=())


class TestAuthPermissionOrmMapper:
    """Tests mapper Permission."""

    def test_FEAT_004_1_roundtrip_permission(self, now_utc: datetime) -> None:
        perm = Permission(
            id=PermissionId("p1"),
            name=PermissionName("auth:user:read"),
            resource="user",
            action="read",
            is_system=True,
            created_at=now_utc,
        )
        mapper = AuthPermissionOrmMapper()
        restored = mapper.to_domain(mapper.to_model(perm))
        assert restored.resource == "user"
        assert restored.action == "read"

    def test_FEAT_004_1_permission_invalide(self, now_utc: datetime) -> None:
        model = AuthPermissionModel(
            id="p1",
            name="invalid name with spaces",
            resource="user",
            action="read",
            is_system=False,
            created_at=now_utc,
        )
        with pytest.raises(AuthDatabaseMappingError):
            AuthPermissionOrmMapper().to_domain(model)
