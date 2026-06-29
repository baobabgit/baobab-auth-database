# Rapport de tests — BL-004

**Date** : 2026-06-28  
**Verdict QA** : **PASSED** (avec réserves couverture fichier)

## Tests BL-004

| Fichier | Tests | Résultat |
|---------|-------|----------|
| `test_auth_orm_value_converter.py` | 5 | PASS |
| `test_auth_user_orm_mapper.py` | 2 | PASS |
| `test_auth_role_permission_mappers.py` | 4 | PASS |
| `test_auth_session_audit_jwk_mappers.py` | 4 | PASS |
| **Total** | **15** | **PASS** |

*(+ 4 tests converter/mappers indirects dans périmètre global 47 tests)*

## Couverture mappers

| Module | Couverture | Lignes manquantes |
|--------|------------|-------------------|
| `auth_orm_value_converter.py` | 100 % | — |
| `auth_permission_orm_mapper.py` | 100 % | — |
| `auth_user_orm_mapper.py` | 90 % | 56–57 |
| `auth_session_orm_mapper.py` | 83 % | 51–53 |
| `auth_role_orm_mapper.py` | 81 % | 46–48 |
| `auth_jwk_key_orm_mapper.py` | 80 % | 47–49 |
| `auth_user_profile_orm_mapper.py` | 79 % | 39–41 |
| `auth_audit_event_orm_mapper.py` | 84 % | 55–57 |

**Couverture globale projet : 95,24 %** — seuil `--cov-fail-under=95` respecté.

## Cas testés

- Roundtrip domaine ↔ ORM (User, Role, Permission, Session, Audit, JWK)
- Conversion enum/statut invalide → `AuthDatabaseMappingError`
- `AuthOrmValueConverter` timezone-aware UTC

## Réserves QA

Branches `except` dans `to_model()` non exercées (5 mappers). Recommandation :
ajouter tests d'erreur `to_model` avant BL-005 ou dans BL-005 (non bloquant QA global).
