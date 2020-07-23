import json
import random
import requests
import time
from urllib.parse import urljoin

import files_com
from files_com.exceptions import (APIConnectionError,
                                  APIError,
                                  AuthenticationError,
                                  Error,
                                  InvalidRequestError,
                                  PermissionsError,
                                  RateLimitError)

class ApiClient:
    '''
    The Files.com API Client.
    '''

    def __init__(self):
        pass

    def send_request(self, method, path, api_key=None, headers={}, params=None):
        path = files_com.base_path + path
        url = urljoin(files_com.base_url, path)

        if not api_key:
            api_key = files_com.api_key
        self.check_api_key(api_key)

        headers = {**headers, **self.request_headers(api_key, None)}

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
                data=data
        ).prepare()

        response = self.execute_request_with_auto_retry(req)

        #print(params)
        #print(headers)
        #print(response.status_code)
        #print(response.json())
        #print(response.content)
        #print(url)

        if response.status_code != 204:
            try:
                response.data = response.json()
            except json.decoder.JSONDecodeError:
                raise self.general_api_error(response, "Error parsing JSON response")
        else:
            response.data = None



        return response

    def stream_download(self, uri, io):
        # NOTE the stream=True parameter below
        with requests.get(uri, stream=True) as r:
            r.raise_for_status() # TODO check this later
            for chunk in r.iter_content(chunk_size=8192): 
                # If you have chunk encoded response uncomment if
                # and set chunk_size parameter to None.
                #if chunk: 
                io.write(chunk)

    #     ####
    #         def stream_download(uri, io)
    #   if conn.adapter == Faraday::Adapter::NetHttp
    #     uri = URI(uri)
    #     Net::HTTP.start(uri.host, uri.port, use_ssl: uri.scheme == 'https') do |http|
    #       request = Net::HTTP::Get.new uri
    #       http.request request do |response|
    #         io.fulfill_content_length(response.content_length) if io.respond_to?(:fulfill_content_length)
    #         response.read_body do |chunk|
    #           io << chunk.encode!
    #         end
    #       end
    #     end
    #   else
    #     response = remote_request(:get, uri)
    #     io.fulfill_content_length(response.content_length) if io.respond_to?(:fulfill_content_length)
    #     io.write(response.body)
    #   end
    # end

    def execute_request_with_auto_retry(self, request, skip_body_logging = False):
        for try_num in range(0, files_com.max_network_retries):
            try:
                #TODO make Python # request_start = Time.now
                #TODO #log_request(context, num_retries, skip_body_logging)
                response = None
                with requests.Session() as s:
                    response = s.send(request, timeout=(files_com.open_timeout, files_com.read_timeout))
                response.raise_for_status()
                return response

                #TODO #log_response(context, request_start, resp.status, resp.body, skip_body_logging)
            except Exception as e:
                #TODO error_context = context

                # TODO Log nicely if possible
                # if e.respond_to?(:response) && e.response
                #   error_context = context
                #   log_response(error_context, request_start,
                #                e.response[:status], e.response[:body], skip_body_logging
                #   )
                # else
                #   log_response_error(error_context, request_start, e)
                # end

                if try_num + 1 == files_com.max_network_retries:
                    error_context = None # TODO Fix this??
                    if response:
                        raise self.handle_error_response(response, error_context)
                    else:
                        raise self.handle_network_error(e, request, error_context, try_num)
                    raise e

                #TODO handle_network_error(e, error_context, num_retries, base_url)
                time.sleep(ApiClient.sleep_time(try_num))

    @staticmethod
    def sleep_time(num_retries):
        sleep_seconds = min(
            files_com.initial_network_retry_delay * (2**(num_retries - 1)),
            files_com.max_network_retry_delay
        )
        sleep_seconds *= (0.5 * (1 + random.random()))
        return max(files_com.initial_network_retry_delay, sleep_seconds)

    def request_headers(self, api_key, session_id):
        user_agent = "Files.com Python SDK v{version}".format(version=files_com.version)
        #user_agent += " " + format_app_info(Files.app_info) unless Files.app_info.nil?

        headers = {
            "User-Agent": user_agent,
            "Content-Type": "application/x-www-form-urlencoded",
        }
        if api_key:
            headers["X-FilesAPI-Key"] = api_key
        #headers["X-FilesAPI-Auth"] = session_id if session_id

        return headers

    def check_api_key(self, api_key):
        if not api_key:
            raise AuthenticationError("No Files.com API key provided. " \
              'Set your API key using "Files.api_key = <API-KEY>". ' \
              "You can generate API keys from the Files.com's web interface. ")

        if not api_key.isalnum():
            raise AuthenticationError("Your API key is invalid (it contains whitespace)")

    def general_api_error(self, response, extra_info=None):
        msg = "Unexpected response object from API: {body} (HTTP response code was {status})".format(body=repr(response.content), status=response.http_status)
        if extra_info:
            msg += " Additional Information: {}".format(extra_info)
        return APIError(msg)

    def handle_error_response(self, response, context):
        error_data = None
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

        error = self.specific_api_error(response, error_data, context)

        error.response = response
        raise(error)

    def specific_api_error(self, response, error_data, _context):
        #Util.log_error("API error", status: resp.http_status, error_message: error_data[:message])
        opts = {
            "http_body" : response.content,
            "headers" : response.headers,
            "http_status" : response.status_code,
            "json_body" : response.data,
            "code" : error_data.get("code", response.http_status),
        }

        if response.http_status in [400, 404]:
            return InvalidRequestError(error_data["message"], **opts)
        elif response.http_status in [401]:
            return AuthenticationError(error_data["message"], **opts)
        elif response.http_status in [403]:
            return PermissionsError(error_data["message"], **opts)
        elif response.http_status in [429]:
            return RateLimitError(error_data["message"], **opts)
        else: 
            return APIError(error_data["message"], **opts)

    def handle_network_error(self, error, request, context, num_retries):
        #Util.log_error("Network error", error_message: error.message, request_id: context.request_id)
        msg = "Could not connect to Files.com at URL {}. Please check your internet connection and try again. If this problem persists, you should check Files.com's service status at https://status.files.com, or contact your primary account representative.".format(files_com.base_url)
        if num_retries > 0:
            msg += " Request was retried {} times.".format(num_retries)
        msg += "\n\n(Network error: {})".format(error)

        return APIConnectionError(msg)