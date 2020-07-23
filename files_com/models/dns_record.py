import datetime
from files_com.api import Api
from files_com.exceptions import InvalidParameterError, MissingParameterError, NotImplementedError

class DnsRecord:
    default_attributes = {
        'id': None,     # string - Unique label for DNS record; used by Zapier and other integrations.
        'domain': None,     # string - DNS record domain name
        'rrtype': None,     # string - DNS record type
        'value': None,     # string - DNS record value
    }

    def __init__(self, attributes, options={}):
        self.set_attributes(attributes)
        self.options = options

    def set_attributes(self, attributes):
        for (attribute, default_value) in DnsRecord.default_attributes.items():
            setattr(self, attribute, attributes.get(attribute, default_value))

    def get_attributes(self):
        return {k: getattr(self, k, None) for k in DnsRecord.default_attributes}


    # Parameters:
    #   page - int64 - Current page number.
    #   per_page - int64 - Number of records to show per page.  (Max: 10,000, 1,000 or less is recommended).
    #   action - string - Deprecated: If set to `count` returns a count of matching records rather than the records themselves.
    @staticmethod
    def do_list(params = {}, options = {}):
        if "page" in params and not isinstance(params["page"], int):
            raise InvalidParameterError("Bad parameter: page must be an int")
        if "per_page" in params and not isinstance(params["per_page"], int):
            raise InvalidParameterError("Bad parameter: per_page must be an int")
        if "action" in params and not isinstance(params["action"], str):
            raise InvalidParameterError("Bad parameter: action must be an str")

        response, options = Api.send_request("GET", "/dns_records", params, options)
        return [ DnsRecord(entity_data, options) for entity_data in response.data ]

    @staticmethod
    def do_all(params = {}):
        DnsRecord.do_list(params)
    