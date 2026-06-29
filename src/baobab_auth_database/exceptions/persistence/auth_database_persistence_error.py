"""Erreur de persistance SQLAlchemy.

:spec: FEAT-003.1
"""


class AuthDatabasePersistenceError(Exception):
    """Levée lorsqu'une opération de persistance échoue.

    :param message: Description de l'échec sans secret.
    :param cause: Exception SQLAlchemy source.
    :spec: FEAT-003.1
    """

    def __init__(self, message: str, *, cause: Exception | None = None) -> None:
        """Initialise l'erreur de persistance.

        :param message: Message explicite.
        :param cause: Exception encapsulée.
        """
        super().__init__(message)
        self.message = message
        self.cause = cause
