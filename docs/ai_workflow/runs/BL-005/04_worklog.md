# Worklog — BL-005

## 2026-06-28 — Product Owner (Spec → Design)

**Gate Spec — Done**

| Critère FEAT-003.1 | Statut | Preuve |
|--------------------|--------|--------|
| Port `UserRepository` | OK | `SqlAlchemyUserRepository` |
| Port `RoleRepository` | OK | `SqlAlchemyRoleRepository` |
| Port `PermissionRepository` | OK | `SqlAlchemyPermissionRepository` |
| Port `SessionRepository` | OK | `SqlAlchemySessionRepository` |
| Port `AuditRepository` | OK | `SqlAlchemyAuditRepository` |
| Profils | OK | `SqlAlchemyUserProfileRepository` (pas de port 0.5.1) |
| JWK | OK | `SqlAlchemyJwkKeyRepository` (snapshot local) |
| Unicité email, subject, role, permission, refresh token, kid | OK | tests dédiés |
| SQLite mémoire | OK | fixture `db_session` |

**Handoff PO → Architecte** : Spec validée.

---

## 2026-06-28 — Architecte (Design → In progress)

**Gate Design — Done**

- Injection `Session` + mappers (composition, pas de singleton).
- Sync explicite `auth_user_roles` / `auth_role_permissions` (pas de lazy ORM).
- `SqlAlchemyPersistenceGuard` centralise `IntegrityError` → `AuthDatabasePersistenceError`.
- Repositories **non** exportés dans `__all__` (contrat public = BL-008 / UoW BL-006).

**Handoff Architecte → Développeur** : TASK-003.1.1 à 003.1.3 prêtes.

---

## 2026-06-28 — Développeur (In progress → In review)

- 8 modules repository + exception persistance.
- 22 tests repositories (+ fixtures conftest).
- Commits `68ee61b`, merge `1a4fc3b` sur `version/v0.1.0`.

**Handoff Dev → QA** : code prêt pour revue qualité.

---

## 2026-06-29 — Ingénieur QA (In review)

Exécution gate U2 (2026-06-29) :

- `black --check` : OK (après format session test)
- `ruff` : OK
- `mypy` strict : OK
- `bandit` : OK
- `pytest --cov-fail-under=95` : 75 tests, 96,34 %
- `check_traceability` : OK

Verdict : **QA_PASSED**. Voir `05_tests_report.md`.

**Handoff QA → Relecteur** : revue technique.

---

## 2026-06-29 — Relecteur (In review)

Voir `06_review.md`. Verdict : **APPROUVÉ** (observations process PR).

**Handoff Relecteur → BL-006** : voir `07_handoff.md`.
