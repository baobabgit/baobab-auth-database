# Rapport de tests — BL-002

**Date** : 2026-06-28  
**Périmètre** : modèles ORM + registry  
**Verdict QA** : **PASSED**

## Commandes

```bash
uv run pytest tests/unit/baobab_auth_database/models/orm/ \
  --cov=src/baobab_auth_database/models/orm --cov-report=term-missing -q
uv run pytest --cov=src --cov-fail-under=95 -q
```

## Tests unitaires BL-002

| Fichier | Tests | Résultat |
|---------|-------|----------|
| `test_auth_orm_models.py` | 8 | PASS |
| `test_auth_orm_registry.py` | 2 | PASS |
| **Total** | **10** | **PASS** |

## Couverture modules ORM

| Module | Couverture | Note |
|--------|------------|------|
| `auth_user_model.py` | 100 % | |
| `auth_session_model.py` | 100 % | |
| `auth_jwk_key_model.py` | 100 % | |
| `auth_orm_registry.py` | 100 % | |
| Autres modèles | 92–95 % | branches `__repr__` partielles |

Couverture globale projet : **95,24 %** (47 tests) — seuil respecté.

## Critères FEAT-002.1 vérifiés

- Création schéma SQLite (`create_all`)
- Colonnes CDC présentes sur Permission, Role, Session, AuditEvent
- Contraintes uniques testées (email normalisé, refresh_token_hash)
- Registry expose les 9 modèles dans l'ordre stable

## Observations

- Pas de test PostgreSQL natif (accepté MVP ; BL-005/BL-008).
- `UniqueConstraint("id")` sur `auth_sessions` redondante avec PK — signalée au relecteur.
