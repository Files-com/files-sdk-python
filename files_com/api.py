import copy
import sys
import files_com
from files_com.api_client import ApiClient
      
class Api:
    @staticmethod
    def api_client():
        return ApiClient()

    @staticmethod
    def send_request(verb, path, params, options ={}):
        Api.warn_on_options_in_params(params)

        headers = copy.deepcopy(options)
        api_key = headers.pop("api_key", None)
        
        #client = headers.delete(:client)
        #session_id = headers.delete(:session_id)
        #if session = headers.delete(:session)
        #  session.save unless session.id
        #  session_id = session.id
        #end

        client = ApiClient()

        response = client.send_request(verb, path, api_key=api_key, params=params)

        # Remove options not in the allow list
        options = {k: options[k] for k in files_com.OPTS if k in options}

        return response, options

        # Hash#select returns an array before 1.9
        #options_to_persist = {}
        #options.each do |k, v|
        #  options_to_persist[k] = v if Util::OPTS.include?(k)
        #end

    @staticmethod
    def warn_on_options_in_params(params):
        for opt in files_com.OPTS:
            if opt in params:
                print("WARNING: {opt} should be in the options dictionary, not the params dictionary.  You may need to create a second dictionary that goes after params.)".format(opt=opt), file=sys.stderr)
