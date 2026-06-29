# Cahier des charges — `baobab-auth-database` `v0.7.0` — Audit, pagination et observabilité

> Destination : IA de développement  
> Projet : `baobab-auth-database`  
> Format : Markdown  
> Règle projet : ne jamais mentionner une IA comme contributeur, auteur ou co-auteur dans le code, la documentation, les commits ou les releases.  


## 1. Objectif de la version

Éviter que les briques consommatrices écrivent leurs propres requêtes SQL : fournir pagination, filtres, tri contrôlé, lectures audit/sessions/users/JWK et indexes adaptés.

## 2. Positionnement

```text
Version cible : v0.7.0
Dépendance core : `baobab-auth-core>=0.8.0,<1.0.0`
Validation externe : Validation obligatoire par `baobab-auth-api` et `baobab-auth-admin`.
```

## 3. Préconditions

`v0.6.0` validée, API/admin capables d’exposer des lectures avancées.

## 4. Périmètre inclus

- Pagination générique.
- Filtres utilisateurs.
- Filtres sessions.
- Filtres audit.
- Filtres JWK.
- Tri contrôlé.
- Indexes de lecture avancée.
- Métriques basiques.

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

Validation obligatoire par `baobab-auth-api` et `baobab-auth-admin`.

La validation doit être réalisée par scénario réel ou par harness d’intégration documenté. Une simulation locale est acceptable uniquement si la brique externe n’est pas encore publiée.

## 8. Travaux d’implémentation détaillés

- Créer `Page`, `PageRequest`, `SortSpec` ou utiliser les DTO du core s’ils existent.
- Ajouter `list_users_paginated`, `search_users_by_email`, `list_users_by_status`.
- Ajouter `list_sessions_paginated`, `list_sessions_by_status`, `list_sessions_expiring_before`.
- Ajouter `list_audit_events_paginated`, `list_by_actor_subject`, `list_by_target_subject`, `list_by_event_type`, `list_by_time_range`.
- Ajouter indexes : audit event_type/actor/target/occurred_at, sessions user/status/expires_at, jwk status.
- Documenter que toute liste admin doit être paginée.

## 9. Tests obligatoires

- Pagination stable.
- Tri stable.
- Filtres audit.
- Filtres sessions.
- Filtres users.
- Tests indexes via migration/inspection.
- Tests API/admin utilisant ces lectures.

## 10. Critères d’acceptation

- API/admin n’ont plus besoin de SQL direct pour les lectures.
- Les lectures sont paginées.
- Les indexes requis sont présents.
- L’audit reste append-only.

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
