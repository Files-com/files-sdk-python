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


class As2IncomingMessage:
    """A as2 incoming message record from the Files.com API.

    An attribute the API did not send is None.

    Attributes:
        id: int64 - Id of the AS2 Partner.
        workspace_id: int64 - ID of the Workspace associated with this AS2 Incoming Message.
        as2_partner_id: int64 - Id of the AS2 Partner associated with this message.
        as2_station_id: int64 - Id of the AS2 Station associated with this message.
        uuid: string - UUID assigned to this message.
        content_type: string - Content Type header of the incoming message.
        http_headers: object - HTTP Headers sent with this message.
        processing_result: string - Result of processing.
        processing_result_description: string - Result of processing description.
        mic: string - AS2 Message Integrity Check
        mic_algo: string - AS2 Message Integrity Check Algorithm Used
        as2_to: string - AS2 TO header of message
        as2_from: string - AS2 FROM header of message
        message_id: string - AS2 Message Id
        subject: string - AS2 Subject Header
        date: string - Date Header
        body_size: string - Encrypted Payload Body Size
        attachment_filename: string - Filename of the file being received.
        ip: string - IP Address of the Sender
        created_at: date-time - Message creation date/time
        http_response_code: string - HTTP Response Code sent for this message
        http_response_headers: object - HTTP Headers sent for this message.
        recipient_serial: string - Incoming Message Recipient(the Client Cert used to encrypt this message)'s serial
        hex_recipient_serial: string - Incoming Message Recipient(the Client Cert used to encrypt this message)'s serial in hex format.
        recipient_issuer: string - Incoming Message Recipient(the Client Cert used to encrypt this message)'s issuer
        message_received: boolean - Message body received?
        message_decrypted: boolean - Message decrypted successfully?
        message_signature_verified: boolean - Message signature verified?
        message_processing_success: boolean - Message processed successfully?
        message_mdn_returned: boolean - MDN returned?
        encrypted_uri: string - URL to download the encrypted signed smime that is to sent as AS2 body
        smime_signed_uri: string - URL to download the file contents as smime with signature
        smime_uri: string - URL to download the file contents encoded as smime
        raw_uri: string - URL to download the original file contents
        mdn_response_uri: string - URL to download the http response body
    """

    default_attributes = {
        "id": None,  # int64 - Id of the AS2 Partner.
        "workspace_id": None,  # int64 - ID of the Workspace associated with this AS2 Incoming Message.
        "as2_partner_id": None,  # int64 - Id of the AS2 Partner associated with this message.
        "as2_station_id": None,  # int64 - Id of the AS2 Station associated with this message.
        "uuid": None,  # string - UUID assigned to this message.
        "content_type": None,  # string - Content Type header of the incoming message.
        "http_headers": None,  # object - HTTP Headers sent with this message.
        "processing_result": None,  # string - Result of processing.
        "processing_result_description": None,  # string - Result of processing description.
        "mic": None,  # string - AS2 Message Integrity Check
        "mic_algo": None,  # string - AS2 Message Integrity Check Algorithm Used
        "as2_to": None,  # string - AS2 TO header of message
        "as2_from": None,  # string - AS2 FROM header of message
        "message_id": None,  # string - AS2 Message Id
        "subject": None,  # string - AS2 Subject Header
        "date": None,  # string - Date Header
        "body_size": None,  # string - Encrypted Payload Body Size
        "attachment_filename": None,  # string - Filename of the file being received.
        "ip": None,  # string - IP Address of the Sender
        "created_at": None,  # date-time - Message creation date/time
        "http_response_code": None,  # string - HTTP Response Code sent for this message
        "http_response_headers": None,  # object - HTTP Headers sent for this message.
        "recipient_serial": None,  # string - Incoming Message Recipient(the Client Cert used to encrypt this message)'s serial
        "hex_recipient_serial": None,  # string - Incoming Message Recipient(the Client Cert used to encrypt this message)'s serial in hex format.
        "recipient_issuer": None,  # string - Incoming Message Recipient(the Client Cert used to encrypt this message)'s issuer
        "message_received": None,  # boolean - Message body received?
        "message_decrypted": None,  # boolean - Message decrypted successfully?
        "message_signature_verified": None,  # boolean - Message signature verified?
        "message_processing_success": None,  # boolean - Message processed successfully?
        "message_mdn_returned": None,  # boolean - MDN returned?
        "encrypted_uri": None,  # string - URL to download the encrypted signed smime that is to sent as AS2 body
        "smime_signed_uri": None,  # string - URL to download the file contents as smime with signature
        "smime_uri": None,  # string - URL to download the file contents encoded as smime
        "raw_uri": None,  # string - URL to download the original file contents
        "mdn_response_uri": None,  # string - URL to download the http response body
    }

    # Declared for type checkers and editors: the type the API sends each
    # attribute as, or None. set_attributes stores each value as given,
    # converting only decimals, so a value a caller sets can differ.
    id: int | None
    workspace_id: int | None
    as2_partner_id: int | None
    as2_station_id: int | None
    uuid: str | None
    content_type: str | None
    http_headers: dict[str, Any] | None
    processing_result: str | None
    processing_result_description: str | None
    mic: str | None
    mic_algo: str | None
    as2_to: str | None
    as2_from: str | None
    message_id: str | None
    subject: str | None
    date: str | None
    body_size: str | None
    attachment_filename: str | None
    ip: str | None
    created_at: str | None
    http_response_code: str | None
    http_response_headers: dict[str, Any] | None
    recipient_serial: str | None
    hex_recipient_serial: str | None
    recipient_issuer: str | None
    message_received: bool | None
    message_decrypted: bool | None
    message_signature_verified: bool | None
    message_processing_success: bool | None
    message_mdn_returned: bool | None
    encrypted_uri: str | None
    smime_signed_uri: str | None
    smime_uri: str | None
    raw_uri: str | None
    mdn_response_uri: str | None

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
        ) in As2IncomingMessage.default_attributes.items():
            value = attributes.get(attribute, default_value)
            setattr(self, attribute, value)

    def get_attributes(self):
        attrs = {
            k: getattr(self, k, None)
            for k in As2IncomingMessage.default_attributes
            if getattr(self, k, None) is not None
        }
        return attrs

    def _scope(self):
        if self._context is not None:
            return self._context
        return LegacyScope(self.options)


