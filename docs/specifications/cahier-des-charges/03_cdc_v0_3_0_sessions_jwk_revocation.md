# Cahier des charges — `baobab-auth-database` `v0.3.0` — Sessions, refresh tokens, révocation et JWK persistence

> Destination : IA de développement  
> Projet : `baobab-auth-database`  
> Format : Markdown  
> Règle projet : ne jamais mentionner une IA comme contributeur, auteur ou co-auteur dans le code, la documentation, les commits ou les releases.  


## 1. Objectif de la version

Finaliser la persistance nécessaire à la sécurité technique : sessions, empreintes de refresh tokens, révocation, clés JWK/JWKS, statuts et requêtes nécessaires à `baobab-auth-security`, sans implémenter la cryptographie dans database.

## 2. Positionnement

```text
Version cible : v0.3.0
Dépendance core : `baobab-auth-core>=0.8.0,<1.0.0`
Validation externe : Validation obligatoire par `baobab-auth-security`.
```

## 3. Préconditions

`v0.2.0` validée, catalogue versionné, tables sessions/JWK cohérentes.

## 4. Périmètre inclus

- Repository sessions complet.
- Repository JWK complet.
- Adaptateur async JWK.
- Révocation session unitaire et globale.
- Listing des sessions actives/expirées.
- Listing des JWK actives.
- Recherche JWK par `kid`.
- Préparation révocation par token id, session id, subject et key id.

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

Validation obligatoire par `baobab-auth-security`.

La validation doit être réalisée par scénario réel ou par harness d’intégration documenté. Une simulation locale est acceptable uniquement si la brique externe n’est pas encore publiée.

## 8. Travaux d’implémentation détaillés

- Ajouter `SqlAlchemyAsyncJwkKeyRepository` et l’exposer dans `SqlAlchemyAuthAsyncUnitOfWork.jwk_keys`.
- Compléter `SqlAlchemyJwkKeyRepository` : `get_current_signing_key`, `retire_key`, `revoke_key`, `list_by_status` si utile.
- Compléter les sessions : `delete_expired`, `list_expired`, `mark_used`, recherche par hash/token id selon le contrat retenu.
- Documenter clairement que le refresh token brut n’est jamais stocké.
- Clarifier la différence entre `refresh_token_hash`, `TokenId` et identifiant de session.
- Prévoir les points d’extension pour révocation enrichie.

## 9. Tests obligatoires

- Tests JWK sync et async.
- Tests `list_active`, `retire_key`, `revoke_key`.
- Tests session active, expirée, révoquée.
- Tests révocation globale avec exclusion de session courante.
- Tests unicité `session_id` et `refresh_token_hash`.
- Tests absence de clé privée/token brut dans logs et repr.
- Tests d’intégration simulée avec `baobab-auth-security`.

## 10. Critères d’acceptation

- `baobab-auth-security` peut stocker et lire les JWK.
- Les sessions persistées supportent login/refresh/logout/revoke.
- Aucun token brut n’est persisté.
- L’UoW async expose aussi les JWK.

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
