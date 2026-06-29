"""Erreur de conversion entre modèles ORM et entités core.

:spec: FEAT-004.1
"""


class AuthDatabaseMappingError(Exception):
    """Levée lorsqu'une conversion ORM ↔ domaine échoue.

    :param message: Description de l'échec de mapping.
    :param cause: Exception d'origine (validation core, enum invalide…).
    :spec: FEAT-004.1
    """

    def __init__(self, message: str, *, cause: Exception | None = None) -> None:
        """Initialise l'erreur de mapping.

        :param message: Message explicite sans secret.
        :param cause: Exception source encapsulée.
        """
        super().__init__(message)
        self.message = message
        self.cause = cause
