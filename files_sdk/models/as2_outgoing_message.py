import builtins  # noqa: F401
from files_sdk.api import Api  # noqa: F401
from files_sdk.list_obj import ListObj
from files_sdk.error import (  # noqa: F401
    InvalidParameterError,
    MissingParameterError,
    NotImplementedError,
)


class As2OutgoingMessage:
    default_attributes = {
        "id": None,  # int64 - Id of the AS2 Partner.
        "as2_partner_id": None,  # int64 - Id of the AS2 Partner associated with this message.
        "as2_station_id": None,  # int64 - Id of the AS2 Station associated with this message.
        "uuid": None,  # string - UUID assigned to this message.
        "http_headers": None,  # object - HTTP Headers sent with this message.
        "activity_log": None,  # string - JSON Structure of the activity log.
        "processing_result": None,  # string - Result of processing.
        "processing_result_description": None,  # string - Result of processing description.
        "mic": None,  # string - AS2 Message Integrity Check SHA1
        "mic_sha_256": None,  # string - AS2 Message Integrity Check SHA256
        "as2_to": None,  # string - AS2 TO
        "as2_from": None,  # string - AS2 FROM
        "date": None,  # string - Date Header
        "message_id": None,  # string - AS2 Message Id
        "body_size": None,  # string - Encrypted Payload Body Size
        "attachment_filename": None,  # string - Filename of the file being sent.
        "created_at": None,  # date-time - Message creation date/time
        "http_response_code": None,  # string - HTTP Response Code received for this message
        "http_response_headers": None,  # object - HTTP Headers received for this message.
        "http_transmission_duration": None,  # double - HTTP transmission duration in seceonds
        "mdn_received": None,  # boolean - Did the partner give a response body?
        "mdn_valid": None,  # boolean - Is the response in MDN format?
        "mdn_signature_verified": None,  # boolean - MDN signature verified?
        "mdn_message_id_matched": None,  # boolean - MDN message id matched?
        "mdn_mic_matched": None,  # boolean - MDN MIC matched?
        "mdn_processing_success": None,  # boolean - MDN disposition indicate a successful processing?
        "raw_uri": None,  # string - URL to download the original file contents
        "smime_uri": None,  # string - URL to download the file contents encoded as smime
        "smime_signed_uri": None,  # string - URL to download the file contents as smime with signature
        "encrypted_uri": None,  # string - URL to download the encrypted signed smime that is to sent as AS2 body
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
        ) in As2OutgoingMessage.default_attributes.items():
            setattr(self, attribute, attributes.get(attribute, default_value))

    def get_attributes(self):
        return {
            k: getattr(self, k, None)
            for k in As2OutgoingMessage.default_attributes
            if getattr(self, k, None) is not None
        }


# Parameters:
#   cursor - string - Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
#   per_page - int64 - Number of records to show per page.  (Max: 10,000, 1,000 or less is recommended).
#   sort_by - object - If set, sort records by the specified field in either `asc` or `desc` direction. Valid fields are `created_at` and `as2_partner_id`.
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
        As2OutgoingMessage, "GET", "/as2_outgoing_messages", params, options
    )


def all(params=None, options=None):
    list(params, options)


def new(*args, **kwargs):
    return As2OutgoingMessage(*args, **kwargs)
