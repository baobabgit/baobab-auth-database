# ADR-001 — Architecture persistance v0.1.0

## Statut

Accepté — 2026-06-28

## Contexte

Le cahier des charges v0.1.0 exige une librairie de persistance pour l'écosystème
Baobab Auth, sans logique métier locale, intégrée à `baobab-auth-core`.

Le dépôt part d'un template Python ; il n'existe pas encore de code SQLAlchemy.
La roadmap mentionne un socle avancé préexistant qui n'est pas présent dans Git.

## Décision

1. **Package** : `baobab_auth_database` (1 classe = 1 fichier).
2. **Couches** :
   - `settings/` — configuration `AuthDatabaseSettings` (pydantic-settings)
   - `factories/` — engine et session SQLAlchemy
   - `models/orm/` — modèles SQLAlchemy (tables `auth_*`)
   - `mappers/` — conversion ORM ↔ entités core
   - `repositories/` — implémentations des ports core
   - `unit_of_work/` — `SqlAlchemyAuthUnitOfWork`
   - `bootstrap/` — seed catalogue via `DefaultAuthCatalog`
   - `cli/` — migrations et commandes opérationnelles
   - `exceptions/` — `AuthDatabaseMappingError`, erreurs persistance
3. **Migrations** : Alembic embarqué dans le package.
4. **Async** : hors périmètre v0.1.0 (repositories synchrones uniquement).
5. **Contrat public** : factories, settings, UoW, CLI, exceptions exportées dans `__all__`.
6. **Core** : entités, ports et catalogue importés depuis `baobab-auth-core` ; pas de duplication.

## Conséquences

- Construction greenfield complète du MVP database.
- Dépendances runtime : `baobab-auth-core`, `sqlalchemy`, `alembic`, `pydantic-settings`.
- Tests miroir sous `tests/unit/baobab_auth_database/`.
- Tests contrat sous `tests/contracts/`.

## Points ouverts (décision utilisateur requise)

~~1. Version core~~ — **Résolu** : implémentation contre `baobab-auth-core>=0.5.1,<0.6.0` jusqu'à publication 0.8.0.

~~2. Socle préexistant~~ — **Résolu** : implémentation greenfield complète.
