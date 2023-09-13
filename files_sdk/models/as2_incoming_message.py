import builtins  # noqa: F401
from files_sdk.api import Api  # noqa: F401
from files_sdk.list_obj import ListObj
from files_sdk.error import (  # noqa: F401
    InvalidParameterError,
    MissingParameterError,
    NotImplementedError,
)


class As2IncomingMessage:
    default_attributes = {
        "id": None,  # int64 - Id of the AS2 Partner.
        "as2_partner_id": None,  # int64 - Id of the AS2 Partner associated with this message.
        "as2_station_id": None,  # int64 - Id of the AS2 Station associated with this message.
        "uuid": None,  # string - UUID assigned to this message.
        "content_type": None,  # string - Content Type header of the incoming message.
        "http_headers": None,  # object - HTTP Headers sent with this message.
        "activity_log": None,  # string - JSON Structure of the activity log.
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

    def __init__(self, attributes=None, options=None):
        if not isinstance(attributes, dict):
            attributes = {}
        if not isinstance(options, dict):
            options = {}
        self.set_attributes(attributes)
        self.options = options

    def set_attributes(self, attributes):
        for (
            attribute,
            default_value,
        ) in As2IncomingMessage.default_attributes.items():
            setattr(self, attribute, attributes.get(attribute, default_value))

    def get_attributes(self):
        return {
            k: getattr(self, k, None)
            for k in As2IncomingMessage.default_attributes
            if getattr(self, k, None) is not None
        }


# Parameters:
#   cursor - string - Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
#   per_page - int64 - Number of records to show per page.  (Max: 10,000, 1,000 or less is recommended).
#   sort_by - object - If set, sort records by the specified field in either `asc` or `desc` direction (e.g. `sort_by[created_at]=desc`). Valid fields are `created_at` and `as2_partner_id`.
#   filter - object - If set, return records where the specified field is equal to the supplied value. Valid fields are `created_at`.
#   filter_gt - object - If set, return records where the specified field is greater than the supplied value. Valid fields are `created_at`.
#   filter_gteq - object - If set, return records where the specified field is greater than or equal the supplied value. Valid fields are `created_at`.
#   filter_lt - object - If set, return records where the specified field is less than the supplied value. Valid fields are `created_at`.
#   filter_lteq - object - If set, return records where the specified field is less than or equal the supplied value. Valid fields are `created_at`.
#   as2_partner_id - int64 - As2 Partner ID.  If provided, will return message specific to that partner.
def list(params=None, options=None):
    if not isinstance(params, dict):
        params = {}
    if not isinstance(options, dict):
        options = {}
    if "cursor" in params and not isinstance(params["cursor"], str):
        raise InvalidParameterError("Bad parameter: cursor must be an str")
    if "per_page" in params and not isinstance(params["per_page"], int):
        raise InvalidParameterError("Bad parameter: per_page must be an int")
    if "sort_by" in params and not isinstance(params["sort_by"], dict):
        raise InvalidParameterError("Bad parameter: sort_by must be an dict")
    if "filter" in params and not isinstance(params["filter"], dict):
        raise InvalidParameterError("Bad parameter: filter must be an dict")
    if "filter_gt" in params and not isinstance(params["filter_gt"], dict):
        raise InvalidParameterError("Bad parameter: filter_gt must be an dict")
    if "filter_gteq" in params and not isinstance(params["filter_gteq"], dict):
        raise InvalidParameterError(
            "Bad parameter: filter_gteq must be an dict"
        )
    if "filter_lt" in params and not isinstance(params["filter_lt"], dict):
        raise InvalidParameterError("Bad parameter: filter_lt must be an dict")
    if "filter_lteq" in params and not isinstance(params["filter_lteq"], dict):
        raise InvalidParameterError(
            "Bad parameter: filter_lteq must be an dict"
        )
    if "as2_partner_id" in params and not isinstance(
        params["as2_partner_id"], int
    ):
        raise InvalidParameterError(
            "Bad parameter: as2_partner_id must be an int"
        )
    return ListObj(
        As2IncomingMessage, "GET", "/as2_incoming_messages", params, options
    )


def all(params=None, options=None):
    list(params, options)


def new(*args, **kwargs):
    return As2IncomingMessage(*args, **kwargs)
