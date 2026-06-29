# Assignment — BL-004

| Champ | Valeur |
|-------|--------|
| **ID** | BL-004 |
| **Titre** | Mappers ORM vers entités baobab-auth-core |
| **Version** | v0.1.0 |
| **Priorité** | P1 |
| **FEAT** | FEAT-004.1 |
| **US** | US-004 — Mapping domaine ↔ persistance |
| **Dépendances** | BL-002 |

## Périmètre

- `AuthOrmValueConverter` (types, enums, datetimes UTC)
- Mappers bidirectionnels : User, Profile, Role, Permission, Session, AuditEvent, JWK
- `AuthJwkKeySnapshot` (core 0.5.1 sans entité JWK)
- `AuthDatabaseMappingError`

## Hors périmètre

Repositories (BL-005), UoW (BL-006).
