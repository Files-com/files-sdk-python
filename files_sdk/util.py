import logging
import sys

import files_sdk

logger = logging.getLogger("files_sdk")


def _logfmt(data):
    def fmt(key, val):
        return "{key}={val}".format(key=key, val=val)

    return " ".join([fmt(key, val) for key, val in sorted(data.items())])


def log_debug(message, **params):
    msg = "message={} ".format(message) + _logfmt(dict(**params))
    if files_sdk.console_log_level.lower() == "debug":
        print("DEBUG " + msg, file=sys.stderr)
    logger.debug(msg)


def log_info(message, **params):
    msg = "message={} ".format(message) + _logfmt(dict(**params))
    if files_sdk.console_log_level.lower() in ["debug", "info"]:
        print("INFO " + msg, file=sys.stderr)
    logger.info(msg)


def log_error(message, **params):
    msg = "message={} ".format(message) + _logfmt(dict(**params))
    if files_sdk.console_log_level.lower() in ["debug", "info", "error"]:
        print("ERROR " + msg, file=sys.stderr)
    logger.error(msg)
