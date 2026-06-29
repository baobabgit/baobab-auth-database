# Worklog — BL-006

## 2026-06-29 — Product Owner (Spec → Design)

**Gate Spec — Done**

| Critère FEAT-003.2 | Statut |
|--------------------|--------|
| Protocole `UnitOfWork` core | OK |
| Expose users, profiles, roles, permissions, sessions, audit, jwk_keys | OK |
| Tests commit et rollback | OK |

**Handoff PO → Architecte** : Spec validée.

---

## 2026-06-29 — Architecte (Design → In progress)

**Gate Design — Done**

- Injection `SqlAlchemySessionFactory` (composition, pas de singleton).
- Session créée dans `__enter__`, fermée dans `__exit__`.
- Repositories lazy partageant la session ; rollback si exception propagée.
- UoW hors `__all__` jusqu'à BL-008.

**Handoff Architecte → Développeur** : TASK-003.2.1 / 003.2.2 prêtes.

---

## 2026-06-29 — Développeur (In progress → In review)

- `SqlAlchemyAuthUnitOfWork` + 7 tests UoW.
- `uv run nox -s all` : 82 tests, 96,02 %.
- PR ouverte vers `version/v0.1.0` (process strict).

**Handoff Dev → QA** : en attente CI verte.
