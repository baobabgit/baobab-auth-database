US-003 — Repositories synchrones et Unit of Work
================================================

:origin: ``01_cdc_v0_1_0_stabilisation_mvp.md`` §4, §8
:Version cible: ``v0.1.0``

Description
-----------

Implémentations SQLAlchemy des ports ``UserRepository``, ``RoleRepository``,
``PermissionRepository``, ``SessionRepository``, ``AuditRepository`` et
``SqlAlchemyAuthUnitOfWork`` conforme au port ``UnitOfWork`` du core.

Features
--------

.. toctree::
   :maxdepth: 1

   FEAT-003.1-repositories-sync
   FEAT-003.2-unit-of-work

Critères d'acceptation (US)
---------------------------

#. Repositories fonctionnent sur SQLite et PostgreSQL.
#. UoW commit/rollback transactionnels.
#. Erreurs techniques transformées en exceptions database contrôlées.
