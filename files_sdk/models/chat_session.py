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
from files_sdk.list_obj import ListObj
from files_sdk.error import (  # noqa: F401
    InvalidParameterError,
    MissingParameterError,
    NotImplementedError,
)


class ChatSession:
    """A chat session record from the Files.com API.

    An attribute the API did not send is None.

    Attributes:
        id: string - Chat Session ID.
        title: string - Short AI-generated chat title.
        user_id: int64 - User ID.
        ai_task_id: int64 - AI Task ID. Present when the conversation was started by an AI Task.
        workspace_id: int64 - Workspace ID. `0` means the default workspace.
        last_active_at: date-time - Most recent chat activity date/time.
        created_at: date-time - Chat session creation date/time.
        messages: array(object) - Visible conversation messages in this chat session. For performance reasons, this is not provided when listing chat sessions.
    """

    default_attributes = {
        "id": None,  # string - Chat Session ID.
        "title": None,  # string - Short AI-generated chat title.
        "user_id": None,  # int64 - User ID.
        "ai_task_id": None,  # int64 - AI Task ID. Present when the conversation was started by an AI Task.
        "workspace_id": None,  # int64 - Workspace ID. `0` means the default workspace.
        "last_active_at": None,  # date-time - Most recent chat activity date/time.
        "created_at": None,  # date-time - Chat session creation date/time.
        "messages": None,  # array(object) - Visible conversation messages in this chat session. For performance reasons, this is not provided when listing chat sessions.
    }

    # Declared for type checkers and editors: the type the API sends each
    # attribute as, or None. set_attributes stores each value as given,
    # converting only decimals, so a value a caller sets can differ.
    id: str | None
    title: str | None
    user_id: int | None
    ai_task_id: int | None
    workspace_id: int | None
    last_active_at: str | None
    created_at: str | None
    messages: builtins.list[dict[str, Any]] | None

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
        for attribute, default_value in ChatSession.default_attributes.items():
            value = attributes.get(attribute, default_value)
            setattr(self, attribute, value)

    def get_attributes(self):
        attrs = {
            k: getattr(self, k, None)
            for k in ChatSession.default_attributes
            if getattr(self, k, None) is not None
        }
        return attrs

    def _scope(self):
        if self._context is not None:
            return self._context
        return LegacyScope(self.options)


class ChatSessionResource:
    """ChatSession operations that use one client's configuration.

    Get one from a client, such as ``client.chat_session``. Each operation
    takes the same arguments as the module-level function of the same name,
    and its options apply on top of the client's.
    """

    def __init__(self, scope):
        self._scope = scope

    def list(
        self,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> ListObj[ChatSession]:
        """Parameters:
        cursor - string - Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
        per_page - int64 - Number of records to show per page.  (Max: 10000, 1,000 or less is recommended).
        sort_by - object - If set, sort records by the specified field in either `asc` or `desc` direction. Valid fields are `id`.
        filter - object - If set, return records where the specified field is equal to the supplied value. Valid fields are `ai_task_id`, `user_id` or `workspace_id`.
        """
        params = copy_params(params)
        if "cursor" in params and not isinstance(params["cursor"], str):
            raise InvalidParameterError("Bad parameter: cursor must be an str")
        if "per_page" in params and (
            not isinstance(params["per_page"], int)
            or isinstance(params["per_page"], bool)
        ):
            raise InvalidParameterError(
                "Bad parameter: per_page must be an int"
            )
        if "sort_by" in params and not isinstance(params["sort_by"], dict):
            raise InvalidParameterError(
                "Bad parameter: sort_by must be an dict"
            )
        if "filter" in params and not isinstance(params["filter"], dict):
            raise InvalidParameterError(
                "Bad parameter: filter must be an dict"
            )
        operation = Operation.start(self._scope, options)
        return ListObj(ChatSession, "GET", "/chat_sessions", params, operation)

    def all(
        self,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> ListObj[ChatSession]:
        """The same as list()."""
        return self.list(params, options)

    def find(
        self,
        id: str,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> ChatSession:
        """Parameters:
        id (required) - string - Chat Session ID.
        """
        return self.__find({"id": id}, params, options)

    def __find(
        self,
        path_values: dict[str, Any],
        params: dict[str, Any] | None,
        options: RequestOptions | Mapping[str, Any] | None,
    ) -> ChatSession:
        params = copy_params(params, path_values)
        if "id" in params and not isinstance(params["id"], str):
            raise InvalidParameterError("Bad parameter: id must be an str")
        if "id" not in params:
            raise MissingParameterError("Parameter missing: id")
        operation = Operation.start(self._scope, options)
        response = operation.request(
            "GET", "/chat_sessions/" + path_value(params["id"]), params
        )
        return operation.decode_model(response, ChatSession)

    def get(
        self,
        id: str,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> ChatSession:
        """The same as find()."""
        return self.find(id, params, options)

    def new(
        self,
        attributes: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> ChatSession:
        """A new ChatSession with attributes, not yet saved, whose
        operations use this resource's client."""
        obj = ChatSession(attributes, options)
        obj._context = self._scope._context_for(options)
        return obj


_legacy_resource = ChatSessionResource(LEGACY)


def list(
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> ListObj[ChatSession]:
    """Parameters:
    cursor - string - Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
    per_page - int64 - Number of records to show per page.  (Max: 10000, 1,000 or less is recommended).
    sort_by - object - If set, sort records by the specified field in either `asc` or `desc` direction. Valid fields are `id`.
    filter - object - If set, return records where the specified field is equal to the supplied value. Valid fields are `ai_task_id`, `user_id` or `workspace_id`.
    """
    return _legacy_resource.list(params, options)


def all(
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> ListObj[ChatSession]:
    """The same as list()."""
    return _legacy_resource.list(params, options)


def find(
    id: str,
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> ChatSession:
    """Parameters:
    id (required) - string - Chat Session ID.
    """
    return _legacy_resource.find(id, params, options)


def get(
    id: str,
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> ChatSession:
    """The same as find()."""
    return _legacy_resource.find(id, params, options)


def new(*args, **kwargs) -> ChatSession:
    return ChatSession(*args, **kwargs)
