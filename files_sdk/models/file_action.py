import builtins  # noqa: F401
from typing import Any, Mapping  # noqa: F401
from typing import Callable
import files_sdk.migration as migrations
from files_sdk.models.file_migration import FileMigration
from files_sdk.api import (  # noqa: F401
    LEGACY,
    LegacyScope,
    Operation,
    copy_params,
    decode_record,
    path_value,
)
from files_sdk.api_client import unexpected_response_error  # noqa: F401
from files_sdk.context import RequestOptions  # noqa: F401
from files_sdk.error import (  # noqa: F401
    InvalidParameterError,
    MissingParameterError,
    NotImplementedError,
)


class FileAction:
    """A file action record from the Files.com API.

    An attribute the API did not send is None.

    Attributes:
        status: string - Status of file operation.
        file_migration_id: int64 - If status is pending, this is the id of the File Migration to check for status updates. Delete actions include it whenever the deletion runs as a File Migration, including while it is processing.
    """

    default_attributes = {
        "status": None,  # string - Status of file operation.
        "file_migration_id": None,  # int64 - If status is pending, this is the id of the File Migration to check for status updates.  Delete actions include it whenever the deletion runs as a File Migration, including while it is processing.
        "path": None,
        "destination": None,
    }

    # Declared for type checkers and editors: the type the API sends each
    # attribute as, or None. set_attributes stores each value as given,
    # converting only decimals, so a value a caller sets can differ.
    status: str | None
    file_migration_id: int | None
    path: str | None
    destination: str | None

    # The client and settings this object's operations use: those of the
    # operation or client that made it, or the module's when it starts an
    # operation if neither did.
    _context: Any = None

    def __init__(self, attributes=None, options=None):
        if not isinstance(attributes, dict):
            attributes = {}
        if not isinstance(options, dict):
            options = {}
        self.set_attributes(attributes)
        self.options = dict(options)

    def set_attributes(self, attributes):
        for attribute, default_value in FileAction.default_attributes.items():
            value = attributes.get(attribute, default_value)
            setattr(self, attribute, value)

    def get_attributes(self):
        attrs = {
            k: getattr(self, k, None)
            for k in FileAction.default_attributes
            if getattr(self, k, None) is not None
        }
        return attrs

    def _scope(self):
        if self._context is not None:
            return self._context
        return LegacyScope(self.options)

    def wait(
        self,
        options: RequestOptions | Mapping[str, Any] | None = None,
        *,
        interval: float = 1.0,
        progress: Callable[[FileMigration], None] | None = None,
    ) -> FileMigration | None:
        """Wait until Files.com has finished this action, such as a copy or
        move whose status is "pending", and return the FileMigration that
        did it, or None if the action had already finished without one.

        The migration is checked every interval seconds, and passed to
        progress, if given, each time. A migration that fails or is
        cancelled raises FileMigrationError. The cancel_token,
        request_timeout and deadline options apply to the whole wait; give
        one of them to bound it."""
        operation = Operation.start(self._scope(), options)
        return migrations.wait_for(operation, self, interval, progress)


def new(*args, **kwargs) -> FileAction:
    return FileAction(*args, **kwargs)
