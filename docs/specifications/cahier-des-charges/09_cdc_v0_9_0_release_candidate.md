# Cahier des charges — `baobab-auth-database` `v0.9.0` — Durcissement production et release candidate

> Destination : IA de développement  
> Projet : `baobab-auth-database`  
> Format : Markdown  
> Règle projet : ne jamais mentionner une IA comme contributeur, auteur ou co-auteur dans le code, la documentation, les commits ou les releases.  


## 1. Objectif de la version

Préparer la version stable : concurrence, performance, compatibilité, API publique, migrations non régressives, documentation de migration et décision finale sur l’async.

## 2. Positionnement

```text
Version cible : v0.9.0
Dépendance core : `baobab-auth-core>=0.8.0,<1.0.0`, préparation core `1.0` si disponible
Validation externe : Validation par stack complète.
```

## 3. Préconditions

`v0.8.0` validée, toutes les briques principales disponibles.

## 4. Périmètre inclus

- Tests concurrence PostgreSQL.
- Benchmarks légers.
- Décision async finale.
- Audit des exports publics.
- Guide migration 0.x → 1.0.
- Matrice de compatibilité inter-briques.

## 5. Hors périmètre permanent

- Pas d’API HTTP dans `baobab-auth-database`.
- Pas de FastAPI.
- Pas de génération ou validation JWT.
- Pas de hash de mot de passe.
- Pas de logique métier applicative Riftbound, Altered ou autre.
- Pas de catalogue RBAC concurrent au core.
- Pas de stockage de secrets bruts.

## 6. Intégration avec `baobab-auth-core`

`baobab-auth-database` doit intégrer `baobab-auth-core>=0.8.0,<1.0.0`, préparation core `1.0` si disponible.

Règles obligatoires :

- importer les entités, value objects, statuts et ports réels du core lorsqu’ils existent ;
- importer `DefaultAuthCatalog` depuis le core ;
- ne pas dupliquer `User`, `Role`, `Permission`, `Session`, `AuditEvent`, `AuthSubject`, `Email`, `RoleName`, `PermissionName`, `SessionId`, `TokenId` ;
- transformer les erreurs techniques en exceptions database contrôlées ;
- ne jamais introduire de dépendance du core vers SQLAlchemy.

## 7. Intégration avec les autres librairies

Validation par stack complète.

La validation doit être réalisée par scénario réel ou par harness d’intégration documenté. Une simulation locale est acceptable uniquement si la brique externe n’est pas encore publiée.

## 8. Travaux d’implémentation détaillés

- Tester création concurrente même email et même auth_subject.
- Tester seed catalogue concurrent.
- Tester révocation concurrente de session.
- Tester unicité refresh_token_hash.
- Décider : wrapper async sync, vraie `AsyncSession`, ou double support.
- Lister tous les exports publics et retirer ceux qui ne doivent pas être SemVer-stables.
- Créer `docs/migration_to_1_0.md`.
- Préparer la compatibilité core 1.0 si publié, sans élargir la contrainte sans tests.

## 9. Tests obligatoires

- Tests concurrence PostgreSQL.
- Tests stack complète.
- Tests imports publics.
- Tests non-régression migrations.
- Tests CLI stable.
- Build docs strict.
- Build wheel/sdist et installation wheel.

## 10. Critères d’acceptation

- Aucune divergence catalogue.
- Aucune incohérence migration/modèle.
- Les intégrations externes passent.
- L’API publique est documentée.
- La stratégie async est décidée.

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
