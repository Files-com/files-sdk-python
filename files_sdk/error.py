from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from files_sdk.api_client import ApiResponse
    from files_sdk.download_status import DownloadRequestStatus


class Error(Exception):
    # File storage's status of the download request this error came from,
    # when a download read one that explains it (see
    # files_sdk.download_status); otherwise None.
    download_request_status: "DownloadRequestStatus | None" = None

    def __init__(
        self,
        message=None,
        http_body=None,
        http_status=None,
        json_body=None,
        headers=None,
        code=None,
    ):
        super().__init__(message)

        if http_body and hasattr(http_body, "decode"):
            try:
                http_body = http_body.decode("utf-8")
            except BaseException:
                http_body = "<Could not decode body as utf-8. "

        self._message = message
        self.http_body: Any = http_body
        self.http_status: Any = http_status
        self.json_body: Any = json_body
        self.headers: Any = headers or {}
        self.code: Any = code
        # The API response that reported this error, when there was one.
        self.response: ApiResponse | None = None

    def __str__(self):
        msg = ""
        if self.http_status:
            msg += "HTTP {} ".format(self.http_status)
        if self._message:
            msg += self._message
        return msg


class APIConnectionError(Error):
    """No usable response arrived: the connection failed, timed out or
    broke, or the response could not be used.

    phase names the step that failed, such as "response" while waiting for
    or reading a response. remote_outcome_unknown is True when the request
    may have reached the server first, so what it asked for may have
    happened.
    """

    def __init__(
        self,
        message=None,
        http_body=None,
        http_status=None,
        json_body=None,
        headers=None,
        code=None,
        *,
        phase=None,
        remote_outcome_unknown=False,
    ):
        super().__init__(
            message, http_body, http_status, json_body, headers, code
        )
        self.phase: str | None = phase
        self.remote_outcome_unknown: bool = remote_outcome_unknown


class DeadlineExceededError(APIConnectionError):
    """The operation ran out of the time its request_timeout or deadline
    option allowed."""


class OperationCancelledError(Error):
    """The operation stopped because its cancel_token was cancelled.

    phase and remote_outcome_unknown mean what they do on
    APIConnectionError.
    """

    def __init__(
        self, message=None, *, phase=None, remote_outcome_unknown=False
    ):
        super().__init__(message)
        self.phase: str | None = phase
        self.remote_outcome_unknown: bool = remote_outcome_unknown


class ClientClosedError(OperationCancelledError):
    """The client the operation uses was closed, before or while it ran."""


class FileMigrationError(Error):
    """A copy, move or other file migration that was waited for failed or
    was cancelled. migration is the FileMigration, with its status and
    failure_message, or None when Files.com reported the failure at once."""

    def __init__(self, message=None, *, migration: Any = None):
        super().__init__(message)
        self.migration: Any = migration


class TransferPausedError(Error):
    """A transfer stopped because its pause_token was paused.

    checkpoint is the path of the checkpoint it saved; calling the same
    transfer again with it resumes where it stopped. result, for a job of
    many files, is the TransferResult so far.
    """

    def __init__(
        self,
        message=None,
        *,
        checkpoint: str | None = None,
        result: Any = None,
    ):
        super().__init__(message)
        self.checkpoint: str | None = checkpoint
        self.result: Any = result


class APIError(Error):
    """Files.com, or storage, answered with an error.

    remote_outcome_unknown is True when the request may have changed
    something and the answer does not show that it did not. Files.com can
    answer such a request, a create for example, with an error after
    carrying out all or part of it, whatever the error's status or type, so
    the SDK does not send it again: check whether it took effect before
    repeating it. It is False for a request that only asks for something,
    and for Files.com's answer while its site is disabled, which comes
    before anything is carried out.
    """

    def __init__(
        self,
        message=None,
        http_body=None,
        http_status=None,
        json_body=None,
        headers=None,
        code=None,
    ):
        super().__init__(
            message, http_body, http_status, json_body, headers, code
        )

        # Errors raised without a structured body, such as transfer failures,
        # still carry every field, set to None.
        body = json_body if isinstance(json_body, dict) else {}
        self.detail = body.get("detail")
        self.error = body.get("error")
        self.errors = body.get("errors")
        self.http_code = body.get("http-code")
        self.instance = body.get("instance")
        self.model_errors = body.get("model-errors")
        self.title = body.get("title")
        self.error_type = body.get("type")
        self.data = body.get("data")
        self.remote_outcome_unknown: bool = False


class AuthenticationError(Error):
    pass


class InvalidRequestError(Error):
    pass


class NotImplementedError(Error):
    pass


class PermissionsError(Error):
    pass


class RateLimitError(Error):
    pass


class ValidationError(Error):
    pass


class InvalidParameterError(InvalidRequestError):
    pass


class MissingParameterError(InvalidRequestError):
    pass


class BadRequestError(APIError):
    def __init__(
        self,
        message=None,
        http_body=None,
        http_status=None,
        json_body=None,
        headers=None,
        code=None,
    ):
        super().__init__(
            message, http_body, http_status, json_body, headers, code
        )


class AgentUpgradeRequiredError(BadRequestError):
    def __init__(
        self,
        message=None,
        http_body=None,
        http_status=None,
        json_body=None,
        headers=None,
        code=None,
    ):
        super().__init__(
            message, http_body, http_status, json_body, headers, code
        )


class AttachmentTooLargeError(BadRequestError):
    def __init__(
        self,
        message=None,
        http_body=None,
        http_status=None,
        json_body=None,
        headers=None,
        code=None,
    ):
        super().__init__(
            message, http_body, http_status, json_body, headers, code
        )


class CannotDownloadDirectoryError(BadRequestError):
    def __init__(
        self,
        message=None,
        http_body=None,
        http_status=None,
        json_body=None,
        headers=None,
        code=None,
    ):
        super().__init__(
            message, http_body, http_status, json_body, headers, code
        )


class CantMoveWithMultipleLocationsError(BadRequestError):
    def __init__(
        self,
        message=None,
        http_body=None,
        http_status=None,
        json_body=None,
        headers=None,
        code=None,
    ):
        super().__init__(
            message, http_body, http_status, json_body, headers, code
        )


class DatetimeParseError(BadRequestError):
    def __init__(
        self,
        message=None,
        http_body=None,
        http_status=None,
        json_body=None,
        headers=None,
        code=None,
    ):
        super().__init__(
            message, http_body, http_status, json_body, headers, code
        )


class DestinationSameError(BadRequestError):
    def __init__(
        self,
        message=None,
        http_body=None,
        http_status=None,
        json_body=None,
        headers=None,
        code=None,
    ):
        super().__init__(
            message, http_body, http_status, json_body, headers, code
        )


class DestinationSiteMismatchError(BadRequestError):
    def __init__(
        self,
        message=None,
        http_body=None,
        http_status=None,
        json_body=None,
        headers=None,
        code=None,
    ):
        super().__init__(
            message, http_body, http_status, json_body, headers, code
        )


class DoesNotSupportSortingError(BadRequestError):
    def __init__(
        self,
        message=None,
        http_body=None,
        http_status=None,
        json_body=None,
        headers=None,
        code=None,
    ):
        super().__init__(
            message, http_body, http_status, json_body, headers, code
        )


class FolderMustNotBeAFileError(BadRequestError):
    def __init__(
        self,
        message=None,
        http_body=None,
        http_status=None,
        json_body=None,
        headers=None,
        code=None,
    ):
        super().__init__(
            message, http_body, http_status, json_body, headers, code
        )


class FoldersNotAllowedError(BadRequestError):
    def __init__(
        self,
        message=None,
        http_body=None,
        http_status=None,
        json_body=None,
        headers=None,
        code=None,
    ):
        super().__init__(
            message, http_body, http_status, json_body, headers, code
        )


class InternalGeneralErrorError(BadRequestError):
    def __init__(
        self,
        message=None,
        http_body=None,
        http_status=None,
        json_body=None,
        headers=None,
        code=None,
    ):
        super().__init__(
            message, http_body, http_status, json_body, headers, code
        )


class InvalidBodyError(BadRequestError):
    def __init__(
        self,
        message=None,
        http_body=None,
        http_status=None,
        json_body=None,
        headers=None,
        code=None,
    ):
        super().__init__(
            message, http_body, http_status, json_body, headers, code
        )


