# Périmètre — v0.1.0

## Objectif

Stabiliser le socle MVP database : configuration, modèles ORM, migrations Alembic,
repositories synchrones, Unit of Work, mappers et bootstrap catalogue.

Source : `docs/specifications/cahier-des-charges/01_cdc_v0_1_0_stabilisation_mvp.md`

## Backlogs inclus

| ID | Titre | Priorité |
|----|-------|---------|
| BL-001 | Configuration AuthDatabaseSettings et factories SQLAlchemy | P0 |
| BL-002 | Modèles ORM auth (9 tables) | P0 |
| BL-003 | Migrations Alembic et cohérence schéma | P0 |
| BL-004 | Mappers ORM vers entités core | P1 |
| BL-005 | Repositories synchrones SQLAlchemy | P0 |
| BL-006 | SqlAlchemyAuthUnitOfWork | P0 |
| BL-007 | CLI migrations et bootstrap DefaultAuthCatalog | P1 |
| BL-008 | Tests contrat core et documentation v0.1.0 | P1 |

## Backlogs reportés

Aucun — périmètre v0.2.0+ couvert par les cahiers des charges suivants.
