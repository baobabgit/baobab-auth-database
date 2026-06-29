"""Formateur texte des rapports catalogue.

:spec: FEAT-006.5
"""

from baobab_auth_database.catalog.auth_catalog_diagnostic_report import (
    AuthCatalogDiagnosticReport,
)


class AuthCatalogReportFormatter:
    """Formate un ``AuthCatalogDiagnosticReport`` en texte lisible.

    :spec: FEAT-006.5
    """

    def format(self, report: AuthCatalogDiagnosticReport) -> str:
        """Produit un rapport texte multi-lignes.

        :param report: Rapport source.
        :returns: Texte exploitable en CLI ou logs.
        """
        lines = [
            f"Profil: {report.compat_profile}",
            f"Core: {report.core_version}",
            f"Checksum attendu: {report.expected_checksum}",
            f"Checksum base: {report.actual_checksum or '(vide)'}",
            f"Conforme: {'oui' if report.is_conform else 'non'}",
        ]
        if report.missing_permissions:
            lines.append(
                "Permissions manquantes: " + ", ".join(report.missing_permissions)
            )
        if report.obsolete_permissions:
            lines.append(
                "Permissions obsolètes: " + ", ".join(report.obsolete_permissions)
            )
        if report.missing_roles:
            lines.append("Rôles manquants: " + ", ".join(report.missing_roles))
        if report.obsolete_roles:
            lines.append("Rôles obsolètes: " + ", ".join(report.obsolete_roles))
        for role, expected, actual in report.divergent_role_mappings:
            lines.append(
                f"Mapping divergent {role}: "
                f"attendu={list(expected)} actuel={list(actual)}"
            )
        return "\n".join(lines)
