# Cahier des charges — `baobab-auth-database` `v0.2.0` — Catalogue RBAC versionné et diagnostics

> Destination : IA de développement  
> Projet : `baobab-auth-database`  
> Format : Markdown  
> Règle projet : ne jamais mentionner une IA comme contributeur, auteur ou co-auteur dans le code, la documentation, les commits ou les releases.  


## 1. Objectif de la version

Rendre le catalogue RBAC exploitable en production : seed idempotent, détection de dérive, version de catalogue, checksum, rapport textuel/JSON et stratégie claire de profil de compatibilité.

## 2. Positionnement

```text
Version cible : v0.2.0
Dépendance core : `baobab-auth-core>=0.8.0,<1.0.0`
Validation externe : Validation par `baobab-auth-admin` si disponible ; sinon CLI `baobab-auth-db`.
```

## 3. Préconditions

`v0.1.0` validée, migration cohérente, `DefaultAuthCatalog` importable depuis le core.

## 4. Périmètre inclus

- Table `auth_catalog_versions`.
- Checksum déterministe du catalogue core.
- Commandes CLI `catalog check`, `catalog seed`, `catalog report`.
- Option `--format json` pour les rapports.
- Détection des rôles/permissions manquants ou obsolètes.
- Détection des mappings rôle → permissions divergents.
- Documentation du profil prioritaire `core_080`.

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

Validation par `baobab-auth-admin` si disponible ; sinon CLI `baobab-auth-db`.

La validation doit être réalisée par scénario réel ou par harness d’intégration documenté. Une simulation locale est acceptable uniquement si la brique externe n’est pas encore publiée.

## 8. Travaux d’implémentation détaillés

- Créer la migration de `auth_catalog_versions` avec `id`, `core_version`, `compat_profile`, `catalog_checksum`, `applied_at`, `applied_by`, `metadata_json`.
- Calculer un checksum stable à partir des rôles, permissions, mappings et descriptions contractuelles.
- Enregistrer une ligne de version catalogue après chaque seed réussi.
- Clarifier `--profile` : soit profil unique `core_080`, soit vrais profils figés ; éviter un `core_040` décoratif qui utilise le catalogue du core installé.
- Ajouter `catalog sync --dry-run` ou documenter que `catalog seed` est l’opération de synchronisation non destructive.
- Garantir que les permissions obsolètes `auth:permission:read`, `auth:permission:write`, `auth:jwk:write` ne sont jamais recréées si le core ne les expose pas.

## 9. Tests obligatoires

- Checksum déterministe.
- Seed catalogue idempotent.
- Check conforme → exit code 0.
- Check divergent → exit code 1.
- Report JSON stable.
- Version catalogue enregistrée.
- SERVICE sans permission.
- SUPER_ADMIN possède toutes les permissions exposées par le core.

## 10. Critères d’acceptation

- La base peut prouver quel catalogue a été appliqué.
- Le diagnostic détecte les divergences sans modifier la base.
- Le rapport est exploitable par `baobab-auth-admin`.
- Le profil de compatibilité est cohérent avec la dépendance réelle au core.

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
