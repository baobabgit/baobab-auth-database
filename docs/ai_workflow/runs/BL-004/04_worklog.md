# Worklog — BL-004

## 2026-06-28 — Product Owner (Spec → Design)

**Gate Spec — Done**

| Critère FEAT-004.1 | Statut |
|--------------------|--------|
| User + Profile roundtrip | OK |
| Role + Permission + associations | OK (paramètres explicites) |
| Session (refresh_token_id ↔ hash) | OK |
| AuditEvent | OK |
| JWK via snapshot | OK (core 0.5.1) |
| `AuthDatabaseMappingError` | OK |

**Écart D1** : entité JWK absente du core 0.5.1 — `AuthJwkKeySnapshot` documenté ADR-001.

**Handoff PO → Architecte** : Spec validée.

---

## 2026-06-28 — Architecte (Design → Dev)

- Converter centralise enums/statuts/dates.
- User/Role mappers reçoivent collections rôles/permissions (évite relations ORM).
- Exception unique `AuthDatabaseMappingError` pour conversions invalides.

---

## 2026-06-28 — Dev → QA → Relecteur

19 tests mappers. Couverture globale 95,24 % ; fichiers mapper individuels 79–90 %
(branches `to_model` except).
