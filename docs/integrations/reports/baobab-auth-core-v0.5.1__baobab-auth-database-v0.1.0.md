# Rapport d'intégration — baobab-auth-core v0.5.1 ↔ baobab-auth-database v0.1.1

**Date** : 2026-06-29  
**Producteur** : baobab-auth-core `0.5.1` (PyPI) / branche `version/v0.5.1`  
**Consommateur** : baobab-auth-database `v0.1.1` (PyPI) / jalon dev `version/v0.1.0`  
**Verdict** : **PASSED**

## Contexte

Validation du contrat ``database`` défini dans le cahier des charges core v0.5.0.
Dépendance consommatrice : ``baobab-auth-core>=0.5.1,<0.6.0``.

## Commandes exécutées

```bash
uv sync
uv run nox -s all
uv run pytest tests/contracts/ -v
```

## Résultats

| Contrôle | Résultat |
|----------|----------|
| Import ports core | PASS |
| ``UserRepository`` | PASS (`SqlAlchemyUserRepository`) |
| ``RoleRepository`` | PASS (`SqlAlchemyRoleRepository`) |
| ``PermissionRepository`` | PASS (`SqlAlchemyPermissionRepository`) |
| ``SessionRepository`` | PASS (`SqlAlchemySessionRepository`) |
| ``AuditRepository`` | PASS (`SqlAlchemyAuditRepository`) |
| ``UnitOfWork`` | PASS (`SqlAlchemyAuthUnitOfWork`) |
| ``DefaultAuthCatalog`` bootstrap | PASS (idempotent) |
| Couverture globale | ≥ 95 % |
| CI PR BL-008 | PASS |

## Fonctionnalités core validées

- Entités et value objects importés sans duplication locale
- Catalogue ``DefaultAuthCatalog`` (10 permissions, 4 rôles système)
- Ports synchrones repositories + UoW commit/rollback
- Erreurs techniques encapsulées (``AuthDatabaseMappingError``,
  ``AuthDatabasePersistenceError``)

## Notes

- Implémentation contre PyPI ``0.5.1`` (republication packaging de v0.5.0).
- PostgreSQL non testé en CI MVP ; SQLite mémoire + fichiers temporaires.
