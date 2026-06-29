# Prompts de rôle — BL-002

## Product Owner (Spec)

Vérifier les 9 tables, colonnes CDC (`resource`, `action`, `is_system`,
`last_used_at`, `device_label`, `target_type`, `target_id`, `refresh_token_hash`),
contraintes d'unicité et absence de secrets dans `repr()`.

## Architecte (Design)

Valider le registre ORM, la base déclarative, le mapping table ↔ entité future,
cohérence avec `AuthTableNamingConvention`.

## Développeur (In progress)

Tests : `create_all` SQLite, contraintes, registry, repr sécurisé.

## Ingénieur QA (In review — tests)

Couverture modèles ≥ 95 % (global projet), tests registry + create_all.

## Relecteur (In review — code)

Revue sécurité `repr()`, redondance contraintes, conformité CDC colonnes.
