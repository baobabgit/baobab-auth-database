# Context — BL-007

## État au démarrage

- BL-006 mergé : `SqlAlchemyAuthUnitOfWork` opérationnel.
- `AuthDatabaseMigrator` (BL-003) prêt pour la CLI.
- `DefaultAuthCatalog` disponible dans `baobab_auth_core.domain.catalogs`.

## Objectif

Exposer migrations et bootstrap catalogue via CLI embarquée ; process PR → CI → merge.

## Références

- FEAT-005.1, FEAT-005.2
- Handoff BL-006