class InvalidCursorError(BadRequestError):
    def __init__(
        self,
        message=None,
        http_body=None,
        http_status=None,
        json_body=None,
        headers=None,
        code=None,
    ):
        super().__init__(
            message, http_body, http_status, json_body, headers, code
        )


class InvalidCursorTypeForSortError(BadRequestError):
    def __init__(
        self,
        message=None,
        http_body=None,
        http_status=None,
        json_body=None,
        headers=None,
        code=None,
    ):
        super().__init__(
            message, http_body, http_status, json_body, headers, code
        )


class InvalidEtagsError(BadRequestError):
    def __init__(
        self,
        message=None,
        http_body=None,
        http_status=None,
        json_body=None,
        headers=None,
        code=None,
    ):
        super().__init__(
            message, http_body, http_status, json_body, headers, code
        )


class InvalidFilterAliasCombinationError(BadRequestError):
    def __init__(
        self,
        message=None,
        http_body=None,
        http_status=None,
        json_body=None,
        headers=None,
        code=None,
    ):
        super().__init__(
            message, http_body, http_status, json_body, headers, code
        )


class InvalidFilterFieldError(BadRequestError):
    def __init__(
        self,
        message=None,
        http_body=None,
        http_status=None,
        json_body=None,
        headers=None,
        code=None,
    ):
        super().__init__(
            message, http_body, http_status, json_body, headers, code
        )


class InvalidFilterParamError(BadRequestError):
    def __init__(
        self,
        message=None,
        http_body=None,
        http_status=None,
        json_body=None,
        headers=None,
        code=None,
    ):
        super().__init__(
            message, http_body, http_status, json_body, headers, code
        )


class InvalidFilterParamFormatError(BadRequestError):
    def __init__(
        self,
        message=None,
        http_body=None,
        http_status=None,
        json_body=None,
        headers=None,
        code=None,
    ):
        super().__init__(
            message, http_body, http_status, json_body, headers, code
        )


class InvalidFilterParamValueError(BadRequestError):
    def __init__(
        self,
        message=None,
        http_body=None,
        http_status=None,
        json_body=None,
        headers=None,
        code=None,
    ):
        super().__init__(
            message, http_body, http_status, json_body, headers, code
        )


class InvalidInputEncodingError(BadRequestError):
    def __init__(
        self,
        message=None,
        http_body=None,
        http_status=None,
        json_body=None,
        headers=None,
        code=None,
    ):
        super().__init__(
            message, http_body, http_status, json_body, headers, code
        )


class InvalidInterfaceError(BadRequestError):
    def __init__(
        self,
        message=None,
        http_body=None,
        http_status=None,
        json_body=None,
        headers=None,
        code=None,
    ):
        super().__init__(
            message, http_body, http_status, json_body, headers, code
        )


class InvalidOauthProviderError(BadRequestError):
    def __init__(
        self,
        message=None,
        http_body=None,
        http_status=None,
        json_body=None,
        headers=None,
        code=None,
    ):
        super().__init__(
            message, http_body, http_status, json_body, headers, code
        )


class InvalidPathError(BadRequestError):
    def __init__(
        self,
        message=None,
        http_body=None,
        http_status=None,
        json_body=None,
        headers=None,
        code=None,
    ):
        super().__init__(
            message, http_body, http_status, json_body, headers, code
        )


class InvalidReturnToUrlError(BadRequestError):
    def __init__(
        self,
        message=None,
        http_body=None,
        http_status=None,
        json_body=None,
        headers=None,
        code=None,
    ):
        super().__init__(
            message, http_body, http_status, json_body, headers, code
        )


class InvalidSearchQueryError(BadRequestError):
    def __init__(
        self,
        message=None,
        http_body=None,
        http_status=None,
        json_body=None,
        headers=None,
        code=None,
    ):
        super().__init__(
            message, http_body, http_status, json_body, headers, code
        )


class InvalidSortFieldError(BadRequestError):
    def __init__(
        self,
        message=None,
        http_body=None,
        http_status=None,
        json_body=None,
        headers=None,
        code=None,
    ):
        super().__init__(
            message, http_body, http_status, json_body, headers, code
        )


class InvalidSortFilterCombinationError(BadRequestError):
    def __init__(
        self,
        message=None,
        http_body=None,
        http_status=None,
        json_body=None,
        headers=None,
        code=None,
    ):
        super().__init__(
            message, http_body, http_status, json_body, headers, code
        )


class InvalidUploadOffsetError(BadRequestError):
    def __init__(
        self,
        message=None,
        http_body=None,
        http_status=None,
        json_body=None,
        headers=None,
        code=None,
    ):
        super().__init__(
            message, http_body, http_status, json_body, headers, code
        )


class InvalidUploadPartGapError(BadRequestError):
    def __init__(
        self,
        message=None,
        http_body=None,
        http_status=None,
        json_body=None,
        headers=None,
        code=None,
    ):
        super().__init__(
            message, http_body, http_status, json_body, headers, code
        )


class InvalidUploadPartSizeError(BadRequestError):
    def __init__(
        self,
        message=None,
        http_body=None,
        http_status=None,
        json_body=None,
        headers=None,
        code=None,
    ):
        super().__init__(
            message, http_body, http_status, json_body, headers, code
        )


class InvalidWorkspaceIdHeaderError(BadRequestError):
    def __init__(
        self,
        message=None,
        http_body=None,
        http_status=None,
        json_body=None,
        headers=None,
        code=None,
    ):
        super().__init__(
            message, http_body, http_status, json_body, headers, code
        )


class MethodNotAllowedError(BadRequestError):
    def __init__(
        self,
        message=None,
        http_body=None,
        http_status=None,
        json_body=None,
        headers=None,
        code=None,
    ):
        super().__init__(
            message, http_body, http_status, json_body, headers, code
        )


class MultipleSortParamsNotAllowedError(BadRequestError):
    def __init__(
        self,
        message=None,
        http_body=None,
        http_status=None,
        json_body=None,
        headers=None,
        code=None,
    ):
        super().__init__(
            message, http_body, http_status, json_body, headers, code
        )


class NoValidInputParamsError(BadRequestError):
    def __init__(
        self,
        message=None,
        http_body=None,
        http_status=None,
        json_body=None,
        headers=None,
        code=None,
    ):
        super().__init__(
            message, http_body, http_status, json_body, headers, code
        )


class OffsetUploadNotAllowedWithMalwareScanningError(BadRequestError):
    def __init__(
        self,
        message=None,
        http_body=None,
        http_status=None,
        json_body=None,
        headers=None,
        code=None,
    ):
        super().__init__(
            message, http_body, http_status, json_body, headers, code
        )


class PartNumberTooLargeError(BadRequestError):
    def __init__(
        self,
        message=None,
        http_body=None,
        http_status=None,
        json_body=None,
        headers=None,
        code=None,
    ):
        super().__init__(
            message, http_body, http_status, json_body, headers, code
        )


class PathCannotHaveTrailingWhitespaceError(BadRequestError):
    def __init__(
        self,
        message=None,
        http_body=None,
        http_status=None,
        json_body=None,
        headers=None,
        code=None,
    ):
        super().__init__(
            message, http_body, http_status, json_body, headers, code
        )


class ReauthenticationNeededFieldsError(BadRequestError):
    def __init__(
        self,
        message=None,
        http_body=None,
        http_status=None,
        json_body=None,
        headers=None,
        code=None,
    ):
        super().__init__(
            message, http_body, http_status, json_body, headers, code
        )


class RequestBodyTooLargeError(BadRequestError):
    def __init__(
        self,
        message=None,
        http_body=None,
        http_status=None,
        json_body=None,
        headers=None,
        code=None,
    ):
        super().__init__(
            message, http_body, http_status, json_body, headers, code
        )


class RequestParamsContainInvalidCharacterError(BadRequestError):
    def __init__(
        self,
        message=None,
        http_body=None,
        http_status=None,
        json_body=None,
        headers=None,
        code=None,
    ):
        super().__init__(
            message, http_body, http_status, json_body, headers, code
        )


class RequestParamsInvalidError(BadRequestError):
    def __init__(
        self,
        message=None,
        http_body=None,
        http_status=None,
        json_body=None,
        headers=None,
        code=None,
    ):
        super().__init__(
            message, http_body, http_status, json_body, headers, code
        )


