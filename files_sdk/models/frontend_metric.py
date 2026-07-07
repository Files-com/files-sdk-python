import builtins  # noqa: F401
from files_sdk.api import Api  # noqa: F401
from files_sdk.error import (  # noqa: F401
    InvalidParameterError,
    MissingParameterError,
    NotImplementedError,
)


class FrontendMetric:
    default_attributes = {
        "metric_type": None,  # string - Statsd metric type
        "subkey": None,  # string - Where in statsd to store the metric. The final key in statsd will be `files-react.[environment].[subkey]`
        "ms": None,  # int64 - For timing metrics, the number of milliseconds. Required if `metric_type` is `timing`.
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
        ) in FrontendMetric.default_attributes.items():
            value = attributes.get(attribute, default_value)
            setattr(self, attribute, value)

    def get_attributes(self):
        attrs = {
            k: getattr(self, k, None)
            for k in FrontendMetric.default_attributes
            if getattr(self, k, None) is not None
        }
        return attrs

    def save(self):
        if hasattr(self, "id") and self.id:
            raise NotImplementedError(
                "The FrontendMetric object doesn't support updates."
            )
        else:
            new_obj = create(self.get_attributes(), self.options)
            self.set_attributes(new_obj.get_attributes())
            return True


# Parameters:
#   metric_type (required) - string - Statsd metric type.  Use `timing` to submit the amount of time something took, or `increment` to increment a counter
#   subkey (required) - string - Where in statsd to store the metric. The final key in statsd will be `files-react.[environment].[subkey]`
#   ms - int64 - For timing metrics, the number of milliseconds. Required if `metric_type` is `timing`.
def create(params=None, options=None):
    if not isinstance(params, dict):
        params = {}
    if not isinstance(options, dict):
        options = {}
    if "metric_type" in params and not isinstance(params["metric_type"], str):
        raise InvalidParameterError(
            "Bad parameter: metric_type must be an str"
        )
    if "subkey" in params and not isinstance(params["subkey"], str):
        raise InvalidParameterError("Bad parameter: subkey must be an str")
    if "ms" in params and not isinstance(params["ms"], int):
        raise InvalidParameterError("Bad parameter: ms must be an int")
    if "metric_type" not in params:
        raise MissingParameterError("Parameter missing: metric_type")
    if "subkey" not in params:
        raise MissingParameterError("Parameter missing: subkey")
    response, options = Api.send_request(
        "POST", "/frontend_metrics", params, options
    )
    return FrontendMetric(response.data, options)


def new(*args, **kwargs):
    return FrontendMetric(*args, **kwargs)
