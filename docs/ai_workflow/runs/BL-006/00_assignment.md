# Assignment — BL-006

| Champ | Valeur |
|-------|--------|
| **ID** | BL-006 |
| **Titre** | SqlAlchemyAuthUnitOfWork |
| **Version** | v0.1.0 |
| **Priorité** | P0 |
| **FEAT** | FEAT-003.2 |
| **US** | US-003 — Repositories et Unit of Work |
| **Origin** | CDC v0.1.0 §8 |
| **Dépendances** | BL-005 |
| **Branche** | `bl/006-unit-of-work` → `version/v0.1.0` |

## Périmètre assigné

Implémenter `SqlAlchemyAuthUnitOfWork` : protocole `UnitOfWork` du core, exposition
des 7 repositories (users, profiles, roles, permissions, sessions, audit, jwk_keys),
gestion commit/rollback transactionnelle.

## Hors périmètre

- Export public `__all__` (BL-008)
- Tests contrat core FEAT-006.1 (BL-008)
- CLI bootstrap (BL-007)
