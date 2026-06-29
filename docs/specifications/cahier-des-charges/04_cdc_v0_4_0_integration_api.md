# Cahier des charges — `baobab-auth-database` `v0.4.0` — Intégration fonctionnelle avec `baobab-auth-api`

> Destination : IA de développement  
> Projet : `baobab-auth-database`  
> Format : Markdown  
> Règle projet : ne jamais mentionner une IA comme contributeur, auteur ou co-auteur dans le code, la documentation, les commits ou les releases.  


## 1. Objectif de la version

Valider la librairie dans une vraie API d’authentification assemblant core + security + database. Les flux applicatifs principaux doivent fonctionner avec PostgreSQL et transactions réelles.

## 2. Positionnement

```text
Version cible : v0.4.0
Dépendance core : `baobab-auth-core>=0.8.0,<1.0.0`
Validation externe : Validation obligatoire par `baobab-auth-api` et `baobab-auth-security`.
```

## 3. Préconditions

`v0.3.0` validée, security disponible ou simulable, API prête à consommer une UoW.

## 4. Périmètre inclus

- Flux register.
- Flux login.
- Flux logout.
- Flux refresh.
- Endpoint ou use case `/me`.
- List roles/permissions.
- JWKS read via persistence.
- Assign/remove role.
- Audit des événements sensibles.

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

Validation obligatoire par `baobab-auth-api` et `baobab-auth-security`.

La validation doit être réalisée par scénario réel ou par harness d’intégration documenté. Une simulation locale est acceptable uniquement si la brique externe n’est pas encore publiée.

## 8. Travaux d’implémentation détaillés

- Documenter l’injection d’UoW par requête API.
- Fournir un exemple d’assemblage `AuthDatabaseSettings` → engine → session_factory → UoW.
- Harmoniser `AuditRepository.save` vs `append` selon le port core réel.
- Ajouter des tests de scénario applicatif sans dépendance HTTP.
- Transformer proprement les erreurs SQL en exceptions database contrôlées.
- Empêcher les accès directs aux modèles ORM depuis l’API.

## 9. Tests obligatoires

- Register persiste user + profile + rôle USER.
- Login crée session + audit.
- Refresh met à jour session/last_used_at.
- Logout révoque session.
- Assign/remove role persiste les associations.
- Rollback si une étape échoue.
- Tests PostgreSQL via API ou harness d’intégration.

## 10. Critères d’acceptation

- `baobab-auth-api` utilise database sans requêtes SQL directes.
- Les principaux flux auth fonctionnent avec PostgreSQL.
- Les transactions sont atomiques.
- Aucune logique HTTP n’est introduite dans database.

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
