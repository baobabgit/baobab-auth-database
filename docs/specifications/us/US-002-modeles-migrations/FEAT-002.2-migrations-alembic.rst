FEAT-002.2 — Migrations Alembic
===============================

:Rattachée à: :ref:`us-002-modeles-migrations`
:origin: ``01_cdc_v0_1_0_stabilisation_mvp.md`` §8
:Implémentation: package ``baobab_auth_database.migrations``

Description
-----------

Migration initiale ou corrective ; migration ``0002`` si ``0001`` déjà publiée.

Critères d'acceptation
----------------------

#. ``upgrade head`` et ``downgrade base`` fonctionnent sur base vierge.
#. ``alembic current`` et ``history`` opérationnels.
#. CLI embarquée pour invoquer Alembic.

Tâches
------

* ``TASK-002.2.1`` Initialiser Alembic embarqué.
* ``TASK-002.2.2`` Rédiger migration alignée sur les modèles ORM.
