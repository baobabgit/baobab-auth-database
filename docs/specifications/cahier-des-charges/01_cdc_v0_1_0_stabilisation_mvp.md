# Cahier des charges — `baobab-auth-database` `v0.1.0` — Stabilisation MVP database

> Destination : IA de développement  
> Projet : `baobab-auth-database`  
> Format : Markdown  
> Règle projet : ne jamais mentionner une IA comme contributeur, auteur ou co-auteur dans le code, la documentation, les commits ou les releases.  


## 1. Objectif de la version

Stabiliser le socle minimal : configuration, modèles ORM, migrations Alembic, repositories synchrones, Unit of Work, mappers et bootstrap catalogue. Cette version doit garantir que le schéma réellement migré correspond aux modèles ORM et aux repositories utilisés.

## 2. Positionnement

```text
Version cible : v0.1.0
Dépendance core : `baobab-auth-core>=0.8.0,<1.0.0`
Validation externe : Aucune brique externe obligatoire ; validation par tests de contrat avec `baobab-auth-core`.
```

## 3. Préconditions

Le dépôt existe, le package est installable, `baobab-auth-core>=0.8.0,<1.0.0` est disponible, les outils qualité sont configurés.

## 4. Périmètre inclus

- Configuration `AuthDatabaseSettings`.
- Factories SQLAlchemy engine/session.
- Modèles ORM pour users, profiles, roles, permissions, user_roles, role_permissions, sessions, audit_events, jwk_keys.
- Migration Alembic initiale ou corrective alignée sur les modèles.
- Repositories synchrones principaux.
- Unit of Work synchrone avec commit/rollback.
- Mappers ORM ↔ core.
- CLI minimale migrations et seed defaults.
- Bootstrap idempotent à partir du `DefaultAuthCatalog` du core.

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

Aucune brique externe obligatoire ; validation par tests de contrat avec `baobab-auth-core`.

La validation doit être réalisée par scénario réel ou par harness d’intégration documenté. Une simulation locale est acceptable uniquement si la brique externe n’est pas encore publiée.

## 8. Travaux d’implémentation détaillés

- Comparer toutes les colonnes ORM avec les migrations et corriger les écarts : `auth_permissions.resource`, `auth_permissions.action`, `auth_permissions.is_system`, `auth_sessions.last_used_at`, `auth_sessions.device_label`, `auth_audit_events.target_type`, `auth_audit_events.target_id`.
- Créer une migration `0002` si la migration `0001` a déjà été utilisée ; sinon corriger `0001` avant publication.
- Vérifier toutes les contraintes uniques : `auth_subject`, `normalized_email`, rôle, permission, `session_id`, `refresh_token_hash`, `kid`.
- Finaliser `SqlAlchemyAuthUnitOfWork` avec tous les repositories synchrones : users, profiles, roles, permissions, sessions, audit, jwk_keys.
- Stabiliser les mappers et transformer toute erreur de conversion en `AuthDatabaseMappingError`.
- Garantir que `repr()` des modèles ne contient aucun `password_hash`, refresh token ou clé privée.

## 9. Tests obligatoires

- Tests unitaires settings, factories, naming convention.
- Tests mappers pour chaque entité core.
- Tests repositories SQLite mémoire.
- Tests Alembic `upgrade head`, `downgrade base`, `current`, `history`.
- Test automatisé de cohérence migration ↔ modèles ORM.
- Tests unicité email, subject, rôle, permission, session, refresh token hash, kid.
- Tests UoW commit et rollback.
- Tests absence de secrets dans `repr`.

## 10. Critères d’acceptation

- Base vierge migrable jusqu’à `head`.
- Le schéma migré contient toutes les colonnes utilisées par les modèles.
- Les repositories fonctionnent sur SQLite et PostgreSQL.
- Le bootstrap utilise le catalogue core sans catalogue métier local concurrent.
- Couverture >= 90 %.

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
