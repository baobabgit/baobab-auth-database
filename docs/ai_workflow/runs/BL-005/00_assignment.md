# Assignment — BL-005

| Champ | Valeur |
|-------|--------|
| **ID** | BL-005 |
| **Titre** | Repositories synchrones SQLAlchemy |
| **Version** | v0.1.0 |
| **Priorité** | P0 |
| **FEAT** | FEAT-003.1 |
| **US** | US-003 — Repositories et Unit of Work |
| **Origin** | CDC v0.1.0 §4, §8 |
| **Dépendances** | BL-003, BL-004 |
| **Branche** | `bl/005-repositories-sync` → `version/v0.1.0` |

## Périmètre assigné

Implémenter les repositories synchrones SQLAlchemy pour les ports core
(`UserRepository`, `RoleRepository`, `PermissionRepository`, `SessionRepository`,
`AuditRepository`) plus profils et JWK (pas de port core en 0.5.1).

## Hors périmètre

- `SqlAlchemyAuthUnitOfWork` (BL-006)
- Export public `__all__` des repositories (BL-008)
- Tests contrat core FEAT-006.1 (BL-008)
