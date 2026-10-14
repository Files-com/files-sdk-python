"""Waiting for what Files.com finishes in the background: the copy or move
a FileAction describes, and a deletion.

Files.com may answer a copy or move before it is done, with a FileAction
whose status is "pending" and the id of the FileMigration doing it. Waiting
polls that migration, once every interval seconds, until it completes or
fails. A deletion answers with no body; waiting for it polls the path until
Files.com says it is gone. Polling uses the operation's cancel_token,
request_timeout and deadline, so give one of those to bound the wait.
"""

import math

from files_sdk.error import (
    FileMigrationError,
    InvalidParameterError,
    NotFoundError,
)

DEFAULT_INTERVAL = 1.0
"""Seconds between checks while waiting."""

_FINISHED = frozenset({"completed", "failed", "cancelled"})


def checked_interval(value) -> float:
    if (
        isinstance(value, bool)
        or not isinstance(value, (int, float))
        or not math.isfinite(value)
        or value <= 0
    ):
        raise InvalidParameterError(
            "interval must be a positive number of seconds"
        )
    return float(value)


def wait_for(operation, action, interval=DEFAULT_INTERVAL, progress=None):
    """The FileMigration that did action, once it completed, or None when
    action finished without one. Raises FileMigrationError if it failed or
    was cancelled."""
    from files_sdk.models.file_migration import FileMigrationResource

    interval = checked_interval(interval)
    if progress is not None and not callable(progress):
        raise InvalidParameterError("progress must be a function")
    migration_id = getattr(action, "file_migration_id", None)
    if migration_id is None:
        if getattr(action, "status", None) == "failed":
            raise FileMigrationError(
                "Files.com reported that the action on {} failed.".format(
                    getattr(action, "path", None)
                ),
                migration=None,
            )
        return None
    while True:
        operation.lifetime.check("waiting for the file migration")
        migration = FileMigrationResource(operation).find(migration_id)
        if progress is not None:
            progress(migration)
        if migration.status in _FINISHED:
            if migration.status == "completed":
                return migration
            raise FileMigrationError(
                "The file migration {} ({}) {}{}".format(
                    migration.id,
                    migration.operation or "operation",
                    (
                        "was cancelled"
                        if migration.status == "cancelled"
                        else "failed"
                    ),
                    (
                        ": {}".format(migration.failure_message)
                        if migration.failure_message
                        else "."
                    ),
                ),
                migration=migration,
            )
        operation.lifetime.sleep(interval, "waiting for the file migration")


def wait_until_gone(operation, path, interval=DEFAULT_INTERVAL):
    """Return once Files.com says path does not exist."""
    from files_sdk.models.file import FileResource

    interval = checked_interval(interval)
    while True:
        try:
            FileResource(operation).find(path)
        except NotFoundError:
            return
        operation.lifetime.sleep(interval, "waiting for the deletion")
