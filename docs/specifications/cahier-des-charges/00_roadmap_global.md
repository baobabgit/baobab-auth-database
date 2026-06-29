# Roadmap globale — `baobab-auth-database` de `v0.1.0` à `v1.0.0`

> Destination : IA de développement  
> Projet : `baobab-auth-database`  
> Format : Markdown  
> Règle projet : ne jamais mentionner une IA comme contributeur, auteur ou co-auteur dans le code, la documentation, les commits ou les releases.  


## 1. Version finale retenue

La version finale proposée pour terminer le projet est `v1.0.0`.

Cette version correspond à une librairie stable, publiée, documentée, intégrable par les briques `baobab-auth-core`, `baobab-auth-security`, `baobab-auth-api`, `baobab-auth-admin`, `baobab-auth-client` et `baobab-auth-service`.

## 2. État initial supposé

Le dépôt possède déjà un socle avancé : SQLAlchemy, Alembic embarqué, repositories synchrones, adaptateurs async, Unit of Work, CLI, bootstrap catalogue et dépendance à `baobab-auth-core>=0.8.0,<1.0.0`. Les cahiers des charges ci-dessous ordonnent les corrections et compléments restant à produire.

## 3. Matrice des versions

| Version | Objectif | Core intégré | Validation externe obligatoire |
|---|---|---|---|
| `v0.1.0` | Stabiliser le MVP database : schéma, migrations, ORM, repositories, UoW | `baobab-auth-core>=0.8.0,<1.0.0` | Aucune autre librairie ; contrat core uniquement |
| `v0.2.0` | Catalogue RBAC versionné et diagnostics catalogue | `baobab-auth-core>=0.8.0,<1.0.0` | `baobab-auth-admin` ou CLI autonome |
| `v0.3.0` | Sessions, refresh tokens, révocation, JWK persistence | `baobab-auth-core>=0.8.0,<1.0.0` | `baobab-auth-security` |
| `v0.4.0` | Intégration fonctionnelle avec l’API auth | `baobab-auth-core>=0.8.0,<1.0.0` | `baobab-auth-api` + `baobab-auth-security` |
| `v0.5.0` | Exploitation PostgreSQL/Docker/service | `baobab-auth-core>=0.8.0,<1.0.0` | `baobab-auth-service` |
| `v0.6.0` | Administration avancée et diagnostics d’exploitation | `baobab-auth-core>=0.8.0,<1.0.0` | `baobab-auth-admin` |
| `v0.7.0` | Audit, pagination, lecture avancée et observabilité | `baobab-auth-core>=0.8.0,<1.0.0` | `baobab-auth-api` + `baobab-auth-admin` |
| `v0.8.0` | Cycle de vie utilisateur, suppression logique, anonymisation | `baobab-auth-core>=0.8.0,<1.0.0` | `baobab-auth-api` + `baobab-auth-admin` |
| `v0.9.0` | Durcissement production et release candidate | `baobab-auth-core>=0.8.0,<1.0.0`, préparation core `1.0` si disponible | stack complète |
| `v1.0.0` | Version stable finale | `baobab-auth-core>=0.8.0,<1.0.0` ou core `>=1.0.0,<2.0.0` si publié et validé | stack complète `baobab-auth` |

## 4. Règles transverses

Pour chaque version, l’IA de développement doit exécuter :

```bash
ruff check .
ruff format --check .
mypy
bandit -c pyproject.toml -r src
pip-audit
pytest --cov=src --cov-report=term-missing --cov-fail-under=90
python -m build
```

## 5. Principe de dépendance au core

`baobab-auth-database` implémente la persistance du core. Elle ne définit pas la logique métier. Le catalogue RBAC, les entités, les value objects, les statuts, les ports et les invariants doivent venir de `baobab-auth-core` lorsqu’ils existent.

## 6. Principe de validation inter-briques

Une version n’est considérée validée que si :

1. les tests internes passent ;
2. les tests de contrat avec `baobab-auth-core` passent ;
3. les migrations passent sur SQLite et PostgreSQL ;
4. la ou les briques indiquées dans la matrice consomment réellement `baobab-auth-database` sans contournement SQL direct.
