"""Tests mappers session, audit et JWK."""

from datetime import datetime
from unittest.mock import patch

import pytest
from baobab_auth_core.domain.entities.audit_event import AuditEvent
from baobab_auth_core.domain.entities.session import Session
from baobab_auth_core.domain.enums.audit_event_type import AuditEventType
from baobab_auth_core.domain.enums.audit_severity import AuditSeverity
from baobab_auth_core.domain.enums.session_status import SessionStatus
from baobab_auth_core.domain.value_objects.audit_event_id import AuditEventId
from baobab_auth_core.domain.value_objects.auth_subject import AuthSubject
from baobab_auth_core.domain.value_objects.session_id import SessionId
from baobab_auth_core.domain.value_objects.token_id import TokenId
from baobab_auth_core.domain.value_objects.user_id import UserId

from baobab_auth_database.exceptions.mapping.auth_database_mapping_error import (
    AuthDatabaseMappingError,
)
from baobab_auth_database.mappers.auth_audit_event_orm_mapper import (
    AuthAuditEventOrmMapper,
)
from baobab_auth_database.mappers.auth_jwk_key_orm_mapper import AuthJwkKeyOrmMapper
from baobab_auth_database.mappers.auth_jwk_key_snapshot import AuthJwkKeySnapshot
from baobab_auth_database.mappers.auth_session_orm_mapper import AuthSessionOrmMapper
from baobab_auth_database.models.orm.auth_audit_event_model import AuthAuditEventModel
from baobab_auth_database.models.orm.auth_jwk_key_model import AuthJwkKeyModel
from baobab_auth_database.models.orm.auth_session_model import AuthSessionModel


class TestAuthSessionOrmMapper:
    """Tests mapper Session."""

    def test_FEAT_004_1_roundtrip_session(self, now_utc: datetime) -> None:
        session = Session(
            id=SessionId("sess-1"),
            user_id=UserId("u1"),
            refresh_token_id=TokenId("refresh-hash-1"),
            status=SessionStatus.ACTIVE,
            created_at=now_utc,
            expires_at=now_utc,
            device_label="Mobile",
        )
        mapper = AuthSessionOrmMapper()
        model = mapper.to_model(session)
        assert model.refresh_token_hash == "refresh-hash-1"
        restored = mapper.to_domain(model)
        assert restored.device_label == "Mobile"
        assert restored.refresh_token_id == session.refresh_token_id

    def test_FEAT_004_1_session_token_vide(self, now_utc: datetime) -> None:
        model = AuthSessionModel(
            id="sess-1",
            user_id="u1",
            refresh_token_hash="",
            status=SessionStatus.ACTIVE.value,
            created_at=now_utc,
            expires_at=now_utc,
        )
        with pytest.raises(
            AuthDatabaseMappingError, match="AuthSessionModel vers Session"
        ):
            AuthSessionOrmMapper().to_domain(model)


class TestAuthAuditEventOrmMapper:
    """Tests mapper AuditEvent."""

    def test_FEAT_004_1_roundtrip_audit(self, now_utc: datetime) -> None:
        event = AuditEvent(
            id=AuditEventId("audit-1"),
            event_type=AuditEventType.LOGIN_SUCCESS,
            severity=AuditSeverity.INFO,
            created_at=now_utc,
            actor_subject=AuthSubject("sub-1"),
            target_type="user",
            target_id="u1",
            metadata={"ip": "127.0.0.1"},
        )
        mapper = AuthAuditEventOrmMapper()
        restored = mapper.to_domain(mapper.to_model(event))
        assert restored.target_type == "user"
        assert dict(restored.metadata) == {"ip": "127.0.0.1"}

    def test_FEAT_004_1_audit_acteur_invalide(self, now_utc: datetime) -> None:
        model = AuthAuditEventModel(
            id="audit-1",
            event_type=AuditEventType.LOGIN_SUCCESS.value,
            severity=AuditSeverity.INFO.value,
            created_at=now_utc,
            actor_subject="",
            event_metadata={},
        )
        with pytest.raises(
            AuthDatabaseMappingError, match="AuthAuditEventModel vers AuditEvent"
        ):
            AuthAuditEventOrmMapper().to_domain(model)


class TestAuthJwkKeyOrmMapper:
    """Tests mapper JWK snapshot."""

    def test_FEAT_004_1_roundtrip_jwk(self, now_utc: datetime) -> None:
        snapshot = AuthJwkKeySnapshot(
            id="k1",
            kid="kid-1",
            algorithm="RS256",
            public_key='{"kty":"RSA"}',
            private_key_encrypted="enc",
            is_active=True,
            created_at=now_utc,
            expires_at=None,
            revoked_at=None,
        )
        mapper = AuthJwkKeyOrmMapper()
        restored = mapper.to_snapshot(mapper.to_model(snapshot))
        assert restored.kid == snapshot.kid

    def test_FEAT_004_1_jwk_kid_vide(self, now_utc: datetime) -> None:
        model = AuthJwkKeyModel(
            id="k1",
            kid="",
            algorithm="RS256",
            public_key="pub",
            private_key_encrypted="enc",
            is_active=True,
            created_at=now_utc,
        )
        with pytest.raises(AuthDatabaseMappingError):
            AuthJwkKeyOrmMapper().to_snapshot(model)

    def test_FEAT_004_1_jwk_value_error_encapsule(self, now_utc: datetime) -> None:
        model = AuthJwkKeyModel(
            id="k1",
            kid="kid-1",
            algorithm="RS256",
            public_key="pub",
            private_key_encrypted="enc",
            is_active=True,
            created_at=now_utc,
        )
        with patch(
            "baobab_auth_database.mappers.auth_jwk_key_orm_mapper.AuthJwkKeySnapshot",
            side_effect=ValueError("unexpected"),
        ):
            with pytest.raises(
                AuthDatabaseMappingError,
                match="AuthJwkKeyModel vers AuthJwkKeySnapshot",
            ):
                AuthJwkKeyOrmMapper().to_snapshot(model)