class RequestParamsRequiredError(BadRequestError):
    def __init__(
        self,
        message=None,
        http_body=None,
        http_status=None,
        json_body=None,
        headers=None,
        code=None,
    ):
        super().__init__(
            message, http_body, http_status, json_body, headers, code
        )


class SearchAllOnChildPathError(BadRequestError):
    def __init__(
        self,
        message=None,
        http_body=None,
        http_status=None,
        json_body=None,
        headers=None,
        code=None,
    ):
        super().__init__(
            message, http_body, http_status, json_body, headers, code
        )


class UnrecognizedSortIndexError(BadRequestError):
    def __init__(
        self,
        message=None,
        http_body=None,
        http_status=None,
        json_body=None,
        headers=None,
        code=None,
    ):
        super().__init__(
            message, http_body, http_status, json_body, headers, code
        )


class UnsupportedCurrencyError(BadRequestError):
    def __init__(
        self,
        message=None,
        http_body=None,
        http_status=None,
        json_body=None,
        headers=None,
        code=None,
    ):
        super().__init__(
            message, http_body, http_status, json_body, headers, code
        )


class UnsupportedHttpResponseFormatError(BadRequestError):
    def __init__(
        self,
        message=None,
        http_body=None,
        http_status=None,
        json_body=None,
        headers=None,
        code=None,
    ):
        super().__init__(
            message, http_body, http_status, json_body, headers, code
        )


class UnsupportedMediaTypeError(BadRequestError):
    def __init__(
        self,
        message=None,
        http_body=None,
        http_status=None,
        json_body=None,
        headers=None,
        code=None,
    ):
        super().__init__(
            message, http_body, http_status, json_body, headers, code
        )


class UserIdInvalidError(BadRequestError):
    def __init__(
        self,
        message=None,
        http_body=None,
        http_status=None,
        json_body=None,
        headers=None,
        code=None,
    ):
        super().__init__(
            message, http_body, http_status, json_body, headers, code
        )


class UserIdOnUserEndpointError(BadRequestError):
    def __init__(
        self,
        message=None,
        http_body=None,
        http_status=None,
        json_body=None,
        headers=None,
        code=None,
    ):
        super().__init__(
            message, http_body, http_status, json_body, headers, code
        )


class UserRequiredError(BadRequestError):
    def __init__(
        self,
        message=None,
        http_body=None,
        http_status=None,
        json_body=None,
        headers=None,
        code=None,
    ):
        super().__init__(
            message, http_body, http_status, json_body, headers, code
        )


class NotAuthenticatedError(APIError):
    def __init__(
        self,
        message=None,
        http_body=None,
        http_status=None,
        json_body=None,
        headers=None,
        code=None,
    ):
        super().__init__(
            message, http_body, http_status, json_body, headers, code
        )


class AdditionalAuthenticationRequiredError(NotAuthenticatedError):
    def __init__(
        self,
        message=None,
        http_body=None,
        http_status=None,
        json_body=None,
        headers=None,
        code=None,
    ):
        super().__init__(
            message, http_body, http_status, json_body, headers, code
        )


class ApiKeySessionsNotSupportedError(NotAuthenticatedError):
    def __init__(
        self,
        message=None,
        http_body=None,
        http_status=None,
        json_body=None,
        headers=None,
        code=None,
    ):
        super().__init__(
            message, http_body, http_status, json_body, headers, code
        )


class AuthenticationRequiredError(NotAuthenticatedError):
    def __init__(
        self,
        message=None,
        http_body=None,
        http_status=None,
        json_body=None,
        headers=None,
        code=None,
    ):
        super().__init__(
            message, http_body, http_status, json_body, headers, code
        )


class BundleRegistrationCodeFailedError(NotAuthenticatedError):
    def __init__(
        self,
        message=None,
        http_body=None,
        http_status=None,
        json_body=None,
        headers=None,
        code=None,
    ):
        super().__init__(
            message, http_body, http_status, json_body, headers, code
        )


class InboxRegistrationCodeFailedError(NotAuthenticatedError):
    def __init__(
        self,
        message=None,
        http_body=None,
        http_status=None,
        json_body=None,
        headers=None,
        code=None,
    ):
        super().__init__(
            message, http_body, http_status, json_body, headers, code
        )


class InvalidCredentialsError(NotAuthenticatedError):
    def __init__(
        self,
        message=None,
        http_body=None,
        http_status=None,
        json_body=None,
        headers=None,
        code=None,
    ):
        super().__init__(
            message, http_body, http_status, json_body, headers, code
        )


class InvalidOauthError(NotAuthenticatedError):
    def __init__(
        self,
        message=None,
        http_body=None,
        http_status=None,
        json_body=None,
        headers=None,
        code=None,
    ):
        super().__init__(
            message, http_body, http_status, json_body, headers, code
        )


class InvalidOrExpiredCodeError(NotAuthenticatedError):
    def __init__(
        self,
        message=None,
        http_body=None,
        http_status=None,
        json_body=None,
        headers=None,
        code=None,
    ):
        super().__init__(
            message, http_body, http_status, json_body, headers, code
        )


class InvalidSessionError(NotAuthenticatedError):
    def __init__(
        self,
        message=None,
        http_body=None,
        http_status=None,
        json_body=None,
        headers=None,
        code=None,
    ):
        super().__init__(
            message, http_body, http_status, json_body, headers, code
        )


class InvalidUsernameOrPasswordError(NotAuthenticatedError):
    def __init__(
        self,
        message=None,
        http_body=None,
        http_status=None,
        json_body=None,
        headers=None,
        code=None,
    ):
        super().__init__(
            message, http_body, http_status, json_body, headers, code
        )


class LockedOutError(NotAuthenticatedError):
    def __init__(
        self,
        message=None,
        http_body=None,
        http_status=None,
        json_body=None,
        headers=None,
        code=None,
    ):
        super().__init__(
            message, http_body, http_status, json_body, headers, code
        )


class LockoutRegionMismatchError(NotAuthenticatedError):
    def __init__(
        self,
        message=None,
        http_body=None,
        http_status=None,
        json_body=None,
        headers=None,
        code=None,
    ):
        super().__init__(
            message, http_body, http_status, json_body, headers, code
        )


class OneTimePasswordIncorrectError(NotAuthenticatedError):
    def __init__(
        self,
        message=None,
        http_body=None,
        http_status=None,
        json_body=None,
        headers=None,
        code=None,
    ):
        super().__init__(
            message, http_body, http_status, json_body, headers, code
        )


class TwoFactorAuthenticationErrorError(NotAuthenticatedError):
    def __init__(
        self,
        message=None,
        http_body=None,
        http_status=None,
        json_body=None,
        headers=None,
        code=None,
    ):
        super().__init__(
            message, http_body, http_status, json_body, headers, code
        )


class TwoFactorAuthenticationSetupExpiredError(NotAuthenticatedError):
    def __init__(
        self,
        message=None,
        http_body=None,
        http_status=None,
        json_body=None,
        headers=None,
        code=None,
    ):
        super().__init__(
            message, http_body, http_status, json_body, headers, code
        )


class NotAuthorizedError(APIError):
    def __init__(
        self,
        message=None,
        http_body=None,
        http_status=None,
        json_body=None,
        headers=None,
        code=None,
    ):
        super().__init__(
            message, http_body, http_status, json_body, headers, code
        )


class ApiKeyIsDisabledError(NotAuthorizedError):
    def __init__(
        self,
        message=None,
        http_body=None,
        http_status=None,
        json_body=None,
        headers=None,
        code=None,
    ):
        super().__init__(
            message, http_body, http_status, json_body, headers, code
        )


class ApiKeyIsPathRestrictedError(NotAuthorizedError):
    def __init__(
        self,
        message=None,
        http_body=None,
        http_status=None,
        json_body=None,
        headers=None,
        code=None,
    ):
        super().__init__(
            message, http_body, http_status, json_body, headers, code
        )


class ApiKeyOnlyForDesktopAppError(NotAuthorizedError):
    def __init__(
        self,
        message=None,
        http_body=None,
        http_status=None,
        json_body=None,
        headers=None,
        code=None,
    ):
        super().__init__(
            message, http_body, http_status, json_body, headers, code
        )


