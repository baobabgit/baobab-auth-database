# Assignment — BL-002

| Champ | Valeur |
|-------|--------|
| **ID** | BL-002 |
| **Titre** | Modèles ORM auth (9 tables) |
| **Version** | v0.1.0 |
| **Priorité** | P0 |
| **FEAT** | FEAT-002.1 |
| **US** | US-002 — Modèles de persistance auth |
| **Origin** | CDC v0.1.0 §5 |
| **Dépendances** | BL-001 |

## Périmètre assigné

- `AuthOrmBase`, `AuthOrmRegistry`
- 9 modèles ORM : User, Profile, Role, Permission, UserRole, RolePermission,
  Session, AuditEvent, JwkKey
- Colonnes et contraintes CDC (unicité, FK, champs métier)
- `repr()` sans secrets sur User, Session, JWK

## Hors périmètre

Migrations Alembic (BL-003), mappers (BL-004), repositories (BL-005).
