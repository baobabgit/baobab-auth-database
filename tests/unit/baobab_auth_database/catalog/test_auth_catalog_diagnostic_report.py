"""Tests AuthCatalogDiagnosticReport."""

import json

from baobab_auth_database.catalog.auth_catalog_diagnostic_report import (
    AuthCatalogDiagnosticReport,
)


class TestAuthCatalogDiagnosticReport:
    """Tests FEAT-006.3 — sérialisation rapport."""

    def test_FEAT_006_3_json_stable(self) -> None:
        report = AuthCatalogDiagnosticReport(
            compat_profile="core_051",
            core_version="0.5.1",
            expected_checksum="abc",
            actual_checksum="abc",
        )
        first = json.dumps(report.to_dict(), sort_keys=True)
        second = json.dumps(report.to_dict(), sort_keys=True)
        assert first == second
        assert json.loads(first)["conform"] is True
