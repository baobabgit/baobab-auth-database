# Sorties attendues — BL-005

## Code

| Classe | Fichier | Port core |
|--------|---------|-----------|
| `SqlAlchemyPersistenceGuard` | `repositories/sqlalchemy_persistence_guard.py` | — |
| `AuthDatabasePersistenceError` | `exceptions/persistence/auth_database_persistence_error.py` | — |
| `SqlAlchemyUserRepository` | `repositories/sqlalchemy_user_repository.py` | `UserRepository` |
| `SqlAlchemyUserProfileRepository` | `repositories/sqlalchemy_user_profile_repository.py` | — |
| `SqlAlchemyRoleRepository` | `repositories/sqlalchemy_role_repository.py` | `RoleRepository` |
| `SqlAlchemyPermissionRepository` | `repositories/sqlalchemy_permission_repository.py` | `PermissionRepository` |
| `SqlAlchemySessionRepository` | `repositories/sqlalchemy_session_repository.py` | `SessionRepository` |
| `SqlAlchemyAuditRepository` | `repositories/sqlalchemy_audit_repository.py` | `AuditRepository` |
| `SqlAlchemyJwkKeyRepository` | `repositories/sqlalchemy_jwk_key_repository.py` | — |

## Tests (miroir)

- `tests/unit/baobab_auth_database/repositories/test_sqlalchemy_*.py` (8 fichiers)
- Fixtures partagées : `tests/conftest.py` (`sqlite_engine`, `db_session`)

## Qualité

- Couverture globale ≥ 95 %
- `make traceability` OK (script direct si pas de `make`)

## Git

- Branche `bl/005-repositories-sync`
- Commits : `BL-005: add synchronous sqlalchemy repositories`
- Merge `--no-ff` vers `version/v0.1.0`