class ApiKeyOnlyForFileOperationsError(NotAuthorizedError):
    def __init__(
        self,
        message=None,
        http_body=None,
        http_status=None,
        json_body=None,
        headers=None,
        code=None,
    ):
        super().__init__(
            message, http_body, http_status, json_body, headers, code
        )


class ApiKeyOnlyForMobileAppError(NotAuthorizedError):
    def __init__(
        self,
        message=None,
        http_body=None,
        http_status=None,
        json_body=None,
        headers=None,
        code=None,
    ):
        super().__init__(
            message, http_body, http_status, json_body, headers, code
        )


class ApiKeyOnlyForOfficeIntegrationError(NotAuthorizedError):
    def __init__(
        self,
        message=None,
        http_body=None,
        http_status=None,
        json_body=None,
        headers=None,
        code=None,
    ):
        super().__init__(
            message, http_body, http_status, json_body, headers, code
        )


class BillingInformationHiddenError(NotAuthorizedError):
    def __init__(
        self,
        message=None,
        http_body=None,
        http_status=None,
        json_body=None,
        headers=None,
        code=None,
    ):
        super().__init__(
            message, http_body, http_status, json_body, headers, code
        )


class BillingPermissionRequiredError(NotAuthorizedError):
    def __init__(
        self,
        message=None,
        http_body=None,
        http_status=None,
        json_body=None,
        headers=None,
        code=None,
    ):
        super().__init__(
            message, http_body, http_status, json_body, headers, code
        )


class BundleMaximumUsesReachedError(NotAuthorizedError):
    def __init__(
        self,
        message=None,
        http_body=None,
        http_status=None,
        json_body=None,
        headers=None,
        code=None,
    ):
        super().__init__(
            message, http_body, http_status, json_body, headers, code
        )


class BundlePermissionRequiredError(NotAuthorizedError):
    def __init__(
        self,
        message=None,
        http_body=None,
        http_status=None,
        json_body=None,
        headers=None,
        code=None,
    ):
        super().__init__(
            message, http_body, http_status, json_body, headers, code
        )


class CannotAdministerHigherLevelUserError(NotAuthorizedError):
    def __init__(
        self,
        message=None,
        http_body=None,
        http_status=None,
        json_body=None,
        headers=None,
        code=None,
    ):
        super().__init__(
            message, http_body, http_status, json_body, headers, code
        )


class CannotLoginWhileUsingKeyError(NotAuthorizedError):
    def __init__(
        self,
        message=None,
        http_body=None,
        http_status=None,
        json_body=None,
        headers=None,
        code=None,
    ):
        super().__init__(
            message, http_body, http_status, json_body, headers, code
        )


class CantActForOtherUserError(NotAuthorizedError):
    def __init__(
        self,
        message=None,
        http_body=None,
        http_status=None,
        json_body=None,
        headers=None,
        code=None,
    ):
        super().__init__(
            message, http_body, http_status, json_body, headers, code
        )


class ContactAdminForPasswordChangeHelpError(NotAuthorizedError):
    def __init__(
        self,
        message=None,
        http_body=None,
        http_status=None,
        json_body=None,
        headers=None,
        code=None,
    ):
        super().__init__(
            message, http_body, http_status, json_body, headers, code
        )


class FilesAgentFailedAuthorizationError(NotAuthorizedError):
    def __init__(
        self,
        message=None,
        http_body=None,
        http_status=None,
        json_body=None,
        headers=None,
        code=None,
    ):
        super().__init__(
            message, http_body, http_status, json_body, headers, code
        )


class FolderAdminOrBillingPermissionRequiredError(NotAuthorizedError):
    def __init__(
        self,
        message=None,
        http_body=None,
        http_status=None,
        json_body=None,
        headers=None,
        code=None,
    ):
        super().__init__(
            message, http_body, http_status, json_body, headers, code
        )


class FolderAdminPermissionRequiredError(NotAuthorizedError):
    def __init__(
        self,
        message=None,
        http_body=None,
        http_status=None,
        json_body=None,
        headers=None,
        code=None,
    ):
        super().__init__(
            message, http_body, http_status, json_body, headers, code
        )


class FullPermissionRequiredError(NotAuthorizedError):
    def __init__(
        self,
        message=None,
        http_body=None,
        http_status=None,
        json_body=None,
        headers=None,
        code=None,
    ):
        super().__init__(
            message, http_body, http_status, json_body, headers, code
        )


class HistoryPermissionRequiredError(NotAuthorizedError):
    def __init__(
        self,
        message=None,
        http_body=None,
        http_status=None,
        json_body=None,
        headers=None,
        code=None,
    ):
        super().__init__(
            message, http_body, http_status, json_body, headers, code
        )


class InAppAiAssistantUnavailableError(NotAuthorizedError):
    def __init__(
        self,
        message=None,
        http_body=None,
        http_status=None,
        json_body=None,
        headers=None,
        code=None,
    ):
        super().__init__(
            message, http_body, http_status, json_body, headers, code
        )


class InsufficientPermissionForParamsError(NotAuthorizedError):
    def __init__(
        self,
        message=None,
        http_body=None,
        http_status=None,
        json_body=None,
        headers=None,
        code=None,
    ):
        super().__init__(
            message, http_body, http_status, json_body, headers, code
        )


class InsufficientPermissionForSiteError(NotAuthorizedError):
    def __init__(
        self,
        message=None,
        http_body=None,
        http_status=None,
        json_body=None,
        headers=None,
        code=None,
    ):
        super().__init__(
            message, http_body, http_status, json_body, headers, code
        )


class MoverAccessDeniedError(NotAuthorizedError):
    def __init__(
        self,
        message=None,
        http_body=None,
        http_status=None,
        json_body=None,
        headers=None,
        code=None,
    ):
        super().__init__(
            message, http_body, http_status, json_body, headers, code
        )


class MoverPackageRequiredError(NotAuthorizedError):
    def __init__(
        self,
        message=None,
        http_body=None,
        http_status=None,
        json_body=None,
        headers=None,
        code=None,
    ):
        super().__init__(
            message, http_body, http_status, json_body, headers, code
        )


class MustAuthenticateWithApiKeyError(NotAuthorizedError):
    def __init__(
        self,
        message=None,
        http_body=None,
        http_status=None,
        json_body=None,
        headers=None,
        code=None,
    ):
        super().__init__(
            message, http_body, http_status, json_body, headers, code
        )


class NeedAdminPermissionForInboxError(NotAuthorizedError):
    def __init__(
        self,
        message=None,
        http_body=None,
        http_status=None,
        json_body=None,
        headers=None,
        code=None,
    ):
        super().__init__(
            message, http_body, http_status, json_body, headers, code
        )


class NonAdminsMustQueryByFolderOrPathError(NotAuthorizedError):
    def __init__(
        self,
        message=None,
        http_body=None,
        http_status=None,
        json_body=None,
        headers=None,
        code=None,
    ):
        super().__init__(
            message, http_body, http_status, json_body, headers, code
        )


class NotAllowedToCreateBundleError(NotAuthorizedError):
    def __init__(
        self,
        message=None,
        http_body=None,
        http_status=None,
        json_body=None,
        headers=None,
        code=None,
    ):
        super().__init__(
            message, http_body, http_status, json_body, headers, code
        )


class NotEnqueuableSyncError(NotAuthorizedError):
    def __init__(
        self,
        message=None,
        http_body=None,
        http_status=None,
        json_body=None,
        headers=None,
        code=None,
    ):
        super().__init__(
            message, http_body, http_status, json_body, headers, code
        )


class PasswordChangeNotRequiredError(NotAuthorizedError):
    def __init__(
        self,
        message=None,
        http_body=None,
        http_status=None,
        json_body=None,
        headers=None,
        code=None,
    ):
        super().__init__(
            message, http_body, http_status, json_body, headers, code
        )


class PasswordChangeRequiredError(NotAuthorizedError):
    def __init__(
        self,
        message=None,
        http_body=None,
        http_status=None,
        json_body=None,
        headers=None,
        code=None,
    ):
        super().__init__(
            message, http_body, http_status, json_body, headers, code
        )


class PaymentMethodErrorError(NotAuthorizedError):
    def __init__(
        self,
        message=None,
        http_body=None,
        http_status=None,
        json_body=None,
        headers=None,
        code=None,
    ):
        super().__init__(
            message, http_body, http_status, json_body, headers, code
        )


