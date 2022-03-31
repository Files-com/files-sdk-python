import builtins
import datetime
from files_sdk.api import Api
from files_sdk.list_obj import ListObj
from files_sdk.exceptions import InvalidParameterError, MissingParameterError, NotImplementedError

class As2OutgoingMessage:
    default_attributes = {
        'id': None,     # int64 - Id of the AS2 Partner.
        'as2_partner_id': None,     # int64 - Id of the AS2 Partner associated with this message.
        'uuid': None,     # string - UUID assigned to this message.
        'http_headers': None,     # object - HTTP Headers sent with this message.
        'activity_log': None,     # string - JSON Structure of the activity log.
        'processing_result': None,     # string - Result of processing.
        'mic': None,     # string - AS2 Message Integrity Check
        'message_id': None,     # string - AS2 Message Id
        'body_size': None,     # string - Encrypted Payload Body Size
        'attachment_filename': None,     # string - Filename of the file being sent.
        'created_at': None,     # date-time - Message creation date/time
    }

    def __init__(self, attributes=None, options=None):
        if not isinstance(attributes, dict):
            attributes = {}
        if not isinstance(options, dict):
            options = {}
        self.set_attributes(attributes)
        self.options = options

    def set_attributes(self, attributes):
        for (attribute, default_value) in As2OutgoingMessage.default_attributes.items():
            setattr(self, attribute, attributes.get(attribute, default_value))

    def get_attributes(self):
        return {k: getattr(self, k, None) for k in As2OutgoingMessage.default_attributes if getattr(self, k, None) is not None}


# Parameters:
#   cursor - string - Used for pagination.  Send a cursor value to resume an existing list from the point at which you left off.  Get a cursor from an existing list via either the X-Files-Cursor-Next header or the X-Files-Cursor-Prev header.
#   per_page - int64 - Number of records to show per page.  (Max: 10,000, 1,000 or less is recommended).
#   as2_partner_id - int64 - As2 Partner ID.  If provided, will return message specific to that partner.
def list(params = None, options = None):
    if not isinstance(params, dict):
        params = {}
    if not isinstance(options, dict):
        options = {}
    if "cursor" in params and not isinstance(params["cursor"], str):
        raise InvalidParameterError("Bad parameter: cursor must be an str")
    if "per_page" in params and not isinstance(params["per_page"], int):
        raise InvalidParameterError("Bad parameter: per_page must be an int")
    if "as2_partner_id" in params and not isinstance(params["as2_partner_id"], int):
        raise InvalidParameterError("Bad parameter: as2_partner_id must be an int")
    return ListObj(As2OutgoingMessage,"GET", "/as2_outgoing_messages", params, options)

def all(params = None, options = None):
    list(params, options)

def new(*args, **kwargs):
    return As2OutgoingMessage(*args, **kwargs)