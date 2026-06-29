"""Fixtures pytest partagées."""

from datetime import UTC, datetime

import pytest


@pytest.fixture
def now_utc() -> datetime:
    """Horodatage UTC fixe pour les tests de mappers.

    :returns: Datetime timezone-aware reproductible.
    """
    return datetime(2026, 1, 15, 12, 0, 0, tzinfo=UTC)
