import datetime
from files_com.api import Api
from files_com.exceptions import InvalidParameterError, MissingParameterError, NotImplementedError

class Request:
    default_attributes = {
        'id': None,     # int64 - Request ID
        'path': None,     # string - Folder path This must be slash-delimited, but it must neither start nor end with a slash. Maximum of 5000 characters.
        'source': None,     # string - Source filename, if applicable
        'destination': None,     # string - Destination filename
        'automation_id': None,     # string - ID of automation that created request
        'user_display_name': None,     # string - User making the request (if applicable)
        'user_ids': None,     # string - A list of user IDs to request the file from. If sent as a string, it should be comma-delimited.
        'group_ids': None,     # string - A list of group IDs to request the file from. If sent as a string, it should be comma-delimited.
    }

    def __init__(self, attributes, options={}):
        self.set_attributes(attributes)
        self.options = options

    def set_attributes(self, attributes):
        for (attribute, default_value) in Request.default_attributes.items():
            setattr(self, attribute, attributes.get(attribute, default_value))

    def get_attributes(self):
        return {k: getattr(self, k, None) for k in Request.default_attributes}


    def save(self):
        if hasattr(self, "path") and self.path:
            raise NotImplementedError("The Request object doesn't support updates.")
        else:
            new_obj = Request.do_create(self.get_attributes(), self.options)
            self.set_attributes(new_obj.get_attributes())

    # Parameters:
    #   page - int64 - Current page number.
    #   per_page - int64 - Number of records to show per page.  (Max: 10,000, 1,000 or less is recommended).
    #   action - string - Deprecated: If set to `count` returns a count of matching records rather than the records themselves.
    #   cursor - string - Send cursor to resume an existing list from the point at which you left off.  Get a cursor from an existing list via the X-Files-Cursor-Next header.
    #   sort_by - object - If set, sort records by the specified field in either 'asc' or 'desc' direction (e.g. sort_by[last_login_at]=desc). Valid fields are `site_id`, `folder_id` or `destination`.
    #   mine - boolean - Only show requests of the current user?  (Defaults to true if current user is not a site admin.)
    #   path - string - Path to show requests for.  If omitted, shows all paths. Send `/` to represent the root directory.
    @staticmethod
    def do_list(path, params = {}, options = {}):
        if not isinstance(params, dict):
            params = {}
        params["path"] = path
        if "page" in params and not isinstance(params["page"], int):
            raise InvalidParameterError("Bad parameter: page must be an int")
        if "per_page" in params and not isinstance(params["per_page"], int):
            raise InvalidParameterError("Bad parameter: per_page must be an int")
        if "action" in params and not isinstance(params["action"], str):
            raise InvalidParameterError("Bad parameter: action must be an str")
        if "cursor" in params and not isinstance(params["cursor"], str):
            raise InvalidParameterError("Bad parameter: cursor must be an str")
        if "sort_by" in params and not isinstance(params["sort_by"], dict):
            raise InvalidParameterError("Bad parameter: sort_by must be an dict")
        if "path" in params and not isinstance(params["path"], str):
            raise InvalidParameterError("Bad parameter: path must be an str")

      #TODO: List is a custom class in the ruby SDK for paging, tackle later 
      # List.new(Request, params) do
      # 
      #    Api.send_request("GET", "/requests", params, options)
      #  end

    @staticmethod
    def do_all(path, params = {}):
        Request.do_list(path, params)
    
    # Parameters:
    #   page - int64 - Current page number.
    #   per_page - int64 - Number of records to show per page.  (Max: 10,000, 1,000 or less is recommended).
    #   action - string - Deprecated: If set to `count` returns a count of matching records rather than the records themselves.
    #   cursor - string - Send cursor to resume an existing list from the point at which you left off.  Get a cursor from an existing list via the X-Files-Cursor-Next header.
    #   sort_by - object - If set, sort records by the specified field in either 'asc' or 'desc' direction (e.g. sort_by[last_login_at]=desc). Valid fields are `site_id`, `folder_id` or `destination`.
    #   mine - boolean - Only show requests of the current user?  (Defaults to true if current user is not a site admin.)
    #   path (required) - string - Path to show requests for.  If omitted, shows all paths. Send `/` to represent the root directory.
    @staticmethod
    def do_find_folder(path, params = {}, options = {}):
        if not isinstance(params, dict):
            params = {}
        params["path"] = path
        if "page" in params and not isinstance(params["page"], int):
            raise InvalidParameterError("Bad parameter: page must be an int")
        if "per_page" in params and not isinstance(params["per_page"], int):
            raise InvalidParameterError("Bad parameter: per_page must be an int")
        if "action" in params and not isinstance(params["action"], str):
            raise InvalidParameterError("Bad parameter: action must be an str")
        if "cursor" in params and not isinstance(params["cursor"], str):
            raise InvalidParameterError("Bad parameter: cursor must be an str")
        if "sort_by" in params and not isinstance(params["sort_by"], dict):
            raise InvalidParameterError("Bad parameter: sort_by must be an dict")
        if "path" in params and not isinstance(params["path"], str):
            raise InvalidParameterError("Bad parameter: path must be an str")
        if "path" not in params:
            raise MissingParameterError("Parameter missing: path")

      #TODO: List is a custom class in the ruby SDK for paging, tackle later 
      # List.new(Request, params) do
      # 
      #    Api.send_request("GET", "/requests/folders/#{params[:path]}", params, options)
      #  end
    
    # Parameters:
    #   path (required) - string - Folder path on which to request the file.
    #   destination (required) - string - Destination filename (without extension) to request.
    #   user_ids - string - A list of user IDs to request the file from. If sent as a string, it should be comma-delimited.
    #   group_ids - string - A list of group IDs to request the file from. If sent as a string, it should be comma-delimited.
    @staticmethod
    def do_create(path, params = {}, options = {}):
        if not isinstance(params, dict):
            params = {}
        params["path"] = path
        if "path" in params and not isinstance(params["path"], str):
            raise InvalidParameterError("Bad parameter: path must be an str")
        if "destination" in params and not isinstance(params["destination"], str):
            raise InvalidParameterError("Bad parameter: destination must be an str")
        if "user_ids" in params and not isinstance(params["user_ids"], str):
            raise InvalidParameterError("Bad parameter: user_ids must be an str")
        if "group_ids" in params and not isinstance(params["group_ids"], str):
            raise InvalidParameterError("Bad parameter: group_ids must be an str")
        if "path" not in params:
            raise MissingParameterError("Parameter missing: path")
        if "destination" not in params:
            raise MissingParameterError("Parameter missing: destination")

        response, options = Api.send_request("POST", "/requests", params, options)
        return Request(response.data, options)
    
    # Parameters:
    #   id (required) - int64 - Request ID.
    @staticmethod
    def do_delete(id, params = {}, options = {}):
        if not isinstance(params, dict):
            params = {}
        params["id"] = id
        if "id" in params and not isinstance(params["id"], int):
            raise InvalidParameterError("Bad parameter: id must be an int")
        if "id" not in params:
            raise MissingParameterError("Parameter missing: id")

        response, _options = Api.send_request("DELETE", "/requests/{id}".format(id=params['id']), params, options)
        return response.data

    @staticmethod
    def do_destroy(id, params = {}):
        Request.do_delete(id, params)
    