class As2IncomingMessageResource:
    """As2IncomingMessage operations that use one client's configuration.

    Get one from a client, such as ``client.as2_incoming_message``. Each operation
    takes the same arguments as the module-level function of the same name,
    and its options apply on top of the client's.
    """

    def __init__(self, scope):
        self._scope = scope

    def list(
        self,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> ListObj[As2IncomingMessage]:
        """Parameters:
        cursor - string - Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
        per_page - int64 - Number of records to show per page.  (Max: 10000, 1,000 or less is recommended).
        sort_by - object - If set, sort records by the specified field in either `asc` or `desc` direction. Valid fields are `workspace_id`, `created_at` or `as2_partner_id`.
        filter - object - If set, return records where the specified field is equal to the supplied value. Valid fields are `created_at`, `as2_station_id`, `workspace_id` or `as2_partner_id`. Valid field combinations are `[ as2_station_id, created_at ]`, `[ workspace_id, created_at ]`, `[ as2_partner_id, created_at ]`, `[ workspace_id, as2_station_id ]`, `[ workspace_id, as2_partner_id ]`, `[ workspace_id, as2_station_id, created_at ]` or `[ workspace_id, as2_partner_id, created_at ]`.
        filter_gt - object - If set, return records where the specified field is greater than the supplied value. Valid fields are `created_at`.
        filter_gteq - object - If set, return records where the specified field is greater than or equal the supplied value. Valid fields are `created_at`.
        filter_lt - object - If set, return records where the specified field is less than the supplied value. Valid fields are `created_at`.
        filter_lteq - object - If set, return records where the specified field is less than or equal the supplied value. Valid fields are `created_at`.
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
        if "filter_gt" in params and not isinstance(params["filter_gt"], dict):
            raise InvalidParameterError(
                "Bad parameter: filter_gt must be an dict"
            )
        if "filter_gteq" in params and not isinstance(
            params["filter_gteq"], dict
        ):
            raise InvalidParameterError(
                "Bad parameter: filter_gteq must be an dict"
            )
        if "filter_lt" in params and not isinstance(params["filter_lt"], dict):
            raise InvalidParameterError(
                "Bad parameter: filter_lt must be an dict"
            )
        if "filter_lteq" in params and not isinstance(
            params["filter_lteq"], dict
        ):
            raise InvalidParameterError(
                "Bad parameter: filter_lteq must be an dict"
            )
        operation = Operation.start(self._scope, options)
        return ListObj(
            As2IncomingMessage,
            "GET",
            "/as2_incoming_messages",
            params,
            operation,
        )

    def all(
        self,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> ListObj[As2IncomingMessage]:
        """The same as list()."""
        return self.list(params, options)

    def new(
        self,
        attributes: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> As2IncomingMessage:
        """A new As2IncomingMessage with attributes, not yet saved, whose
        operations use this resource's client."""
        obj = As2IncomingMessage(attributes, options)
        obj._context = self._scope._context_for(options)
        return obj


_legacy_resource = As2IncomingMessageResource(LEGACY)


def list(
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> ListObj[As2IncomingMessage]:
    """Parameters:
    cursor - string - Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
    per_page - int64 - Number of records to show per page.  (Max: 10000, 1,000 or less is recommended).
    sort_by - object - If set, sort records by the specified field in either `asc` or `desc` direction. Valid fields are `workspace_id`, `created_at` or `as2_partner_id`.
    filter - object - If set, return records where the specified field is equal to the supplied value. Valid fields are `created_at`, `as2_station_id`, `workspace_id` or `as2_partner_id`. Valid field combinations are `[ as2_station_id, created_at ]`, `[ workspace_id, created_at ]`, `[ as2_partner_id, created_at ]`, `[ workspace_id, as2_station_id ]`, `[ workspace_id, as2_partner_id ]`, `[ workspace_id, as2_station_id, created_at ]` or `[ workspace_id, as2_partner_id, created_at ]`.
    filter_gt - object - If set, return records where the specified field is greater than the supplied value. Valid fields are `created_at`.
    filter_gteq - object - If set, return records where the specified field is greater than or equal the supplied value. Valid fields are `created_at`.
    filter_lt - object - If set, return records where the specified field is less than the supplied value. Valid fields are `created_at`.
    filter_lteq - object - If set, return records where the specified field is less than or equal the supplied value. Valid fields are `created_at`.
    """
    return _legacy_resource.list(params, options)


def all(
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> ListObj[As2IncomingMessage]:
    """The same as list()."""
    return _legacy_resource.list(params, options)


def new(*args, **kwargs) -> As2IncomingMessage:
    return As2IncomingMessage(*args, **kwargs)
