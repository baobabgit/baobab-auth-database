# Assignment — BL-007

| Champ | Valeur |
|-------|--------|
| **ID** | BL-007 |
| **Titre** | CLI migrations et bootstrap DefaultAuthCatalog |
| **Version** | v0.1.0 |
| **Priorité** | P1 |
| **FEAT** | FEAT-005.1, FEAT-005.2 |
| **US** | US-005 — CLI et bootstrap catalogue |
| **Origin** | CDC v0.1.0 §4, §6 |
| **Dépendances** | BL-006 |
| **Branche** | `bl/007-cli-bootstrap` → `version/v0.1.0` |

## Périmètre assigné

- `AuthDatabaseCli` : upgrade, downgrade, current, history, bootstrap
- `AuthCatalogBootstrap` : seed idempotent via `DefaultAuthCatalog` du core
- Entry point `baobab-auth-db`, guide how-to, section README

## Hors périmètre

- Export public `__all__` (BL-008)
- Tests contrat core (BL-008)
