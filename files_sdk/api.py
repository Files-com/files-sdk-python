import copy
import sys
import files_sdk
from files_sdk.api_client import ApiClient


class Api:
    __singleton_instance = None

    @staticmethod
    def client():
        if not Api.__singleton_instance:
            Api.__singleton_instance = ApiClient()

        return Api.__singleton_instance

    @staticmethod
    def send_request(verb, path, params, options=None):
        if not isinstance(options, dict):
            options = {}
        Api.warn_on_options_in_params(params)

        headers = copy.deepcopy(options)
        api_key = headers.pop("api_key", None)
        session_id = headers.pop("session_id", None)
        language = headers.pop("language", None)

        session = headers.pop("session", None)
        if session:
            if session.id:
                session.save
            session_id = str(session.id)

        response = Api.client().send_request(
            verb,
            path,
            api_key=api_key,
            session_id=session_id,
            language=language,
            params=params,
        )

        # Remove options not in the allow list
        options = {k: options[k] for k in files_sdk.OPTS if k in options}

        return response, options

        # Hash#select returns an array before 1.9
        # options_to_persist = {}
        # options.each do |k, v|
        #  options_to_persist[k] = v if Util::OPTS.include?(k)
        # end

    @staticmethod
    def warn_on_options_in_params(params):
        for opt in files_sdk.OPTS:
            if opt in params:
                print(
                    "WARNING: {opt} should be in the options dictionary, not the params dictionary.  You may need to create a second dictionary that goes after params.)".format(
                        opt=opt
                    ),
                    file=sys.stderr,
                )
