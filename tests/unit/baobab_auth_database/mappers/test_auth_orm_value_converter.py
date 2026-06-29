"""Tests AuthOrmValueConverter."""

import pytest
from baobab_auth_core.domain.enums.user_status import UserStatus
from baobab_auth_core.exceptions.validation import ValidationError

from baobab_auth_database.exceptions.mapping.auth_database_mapping_error import (
    AuthDatabaseMappingError,
)
from baobab_auth_database.mappers.auth_orm_value_converter import AuthOrmValueConverter


class TestAuthOrmValueConverter:
    """Tests utilitaires de conversion ORM."""

    def test_FEAT_004_1_require_non_empty_ok(self) -> None:
        assert AuthOrmValueConverter.require_non_empty("abc", "field") == "abc"

    def test_FEAT_004_1_require_non_empty_leve(self) -> None:
        with pytest.raises(AuthDatabaseMappingError, match="Champ obligatoire"):
            AuthOrmValueConverter.require_non_empty("  ", "kid")

    def test_FEAT_004_1_to_enum_ok(self) -> None:
        assert (
            AuthOrmValueConverter.to_enum(UserStatus, "ACTIVE", "status")
            is UserStatus.ACTIVE
        )

    def test_FEAT_004_1_to_enum_invalide(self) -> None:
        with pytest.raises(AuthDatabaseMappingError, match="enum invalide"):
            AuthOrmValueConverter.to_enum(UserStatus, "UNKNOWN", "status")

    def test_FEAT_004_1_wrap_validation(self) -> None:
        def _raise() -> str:
            raise ValidationError("invalid")

        with pytest.raises(AuthDatabaseMappingError, match="Validation core"):
            AuthOrmValueConverter.wrap_validation("email", _raise)