class PreviewOnlyPermissionCannotDownloadError(NotAuthorizedError):
    def __init__(
        self,
        message=None,
        http_body=None,
        http_status=None,
        json_body=None,
        headers=None,
        code=None,
    ):
        super().__init__(
            message, http_body, http_status, json_body, headers, code
        )


class ReadOnlySessionError(NotAuthorizedError):
    def __init__(
        self,
        message=None,
        http_body=None,
        http_status=None,
        json_body=None,
        headers=None,
        code=None,
    ):
        super().__init__(
            message, http_body, http_status, json_body, headers, code
        )


class ReadPermissionRequiredError(NotAuthorizedError):
    def __init__(
        self,
        message=None,
        http_body=None,
        http_status=None,
        json_body=None,
        headers=None,
        code=None,
    ):
        super().__init__(
            message, http_body, http_status, json_body, headers, code
        )


class ReauthenticationFailedError(NotAuthorizedError):
    def __init__(
        self,
        message=None,
        http_body=None,
        http_status=None,
        json_body=None,
        headers=None,
        code=None,
    ):
        super().__init__(
            message, http_body, http_status, json_body, headers, code
        )


class ReauthenticationFailedFinalError(NotAuthorizedError):
    def __init__(
        self,
        message=None,
        http_body=None,
        http_status=None,
        json_body=None,
        headers=None,
        code=None,
    ):
        super().__init__(
            message, http_body, http_status, json_body, headers, code
        )


class ReauthenticationNeededActionError(NotAuthorizedError):
    def __init__(
        self,
        message=None,
        http_body=None,
        http_status=None,
        json_body=None,
        headers=None,
        code=None,
    ):
        super().__init__(
            message, http_body, http_status, json_body, headers, code
        )


class RecaptchaFailedError(NotAuthorizedError):
    def __init__(
        self,
        message=None,
        http_body=None,
        http_status=None,
        json_body=None,
        headers=None,
        code=None,
    ):
        super().__init__(
            message, http_body, http_status, json_body, headers, code
        )


class RemoteDesktopDebugLoggingDisabledError(NotAuthorizedError):
    def __init__(
        self,
        message=None,
        http_body=None,
        http_status=None,
        json_body=None,
        headers=None,
        code=None,
    ):
        super().__init__(
            message, http_body, http_status, json_body, headers, code
        )


class RootFolderBehaviorSiteAdminRequiredError(NotAuthorizedError):
    def __init__(
        self,
        message=None,
        http_body=None,
        http_status=None,
        json_body=None,
        headers=None,
        code=None,
    ):
        super().__init__(
            message, http_body, http_status, json_body, headers, code
        )


class RootFolderBehaviorSkipSiteAdminRequiredError(NotAuthorizedError):
    def __init__(
        self,
        message=None,
        http_body=None,
        http_status=None,
        json_body=None,
        headers=None,
        code=None,
    ):
        super().__init__(
            message, http_body, http_status, json_body, headers, code
        )


class SelfManagedRequiredError(NotAuthorizedError):
    def __init__(
        self,
        message=None,
        http_body=None,
        http_status=None,
        json_body=None,
        headers=None,
        code=None,
    ):
        super().__init__(
            message, http_body, http_status, json_body, headers, code
        )


class SiteAdminOrPartnerAdminPermissionRequiredError(NotAuthorizedError):
    def __init__(
        self,
        message=None,
        http_body=None,
        http_status=None,
        json_body=None,
        headers=None,
        code=None,
    ):
        super().__init__(
            message, http_body, http_status, json_body, headers, code
        )


class SiteAdminOrWorkspaceAdminOrFolderAdminPermissionRequiredError(
    NotAuthorizedError
):
    def __init__(
        self,
        message=None,
        http_body=None,
        http_status=None,
        json_body=None,
        headers=None,
        code=None,
    ):
        super().__init__(
            message, http_body, http_status, json_body, headers, code
        )


class SiteAdminOrWorkspaceAdminOrPartnerAdminOrFolderAdminPermissionRequiredError(
    NotAuthorizedError
):
    def __init__(
        self,
        message=None,
        http_body=None,
        http_status=None,
        json_body=None,
        headers=None,
        code=None,
    ):
        super().__init__(
            message, http_body, http_status, json_body, headers, code
        )


class SiteAdminOrWorkspaceAdminOrPartnerAdminPermissionRequiredError(
    NotAuthorizedError
):
    def __init__(
        self,
        message=None,
        http_body=None,
        http_status=None,
        json_body=None,
        headers=None,
        code=None,
    ):
        super().__init__(
            message, http_body, http_status, json_body, headers, code
        )


class SiteAdminOrWorkspaceAdminPermissionRequiredError(NotAuthorizedError):
    def __init__(
        self,
        message=None,
        http_body=None,
        http_status=None,
        json_body=None,
        headers=None,
        code=None,
    ):
        super().__init__(
            message, http_body, http_status, json_body, headers, code
        )


class SiteAdminRequiredError(NotAuthorizedError):
    def __init__(
        self,
        message=None,
        http_body=None,
        http_status=None,
        json_body=None,
        headers=None,
        code=None,
    ):
        super().__init__(
            message, http_body, http_status, json_body, headers, code
        )


class SiteFilesAreImmutableError(NotAuthorizedError):
    def __init__(
        self,
        message=None,
        http_body=None,
        http_status=None,
        json_body=None,
        headers=None,
        code=None,
    ):
        super().__init__(
            message, http_body, http_status, json_body, headers, code
        )


class TwoFactorAuthenticationRequiredError(NotAuthorizedError):
    def __init__(
        self,
        message=None,
        http_body=None,
        http_status=None,
        json_body=None,
        headers=None,
        code=None,
    ):
        super().__init__(
            message, http_body, http_status, json_body, headers, code
        )


class UserIdWithoutSiteAdminError(NotAuthorizedError):
    def __init__(
        self,
        message=None,
        http_body=None,
        http_status=None,
        json_body=None,
        headers=None,
        code=None,
    ):
        super().__init__(
            message, http_body, http_status, json_body, headers, code
        )


class WriteAndBundlePermissionRequiredError(NotAuthorizedError):
    def __init__(
        self,
        message=None,
        http_body=None,
        http_status=None,
        json_body=None,
        headers=None,
        code=None,
    ):
        super().__init__(
            message, http_body, http_status, json_body, headers, code
        )


class WritePermissionRequiredError(NotAuthorizedError):
    def __init__(
        self,
        message=None,
        http_body=None,
        http_status=None,
        json_body=None,
        headers=None,
        code=None,
    ):
        super().__init__(
            message, http_body, http_status, json_body, headers, code
        )


class NotFoundError(APIError):
    def __init__(
        self,
        message=None,
        http_body=None,
        http_status=None,
        json_body=None,
        headers=None,
        code=None,
    ):
        super().__init__(
            message, http_body, http_status, json_body, headers, code
        )


class ApiKeyNotFoundError(NotFoundError):
    def __init__(
        self,
        message=None,
        http_body=None,
        http_status=None,
        json_body=None,
        headers=None,
        code=None,
    ):
        super().__init__(
            message, http_body, http_status, json_body, headers, code
        )


class BundlePathNotFoundError(NotFoundError):
    def __init__(
        self,
        message=None,
        http_body=None,
        http_status=None,
        json_body=None,
        headers=None,
        code=None,
    ):
        super().__init__(
            message, http_body, http_status, json_body, headers, code
        )


class BundleRegistrationNotFoundError(NotFoundError):
    def __init__(
        self,
        message=None,
        http_body=None,
        http_status=None,
        json_body=None,
        headers=None,
        code=None,
    ):
        super().__init__(
            message, http_body, http_status, json_body, headers, code
        )


class CodeNotFoundError(NotFoundError):
    def __init__(
        self,
        message=None,
        http_body=None,
        http_status=None,
        json_body=None,
        headers=None,
        code=None,
    ):
        super().__init__(
            message, http_body, http_status, json_body, headers, code
        )


class FileNotFoundError(NotFoundError):
    def __init__(
        self,
        message=None,
        http_body=None,
        http_status=None,
        json_body=None,
        headers=None,
        code=None,
    ):
        super().__init__(
            message, http_body, http_status, json_body, headers, code
        )


