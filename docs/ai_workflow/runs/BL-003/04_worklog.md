# Worklog — BL-003

## 2026-06-28 — Product Owner (Spec → Design)

**Gate Spec — Done**

| Critère FEAT-002.2 | Statut |
|--------------------|--------|
| upgrade head sur base vierge | OK |
| downgrade base | OK |
| current / history via migrator | OK |
| Révision initiale 0001 | OK |

| Critère FEAT-002.3 | Statut |
|--------------------|--------|
| Comparaison tables/colonnes migration vs ORM | OK |
| Test contrat automatisé | OK |

**Écart assumé** : pas de commande CLI publique (FEAT-002.2 mentionne CLI) → BL-007.

**Handoff PO → Architecte** : Spec validée avec réserve CLI.

---

## 2026-06-28 — Architecte (Design → In progress)

**Gate Design — Done**

- `AuthDatabaseMigrator` encapsule API Alembic (upgrade, downgrade, current, history).
- `MigrationOrmConsistencyChecker` compare metadata ORM vs révision appliquée.
- `env.py` charge settings via factory — exclu couverture (`pyproject.toml`).

---

## 2026-06-28 — Développeur → QA → Relecteur (rétroactif)

6 tests unitaires migrations + 4 tests contrat. Voir rapports 05/06.
