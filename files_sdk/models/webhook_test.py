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


class WebhookTest:
    """A webhook test record from the Files.com API.

    An attribute the API did not send is None.

    Attributes:
        code: int64 - Status HTTP code
        message: string - Error message
        status: string - Status message
        data: Auto - Additional data
        success: boolean - The success status of the webhook test
        url: string - URL for testing the webhook.
        method: string - HTTP method(GET or POST).
        encoding: string - HTTP encoding method. Can be JSON, XML, or RAW (form data).
        headers: object - Additional request headers.
        body: object - Additional body parameters.
        raw_body: string - raw body text
        file_as_body: boolean - Send the file data as the request body?
        file_form_field: string - Send the file data as a named parameter in the request POST body
        action: string - action for test body
        use_dedicated_ips: boolean - Use dedicated IPs for sending the webhook?
    """

    default_attributes = {
        "code": None,  # int64 - Status HTTP code
        "message": None,  # string - Error message
        "status": None,  # string - Status message
        "data": None,  # Auto - Additional data
        "success": None,  # boolean - The success status of the webhook test
        "url": None,  # string - URL for testing the webhook.
        "method": None,  # string - HTTP method(GET or POST).
        "encoding": None,  # string - HTTP encoding method.  Can be JSON, XML, or RAW (form data).
        "headers": None,  # object - Additional request headers.
        "body": None,  # object - Additional body parameters.
        "raw_body": None,  # string - raw body text
        "file_as_body": None,  # boolean - Send the file data as the request body?
        "file_form_field": None,  # string - Send the file data as a named parameter in the request POST body
        "action": None,  # string - action for test body
        "use_dedicated_ips": None,  # boolean - Use dedicated IPs for sending the webhook?
    }

    # Declared for type checkers and editors: the type the API sends each
    # attribute as, or None. set_attributes stores each value as given,
    # converting only decimals, so a value a caller sets can differ.
    code: int | None
    message: str | None
    status: str | None
    data: Any
    success: bool | None
    url: str | None
    method: str | None
    encoding: str | None
    headers: dict[str, Any] | None
    body: dict[str, Any] | None
    raw_body: str | None
    file_as_body: bool | None
    file_form_field: str | None
    action: str | None
    use_dedicated_ips: bool | None

    # Not an attribute of the API's record, but the operations below read it,
    # so set it before calling them.
    id: Any

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
        for attribute, default_value in WebhookTest.default_attributes.items():
            value = attributes.get(attribute, default_value)
            setattr(self, attribute, value)

    def get_attributes(self):
        attrs = {
            k: getattr(self, k, None)
            for k in WebhookTest.default_attributes
            if getattr(self, k, None) is not None
        }
        return attrs

    def _scope(self):
        if self._context is not None:
            return self._context
        return LegacyScope(self.options)

    def save(self) -> None:
        """Create this object on the server, taking in place the record it
        returns. One that already has an id cannot be updated, and raises
        NotImplementedError."""
        if hasattr(self, "id") and self.id:
            raise NotImplementedError(
                "The WebhookTest object doesn't support updates."
            )
        else:
            new_obj = WebhookTestResource(self._scope()).create(
                self.get_attributes()
            )
            self.set_attributes(new_obj.get_attributes())
            self._context = new_obj._context


class WebhookTestResource:
    """WebhookTest operations that use one client's configuration.

    Get one from a client, such as ``client.webhook_test``. Each operation
    takes the same arguments as the module-level function of the same name,
    and its options apply on top of the client's.
    """

    def __init__(self, scope):
        self._scope = scope

    def create(
        self,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> WebhookTest:
        """Parameters:
        url (required) - string - URL for testing the webhook.
        method - string - HTTP method(GET or POST).
        encoding - string - HTTP encoding method.  Can be JSON, XML, or RAW (form data).
        headers - object - Additional request headers.
        body - object - Additional body parameters.
        raw_body - string - raw body text
        file_as_body - boolean - Send the file data as the request body?
        file_form_field - string - Send the file data as a named parameter in the request POST body
        action - string - action for test body
        use_dedicated_ips - boolean - Use dedicated IPs for sending the webhook?
        """
        params = copy_params(params)
        if "url" in params and not isinstance(params["url"], str):
            raise InvalidParameterError("Bad parameter: url must be an str")
        if "method" in params and not isinstance(params["method"], str):
            raise InvalidParameterError("Bad parameter: method must be an str")
        if "encoding" in params and not isinstance(params["encoding"], str):
            raise InvalidParameterError(
                "Bad parameter: encoding must be an str"
            )
        if "headers" in params and not isinstance(params["headers"], dict):
            raise InvalidParameterError(
                "Bad parameter: headers must be an dict"
            )
        if "body" in params and not isinstance(params["body"], dict):
            raise InvalidParameterError("Bad parameter: body must be an dict")
        if "raw_body" in params and not isinstance(params["raw_body"], str):
            raise InvalidParameterError(
                "Bad parameter: raw_body must be an str"
            )
        if "file_as_body" in params and not isinstance(
            params["file_as_body"], bool
        ):
            raise InvalidParameterError(
                "Bad parameter: file_as_body must be an bool"
            )
        if "file_form_field" in params and not isinstance(
            params["file_form_field"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: file_form_field must be an str"
            )
        if "action" in params and not isinstance(params["action"], str):
            raise InvalidParameterError("Bad parameter: action must be an str")
        if "use_dedicated_ips" in params and not isinstance(
            params["use_dedicated_ips"], bool
        ):
            raise InvalidParameterError(
                "Bad parameter: use_dedicated_ips must be an bool"
            )
        if "url" not in params:
            raise MissingParameterError("Parameter missing: url")
        operation = Operation.start(self._scope, options)
        response = operation.request("POST", "/webhook_tests", params)
        return operation.decode_model(response, WebhookTest)

    def new(
        self,
        attributes: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> WebhookTest:
        """A new WebhookTest with attributes, not yet saved, whose
        operations use this resource's client."""
        obj = WebhookTest(attributes, options)
        obj._context = self._scope._context_for(options)
        return obj


_legacy_resource = WebhookTestResource(LEGACY)


def create(
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> WebhookTest:
    """Parameters:
    url (required) - string - URL for testing the webhook.
    method - string - HTTP method(GET or POST).
    encoding - string - HTTP encoding method.  Can be JSON, XML, or RAW (form data).
    headers - object - Additional request headers.
    body - object - Additional body parameters.
    raw_body - string - raw body text
    file_as_body - boolean - Send the file data as the request body?
    file_form_field - string - Send the file data as a named parameter in the request POST body
    action - string - action for test body
    use_dedicated_ips - boolean - Use dedicated IPs for sending the webhook?
    """
    return _legacy_resource.create(params, options)


def new(*args, **kwargs) -> WebhookTest:
    return WebhookTest(*args, **kwargs)
