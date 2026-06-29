# Handoff — BL-001

## État

| Champ | Valeur |
|-------|--------|
| Backlog | BL-001 |
| Statut | TECH_REVIEW_PASSED |
| Gates | Spec ✓ Design ✓ QA ✓ Review ✓ |
| Prochain backlog | BL-002 |

## Réalisé

- Package `baobab_auth_database` initialisé.
- `AuthDatabaseSettings`, factories SQLAlchemy, convention de nommage.
- 12 tests unitaires, couverture 100 % sur le périmètre.
- Revue PO → Architecte → QA → Relecteur complétée (2026-06-28).

## Points d'attention pour BL-002

- Réutiliser `AuthTableNamingConvention` pour nommer les 9 tables ORM.
- Enregistrer les modèles via `AuthOrmRegistry` + `AuthOrmBase`.
- Colonnes CDC §5 : `resource`, `action`, `is_system`, etc.

## Dette / suivi

- README template → BL-008.
- Branches Git `version/v0.1.0` / `bl/001-...` à créer avant commit officiel.
- FEAT-001.1 RST : préciser séparation naming vs settings.

## Commandes de reprise

```bash
uv sync
uv run pytest tests/unit/baobab_auth_database/settings/ \
  tests/unit/baobab_auth_database/naming/ \
  tests/unit/baobab_auth_database/factories/ -q
make traceability
```

## Fichiers clés

- `src/baobab_auth_database/settings/auth_database_settings.py`
- `src/baobab_auth_database/factories/sqlalchemy_engine_factory.py`
- `src/baobab_auth_database/naming/auth_table_naming_convention.py`
