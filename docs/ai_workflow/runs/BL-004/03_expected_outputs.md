# Sorties attendues — BL-004

## Code

| Classe | Fichier |
|--------|---------|
| `AuthDatabaseMappingError` | `exceptions/mapping/auth_database_mapping_error.py` |
| `AuthOrmValueConverter` | `mappers/auth_orm_value_converter.py` |
| `AuthUserOrmMapper` | `mappers/auth_user_orm_mapper.py` |
| `AuthUserProfileOrmMapper` | `mappers/auth_user_profile_orm_mapper.py` |
| `AuthRoleOrmMapper` | `mappers/auth_role_orm_mapper.py` |
| `AuthPermissionOrmMapper` | `mappers/auth_permission_orm_mapper.py` |
| `AuthSessionOrmMapper` | `mappers/auth_session_orm_mapper.py` |
| `AuthAuditEventOrmMapper` | `mappers/auth_audit_event_orm_mapper.py` |
| `AuthJwkKeyOrmMapper` | `mappers/auth_jwk_key_orm_mapper.py` |
| `AuthJwkKeySnapshot` | `mappers/auth_jwk_key_snapshot.py` |

## Tests

- `tests/unit/baobab_auth_database/mappers/test_auth_orm_value_converter.py` (5)
- `tests/unit/baobab_auth_database/mappers/test_auth_user_orm_mapper.py` (2)
- `tests/unit/baobab_auth_database/mappers/test_auth_role_permission_mappers.py` (4)
- `tests/unit/baobab_auth_database/mappers/test_auth_session_audit_jwk_mappers.py` (4)