class FileUploadNotFoundError(NotFoundError):
    def __init__(
        self,
        message=None,
        http_body=None,
        http_status=None,
        json_body=None,
        headers=None,
        code=None,
    ):
        super().__init__(
            message, http_body, http_status, json_body, headers, code
        )


class GroupNotFoundError(NotFoundError):
    def __init__(
        self,
        message=None,
        http_body=None,
        http_status=None,
        json_body=None,
        headers=None,
        code=None,
    ):
        super().__init__(
            message, http_body, http_status, json_body, headers, code
        )


class InboxNotFoundError(NotFoundError):
    def __init__(
        self,
        message=None,
        http_body=None,
        http_status=None,
        json_body=None,
        headers=None,
        code=None,
    ):
        super().__init__(
            message, http_body, http_status, json_body, headers, code
        )


class NestedNotFoundError(NotFoundError):
    def __init__(
        self,
        message=None,
        http_body=None,
        http_status=None,
        json_body=None,
        headers=None,
        code=None,
    ):
        super().__init__(
            message, http_body, http_status, json_body, headers, code
        )


class PlanNotFoundError(NotFoundError):
    def __init__(
        self,
        message=None,
        http_body=None,
        http_status=None,
        json_body=None,
        headers=None,
        code=None,
    ):
        super().__init__(
            message, http_body, http_status, json_body, headers, code
        )


class SiteNotFoundError(NotFoundError):
    def __init__(
        self,
        message=None,
        http_body=None,
        http_status=None,
        json_body=None,
        headers=None,
        code=None,
    ):
        super().__init__(
            message, http_body, http_status, json_body, headers, code
        )


class UserNotFoundError(NotFoundError):
    def __init__(
        self,
        message=None,
        http_body=None,
        http_status=None,
        json_body=None,
        headers=None,
        code=None,
    ):
        super().__init__(
            message, http_body, http_status, json_body, headers, code
        )


class ProcessingFailureError(APIError):
    def __init__(
        self,
        message=None,
        http_body=None,
        http_status=None,
        json_body=None,
        headers=None,
        code=None,
    ):
        super().__init__(
            message, http_body, http_status, json_body, headers, code
        )


class AgentPushUpdateBlockedError(ProcessingFailureError):
    def __init__(
        self,
        message=None,
        http_body=None,
        http_status=None,
        json_body=None,
        headers=None,
        code=None,
    ):
        super().__init__(
            message, http_body, http_status, json_body, headers, code
        )


class AgentUnavailableError(ProcessingFailureError):
    def __init__(
        self,
        message=None,
        http_body=None,
        http_status=None,
        json_body=None,
        headers=None,
        code=None,
    ):
        super().__init__(
            message, http_body, http_status, json_body, headers, code
        )


class AiTaskCannotBeRunManuallyError(ProcessingFailureError):
    def __init__(
        self,
        message=None,
        http_body=None,
        http_status=None,
        json_body=None,
        headers=None,
        code=None,
    ):
        super().__init__(
            message, http_body, http_status, json_body, headers, code
        )


class AlreadyCompletedError(ProcessingFailureError):
    def __init__(
        self,
        message=None,
        http_body=None,
        http_status=None,
        json_body=None,
        headers=None,
        code=None,
    ):
        super().__init__(
            message, http_body, http_status, json_body, headers, code
        )


class AutomationCannotBeRunManuallyError(ProcessingFailureError):
    def __init__(
        self,
        message=None,
        http_body=None,
        http_status=None,
        json_body=None,
        headers=None,
        code=None,
    ):
        super().__init__(
            message, http_body, http_status, json_body, headers, code
        )


class BehaviorNotAllowedOnRemoteServerError(ProcessingFailureError):
    def __init__(
        self,
        message=None,
        http_body=None,
        http_status=None,
        json_body=None,
        headers=None,
        code=None,
    ):
        super().__init__(
            message, http_body, http_status, json_body, headers, code
        )


class BufferedUploadDisabledForThisDestinationError(ProcessingFailureError):
    def __init__(
        self,
        message=None,
        http_body=None,
        http_status=None,
        json_body=None,
        headers=None,
        code=None,
    ):
        super().__init__(
            message, http_body, http_status, json_body, headers, code
        )


class BundleOnlyAllowsPreviewsError(ProcessingFailureError):
    def __init__(
        self,
        message=None,
        http_body=None,
        http_status=None,
        json_body=None,
        headers=None,
        code=None,
    ):
        super().__init__(
            message, http_body, http_status, json_body, headers, code
        )


class BundleOperationRequiresSubfolderError(ProcessingFailureError):
    def __init__(
        self,
        message=None,
        http_body=None,
        http_status=None,
        json_body=None,
        headers=None,
        code=None,
    ):
        super().__init__(
            message, http_body, http_status, json_body, headers, code
        )


class ConfigurationLockedPathError(ProcessingFailureError):
    def __init__(
        self,
        message=None,
        http_body=None,
        http_status=None,
        json_body=None,
        headers=None,
        code=None,
    ):
        super().__init__(
            message, http_body, http_status, json_body, headers, code
        )


class CouldNotCreateParentError(ProcessingFailureError):
    def __init__(
        self,
        message=None,
        http_body=None,
        http_status=None,
        json_body=None,
        headers=None,
        code=None,
    ):
        super().__init__(
            message, http_body, http_status, json_body, headers, code
        )


class DestinationExistsError(ProcessingFailureError):
    def __init__(
        self,
        message=None,
        http_body=None,
        http_status=None,
        json_body=None,
        headers=None,
        code=None,
    ):
        super().__init__(
            message, http_body, http_status, json_body, headers, code
        )


class DestinationFolderLimitedError(ProcessingFailureError):
    def __init__(
        self,
        message=None,
        http_body=None,
        http_status=None,
        json_body=None,
        headers=None,
        code=None,
    ):
        super().__init__(
            message, http_body, http_status, json_body, headers, code
        )


class DestinationParentConflictError(ProcessingFailureError):
    def __init__(
        self,
        message=None,
        http_body=None,
        http_status=None,
        json_body=None,
        headers=None,
        code=None,
    ):
        super().__init__(
            message, http_body, http_status, json_body, headers, code
        )


class DestinationParentDoesNotExistError(ProcessingFailureError):
    def __init__(
        self,
        message=None,
        http_body=None,
        http_status=None,
        json_body=None,
        headers=None,
        code=None,
    ):
        super().__init__(
            message, http_body, http_status, json_body, headers, code
        )


class ExceededRuntimeLimitError(ProcessingFailureError):
    def __init__(
        self,
        message=None,
        http_body=None,
        http_status=None,
        json_body=None,
        headers=None,
        code=None,
    ):
        super().__init__(
            message, http_body, http_status, json_body, headers, code
        )


class ExpectationAlreadyHasOpenWindowError(ProcessingFailureError):
    def __init__(
        self,
        message=None,
        http_body=None,
        http_status=None,
        json_body=None,
        headers=None,
        code=None,
    ):
        super().__init__(
            message, http_body, http_status, json_body, headers, code
        )


class ExpectationNotManualTriggerError(ProcessingFailureError):
    def __init__(
        self,
        message=None,
        http_body=None,
        http_status=None,
        json_body=None,
        headers=None,
        code=None,
    ):
        super().__init__(
            message, http_body, http_status, json_body, headers, code
        )


class ExpiredPrivateKeyError(ProcessingFailureError):
    def __init__(
        self,
        message=None,
        http_body=None,
        http_status=None,
        json_body=None,
        headers=None,
        code=None,
    ):
        super().__init__(
            message, http_body, http_status, json_body, headers, code
        )


class ExpiredPublicKeyError(ProcessingFailureError):
    def __init__(
        self,
        message=None,
        http_body=None,
        http_status=None,
        json_body=None,
        headers=None,
        code=None,
    ):
        super().__init__(
            message, http_body, http_status, json_body, headers, code
        )


class ExportFailureError(ProcessingFailureError):
    def __init__(
        self,
        message=None,
        http_body=None,
        http_status=None,
        json_body=None,
        headers=None,
        code=None,
    ):
        super().__init__(
            message, http_body, http_status, json_body, headers, code
        )


class ExportNotReadyError(ProcessingFailureError):
    def __init__(
        self,
        message=None,
        http_body=None,
        http_status=None,
        json_body=None,
        headers=None,
        code=None,
    ):
        super().__init__(
            message, http_body, http_status, json_body, headers, code
        )


