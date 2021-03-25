import datetime
from files_sdk.api import Api
from files_sdk.exceptions import InvalidParameterError, MissingParameterError, NotImplementedError

class WebhookTest:
    default_attributes = {
        'code': None,     # int64 - Status HTTP code
        'message': None,     # string - Error message
        'status': None,     # string - Status message
        'data': None,     # Additional data
        'success': None,     # boolean - The success status of the webhook test
        'url': None,     # string - URL for testing the webhook.
        'method': None,     # string - HTTP method(GET or POST).
        'encoding': None,     # string - HTTP encoding method.  Can be JSON, XML, or RAW (form data).
        'headers': None,     # object - Additional request headers.
        'body': None,     # object - Additional body parameters.
        'action': None,     # string - action for test body
    }

    def __init__(self, attributes=None, options=None):
        if not isinstance(attributes, dict):
            attributes = {}
        if not isinstance(options, dict):
            options = {}
        self.set_attributes(attributes)
        self.options = options

    def set_attributes(self, attributes):
        for (attribute, default_value) in WebhookTest.default_attributes.items():
            setattr(self, attribute, attributes.get(attribute, default_value))

    def get_attributes(self):
        return {k: getattr(self, k, None) for k in WebhookTest.default_attributes if getattr(self, k, None) is not None}


    def save(self):
        if hasattr(self, "id") and self.id:
            raise NotImplementedError("The WebhookTest object doesn't support updates.")
        else:
            new_obj = create(self.get_attributes(), self.options)
            self.set_attributes(new_obj.get_attributes())

# Parameters:
#   url (required) - string - URL for testing the webhook.
#   method - string - HTTP method(GET or POST).
#   encoding - string - HTTP encoding method.  Can be JSON, XML, or RAW (form data).
#   headers - object - Additional request headers.
#   body - object - Additional body parameters.
#   action - string - action for test body
def create(params = None, options = None):
    if not isinstance(params, dict):
        params = {}
    if not isinstance(options, dict):
        options = {}
    if "url" in params and not isinstance(params["url"], str):
        raise InvalidParameterError("Bad parameter: url must be an str")
    if "method" in params and not isinstance(params["method"], str):
        raise InvalidParameterError("Bad parameter: method must be an str")
    if "encoding" in params and not isinstance(params["encoding"], str):
        raise InvalidParameterError("Bad parameter: encoding must be an str")
    if "headers" in params and not isinstance(params["headers"], dict):
        raise InvalidParameterError("Bad parameter: headers must be an dict")
    if "body" in params and not isinstance(params["body"], dict):
        raise InvalidParameterError("Bad parameter: body must be an dict")
    if "action" in params and not isinstance(params["action"], str):
        raise InvalidParameterError("Bad parameter: action must be an str")
    if "url" not in params:
        raise MissingParameterError("Parameter missing: url")
    response, options = Api.send_request("POST", "/webhook_tests", params, options)
    return WebhookTest(response.data, options)

def new(*args, **kwargs):
    return WebhookTest(*args, **kwargs)