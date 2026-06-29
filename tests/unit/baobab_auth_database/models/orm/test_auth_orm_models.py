"""Tests des modèles ORM auth."""

from datetime import UTC, datetime

from baobab_auth_database.models.orm.auth_audit_event_model import AuthAuditEventModel
from baobab_auth_database.models.orm.auth_jwk_key_model import AuthJwkKeyModel
from baobab_auth_database.models.orm.auth_permission_model import AuthPermissionModel
from baobab_auth_database.models.orm.auth_role_model import AuthRoleModel
from baobab_auth_database.models.orm.auth_session_model import AuthSessionModel
from baobab_auth_database.models.orm.auth_user_model import AuthUserModel
from baobab_auth_database.naming.auth_table_naming_convention import (
    AuthTableNamingConvention,
)

_NOW = datetime(2026, 1, 1, tzinfo=UTC)


class TestAuthOrmModels:
    """Tests FEAT-002.1 — modèles ORM."""

    def test_FEAT_002_1_noms_tables_prefixe_auth(self) -> None:
        assert AuthUserModel.__tablename__ == "auth_users"
        assert AuthPermissionModel.__tablename__ == "auth_permissions"
        assert AuthSessionModel.__tablename__ == "auth_sessions"
        assert AuthAuditEventModel.__tablename__ == "auth_audit_events"
        assert AuthJwkKeyModel.__tablename__ == AuthTableNamingConvention.table_name(
            "jwk_keys"
        )

    def test_FEAT_002_1_colonnes_permission_cdc(self) -> None:
        columns = {c.name for c in AuthPermissionModel.__table__.columns}
        assert {"resource", "action", "is_system"}.issubset(columns)

    def test_FEAT_002_1_colonnes_session_cdc(self) -> None:
        columns = {c.name for c in AuthSessionModel.__table__.columns}
        assert {"last_used_at", "device_label", "refresh_token_hash"}.issubset(columns)

    def test_FEAT_002_1_colonnes_audit_cdc(self) -> None:
        columns = {c.name for c in AuthAuditEventModel.__table__.columns}
        assert {"target_type", "target_id"}.issubset(columns)

    def test_FEAT_002_1_repr_user_sans_password_hash(self) -> None:
        user = AuthUserModel(
            id="u1",
            auth_subject="sub-1",
            normalized_email="a@example.com",
            password_hash="secret-hash",
            status="ACTIVE",
            failed_login_count=0,
            created_at=_NOW,
            updated_at=_NOW,
        )
        text = repr(user)
        assert "secret-hash" not in text
        assert "password_hash" not in text

    def test_FEAT_002_1_repr_session_sans_refresh_token(self) -> None:
        session = AuthSessionModel(
            id="s1",
            user_id="u1",
            refresh_token_hash="token-hash",
            status="ACTIVE",
            created_at=_NOW,
            expires_at=_NOW,
        )
        text = repr(session)
        assert "token-hash" not in text
        assert "refresh_token" not in text

    def test_FEAT_002_1_repr_jwk_sans_cle_privee(self) -> None:
        key = AuthJwkKeyModel(
            id="k1",
            kid="kid-1",
            algorithm="RS256",
            public_key='{"kty":"RSA"}',
            private_key_encrypted="encrypted-private",
            is_active=True,
            created_at=_NOW,
        )
        text = repr(key)
        assert "encrypted-private" not in text
        assert "private_key" not in text

    def test_FEAT_002_1_contraintes_uniques(self) -> None:
        user_constraints = {c.name for c in AuthUserModel.__table__.constraints}
        assert "uq_auth_users_auth_subject" in user_constraints
        assert "uq_auth_users_normalized_email" in user_constraints

        session_constraints = {c.name for c in AuthSessionModel.__table__.constraints}
        assert "uq_auth_sessions_refresh_token_hash" in session_constraints

        jwk_constraints = {c.name for c in AuthJwkKeyModel.__table__.constraints}
        assert "uq_auth_jwk_keys_kid" in jwk_constraints

        role_constraints = {c.name for c in AuthRoleModel.__table__.constraints}
        assert "uq_auth_roles_name" in role_constraints

        perm_constraints = {c.name for c in AuthPermissionModel.__table__.constraints}
        assert "uq_auth_permissions_name" in perm_constraints
