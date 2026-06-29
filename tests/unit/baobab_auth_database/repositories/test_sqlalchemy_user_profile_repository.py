"""Tests SqlAlchemyUserProfileRepository."""

from baobab_auth_core.domain.entities.user_profile import UserProfile
from baobab_auth_core.domain.value_objects.user_id import UserId
from sqlalchemy.orm import Session

from baobab_auth_database.repositories.sqlalchemy_user_profile_repository import (
    SqlAlchemyUserProfileRepository,
)


class TestSqlAlchemyUserProfileRepository:
    """Tests FEAT-003.1 — repository profil."""

    def test_FEAT_003_1_roundtrip_profile(self, db_session: Session, now_utc) -> None:
        profile = UserProfile(
            user_id=UserId("user-1"),
            created_at=now_utc,
            updated_at=now_utc,
            display_name="Alice",
        )
        repo = SqlAlchemyUserProfileRepository(db_session)
        repo.save(profile)
        restored = repo.get_by_user_id(profile.user_id)
        assert restored is not None
        assert restored.user_id == profile.user_id
        assert restored.display_name == profile.display_name
        assert repo.exists_by_user_id(profile.user_id) is True

    def test_FEAT_003_1_delete_profile(self, db_session: Session, now_utc) -> None:
        profile = UserProfile(
            user_id=UserId("user-1"),
            created_at=now_utc,
            updated_at=now_utc,
        )
        repo = SqlAlchemyUserProfileRepository(db_session)
        repo.save(profile)
        repo.delete(profile.user_id)
        assert repo.get_by_user_id(profile.user_id) is None
