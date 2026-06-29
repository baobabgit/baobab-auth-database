FEAT-006.1 — Tests de contrat baobab-auth-core
==============================================

:Rattachée à: :ref:`us-006-validation-contrat`
:origin: ``01_cdc_v0_1_0_stabilisation_mvp.md`` §7
:Implémentation: ``tests/contracts/``

Description
-----------

Harness d'intégration vérifiant que les repositories et UoW satisfont les ports core.

Critères d'acceptation
----------------------

#. Tests contrat pour UserRepository, RoleRepository, PermissionRepository,
   SessionRepository, AuditRepository, UnitOfWork.
#. Documenté dans ``docs/guides/how-to/integration-validation.rst``.

Tâches
------

* ``TASK-006.1.1`` Harness contrat core.
* ``TASK-006.1.2`` Mise à jour documentation intégration.
