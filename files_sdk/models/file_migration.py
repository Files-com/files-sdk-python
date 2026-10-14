import builtins  # noqa: F401
from typing import Any, Mapping  # noqa: F401
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


class FileMigration:
    """A file migration record from the Files.com API.

    An attribute the API did not send is None.

    Attributes:
        id: int64 - File migration ID
        path: string - Source path. This must be slash-delimited, but it must neither start nor end with a slash. Maximum of 5000 characters.
        dest_path: string - Destination path
        failure_message: string - Reason for the failure, if applicable.
        files_moved: int64 - Number of files processed
        files_total: int64
        operation: string - The type of operation
        region: string - Region
        status: string - Status
        log_url: string - Link to download the log file for this migration.
    """

    default_attributes = {
        "id": None,  # int64 - File migration ID
        "path": None,  # string - Source path. This must be slash-delimited, but it must neither start nor end with a slash. Maximum of 5000 characters.
        "dest_path": None,  # string - Destination path
        "failure_message": None,  # string - Reason for the failure, if applicable.
        "files_moved": None,  # int64 - Number of files processed
        "files_total": None,  # int64
        "operation": None,  # string - The type of operation
        "region": None,  # string - Region
        "status": None,  # string - Status
        "log_url": None,  # string - Link to download the log file for this migration.
    }

    # Declared for type checkers and editors: the type the API sends each
    # attribute as, or None. set_attributes stores each value as given,
    # converting only decimals, so a value a caller sets can differ.
    id: int | None
    path: str | None
    dest_path: str | None
    failure_message: str | None
    files_moved: int | None
    files_total: int | None
    operation: str | None
    region: str | None
    status: str | None
    log_url: str | None

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
        for (
            attribute,
            default_value,
        ) in FileMigration.default_attributes.items():
            value = attributes.get(attribute, default_value)
            setattr(self, attribute, value)

    def get_attributes(self):
        attrs = {
            k: getattr(self, k, None)
            for k in FileMigration.default_attributes
            if getattr(self, k, None) is not None
        }
        return attrs

    def _scope(self):
        if self._context is not None:
            return self._context
        return LegacyScope(self.options)


class FileMigrationResource:
    """FileMigration operations that use one client's configuration.

    Get one from a client, such as ``client.file_migration``. Each operation
    takes the same arguments as the module-level function of the same name,
    and its options apply on top of the client's.
    """

    def __init__(self, scope):
        self._scope = scope

    def find(
        self,
        id: int,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> FileMigration:
        """Parameters:
        id (required) - int64 - File Migration ID.
        """
        return self.__find({"id": id}, params, options)

    def __find(
        self,
        path_values: dict[str, Any],
        params: dict[str, Any] | None,
        options: RequestOptions | Mapping[str, Any] | None,
    ) -> FileMigration:
        params = copy_params(params, path_values)
        if "id" in params and (
            not isinstance(params["id"], int) or isinstance(params["id"], bool)
        ):
            raise InvalidParameterError("Bad parameter: id must be an int")
        if "id" not in params:
            raise MissingParameterError("Parameter missing: id")
        operation = Operation.start(self._scope, options)
        response = operation.request(
            "GET", "/file_migrations/" + path_value(params["id"]), params
        )
        return operation.decode_model(response, FileMigration)

    def get(
        self,
        id: int,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> FileMigration:
        """The same as find()."""
        return self.find(id, params, options)

    def new(
        self,
        attributes: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> FileMigration:
        """A new FileMigration with attributes, not yet saved, whose
        operations use this resource's client."""
        obj = FileMigration(attributes, options)
        obj._context = self._scope._context_for(options)
        return obj


_legacy_resource = FileMigrationResource(LEGACY)


def find(
    id: int,
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> FileMigration:
    """Parameters:
    id (required) - int64 - File Migration ID.
    """
    return _legacy_resource.find(id, params, options)


def get(
    id: int,
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> FileMigration:
    """The same as find()."""
    return _legacy_resource.find(id, params, options)


def new(*args, **kwargs) -> FileMigration:
    return FileMigration(*args, **kwargs)
