# Sorties attendues — BL-002

## Code (11 modules)

| Classe | Fichier |
|--------|---------|
| `AuthOrmBase` | `models/orm/auth_orm_base.py` |
| `AuthOrmRegistry` | `models/orm/auth_orm_registry.py` |
| `AuthUserModel` | `models/orm/auth_user_model.py` |
| `AuthUserProfileModel` | `models/orm/auth_user_profile_model.py` |
| `AuthRoleModel` | `models/orm/auth_role_model.py` |
| `AuthPermissionModel` | `models/orm/auth_permission_model.py` |
| `AuthUserRoleModel` | `models/orm/auth_user_role_model.py` |
| `AuthRolePermissionModel` | `models/orm/auth_role_permission_model.py` |
| `AuthSessionModel` | `models/orm/auth_session_model.py` |
| `AuthAuditEventModel` | `models/orm/auth_audit_event_model.py` |
| `AuthJwkKeyModel` | `models/orm/auth_jwk_key_model.py` |

## Tests

- `tests/unit/baobab_auth_database/models/orm/test_auth_orm_models.py`
- `tests/unit/baobab_auth_database/models/orm/test_auth_orm_registry.py`

## Qualité

- `create_all` SQLite sans erreur
- Couverture globale projet ≥ 95 %
