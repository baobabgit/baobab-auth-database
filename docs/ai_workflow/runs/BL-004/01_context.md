# Context — BL-004

## Prérequis

Modèles ORM (BL-002). Dépendance `baobab-auth-core>=0.5.1,<0.6.0` (D1).

## Objectif

Isoler la conversion ORM ↔ entités core pour que les repositories (BL-005)
manipulent uniquement le domaine.

## Références

- ADR-001 § mappers
- FEAT-004.1
- D1 : core 0.5.1 vs CDC >=0.8.0 — JWK via snapshot local
