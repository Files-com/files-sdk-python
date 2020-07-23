import datetime
from files_com.models.account_line_item import AccountLineItem
from files_com.api import Api
from files_com.exceptions import InvalidParameterError, MissingParameterError, NotImplementedError

class Invoice:
    default_attributes = {
        'id': None,     # int64 - Line item Id
        'amount': None,     # double - Line item amount
        'balance': None,     # double - Line item balance
        'created_at': None,     # date-time - Line item created at
        'currency': None,     # string - Line item currency
        'download_uri': None,     # string - Line item download uri
        'invoice_line_items': None,     # array - Associated invoice line items
        'method': None,     # string - Line item payment method
        'payment_line_items': None,     # array - Associated payment line items
        'payment_reversed_at': None,     # date-time - Date/time payment was reversed if applicable
        'payment_type': None,     # string - Type of payment if applicable
        'site_name': None,     # string - Site name this line item is for
        'type': None,     # string - Type of line item, either payment or invoice
        'updated_at': None,     # date-time - Line item updated at
    }

    def __init__(self, attributes, options={}):
        self.set_attributes(attributes)
        self.options = options

    def set_attributes(self, attributes):
        for (attribute, default_value) in Invoice.default_attributes.items():
            setattr(self, attribute, attributes.get(attribute, default_value))

    def get_attributes(self):
        return {k: getattr(self, k, None) for k in Invoice.default_attributes}


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

        response, options = Api.send_request("GET", "/invoices", params, options)
        return [ AccountLineItem(entity_data, options) for entity_data in response.data ]

    @staticmethod
    def do_all(params = {}):
        Invoice.do_list(params)
    
    # Parameters:
    #   id (required) - int64 - Invoice ID.
    @staticmethod
    def do_find(id, params = {}, options = {}):
        if not isinstance(params, dict):
            params = {}
        params["id"] = id
        if "id" in params and not isinstance(params["id"], int):
            raise InvalidParameterError("Bad parameter: id must be an int")
        if "id" not in params:
            raise MissingParameterError("Parameter missing: id")

        response, options = Api.send_request("GET", "/invoices/{id}".format(id=params['id']), params, options)
        return AccountLineItem(response.data, options)

    @staticmethod
    def do_get(id, params = {}):
        Invoice.do_find(id, params)
    