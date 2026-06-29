# Cahier des charges — `baobab-auth-database` `v0.5.0` — Exploitation Docker/PostgreSQL et service complet

> Destination : IA de développement  
> Projet : `baobab-auth-database`  
> Format : Markdown  
> Règle projet : ne jamais mentionner une IA comme contributeur, auteur ou co-auteur dans le code, la documentation, les commits ou les releases.  


## 1. Objectif de la version

Rendre la librairie exploitable dans une stack Docker/PostgreSQL : migrations au démarrage, diagnostics de migration, bootstrap contrôlé, erreurs masquées et guides d’exploitation.

## 2. Positionnement

```text
Version cible : v0.5.0
Dépendance core : `baobab-auth-core>=0.8.0,<1.0.0`
Validation externe : Validation obligatoire par `baobab-auth-service`.
```

## 3. Préconditions

`v0.4.0` validée avec API, migrations stables sur PostgreSQL.

## 4. Périmètre inclus

- Guide PostgreSQL.
- Guide intégration service.
- Commande `check-migrations`.
- Diagnostic `heads`.
- Validation base vide.
- Masquage URL database dans les erreurs.
- Tests testcontainers.

## 5. Hors périmètre permanent

- Pas d’API HTTP dans `baobab-auth-database`.
- Pas de FastAPI.
- Pas de génération ou validation JWT.
- Pas de hash de mot de passe.
- Pas de logique métier applicative Riftbound, Altered ou autre.
- Pas de catalogue RBAC concurrent au core.
- Pas de stockage de secrets bruts.

## 6. Intégration avec `baobab-auth-core`

`baobab-auth-database` doit intégrer `baobab-auth-core>=0.8.0,<1.0.0`.

Règles obligatoires :

- importer les entités, value objects, statuts et ports réels du core lorsqu’ils existent ;
- importer `DefaultAuthCatalog` depuis le core ;
- ne pas dupliquer `User`, `Role`, `Permission`, `Session`, `AuditEvent`, `AuthSubject`, `Email`, `RoleName`, `PermissionName`, `SessionId`, `TokenId` ;
- transformer les erreurs techniques en exceptions database contrôlées ;
- ne jamais introduire de dépendance du core vers SQLAlchemy.

## 7. Intégration avec les autres librairies

Validation obligatoire par `baobab-auth-service`.

La validation doit être réalisée par scénario réel ou par harness d’intégration documenté. Une simulation locale est acceptable uniquement si la brique externe n’est pas encore publiée.

## 8. Travaux d’implémentation détaillés

- Créer `docs/operations/postgresql.md`, `docs/guides/service_integration.md`, `docs/operations/migrations_startup.md`.
- Ajouter `baobab-auth-db check-migrations` qui vérifie connectivité, révision courante, head unique et table Alembic.
- Documenter la séquence `upgrade head`, `catalog check`, `catalog seed`.
- Tester PostgreSQL via testcontainers en CI.
- Garantir que les URLs masquées n’exposent jamais le mot de passe.

## 9. Tests obligatoires

- Migration PostgreSQL from scratch.
- Seed PostgreSQL.
- Rollback UoW PostgreSQL.
- Check migrations base à jour.
- Check migrations base non migrée.
- Masquage URL en cas d’erreur.
- Stack docker-compose minimale si disponible.

## 10. Critères d’acceptation

- `baobab-auth-service` démarre avec une base vierge.
- Les migrations sont vérifiables au démarrage.
- Le catalogue est vérifiable en Docker/PostgreSQL.
- Aucun secret database n’est logué.

## 11. Documentation attendue

Mettre à jour ou créer :

```text
README.md
CHANGELOG.md
docs/specifications/
docs/guides/
docs/api/
docs/operations/
```

La documentation doit préciser : version core supportée, migrations, commandes CLI, exemples d’usage, limites connues, stratégie de sécurité, critères d’intégration externe.

## 12. Commandes de validation

```bash
ruff check .
ruff format --check .
mypy
bandit -c pyproject.toml -r src
pip-audit
pytest --cov=src --cov-report=term-missing --cov-fail-under=90
python -m build
```

## 13. Condition de passage à la version suivante

- Tous les critères d’acceptation sont validés.
- Les migrations sont rejouables depuis une base vierge.
- La brique externe de validation consomme réellement la librairie lorsqu’elle est obligatoire.
- Le changelog est mis à jour.
- La version est taguée si publiée.
