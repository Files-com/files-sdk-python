import json
import random
import requests
import time
from urllib.parse import urljoin

import files_sdk
from files_sdk.error import (
    APIConnectionError,
    APIError,
    AuthenticationError,
    Error,
)
import files_sdk.util as util
from requests_toolbelt.adapters import source


class ApiClient:
    """
    The Files.com API Client.
    """

    def __init__(self):
        pass

        self.session = requests.Session()

        if (
            files_sdk.get_source_ip() is not None
            and self.session.adapters.get(files_sdk.base_url, None) is None
        ):
            self.session.mount(
                files_sdk.base_url,
                source.SourceAddressAdapter(files_sdk.get_source_ip()),
            )

    def send_remote_request(self, method, url, headers=None, body=None):
        if headers is None:
            headers = {}
        req = requests.Request(method, url=url, headers=headers, data=body)

        response = self.execute_request_with_auto_retry(req)
        return response

    def send_request(
        self,
        method,
        path,
        api_key=None,
        session_id=None,
        language=None,
        headers=None,
        params=None,
    ):
        if headers is None:
            headers = {}
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

        if files_sdk.language:
            language = files_sdk.language

        headers = {
            **headers,
            **self.request_headers(api_key, session_id, language),
        }

        data = None
        query_params = None
        if params:
            if method in ["GET", "HEAD", "DELETE"]:
                data = None
                _params = {}
                for k, v in params.items():
                    if isinstance(v, dict):
                        for k2, v2 in v.items():
                            _params[f"{k}[{k2}]"] = v2
                    else:
                        _params[k] = v
                query_params = _params
            else:
                data = params
                query_params = None

        req = requests.Request(
            method, url=url, headers=headers, params=query_params, json=data
        )

        response = self.execute_request_with_auto_retry(req)

        if response.status_code != 204:
            try:
                response.data = response.json()
            except json.decoder.JSONDecodeError:
                if response.status_code == 403:
                    raise AuthenticationError(
                        response.content,
                        http_status=response.status_code,
                        headers=response.headers,
                    )
                if response.status_code >= 500:
                    raise APIConnectionError(
                        response.content,
                        http_status=response.status_code,
                        headers=response.headers,
                    )
                raise self.general_api_error(
                    response, "Error parsing JSON response"
                )
        else:
            response.data = None

        return response

    def stream_download(self, uri, io, is_string_io=False):
        # NOTE the stream=True parameter below
        with requests.get(uri, stream=True) as r:
            r.raise_for_status()  # TODO check this later
            for chunk in r.iter_content(
                chunk_size=8192, decode_unicode=is_string_io
            ):
                # If you have chunk encoded response uncomment if
                # and set chunk_size parameter to None.
                # if chunk:
                io.write(chunk)

    def execute_request_with_auto_retry(
        self, request, skip_body_logging=False
    ):
        for try_num in range(0, files_sdk.max_network_retries):
            response = None
            request_start = time.time()
            try:
                self.log_request(request, try_num)
                prepped = request.prepare()
                settings = self.session.merge_environment_settings(
                    prepped.url, {}, None, None, None
                )
                response = self.session.send(
                    prepped,
                    timeout=(files_sdk.open_timeout, files_sdk.read_timeout),
                    **settings,
                )

                self.log_response(
                    request,
                    request_start,
                    response.status_code,
                    response.content,
                )
                response.raise_for_status()
                return response
            except Exception as e:
                if response is not None:
                    self.log_response(
                        request,
                        request_start,
                        response.status_code,
                        response.content,
                    )
                else:
                    self.log_response_error(request, request_start, e)

                if try_num + 1 == files_sdk.max_network_retries:
                    if response is not None:
                        self.handle_error_response(response)
                    else:
                        raise self.handle_network_error(
                            e, request, try_num
                        ) from None
                    raise

                time.sleep(ApiClient.sleep_time(try_num))
        raise APIConnectionError(
            f"Request failed after {files_sdk.max_network_retries} attempts"
        )

    @staticmethod
    def sleep_time(num_retries):
        sleep_seconds = min(
            files_sdk.initial_network_retry_delay * (2 ** (num_retries - 1)),
            files_sdk.max_network_retry_delay,
        )
        sleep_seconds *= 0.5 * (1 + random.random())
        return max(files_sdk.initial_network_retry_delay, sleep_seconds)

    def request_headers(self, api_key, session_id, language):
        user_agent = "Files.com Python SDK v{version}".format(
            version=files_sdk.version
        )
        # user_agent += " " + format_app_info(Files.app_info) unless Files.app_info.nil?

        headers = {
            "User-Agent": user_agent,
            "Content-Type": "application/json",
        }
        if api_key:
            headers["X-FilesAPI-Key"] = api_key
        if session_id:
            headers["X-FilesAPI-Auth"] = session_id
        if language:
            headers["Accept-Language"] = language

        return headers

    def check_api_key(self, api_key):
        if not api_key:
            raise AuthenticationError(
                "No Files.com API key provided. "
                'Set your API key using "Files.api_key = <API-KEY>". '
                "You can generate API keys from the Files.com's web interface. "
            )

        if not api_key.isalnum():
            raise AuthenticationError(
                "Your API key is invalid (it contains whitespace)"
            )

    def check_session_id(self, session_id):
        if not session_id.isalnum():
            raise AuthenticationError(
                "The provided Session ID is invalid (it contains whitespace)"
            )

    def general_api_error(self, response, extra_info=None):
        msg = "Unexpected response object from API: {body} (HTTP response code was {status})".format(
            body=repr(response.content), status=response.status_code
        )
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
            if isinstance(error_data, str):
                error_data = {"message": error_data}

            if not error_data:
                raise Error("Unknown error")
        except Error:
            raise self.general_api_error(response, "Unknown error")

        error = self.specific_api_error(response, error_data)

        error.response = response
        raise error

    def specific_api_error(self, response, error_data):
        import files_sdk.error

        util.log_error(
            "API error", status=response.status_code, error_message=error_data
        )

        opts = {
            "http_body": response.content,
            "headers": response.headers,
            "http_status": response.status_code,
            "json_body": response.data,
            "code": error_data.get("code", response.status_code),
        }

        error_type = response.data["type"].split("/")[-1]
        error_class_name = (
            "".join(list(map(str.capitalize, error_type.split("-")))) + "Error"
        )
        try:
            return getattr(files_sdk.error, error_class_name)(
                error_data["message"], **opts
            )
        except AttributeError:
            return APIError(error_data["message"], **opts)

    def handle_network_error(self, error, request, num_retries):
        util.log_error("Network error", error_message=error)
        msg = "Could not connect to Files.com at URL {}. Please check your internet connection and try again. If this problem persists, you should check Files.com's service status at https://status.files.com, or contact your primary account representative.".format(
            files_sdk.base_url
        )
        if num_retries > 0:
            msg += " Request was retried {} times.".format(num_retries)
        msg += "\n\n(Network error: {})".format(error)

        return APIConnectionError(msg)

    def log_request(self, request, num_retries):
        util.log_info(
            "Request",
            method=request.method,
            num_retries=num_retries,
            url=request.url,
        )
        util.log_debug(
            "Request details", body=request.data, query_params=request.params
        )

    def log_response(self, request, request_start, status, body):
        util.log_info(
            "Response",
            elapsed=(time.time() - request_start),
            method=request.method,
            url=request.url,
            status=status,
        )
        util.log_debug("Response details", body=body)

    def log_response_error(self, request, request_start, error):
        util.log_error(
            "Error",
            elapsed=(time.time() - request_start),
            error_message=error,
            method=request.method,
            url=request.url,
        )
