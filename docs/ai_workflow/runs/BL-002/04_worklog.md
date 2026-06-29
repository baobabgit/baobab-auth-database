# Worklog — BL-002

## 2026-06-28 — Product Owner (Spec → Design)

**Gate Spec — Done**

| Exigence CDC §5 | Statut | Preuve |
|-----------------|--------|--------|
| 9 tables `auth_*` | OK | registry 9 modèles |
| Colonnes métier CDC | OK | tests colonnes présentes |
| Unicité subject, email, role, permission, refresh_token_hash, kid | OK | `__table_args__` |
| `repr()` sans password / refresh token / clé privée | OK | tests repr User, Session, JWK |
| Associations N-N user↔role, role↔permission | OK | tables pivot |

**Handoff PO → Architecte** : Spec validée.

---

## 2026-06-28 — Architecte (Design → In progress)

**Gate Design — Done**

- Hiérarchie : `AuthOrmBase` (DeclarativeBase) + `AuthOrmRegistry` (liste ordonnée pour Alembic).
- Pas de relations ORM lazy (composition explicite via repositories — ADR-001).
- Nommage tables via `AuthTableNamingConvention.table_name(...)`.

**Handoff Architecte → Développeur** : design figé.

---

## 2026-06-28 — Développeur (In progress → In review)

10 tests ORM (create_all, contraintes, registry, repr).

**Handoff Dev → QA** : modèles prêts.

---

## 2026-06-28 — Ingénieur QA (rétroactif)

Voir `05_tests_report.md`. Verdict : **QA_PASSED**.

---

## 2026-06-28 — Relecteur (rétroactif)

Voir `06_review.md`. Verdict : **APPROUVÉ** avec observation contrainte session.
