import builtins  # noqa: F401
from files_sdk.models.zip_download_files import ZipDownloadFiles
from files_sdk.api import Api  # noqa: F401
from files_sdk.error import (  # noqa: F401
    InvalidParameterError,
    MissingParameterError,
    NotImplementedError,
)


class ZipDownloadFile:
    default_attributes = {
        "site_id": None,  # int64 - Site Id
        "user_id": None,  # int64 - User Id
        "bundle_id": None,  # int64 - Bundle Id
        "bundle_registration_id": None,  # int64 - Bundle Registration Id
        "files": None,  # array(object) - A list of file names, sizes, and signed download URLs.
        "cursor": None,  # string - Cursor for fetching more files in subsequent requests.
        "code": None,  # string - Secure code that was generated when creating the zip download.
        "limit": None,  # int64 - Limit the number of files returned.
    }

    def __init__(self, attributes=None, options=None):
        if not isinstance(attributes, dict):
            attributes = {}
        if not isinstance(options, dict):
            options = {}
        self.set_attributes(attributes)
        self.options = options

    def set_attributes(self, attributes):
        for (
            attribute,
            default_value,
        ) in ZipDownloadFile.default_attributes.items():
            value = attributes.get(attribute, default_value)
            setattr(self, attribute, value)

    def get_attributes(self):
        attrs = {
            k: getattr(self, k, None)
            for k in ZipDownloadFile.default_attributes
            if getattr(self, k, None) is not None
        }
        return attrs

    def save(self):
        if hasattr(self, "id") and self.id:
            raise NotImplementedError(
                "The ZipDownloadFile object doesn't support updates."
            )
        else:
            new_obj = create(self.get_attributes(), self.options)
            self.set_attributes(new_obj.get_attributes())
            return True


# Parameters:
#   code (required) - string - Secure code that was generated when creating the zip download.
#   limit - int64 - Limit the number of files returned.
#   cursor - string - Cursor used for paging through files.
#   site_id - int64 - Only check the given site for the zip download.
def create(params=None, options=None):
    if not isinstance(params, dict):
        params = {}
    if not isinstance(options, dict):
        options = {}
    if "code" in params and not isinstance(params["code"], str):
        raise InvalidParameterError("Bad parameter: code must be an str")
    if "limit" in params and not isinstance(params["limit"], int):
        raise InvalidParameterError("Bad parameter: limit must be an int")
    if "cursor" in params and not isinstance(params["cursor"], str):
        raise InvalidParameterError("Bad parameter: cursor must be an str")
    if "site_id" in params and not isinstance(params["site_id"], int):
        raise InvalidParameterError("Bad parameter: site_id must be an int")
    if "code" not in params:
        raise MissingParameterError("Parameter missing: code")
    response, options = Api.send_request(
        "POST", "/zip_download_files", params, options
    )
    return ZipDownloadFiles(response.data, options)


def new(*args, **kwargs):
    return ZipDownloadFile(*args, **kwargs)