class FailedToChangePasswordError(ProcessingFailureError):
    def __init__(
        self,
        message=None,
        http_body=None,
        http_status=None,
        json_body=None,
        headers=None,
        code=None,
    ):
        super().__init__(
            message, http_body, http_status, json_body, headers, code
        )


class FileLockedError(ProcessingFailureError):
    def __init__(
        self,
        message=None,
        http_body=None,
        http_status=None,
        json_body=None,
        headers=None,
        code=None,
    ):
        super().__init__(
            message, http_body, http_status, json_body, headers, code
        )


class FileNotUploadedError(ProcessingFailureError):
    def __init__(
        self,
        message=None,
        http_body=None,
        http_status=None,
        json_body=None,
        headers=None,
        code=None,
    ):
        super().__init__(
            message, http_body, http_status, json_body, headers, code
        )


class FilePendingProcessingError(ProcessingFailureError):
    def __init__(
        self,
        message=None,
        http_body=None,
        http_status=None,
        json_body=None,
        headers=None,
        code=None,
    ):
        super().__init__(
            message, http_body, http_status, json_body, headers, code
        )


class FileProcessingErrorError(ProcessingFailureError):
    def __init__(
        self,
        message=None,
        http_body=None,
        http_status=None,
        json_body=None,
        headers=None,
        code=None,
    ):
        super().__init__(
            message, http_body, http_status, json_body, headers, code
        )


class FileTooBigToDecryptError(ProcessingFailureError):
    def __init__(
        self,
        message=None,
        http_body=None,
        http_status=None,
        json_body=None,
        headers=None,
        code=None,
    ):
        super().__init__(
            message, http_body, http_status, json_body, headers, code
        )


class FileTooBigToEncryptError(ProcessingFailureError):
    def __init__(
        self,
        message=None,
        http_body=None,
        http_status=None,
        json_body=None,
        headers=None,
        code=None,
    ):
        super().__init__(
            message, http_body, http_status, json_body, headers, code
        )


class FileUploadedToWrongRegionError(ProcessingFailureError):
    def __init__(
        self,
        message=None,
        http_body=None,
        http_status=None,
        json_body=None,
        headers=None,
        code=None,
    ):
        super().__init__(
            message, http_body, http_status, json_body, headers, code
        )


class FilenameTooLongError(ProcessingFailureError):
    def __init__(
        self,
        message=None,
        http_body=None,
        http_status=None,
        json_body=None,
        headers=None,
        code=None,
    ):
        super().__init__(
            message, http_body, http_status, json_body, headers, code
        )


class FolderLockedError(ProcessingFailureError):
    def __init__(
        self,
        message=None,
        http_body=None,
        http_status=None,
        json_body=None,
        headers=None,
        code=None,
    ):
        super().__init__(
            message, http_body, http_status, json_body, headers, code
        )


class FolderNotEmptyError(ProcessingFailureError):
    def __init__(
        self,
        message=None,
        http_body=None,
        http_status=None,
        json_body=None,
        headers=None,
        code=None,
    ):
        super().__init__(
            message, http_body, http_status, json_body, headers, code
        )


class HistoryUnavailableError(ProcessingFailureError):
    def __init__(
        self,
        message=None,
        http_body=None,
        http_status=None,
        json_body=None,
        headers=None,
        code=None,
    ):
        super().__init__(
            message, http_body, http_status, json_body, headers, code
        )


class InvalidBundleCodeError(ProcessingFailureError):
    def __init__(
        self,
        message=None,
        http_body=None,
        http_status=None,
        json_body=None,
        headers=None,
        code=None,
    ):
        super().__init__(
            message, http_body, http_status, json_body, headers, code
        )


class InvalidFileTypeError(ProcessingFailureError):
    def __init__(
        self,
        message=None,
        http_body=None,
        http_status=None,
        json_body=None,
        headers=None,
        code=None,
    ):
        super().__init__(
            message, http_body, http_status, json_body, headers, code
        )


class InvalidFilenameError(ProcessingFailureError):
    def __init__(
        self,
        message=None,
        http_body=None,
        http_status=None,
        json_body=None,
        headers=None,
        code=None,
    ):
        super().__init__(
            message, http_body, http_status, json_body, headers, code
        )


class InvalidPriorityColorError(ProcessingFailureError):
    def __init__(
        self,
        message=None,
        http_body=None,
        http_status=None,
        json_body=None,
        headers=None,
        code=None,
    ):
        super().__init__(
            message, http_body, http_status, json_body, headers, code
        )


class InvalidRangeError(ProcessingFailureError):
    def __init__(
        self,
        message=None,
        http_body=None,
        http_status=None,
        json_body=None,
        headers=None,
        code=None,
    ):
        super().__init__(
            message, http_body, http_status, json_body, headers, code
        )


class InvalidSiteError(ProcessingFailureError):
    def __init__(
        self,
        message=None,
        http_body=None,
        http_status=None,
        json_body=None,
        headers=None,
        code=None,
    ):
        super().__init__(
            message, http_body, http_status, json_body, headers, code
        )


class InvalidZipFileError(ProcessingFailureError):
    def __init__(
        self,
        message=None,
        http_body=None,
        http_status=None,
        json_body=None,
        headers=None,
        code=None,
    ):
        super().__init__(
            message, http_body, http_status, json_body, headers, code
        )


class MetadataNotSupportedOnRemotesError(ProcessingFailureError):
    def __init__(
        self,
        message=None,
        http_body=None,
        http_status=None,
        json_body=None,
        headers=None,
        code=None,
    ):
        super().__init__(
            message, http_body, http_status, json_body, headers, code
        )


class ModelSaveErrorError(ProcessingFailureError):
    def __init__(
        self,
        message=None,
        http_body=None,
        http_status=None,
        json_body=None,
        headers=None,
        code=None,
    ):
        super().__init__(
            message, http_body, http_status, json_body, headers, code
        )


class MultipleProcessingErrorsError(ProcessingFailureError):
    def __init__(
        self,
        message=None,
        http_body=None,
        http_status=None,
        json_body=None,
        headers=None,
        code=None,
    ):
        super().__init__(
            message, http_body, http_status, json_body, headers, code
        )


class PathTooLongError(ProcessingFailureError):
    def __init__(
        self,
        message=None,
        http_body=None,
        http_status=None,
        json_body=None,
        headers=None,
        code=None,
    ):
        super().__init__(
            message, http_body, http_status, json_body, headers, code
        )


class RecipientAlreadySharedError(ProcessingFailureError):
    def __init__(
        self,
        message=None,
        http_body=None,
        http_status=None,
        json_body=None,
        headers=None,
        code=None,
    ):
        super().__init__(
            message, http_body, http_status, json_body, headers, code
        )


class RemoteEntryReadOnlyError(ProcessingFailureError):
    def __init__(
        self,
        message=None,
        http_body=None,
        http_status=None,
        json_body=None,
        headers=None,
        code=None,
    ):
        super().__init__(
            message, http_body, http_status, json_body, headers, code
        )


class RemoteServerErrorError(ProcessingFailureError):
    def __init__(
        self,
        message=None,
        http_body=None,
        http_status=None,
        json_body=None,
        headers=None,
        code=None,
    ):
        super().__init__(
            message, http_body, http_status, json_body, headers, code
        )


class ResourceBelongsToParentSiteError(ProcessingFailureError):
    def __init__(
        self,
        message=None,
        http_body=None,
        http_status=None,
        json_body=None,
        headers=None,
        code=None,
    ):
        super().__init__(
            message, http_body, http_status, json_body, headers, code
        )


class ResourceLockedError(ProcessingFailureError):
    def __init__(
        self,
        message=None,
        http_body=None,
        http_status=None,
        json_body=None,
        headers=None,
        code=None,
    ):
        super().__init__(
            message, http_body, http_status, json_body, headers, code
        )


class SubfolderLockedError(ProcessingFailureError):
    def __init__(
        self,
        message=None,
        http_body=None,
        http_status=None,
        json_body=None,
        headers=None,
        code=None,
    ):
        super().__init__(
            message, http_body, http_status, json_body, headers, code
        )


class SyncInProgressError(ProcessingFailureError):
    def __init__(
        self,
        message=None,
        http_body=None,
        http_status=None,
        json_body=None,
        headers=None,
        code=None,
    ):
        super().__init__(
            message, http_body, http_status, json_body, headers, code
        )


