"""Tests AuthUserOrmMapper."""

from datetime import datetime

import pytest
from baobab_auth_core.domain.entities.user import User
from baobab_auth_core.domain.enums.user_status import UserStatus
from baobab_auth_core.domain.value_objects.auth_subject import AuthSubject
from baobab_auth_core.domain.value_objects.email import Email
from baobab_auth_core.domain.value_objects.password_hash import PasswordHash
from baobab_auth_core.domain.value_objects.role_name import RoleName
from baobab_auth_core.domain.value_objects.user_id import UserId

from baobab_auth_database.exceptions.mapping.auth_database_mapping_error import (
    AuthDatabaseMappingError,
)
from baobab_auth_database.mappers.auth_user_orm_mapper import AuthUserOrmMapper
from baobab_auth_database.models.orm.auth_user_model import AuthUserModel


class TestAuthUserOrmMapper:
    """Tests FEAT-004.1 — mapper User."""

    def test_FEAT_004_1_roundtrip_user(self, now_utc: datetime) -> None:
        user = User(
            id=UserId("user-1"),
            auth_subject=AuthSubject("sub-1"),
            email=Email("alice@example.com"),
            password_hash=PasswordHash("hash-value"),
            status=UserStatus.ACTIVE,
            role_names=(RoleName("USER"),),
            created_at=now_utc,
            updated_at=now_utc,
        )
        mapper = AuthUserOrmMapper()
        model = mapper.to_model(user)
        restored = mapper.to_domain(model, role_names=("USER",))
        assert restored.id == user.id
        assert restored.email == user.email
        assert restored.role_names == user.role_names

    def test_FEAT_004_1_statut_invalide(self, now_utc: datetime) -> None:
        model = AuthUserModel(
            id="u1",
            auth_subject="sub",
            normalized_email="a@b.com",
            password_hash="hash",
            status="NOT_A_STATUS",
            failed_login_count=0,
            created_at=now_utc,
            updated_at=now_utc,
        )
        with pytest.raises(AuthDatabaseMappingError):
            AuthUserOrmMapper().to_domain(model, role_names=())

    def test_FEAT_004_1_email_invalide(self, now_utc: datetime) -> None:
        model = AuthUserModel(
            id="u1",
            auth_subject="sub",
            normalized_email="not-an-email",
            password_hash="hash",
            status=UserStatus.ACTIVE.value,
            failed_login_count=0,
            created_at=now_utc,
            updated_at=now_utc,
        )
        with pytest.raises(AuthDatabaseMappingError, match="AuthUserModel vers User"):
            AuthUserOrmMapper().to_domain(model, role_names=())
