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


class FileCommentReaction:
    """A file comment reaction record from the Files.com API.

    An attribute the API did not send is None.

    Attributes:
        id: int64 - Reaction ID
        emoji: string - Emoji used in the reaction.
        user_id: int64 - User ID. Provide a value of `0` to operate the current session's user.
        file_comment_id: int64 - ID of file comment to attach reaction to.
    """

    default_attributes = {
        "id": None,  # int64 - Reaction ID
        "emoji": None,  # string - Emoji used in the reaction.
        "user_id": None,  # int64 - User ID.  Provide a value of `0` to operate the current session's user.
        "file_comment_id": None,  # int64 - ID of file comment to attach reaction to.
    }

    # Declared for type checkers and editors: the type the API sends each
    # attribute as, or None. set_attributes stores each value as given,
    # converting only decimals, so a value a caller sets can differ.
    id: int | None
    emoji: str | None
    user_id: int | None
    file_comment_id: int | None

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
        ) in FileCommentReaction.default_attributes.items():
            value = attributes.get(attribute, default_value)
            setattr(self, attribute, value)

    def get_attributes(self):
        attrs = {
            k: getattr(self, k, None)
            for k in FileCommentReaction.default_attributes
            if getattr(self, k, None) is not None
        }
        return attrs

    def _scope(self):
        if self._context is not None:
            return self._context
        return LegacyScope(self.options)

    def delete(self, params: dict[str, Any] | None = None) -> None:
        if not (hasattr(self, "id") and self.id):
            raise MissingParameterError("Current object doesn't have a id")
        params = copy_params(params, {"id": self.id})
        if "id" not in params:
            raise MissingParameterError("Parameter missing: id")
        if "id" in params and (
            not isinstance(params["id"], int) or isinstance(params["id"], bool)
        ):
            raise InvalidParameterError("Bad parameter: id must be an int")
        operation = Operation.start(self._scope())
        operation.request(
            "DELETE",
            "/file_comment_reactions/" + path_value(params["id"]),
            params,
        )

    def destroy(self, params: dict[str, Any] | None = None) -> None:
        """The same as delete()."""
        return self.delete(params)

    def save(self) -> None:
        """Create this object on the server, taking in place the record it
        returns. One that already has an id cannot be updated, and raises
        NotImplementedError."""
        if hasattr(self, "id") and self.id:
            raise NotImplementedError(
                "The FileCommentReaction object doesn't support updates."
            )
        else:
            new_obj = FileCommentReactionResource(self._scope()).create(
                self.get_attributes()
            )
            self.set_attributes(new_obj.get_attributes())
            self._context = new_obj._context


class FileCommentReactionResource:
    """FileCommentReaction operations that use one client's configuration.

    Get one from a client, such as ``client.file_comment_reaction``. Each operation
    takes the same arguments as the module-level function of the same name,
    and its options apply on top of the client's.
    """

    def __init__(self, scope):
        self._scope = scope

    def create(
        self,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> FileCommentReaction:
        """Parameters:
        user_id - int64 - User ID.  Provide a value of `0` to operate the current session's user.
        file_comment_id (required) - int64 - ID of file comment to attach reaction to.
        emoji (required) - string - Emoji to react with.
        """
        params = copy_params(params)
        if "user_id" in params and (
            not isinstance(params["user_id"], int)
            or isinstance(params["user_id"], bool)
        ):
            raise InvalidParameterError(
                "Bad parameter: user_id must be an int"
            )
        if "file_comment_id" in params and (
            not isinstance(params["file_comment_id"], int)
            or isinstance(params["file_comment_id"], bool)
        ):
            raise InvalidParameterError(
                "Bad parameter: file_comment_id must be an int"
            )
        if "emoji" in params and not isinstance(params["emoji"], str):
            raise InvalidParameterError("Bad parameter: emoji must be an str")
        if "file_comment_id" not in params:
            raise MissingParameterError("Parameter missing: file_comment_id")
        if "emoji" not in params:
            raise MissingParameterError("Parameter missing: emoji")
        operation = Operation.start(self._scope, options)
        response = operation.request("POST", "/file_comment_reactions", params)
        return operation.decode_model(response, FileCommentReaction)

    def delete(
        self,
        id: int,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> None:
        return self.__delete({"id": id}, params, options)

    def __delete(
        self,
        path_values: dict[str, Any],
        params: dict[str, Any] | None,
        options: RequestOptions | Mapping[str, Any] | None,
    ) -> None:
        params = copy_params(params, path_values)
        if "id" in params and (
            not isinstance(params["id"], int) or isinstance(params["id"], bool)
        ):
            raise InvalidParameterError("Bad parameter: id must be an int")
        if "id" not in params:
            raise MissingParameterError("Parameter missing: id")
        operation = Operation.start(self._scope, options)
        operation.request(
            "DELETE",
            "/file_comment_reactions/" + path_value(params["id"]),
            params,
        )

    def destroy(
        self,
        id: int,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> None:
        """The same as delete()."""
        return self.delete(id, params, options)

    def new(
        self,
        attributes: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> FileCommentReaction:
        """A new FileCommentReaction with attributes, not yet saved, whose
        operations use this resource's client."""
        obj = FileCommentReaction(attributes, options)
        obj._context = self._scope._context_for(options)
        return obj


_legacy_resource = FileCommentReactionResource(LEGACY)


def create(
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> FileCommentReaction:
    """Parameters:
    user_id - int64 - User ID.  Provide a value of `0` to operate the current session's user.
    file_comment_id (required) - int64 - ID of file comment to attach reaction to.
    emoji (required) - string - Emoji to react with.
    """
    return _legacy_resource.create(params, options)


def delete(
    id: int,
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> None:
    _legacy_resource.delete(id, params, options)


def destroy(
    id: int,
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> None:
    """The same as delete()."""
    return _legacy_resource.delete(id, params, options)


def new(*args, **kwargs) -> FileCommentReaction:
    return FileCommentReaction(*args, **kwargs)