class TwoFactorAuthenticationCodeAlreadySentError(ProcessingFailureError):
    def __init__(
        self,
        message=None,
        http_body=None,
        http_status=None,
        json_body=None,
        headers=None,
        code=None,
    ):
        super().__init__(
            message, http_body, http_status, json_body, headers, code
        )


class TwoFactorAuthenticationCountryBlacklistedError(ProcessingFailureError):
    def __init__(
        self,
        message=None,
        http_body=None,
        http_status=None,
        json_body=None,
        headers=None,
        code=None,
    ):
        super().__init__(
            message, http_body, http_status, json_body, headers, code
        )


class TwoFactorAuthenticationGeneralErrorError(ProcessingFailureError):
    def __init__(
        self,
        message=None,
        http_body=None,
        http_status=None,
        json_body=None,
        headers=None,
        code=None,
    ):
        super().__init__(
            message, http_body, http_status, json_body, headers, code
        )


class TwoFactorAuthenticationMethodUnsupportedErrorError(
    ProcessingFailureError
):
    def __init__(
        self,
        message=None,
        http_body=None,
        http_status=None,
        json_body=None,
        headers=None,
        code=None,
    ):
        super().__init__(
            message, http_body, http_status, json_body, headers, code
        )


class TwoFactorAuthenticationUnsubscribedRecipientError(
    ProcessingFailureError
):
    def __init__(
        self,
        message=None,
        http_body=None,
        http_status=None,
        json_body=None,
        headers=None,
        code=None,
    ):
        super().__init__(
            message, http_body, http_status, json_body, headers, code
        )


class UpdatesNotAllowedForRemotesError(ProcessingFailureError):
    def __init__(
        self,
        message=None,
        http_body=None,
        http_status=None,
        json_body=None,
        headers=None,
        code=None,
    ):
        super().__init__(
            message, http_body, http_status, json_body, headers, code
        )


class RateLimitedError(APIError):
    def __init__(
        self,
        message=None,
        http_body=None,
        http_status=None,
        json_body=None,
        headers=None,
        code=None,
    ):
        super().__init__(
            message, http_body, http_status, json_body, headers, code
        )


class DuplicateShareRecipientError(RateLimitedError):
    def __init__(
        self,
        message=None,
        http_body=None,
        http_status=None,
        json_body=None,
        headers=None,
        code=None,
    ):
        super().__init__(
            message, http_body, http_status, json_body, headers, code
        )


class ReauthenticationRateLimitedError(RateLimitedError):
    def __init__(
        self,
        message=None,
        http_body=None,
        http_status=None,
        json_body=None,
        headers=None,
        code=None,
    ):
        super().__init__(
            message, http_body, http_status, json_body, headers, code
        )


class TooManyConcurrentLoginsError(RateLimitedError):
    def __init__(
        self,
        message=None,
        http_body=None,
        http_status=None,
        json_body=None,
        headers=None,
        code=None,
    ):
        super().__init__(
            message, http_body, http_status, json_body, headers, code
        )


class TooManyConcurrentRequestsError(RateLimitedError):
    def __init__(
        self,
        message=None,
        http_body=None,
        http_status=None,
        json_body=None,
        headers=None,
        code=None,
    ):
        super().__init__(
            message, http_body, http_status, json_body, headers, code
        )


class TooManyLoginAttemptsError(RateLimitedError):
    def __init__(
        self,
        message=None,
        http_body=None,
        http_status=None,
        json_body=None,
        headers=None,
        code=None,
    ):
        super().__init__(
            message, http_body, http_status, json_body, headers, code
        )


class TooManyRequestsError(RateLimitedError):
    def __init__(
        self,
        message=None,
        http_body=None,
        http_status=None,
        json_body=None,
        headers=None,
        code=None,
    ):
        super().__init__(
            message, http_body, http_status, json_body, headers, code
        )


class TooManySharesError(RateLimitedError):
    def __init__(
        self,
        message=None,
        http_body=None,
        http_status=None,
        json_body=None,
        headers=None,
        code=None,
    ):
        super().__init__(
            message, http_body, http_status, json_body, headers, code
        )


class ServiceUnavailableError(APIError):
    def __init__(
        self,
        message=None,
        http_body=None,
        http_status=None,
        json_body=None,
        headers=None,
        code=None,
    ):
        super().__init__(
            message, http_body, http_status, json_body, headers, code
        )


class AutomationsUnavailableError(ServiceUnavailableError):
    def __init__(
        self,
        message=None,
        http_body=None,
        http_status=None,
        json_body=None,
        headers=None,
        code=None,
    ):
        super().__init__(
            message, http_body, http_status, json_body, headers, code
        )


class LockOperationBusyError(ServiceUnavailableError):
    def __init__(
        self,
        message=None,
        http_body=None,
        http_status=None,
        json_body=None,
        headers=None,
        code=None,
    ):
        super().__init__(
            message, http_body, http_status, json_body, headers, code
        )


class MigrationInProgressError(ServiceUnavailableError):
    def __init__(
        self,
        message=None,
        http_body=None,
        http_status=None,
        json_body=None,
        headers=None,
        code=None,
    ):
        super().__init__(
            message, http_body, http_status, json_body, headers, code
        )


class SearchUnavailableError(ServiceUnavailableError):
    def __init__(
        self,
        message=None,
        http_body=None,
        http_status=None,
        json_body=None,
        headers=None,
        code=None,
    ):
        super().__init__(
            message, http_body, http_status, json_body, headers, code
        )


class SiteDisabledError(ServiceUnavailableError):
    def __init__(
        self,
        message=None,
        http_body=None,
        http_status=None,
        json_body=None,
        headers=None,
        code=None,
    ):
        super().__init__(
            message, http_body, http_status, json_body, headers, code
        )


class UploadsUnavailableError(ServiceUnavailableError):
    def __init__(
        self,
        message=None,
        http_body=None,
        http_status=None,
        json_body=None,
        headers=None,
        code=None,
    ):
        super().__init__(
            message, http_body, http_status, json_body, headers, code
        )


class SiteConfigurationError(APIError):
    def __init__(
        self,
        message=None,
        http_body=None,
        http_status=None,
        json_body=None,
        headers=None,
        code=None,
    ):
        super().__init__(
            message, http_body, http_status, json_body, headers, code
        )


class AccountAlreadyExistsError(SiteConfigurationError):
    def __init__(
        self,
        message=None,
        http_body=None,
        http_status=None,
        json_body=None,
        headers=None,
        code=None,
    ):
        super().__init__(
            message, http_body, http_status, json_body, headers, code
        )


class AccountOverdueError(SiteConfigurationError):
    def __init__(
        self,
        message=None,
        http_body=None,
        http_status=None,
        json_body=None,
        headers=None,
        code=None,
    ):
        super().__init__(
            message, http_body, http_status, json_body, headers, code
        )


class NoAccountForSiteError(SiteConfigurationError):
    def __init__(
        self,
        message=None,
        http_body=None,
        http_status=None,
        json_body=None,
        headers=None,
        code=None,
    ):
        super().__init__(
            message, http_body, http_status, json_body, headers, code
        )


class SiteWasRemovedError(SiteConfigurationError):
    def __init__(
        self,
        message=None,
        http_body=None,
        http_status=None,
        json_body=None,
        headers=None,
        code=None,
    ):
        super().__init__(
            message, http_body, http_status, json_body, headers, code
        )


class TrialExpiredError(SiteConfigurationError):
    def __init__(
        self,
        message=None,
        http_body=None,
        http_status=None,
        json_body=None,
        headers=None,
        code=None,
    ):
        super().__init__(
            message, http_body, http_status, json_body, headers, code
        )


class TrialLockedError(SiteConfigurationError):
    def __init__(
        self,
        message=None,
        http_body=None,
        http_status=None,
        json_body=None,
        headers=None,
        code=None,
    ):
        super().__init__(
            message, http_body, http_status, json_body, headers, code
        )


class UserRequestsEnabledRequiredError(SiteConfigurationError):
    def __init__(
        self,
        message=None,
        http_body=None,
        http_status=None,
        json_body=None,
        headers=None,
        code=None,
    ):
        super().__init__(
            message, http_body, http_status, json_body, headers, code
        )
