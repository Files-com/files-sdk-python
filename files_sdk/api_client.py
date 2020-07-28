import json
import random
import requests
import time
from urllib.parse import urljoin

import files_sdk
from files_sdk.exceptions import (APIConnectionError,
                                  APIError,
                                  AuthenticationError,
                                  Error,
                                  InvalidRequestError,
                                  PermissionsError,
                                  RateLimitError)
import files_sdk.util as util

class ApiClient:
    '''
    The Files.com API Client.
    '''

    def __init__(self):
        pass

    def send_remote_request(self, method, url, headers = {}, body = None):
        req = requests.Request(
                method,
                url=url,
                headers=headers,
                data=body
        )
        
        response = self.execute_request_with_auto_retry(req)
        return response

    def send_request(self, method, path, api_key=None, session_id=None, headers={}, params=None):
        full_path = files_sdk.base_path + path
        url = urljoin(files_sdk.base_url, full_path)

        if files_sdk.session_id:
            session_id = files_sdk.session_id

        if session_id and session_id != "":
            self.check_session_id(session_id)
        elif not path.startswith("/sessions"):
            if not api_key:
                api_key = files_sdk.get_api_key()
            self.check_api_key(api_key)

        headers = {**headers, **self.request_headers(api_key, session_id)}

        data = None
        query_params = None
        if method in ["GET", "HEAD", "DELETE"]:
            data = None
            query_params = params
        else:
            data = params
            query_params = None
 
        req = requests.Request(
                method,
                url=url,
                headers=headers,
                params=query_params,
                json=data
        )

        response = self.execute_request_with_auto_retry(req)

        if response.status_code != 204:
            try:
                response.data = response.json()
            except json.decoder.JSONDecodeError:
                raise self.general_api_error(response, "Error parsing JSON response")
        else:
            response.data = None

        return response

    def stream_download(self, uri, io, is_string_io=False):
        # NOTE the stream=True parameter below
        with requests.get(uri, stream=True) as r:
            r.raise_for_status() # TODO check this later
            for chunk in r.iter_content(chunk_size=8192, decode_unicode=is_string_io): 
                # If you have chunk encoded response uncomment if
                # and set chunk_size parameter to None.
                #if chunk: 
                io.write(chunk)

    def execute_request_with_auto_retry(self, request, skip_body_logging = False):
        for try_num in range(0, files_sdk.max_network_retries):
            try:
                response = None
                request_start = time.time()
                self.log_request(request, try_num)
                with requests.Session() as s:
                    response = s.send(request.prepare(), timeout=(files_sdk.open_timeout, files_sdk.read_timeout))
                self.log_response(request, request_start, response.status_code, response.content)
                response.raise_for_status()
                return response
            except Exception as e:
                if response is not None:
                    self.log_response(request, request_start, response.status_code, response.content)
                else:
                    self.log_response_error(request, request_start, e)

                if try_num + 1 == files_sdk.max_network_retries:
                    if response is not None:
                        raise self.handle_error_response(response) from None
                    else:
                        raise self.handle_network_error(e, request, try_num) from None
                    raise

                time.sleep(ApiClient.sleep_time(try_num))

    @staticmethod
    def sleep_time(num_retries):
        sleep_seconds = min(
            files_sdk.initial_network_retry_delay * (2**(num_retries - 1)),
            files_sdk.max_network_retry_delay
        )
        sleep_seconds *= (0.5 * (1 + random.random()))
        return max(files_sdk.initial_network_retry_delay, sleep_seconds)

    def request_headers(self, api_key, session_id):
        user_agent = "Files.com Python SDK v{version}".format(version=files_sdk.version)
        #user_agent += " " + format_app_info(Files.app_info) unless Files.app_info.nil?

        headers = {
            "User-Agent": user_agent,
            "Content-Type": "application/json",
        }
        if api_key:
            headers["X-FilesAPI-Key"] = api_key
        if session_id:
            headers["X-FilesAPI-Auth"] = session_id

        return headers

    def check_api_key(self, api_key):
        if not api_key:
            raise AuthenticationError("No Files.com API key provided. " \
              'Set your API key using "Files.api_key = <API-KEY>". ' \
              "You can generate API keys from the Files.com's web interface. ")

        if not api_key.isalnum():
            raise AuthenticationError("Your API key is invalid (it contains whitespace)")

    def check_session_id(self, session_id):
        if not session_id.isalnum():
            raise AuthenticationError("The provided Session ID is invalid (it contains whitespace)")

    def general_api_error(self, response, extra_info=None):
        msg = "Unexpected response object from API: {body} (HTTP response code was {status})".format(body=repr(response.content), status=response.status_code)
        if extra_info is not None:
            msg += " Additional Information: {}".format(extra_info)
        return APIError(msg)

    def handle_error_response(self, response):
        error_data = None

        try:
            response.data = response.json()
        except json.decoder.JSONDecodeError:
            response.data = ""

        try:
            if "error" in response.data:
                error_data = response.data["error"]
            elif "errors" in response.data:
                error_data = response.data["errors"]
            if isinstance(error_data, list) and len(error_data) > 0:
                error_data = error_data[0]
            elif isinstance(error_data, str):
                error_data = { "message" : error_data}

            if not error_data:
                raise Error("Unknown error")
        except Error:
            raise self.general_api_error(response, "Unknown error")

        error = self.specific_api_error(response, error_data)

        error.response = response
        raise error

    def specific_api_error(self, response, error_data):
        util.log_error("API error", status=response.status_code, error_message=error_data)

        opts = {
            "http_body" : response.content,
            "headers" : response.headers,
            "http_status" : response.status_code,
            "json_body" : response.data,
            "code" : error_data.get("code", response.status_code),
        }

        if response.status_code in [400, 404]:
            return InvalidRequestError(error_data["message"], **opts)
        elif response.status_code in [401]:
            return AuthenticationError(error_data["message"], **opts)
        elif response.status_code in [403]:
            return PermissionsError(error_data["message"], **opts)
        elif response.status_code in [429]:
            return RateLimitError(error_data["message"], **opts)
        else: 
            return APIError(error_data["message"], **opts)

    def handle_network_error(self, error, request, num_retries):
        util.log_error("Network error", error_message=error)
        msg = "Could not connect to Files.com at URL {}. Please check your internet connection and try again. If this problem persists, you should check Files.com's service status at https://status.files.com, or contact your primary account representative.".format(files_sdk.base_url)
        if num_retries > 0:
            msg += " Request was retried {} times.".format(num_retries)
        msg += "\n\n(Network error: {})".format(error)

        return APIConnectionError(msg)

    def log_request(self, request, num_retries):
        util.log_info("Request", method=request.method, num_retries=num_retries, url=request.url)
        util.log_debug("Request details", body=request.data, query_params=request.params)

    def log_response(self, request, request_start, status, body):
        util.log_info("Response", elapsed=(time.time() - request_start), method=request.method, url=request.url, status=status)
        util.log_debug("Response details", body=body)
    
    def log_response_error(self, request, request_start, error):
        util.log_error("Error", elapsed=(time.time() - request_start), error_message=error, method=request.method, url=request.url)