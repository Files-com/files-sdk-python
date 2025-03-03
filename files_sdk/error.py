class Error(Exception):
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
        self.http_body = http_body
        self.http_status = http_status
        self.json_body = json_body
        self.headers = headers or {}
        self.code = code
        self.response = None

    def __str__(self):
        msg = ""
        if self.http_status:
            msg += "HTTP {} ".format(self.http_status)
        if self._message:
            msg += self._message
        return msg


class APIConnectionError(Error):
    pass


class APIError(Error):
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

        if json_body is None:
            return

        self.detail = json_body.get("detail")
        self.error = json_body.get("error")
        self.errors = json_body.get("errors")
        self.http_code = json_body.get("http-code")
        self.instance = json_body.get("instance")
        self.model_errors = json_body.get("model-errors")
        self.title = json_body.get("title")
        self.error_type = json_body.get("type")
        self.data = json_body.get("data")


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


class FilesAgentTokenFailedError(NotAuthenticatedError):
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


class BillingOrSiteAdminPermissionRequiredError(NotAuthorizedError):
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


class FolderNotFoundError(NotFoundError):
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


class AgentUnavailableError(ServiceUnavailableError):
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
