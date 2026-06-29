# Revue technique — BL-002

**Relecteur** : relecteur (rétroactif)  
**Date** : 2026-06-28  
**Verdict** : **APPROUVÉ**

## Checklist AGENTS.md

| Critère | Statut |
|---------|--------|
| 1 classe = 1 fichier | OK (11 fichiers) |
| Type hints Mapped[...] | OK |
| Docstrings RST + `:spec: FEAT-002.1` | OK |
| Tests miroir | OK |
| Pas de logique module-level | OK |

## Conformité CDC §5

| Table | Colonnes clés | Conforme |
|-------|---------------|----------|
| auth_users | subject, email, password_hash, status | Oui |
| auth_user_profiles | display_name, locale, timezone | Oui |
| auth_roles | name, is_system | Oui |
| auth_permissions | resource, action | Oui |
| auth_sessions | refresh_token_hash, last_used_at, device_label | Oui |
| auth_audit_events | target_type, target_id, actor_id | Oui |
| auth_jwk_keys | kid, algorithm, public_jwk, status | Oui |

## Sécurité

- `AuthUserModel.__repr__` n'expose pas `password_hash` — OK
- `AuthSessionModel.__repr__` n'expose pas `refresh_token_hash` — OK
- `AuthJwkKeyModel.__repr__` n'expose pas le matériel de clé — OK

## Points positifs

- Registry centralisé pour Alembic et consistency checker (BL-003).
- FK explicites vers tables préfixées `auth_*`.
- Modèles sans relations lazy — aligné ADR-001.

## Observations (non bloquantes)

1. **`UniqueConstraint("id")` sur sessions** : redondant avec PK ; peut être retiré
   lors d'un refactor migration (impact Alembic — à planifier).
2. **Couverture `__repr__`** : certains modèles à 92–94 % ; global projet OK.
3. **Test PG** : absent — traçabilité BL-008 ou intégration.

## Décision

**APPROUVÉ** — modèles ISO demande CDC et FEAT-002.1.
