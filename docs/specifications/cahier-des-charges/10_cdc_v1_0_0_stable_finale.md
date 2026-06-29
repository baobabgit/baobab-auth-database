# Cahier des charges — `baobab-auth-database` `v1.0.0` — Version stable finale

> Destination : IA de développement  
> Projet : `baobab-auth-database`  
> Format : Markdown  
> Règle projet : ne jamais mentionner une IA comme contributeur, auteur ou co-auteur dans le code, la documentation, les commits ou les releases.  


## 1. Objectif de la version

Publier la version stable finale de `baobab-auth-database` avec API publique figée, migrations fiables, diagnostics, documentation complète et intégration validée avec toutes les briques de l’écosystème.

## 2. Positionnement

```text
Version cible : v1.0.0
Dépendance core : `baobab-auth-core>=0.8.0,<1.0.0` ou `>=1.0.0,<2.0.0` si core 1.0 est publié et validé
Validation externe : Validation obligatoire par la stack complète `baobab-auth`.
```

## 3. Préconditions

`v0.9.0` validée, aucune anomalie critique ouverte, documentation complète.

## 4. Périmètre inclus

- API publique stable.
- Migrations stables.
- Catalogue RBAC versionné.
- Repositories sync/async selon décision finale.
- CLI stable.
- Diagnostics exploitation.
- Tests inter-briques.
- Release GitHub et publication PyPI.

## 5. Hors périmètre permanent

- Pas d’API HTTP dans `baobab-auth-database`.
- Pas de FastAPI.
- Pas de génération ou validation JWT.
- Pas de hash de mot de passe.
- Pas de logique métier applicative Riftbound, Altered ou autre.
- Pas de catalogue RBAC concurrent au core.
- Pas de stockage de secrets bruts.

## 6. Intégration avec `baobab-auth-core`

`baobab-auth-database` doit intégrer `baobab-auth-core>=0.8.0,<1.0.0` ou `>=1.0.0,<2.0.0` si core 1.0 est publié et validé.

Règles obligatoires :

- importer les entités, value objects, statuts et ports réels du core lorsqu’ils existent ;
- importer `DefaultAuthCatalog` depuis le core ;
- ne pas dupliquer `User`, `Role`, `Permission`, `Session`, `AuditEvent`, `AuthSubject`, `Email`, `RoleName`, `PermissionName`, `SessionId`, `TokenId` ;
- transformer les erreurs techniques en exceptions database contrôlées ;
- ne jamais introduire de dépendance du core vers SQLAlchemy.

## 7. Intégration avec les autres librairies

Validation obligatoire par la stack complète `baobab-auth`.

La validation doit être réalisée par scénario réel ou par harness d’intégration documenté. Une simulation locale est acceptable uniquement si la brique externe n’est pas encore publiée.

## 8. Travaux d’implémentation détaillés

- Figer les exports publics : settings, factories, MigrationRunner, UoW, repositories, exceptions, testing helpers.
- Figer les commandes CLI : upgrade, downgrade, current, history, heads, seed-defaults, catalog, doctor, check-migrations, check-indexes, check-orphans.
- Publier les guides installation, configuration, migrations, catalog, repositories, UoW, api/admin/security/service integration, operations, migration_to_1_0.
- Valider la matrice complète : core+database, +security, +api, +admin, +client via API, service Docker/PostgreSQL.
- Créer tag `v1.0.0`, release GitHub et publication PyPI selon workflow projet.

## 9. Tests obligatoires

- Tous les tests unitaires.
- Tous les tests SQLite/PostgreSQL.
- Tous les tests contrat core.
- Tous les tests catalogue.
- Tous les tests CLI.
- Tous les tests concurrence.
- Tous les tests inter-briques.
- Build docs strict.
- Installation depuis wheel dans un projet vierge.

## 10. Critères d’acceptation

- Package installable et utilisable depuis PyPI/artifact.
- Base complète migrable depuis zéro.
- API/admin/security/service consomment réellement database.
- Client valide un scénario end-to-end via API.
- SemVer documenté.
- Changelog et release notes complets.

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
