# Context — BL-005

## État au démarrage

- BL-003 (migrations) et BL-004 (mappers) mergés sur `version/v0.1.0`.
- Ports core disponibles dans `baobab_auth_core.ports.*` (core 0.5.1).
- ADR-001 prévoit la couche `repositories/`.

## Objectif

Exposer la persistance synchrone via des repositories testables, prêts pour
l'injection dans `SqlAlchemyAuthUnitOfWork` (BL-006).

## Références

- FEAT-003.1
- ADR-001 § repositories
- Handoff BL-004 : mappers validés, F4-1 clos
