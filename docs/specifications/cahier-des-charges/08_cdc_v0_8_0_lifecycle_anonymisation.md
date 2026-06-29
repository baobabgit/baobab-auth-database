# Cahier des charges — `baobab-auth-database` `v0.8.0` — Cycle de vie utilisateur et anonymisation

> Destination : IA de développement  
> Projet : `baobab-auth-database`  
> Format : Markdown  
> Règle projet : ne jamais mentionner une IA comme contributeur, auteur ou co-auteur dans le code, la documentation, les commits ou les releases.  


## 1. Objectif de la version

Gérer techniquement le cycle de vie utilisateur : désactivation, réactivation, suppression logique, anonymisation contrôlée, révocation des sessions et audit non sensible.

## 2. Positionnement

```text
Version cible : v0.8.0
Dépendance core : `baobab-auth-core>=0.8.0,<1.0.0`
Validation externe : Validation obligatoire par `baobab-auth-api` et `baobab-auth-admin`.
```

## 3. Préconditions

`v0.7.0` validée, statuts utilisateurs du core stabilisés.

## 4. Périmètre inclus

- Persistance statuts utilisateur.
- Méthodes techniques lifecycle.
- Anonymisation email/profil.
- Révocation sessions sur suppression/anonymisation.
- Audit sans secret.
- Documentation conservation/anonymisation.

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

- Créer un composant technique `SqlAlchemyUserLifecycleRepository` ou équivalent.
- Anonymiser email, normalized_email, display_name, first_name, last_name et avatar si présent.
- Préserver les identifiants nécessaires aux liens et audits selon décision core/API.
- Révoquer toutes les sessions actives lors de l’anonymisation/suppression logique.
- Garantir que l’email anonymisé respecte les contraintes uniques.
- Documenter ce que database fait et ne fait pas juridiquement.

## 9. Tests obligatoires

- Désactivation.
- Réactivation.
- Suppression logique.
- Anonymisation email/profil.
- Unicité email après anonymisation.
- Révocation sessions.
- Audit sans données sensibles.
- Idempotence anonymisation.

## 10. Critères d’acceptation

- API/admin peuvent déclencher le lifecycle sans SQL direct.
- Les sessions sont révoquées.
- L’audit reste consultable et non sensible.
- Les contraintes uniques ne cassent pas.

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
