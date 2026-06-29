# Worklog — BL-001

## 2026-06-28 — Product Owner (Spec → Design)

**Gate Spec — Done**

| Critère FEAT-001.1 | Statut | Preuve |
|--------------------|--------|--------|
| Préfixe `AUTH_DB_` | OK | `SettingsConfigDict(env_prefix="AUTH_DB_")` |
| Validation sqlite/postgresql | OK | `_SUPPORTED_BASE_SCHEMES`, tests schéma invalide |
| `repr()` sans secret | OK | `test_FEAT_001_1_repr_sans_secret` |
| Défaut SQLite mémoire | OK | `sqlite:///:memory:` |

| Critère FEAT-001.2 | Statut | Preuve |
|--------------------|--------|--------|
| Engine configuré (pool, echo) | OK | tests SQLite + mock PostgreSQL |
| Session factory | OK | `test_FEAT_001_2_create_session_sqlite_memoire` |
| Convention `auth_*` | OK | `AuthTableNamingConvention.table_name("users")` → `auth_users` |

**Écart documenté** : la spec FEAT-001.1 mentionne le « préfixe de tables » dans
`AuthDatabaseSettings` ; l'ADR-001 sépare `AuthTableNamingConvention` — cohérent
architecturalement, spec RST à ajuster en note (non bloquant).

**Handoff PO → Architecte** : Spec validée.

---

## 2026-06-28 — Architecte (Design → In progress)

**Gate Design — Done**

| FEAT | Classes |
|------|---------|
| FEAT-001.1 | `AuthDatabaseSettings` |
| FEAT-001.2 | `SqlAlchemyEngineFactory`, `SqlAlchemySessionFactory`, `AuthTableNamingConvention` |

- 1 classe = 1 fichier respecté.
- Contrat public initial dans `__all__` : settings, factories, naming.
- ADR-001 § couches `settings/`, `factories/`, `naming/`.

**Handoff Architecte → Développeur** : TASK-001.1.1, TASK-001.2.1 prêtes.

---

## 2026-06-28 — Développeur (In progress → In review)

Implémentation et 12 tests initiaux (settings, naming, factories).
Bootstrap package `baobab-auth-database` dans `pyproject.toml`.

**Handoff Dev → QA** : code prêt pour revue qualité.

---

## 2026-06-28 — Ingénieur QA (rétroactif)

Voir `05_tests_report.md`. Verdict : **QA_PASSED**.

---

## 2026-06-28 — Relecteur (rétroactif)

Voir `06_review.md`. Verdict : **APPROUVÉ** (observations mineures).
