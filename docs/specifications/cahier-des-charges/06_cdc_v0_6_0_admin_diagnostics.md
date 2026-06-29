# Cahier des charges — `baobab-auth-database` `v0.6.0` — Administration avancée et diagnostics

> Destination : IA de développement  
> Projet : `baobab-auth-database`  
> Format : Markdown  
> Règle projet : ne jamais mentionner une IA comme contributeur, auteur ou co-auteur dans le code, la documentation, les commits ou les releases.  


## 1. Objectif de la version

Fournir les primitives de diagnostic et d’administration database : doctor, indexes, orphelins, cohérence RBAC, sessions, JWK et sorties JSON stables.

## 2. Positionnement

```text
Version cible : v0.6.0
Dépendance core : `baobab-auth-core>=0.8.0,<1.0.0`
Validation externe : Validation obligatoire par `baobab-auth-admin`.
```

## 3. Préconditions

`v0.5.0` validée, service exploitable, admin disponible ou en cours.

## 4. Périmètre inclus

- Commande `doctor`.
- Commande `check-indexes`.
- Commande `check-orphans`.
- Rapports JSON stables.
- Vérification statut sessions/JWK.
- Réparations non destructives en dry-run.

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

Validation obligatoire par `baobab-auth-admin`.

La validation doit être réalisée par scénario réel ou par harness d’intégration documenté. Une simulation locale est acceptable uniquement si la brique externe n’est pas encore publiée.

## 8. Travaux d’implémentation détaillés

- Implémenter `doctor` : DB, Alembic, tables, catalogue, indexes, orphelins, sessions, JWK.
- Implémenter `check-orphans` pour user_roles, role_permissions, sessions, profiles.
- Implémenter `check-indexes` pour contraintes et indexes critiques.
- Créer une sortie JSON versionnée pour chaque diagnostic.
- Documenter les commandes lecture seule et les commandes de réparation.

## 9. Tests obligatoires

- Doctor base saine.
- Doctor base non migrée.
- Doctor catalogue divergent.
- Check orphans avec données corrompues contrôlées.
- Check indexes.
- Sortie JSON stable.
- Les diagnostics lecture seule ne modifient pas la base.

## 10. Critères d’acceptation

- `baobab-auth-admin` consomme les diagnostics sans accès SQL direct.
- Les sorties JSON sont documentées et stables.
- Toute réparation est explicitement demandée et dry-run par défaut.

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
