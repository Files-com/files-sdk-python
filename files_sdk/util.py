"""The SDK's logging.

Records go to the "files_sdk" logger, which has only a NullHandler, so an
application that has not configured logging sees nothing. Configure the
logging module, or that logger, to receive them. DEBUG records hold the
full requests and responses, including credentials and signed URLs; INFO
and above never do.

files_sdk.console_log_level, from earlier versions, also prints the SDK's
records at or above that level ("debug", "info", "warning" or "error"; the
default "none" prints nothing) to standard error, whatever the logging
configuration.
"""

import logging
import sys
from typing import TextIO

import files_sdk

logger = logging.getLogger("files_sdk")
logger.addHandler(logging.NullHandler())

_CONSOLE_LEVELS = {
    "debug": logging.DEBUG,
    "info": logging.INFO,
    "warning": logging.WARNING,
    "error": logging.ERROR,
}


class _ConsoleHandler(logging.StreamHandler[TextIO]):
    """Writes to whatever sys.stderr is when a record arrives."""

    def __init__(self):
        logging.Handler.__init__(self)
        self.setFormatter(logging.Formatter("%(levelname)s %(message)s"))

    @property
    def stream(self):  # type: ignore[override]
        return sys.stderr


_console = _ConsoleHandler()


def enabled(level):
    """Whether a record at level would go anywhere, so callers can skip
    preparing details nobody will see."""
    console = _CONSOLE_LEVELS.get(
        str(files_sdk.console_log_level or "").lower()
    )
    return logger.isEnabledFor(level) or (
        console is not None and level >= console
    )


def _log(level, message, params):
    console = _CONSOLE_LEVELS.get(
        str(files_sdk.console_log_level or "").lower()
    )
    to_console = console is not None and level >= console
    if not to_console and not logger.isEnabledFor(level):
        return
    text = "message={}".format(message)
    if params:
        text += " " + " ".join(
            "{}={}".format(key, value) for key, value in sorted(params.items())
        )
    if logger.isEnabledFor(level):
        logger.log(level, text)
    if to_console:
        _console.handle(
            logging.LogRecord(
                logger.name, level, __file__, 0, text, None, None
            )
        )


def log_debug(message, **params):
    _log(logging.DEBUG, message, params)


def log_info(message, **params):
    _log(logging.INFO, message, params)


def log_warning(message, **params):
    _log(logging.WARNING, message, params)


def log_error(message, **params):
    _log(logging.ERROR, message, params)
