"""Tests SqlAlchemyJwkKeyRepository."""

import pytest
from sqlalchemy.orm import Session

from baobab_auth_database.exceptions.persistence import AuthDatabasePersistenceError
from baobab_auth_database.mappers.auth_jwk_key_snapshot import AuthJwkKeySnapshot
from baobab_auth_database.repositories.sqlalchemy_jwk_key_repository import (
    SqlAlchemyJwkKeyRepository,
)


class TestSqlAlchemyJwkKeyRepository:
    """Tests FEAT-003.1 — repository JWK."""

    def _snapshot(
        self, now_utc, *, key_id: str = "k1", kid: str = "kid-1", active: bool = True
    ) -> AuthJwkKeySnapshot:
        return AuthJwkKeySnapshot(
            id=key_id,
            kid=kid,
            algorithm="RS256",
            public_key='{"kty":"RSA"}',
            private_key_encrypted="enc",
            is_active=active,
            created_at=now_utc,
            expires_at=None,
            revoked_at=None,
        )

    def test_FEAT_003_1_roundtrip_jwk(self, db_session: Session, now_utc) -> None:
        repo = SqlAlchemyJwkKeyRepository(db_session)
        snapshot = self._snapshot(now_utc)
        repo.save(snapshot)
        restored = repo.get_by_id(snapshot.id)
        assert restored is not None
        assert restored.kid == snapshot.kid
        assert repo.get_by_kid(snapshot.kid) == restored
        assert repo.list_active() == (restored,)

    def test_FEAT_003_1_unicite_kid(self, db_session: Session, now_utc) -> None:
        repo = SqlAlchemyJwkKeyRepository(db_session)
        repo.save(self._snapshot(now_utc))
        duplicate = self._snapshot(now_utc, key_id="k2", kid="kid-1")
        with pytest.raises(AuthDatabasePersistenceError):
            repo.save(duplicate)

    def test_FEAT_003_1_list_active_exclut_inactif(
        self, db_session: Session, now_utc
    ) -> None:
        repo = SqlAlchemyJwkKeyRepository(db_session)
        repo.save(self._snapshot(now_utc, key_id="k1", kid="kid-a", active=True))
        repo.save(self._snapshot(now_utc, key_id="k2", kid="kid-b", active=False))
        active = repo.list_active()
        assert len(active) == 1
        assert active[0].kid == "kid-a"
