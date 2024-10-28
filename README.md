# Files.com Python Client

The content included here should be enough to get started, but please visit our
[Developer Documentation Website](https://developers.files.com/python/) for the complete documentation.

## Introduction

The Files.com Python package is the best way to use Files.com from applications written in the Python language.

Files.com customers use our Python package for directly working with files and folders as well as performing management tasks such as adding/removing users, onboarding counterparties, retrieving information about automations and more.

Every function in the Files.com application is available via Python.  Nothing is excluded.

This package is officially supported by Files.com for Python 3.8+.  Prior versions of Python are considered end-of-life by the Python Software Foundation and Files.com only supports environments that are still supported by their vendor.  With that said, we believe that this package works in Python 3.5-3.7 as well.

The Python package uses the Files.com RESTful APIs via the HTTPS protocol (port 443) to securely communicate and transfer files so no firewall changes should be required in order to allow connectivity to Files.com.

### Installation

Use `pip` to install the latest version of the `Files.com` package.

```shell
pip3 install Files.com
```

Files.com automatically pushes a new release to PIP every time a commit is made to the `master` branch on GitHub, so there is no benefit in directly linking the package from GitHub.

### Files.com is Committed to Python

Python is the most commonly used language for custom integrations to Files.com.  Our Files.com Desktop v6 application (that we publish) is also written in Python, using this exact same package.

Explore the [files-sdk-python](https://github.com/Files-com/files-sdk-python) code on GitHub.

### Getting Support

The Files.com Support team provides official support for all of our official Files.com integration tools.

To initiate a support conversation, you can send an [Authenticated Support Request](https://www.files.com/docs/overview/requesting-support) or simply send an E-Mail to support@files.com.

## Authentication

### Authenticate with an API Key

Authenticating with an API key is the recommended authentication method for most scenarios, and is
the method used in the examples on this site.

To use the API or SDKs with an API Key, first generate an API key from the [web
interface](https://www.files.com/docs/sdk-and-apis/api-keys) or [via the API or an
SDK](/python/resources/developers/api-keys).

Note that when using a user-specific API key, if the user is an administrator, you will have full
access to the entire API. If the user is not an administrator, you will only be able to access files
that user can access, and no access will be granted to site administration functions in the API.

```python title="Example Request"
files_sdk.set_api_key("YOUR_API_KEY")

## Alternatively, you can specify the API key on a per-request basis in the final parameter to any method or initializer.
files_sdk.user.list(params, {"api_key": "YOUR_API_KEY"})
```

Don't forget to replace the placeholder, `YOUR_API_KEY`, with your actual API key.

### Authenticate with a Session

You can also authenticate to the REST API or SDKs by creating a user session using the username and
password of an active user. If the user is an administrator, the session will have full access to
the entire API. Sessions created from regular user accounts will only be able to access files that
user can access, and no access will be granted to site administration functions.

API sessions use the exact same session timeout settings as web interface sessions. When an API
session times out, simply create a new session and resume where you left off. This process is not
automatically handled by SDKs because we do not want to store password information in memory without
your explicit consent.

#### Logging In

To create a session, the `create` method is called on the `files_sdk` object with the user's username and
password.

This returns a session object that can be used to authenticate SDK method calls.

```python title="Example Request"
session = files_sdk.session.create({ "username": "motor", "password": "vroom" })
```

#### Using a Session

Once a session has been created, you can store the session globally, use the session per object, or use the session per request to authenticate SDK operations.

```python title="Example Request"
## You may set the returned session to be used by default for subsequent requests.
files_sdk.set_session(session)

## Alternatively, you can specify the session ID on a per-object basis in the second parameter to a model constructor.
user = files_sdk.user.User(params, {"session_id": session.id})

## You may also specify the session ID on a per-request basis in the final parameter to static methods.
files_sdk.user.find(id, params, {"session_id": session.id})
```

#### Logging Out

User sessions can be ended calling the `destroy` method on the `session` object.

```python title="Example Request"
session.destroy()
```

## Configuration

### Configuration Options

#### Base URL

Setting the base URL for the API is required if your site is configured to disable global acceleration.
This can also be set to use a mock server in development or CI.

```python title="Example setting"
files_sdk.base_url = "https://SUBDOMAIN.files.com"
```

#### Log Level

This SDK utilizes the standard Python logging framework. It will respect the global log level
and you can set the module specific log level and other logging settings by getting the logger
object in the standard manner as shown below:

```python title="Example setting"
import logging
logging.getLogger("files_sdk")
```

#### Console Log Level

Enables printing of messages to stderr in addition to normal logging.

Allowed values are:

* `None`
* "info"
* "debug"

```python title="Example setting"
files_sdk.console_log_level = "info"
```

#### Open Timeout

Open timeout in seconds. The default value is 30.

```python title="Example setting"
files_sdk.open_timeout = 60
```

#### Read Timeout

Read timeout in seconds. The default value is 80.

```python title="Example setting"
files_sdk.read_timeout = 90
```

#### Initial Network Retry Delay

Initial retry delay in seconds. The default value is 0.5.

```python title="Example setting"
files_sdk.initial_network_retry_delay = 1
```

#### Maximum Retry Delay

Maximum network retry delay in seconds. The default value is 2.

```python title="Example setting"
files_sdk.max_network_retry_delay = 5
```

#### Maximum Network Retries

Maximum number of retries. The default value is 3.

```python title="Example setting"
files_sdk.max_network_retries = 5
```

#### Source IP

Configure the local IP address from which to send requests.

```python title="Example setting"
files_sdk.source_ip = '10.1.2.3'
```

## Sort and Filter

Several of the Files.com API resources have list operations that return multiple instances of the
resource. The List operations can be sorted and filtered.

### Sorting

To sort the returned data, pass in the ```sort_by``` method argument.

Each resource supports a unique set of valid sort fields and can only be sorted by one field at a
time.

The argument value is a Python dictionary that has a key of the resource field name sort on and a
value of either ```"asc"``` or ```"desc"``` to specify the sort order.

```python title="Sort Example"
## users sorted by username
files_sdk.set_api_key("my-key")
users = files_sdk.user.list({
  "sort_by": { "username": "asc"}
})
for user in users.auto_paging_iter():
  # Operate on user
```

### Filtering

Filters apply selection criteria to the underlying query that returns the results. They can be
applied individually or combined with other filters, and the resulting data can be sorted by a
single field.

Each resource supports a unique set of valid filter fields, filter combinations, and combinations of
filters and sort fields.

The passed in argument value is a Python dictionary that has a key of the resource field name to
filter on and a passed in value to use in the filter comparison.

#### Filter Types

| Filter | Type | Description |
| --------- | --------- | --------- |
| `filter` | Exact | Find resources that have an exact field value match to a passed in value. (i.e., FIELD_VALUE = PASS_IN_VALUE). |
| `filter_prefix` | Pattern | Find resources where the specified field is prefixed by the supplied value. This is applicable to values that are strings. |
| `filter_gt` | Range | Find resources that have a field value that is greater than the passed in value.  (i.e., FIELD_VALUE > PASS_IN_VALUE). |
| `filter_gteq` | Range | Find resources that have a field value that is greater than or equal to the passed in value.  (i.e., FIELD_VALUE >=  PASS_IN_VALUE). |
| `filter_lt` | Range | Find resources that have a field value that is less than the passed in value.  (i.e., FIELD_VALUE < PASS_IN_VALUE). |
| `filter_lteq` | Range | Find resources that have a field value that is less than or equal to the passed in value.  (i.e., FIELD_VALUE \<= PASS_IN_VALUE). |

```python title="Exact Filter Example"
## non admin users
files_sdk.set_api_key("my-key")
users = files_sdk.user.list({
  "filter": { "not_site_admin": true}
})
for user in users.auto_paging_iter():
  # Operate on user
```

```python title="Range Filter Example"
## users who haven't logged in since 2024-01-01
files_sdk.set_api_key("my-key")
users = files_sdk.user.list({
  "filter_gteq": { "last_login_at": "2024-01-01" }
})
for user in users.auto_paging_iter():
  # Operate on user
```

```python title="Pattern Filter Example"
## users whose usernames start with 'test'
files_sdk.set_api_key("my-key")
users = files_sdk.user.list({
  "filter_prefix": { "username": "test" }
})
for user in users.auto_paging_iter():
  # Operate on user
```

```python title="Combination Filter with Sort Example"
## users whose usernames start with 'test' and are not admins
files_sdk.set_api_key("my-key")
users = files_sdk.user.list({
  "filter_prefix": { "username": "test" },
  "filter": { "not_site_admin": "true" },
  "sort_by": { "username": "asc"}
})
for user in users.auto_paging_iter():
  # Operate on user
```

## Errors

The Files.com Python SDK will return errors by raising exceptions. There are many exception classes defined in the Files SDK that correspond
to specific errors.

The raised exceptions come from two categories:

1.  SDK Exceptions - errors that originate within the SDK
2.  API Exceptions - errors that occur due to the response from the Files.com API.  These errors are grouped into common error types.

There are several types of exceptions within each category.  Exception classes indicate different types of errors and are named in a
fashion that describe the general premise of the originating error.  More details can be found in the err object message.

Use standard Python exception handling to detect and deal with errors.  It is generally recommended to handle specific errors first, then
handle the general `files_sdk.error.Error` exception as a catch-all.

```python title="Example Error Handling"
try:
  session = files_sdk.session.create({ "username": "USERNAME", "password": "BADPASSWORD" })
except files_sdk.error.NotAuthenticatedError as err:
    print(f"Authentication Error Occurred ({type(err).__name__}):", err)
except files_sdk.error.Error as err:
    print(f"Unknown Error Occurred ({type(err).__name__}):", err)
```

### Error Types

#### SDK Errors

SDK errors are general errors that occur within the SDK code.  Each exception class inherits from a standard `Error` base class.

```python title="Example SDK Exception Class Inheritance Structure"
files_sdk.error.APIConnectionError -> files_sdk.error.Error -> Exception
```
##### SDK Exception Classes

| Error Class Name| Description |
| --------------- | ------------ |
| `APIConnectionError`| The Files.com API cannot be reached |
| `AuthenticationError`| Not enough authentication information has been provided |
| `InvalidParameterError`| A passed in parameter is invalid |
| `MissingParameterError`| A method parameter is missing |
| `NotImplementedError`| The called method has not be implemented by the SDK |

#### API Errors

API errors are errors returned by the Files.com API.  Each exception class inherits from an error group base class.
The error group base class indicates a particular type of error.

```python title="Example API Exception Class Inheritance Structure"
files_sdk.error.FolderAdminPermissionRequiredError -> files_sdk.error.NotAuthorizedError -> files_sdk.error.APIError -> files_sdk.error.Error -> Exception
```
##### API Exception Classes

| Error Class Name | Error Group |
| --------- | --------- |
|`AgentUpgradeRequiredError`|  `BadRequestError` |
|`AttachmentTooLargeError`|  `BadRequestError` |
|`CannotDownloadDirectoryError`|  `BadRequestError` |
|`CantMoveWithMultipleLocationsError`|  `BadRequestError` |
|`DatetimeParseError`|  `BadRequestError` |
|`DestinationSameError`|  `BadRequestError` |
|`FolderMustNotBeAFileError`|  `BadRequestError` |
|`FoldersNotAllowedError`|  `BadRequestError` |
|`InvalidBodyError`|  `BadRequestError` |
|`InvalidCursorError`|  `BadRequestError` |
|`InvalidCursorTypeForSortError`|  `BadRequestError` |
|`InvalidEtagsError`|  `BadRequestError` |
|`InvalidFilterAliasCombinationError`|  `BadRequestError` |
|`InvalidFilterFieldError`|  `BadRequestError` |
|`InvalidFilterParamError`|  `BadRequestError` |
|`InvalidFilterParamValueError`|  `BadRequestError` |
|`InvalidInputEncodingError`|  `BadRequestError` |
|`InvalidInterfaceError`|  `BadRequestError` |
|`InvalidOauthProviderError`|  `BadRequestError` |
|`InvalidPathError`|  `BadRequestError` |
|`InvalidReturnToUrlError`|  `BadRequestError` |
|`InvalidSortFilterCombinationError`|  `BadRequestError` |
|`InvalidUploadOffsetError`|  `BadRequestError` |
|`InvalidUploadPartGapError`|  `BadRequestError` |
|`InvalidUploadPartSizeError`|  `BadRequestError` |
|`MethodNotAllowedError`|  `BadRequestError` |
|`NoValidInputParamsError`|  `BadRequestError` |
|`PartNumberTooLargeError`|  `BadRequestError` |
|`PathCannotHaveTrailingWhitespaceError`|  `BadRequestError` |
|`ReauthenticationNeededFieldsError`|  `BadRequestError` |
|`RequestParamsContainInvalidCharacterError`|  `BadRequestError` |
|`RequestParamsInvalidError`|  `BadRequestError` |
|`RequestParamsRequiredError`|  `BadRequestError` |
|`SearchAllOnChildPathError`|  `BadRequestError` |
|`UnsupportedCurrencyError`|  `BadRequestError` |
|`UnsupportedHttpResponseFormatError`|  `BadRequestError` |
|`UnsupportedMediaTypeError`|  `BadRequestError` |
|`UserIdInvalidError`|  `BadRequestError` |
|`UserIdOnUserEndpointError`|  `BadRequestError` |
|`UserRequiredError`|  `BadRequestError` |
|`AdditionalAuthenticationRequiredError`|  `NotAuthenticatedError` |
|`AuthenticationRequiredError`|  `NotAuthenticatedError` |
|`BundleRegistrationCodeFailedError`|  `NotAuthenticatedError` |
|`FilesAgentTokenFailedError`|  `NotAuthenticatedError` |
|`InboxRegistrationCodeFailedError`|  `NotAuthenticatedError` |
|`InvalidCredentialsError`|  `NotAuthenticatedError` |
|`InvalidOauthError`|  `NotAuthenticatedError` |
|`InvalidOrExpiredCodeError`|  `NotAuthenticatedError` |
|`InvalidSessionError`|  `NotAuthenticatedError` |
|`InvalidUsernameOrPasswordError`|  `NotAuthenticatedError` |
|`LockedOutError`|  `NotAuthenticatedError` |
|`LockoutRegionMismatchError`|  `NotAuthenticatedError` |
|`OneTimePasswordIncorrectError`|  `NotAuthenticatedError` |
|`TwoFactorAuthenticationErrorError`|  `NotAuthenticatedError` |
|`TwoFactorAuthenticationSetupExpiredError`|  `NotAuthenticatedError` |
|`ApiKeyIsDisabledError`|  `NotAuthorizedError` |
|`ApiKeyIsPathRestrictedError`|  `NotAuthorizedError` |
|`ApiKeyOnlyForDesktopAppError`|  `NotAuthorizedError` |
|`ApiKeyOnlyForMobileAppError`|  `NotAuthorizedError` |
|`ApiKeyOnlyForOfficeIntegrationError`|  `NotAuthorizedError` |
|`BillingOrSiteAdminPermissionRequiredError`|  `NotAuthorizedError` |
|`BillingPermissionRequiredError`|  `NotAuthorizedError` |
|`BundleMaximumUsesReachedError`|  `NotAuthorizedError` |
|`CannotLoginWhileUsingKeyError`|  `NotAuthorizedError` |
|`CantActForOtherUserError`|  `NotAuthorizedError` |
|`ContactAdminForPasswordChangeHelpError`|  `NotAuthorizedError` |
|`FilesAgentFailedAuthorizationError`|  `NotAuthorizedError` |
|`FolderAdminOrBillingPermissionRequiredError`|  `NotAuthorizedError` |
|`FolderAdminPermissionRequiredError`|  `NotAuthorizedError` |
|`FullPermissionRequiredError`|  `NotAuthorizedError` |
|`HistoryPermissionRequiredError`|  `NotAuthorizedError` |
|`InsufficientPermissionForParamsError`|  `NotAuthorizedError` |
|`InsufficientPermissionForSiteError`|  `NotAuthorizedError` |
|`MustAuthenticateWithApiKeyError`|  `NotAuthorizedError` |
|`NeedAdminPermissionForInboxError`|  `NotAuthorizedError` |
|`NonAdminsMustQueryByFolderOrPathError`|  `NotAuthorizedError` |
|`NotAllowedToCreateBundleError`|  `NotAuthorizedError` |
|`PasswordChangeNotRequiredError`|  `NotAuthorizedError` |
|`PasswordChangeRequiredError`|  `NotAuthorizedError` |
|`ReadOnlySessionError`|  `NotAuthorizedError` |
|`ReadPermissionRequiredError`|  `NotAuthorizedError` |
|`ReauthenticationFailedError`|  `NotAuthorizedError` |
|`ReauthenticationFailedFinalError`|  `NotAuthorizedError` |
|`ReauthenticationNeededActionError`|  `NotAuthorizedError` |
|`RecaptchaFailedError`|  `NotAuthorizedError` |
|`SelfManagedRequiredError`|  `NotAuthorizedError` |
|`SiteAdminRequiredError`|  `NotAuthorizedError` |
|`SiteFilesAreImmutableError`|  `NotAuthorizedError` |
|`TwoFactorAuthenticationRequiredError`|  `NotAuthorizedError` |
|`UserIdWithoutSiteAdminError`|  `NotAuthorizedError` |
|`WriteAndBundlePermissionRequiredError`|  `NotAuthorizedError` |
|`WritePermissionRequiredError`|  `NotAuthorizedError` |
|`ZipDownloadIpMismatchError`|  `NotAuthorizedError` |
|`ApiKeyNotFoundError`|  `NotFoundError` |
|`BundlePathNotFoundError`|  `NotFoundError` |
|`BundleRegistrationNotFoundError`|  `NotFoundError` |
|`CodeNotFoundError`|  `NotFoundError` |
|`FileNotFoundError`|  `NotFoundError` |
|`FileUploadNotFoundError`|  `NotFoundError` |
|`FolderNotFoundError`|  `NotFoundError` |
|`GroupNotFoundError`|  `NotFoundError` |
|`InboxNotFoundError`|  `NotFoundError` |
|`NestedNotFoundError`|  `NotFoundError` |
|`PlanNotFoundError`|  `NotFoundError` |
|`SiteNotFoundError`|  `NotFoundError` |
|`UserNotFoundError`|  `NotFoundError` |
|`AlreadyCompletedError`|  `ProcessingFailureError` |
|`AutomationCannotBeRunManuallyError`|  `ProcessingFailureError` |
|`BehaviorNotAllowedOnRemoteServerError`|  `ProcessingFailureError` |
|`BundleOnlyAllowsPreviewsError`|  `ProcessingFailureError` |
|`BundleOperationRequiresSubfolderError`|  `ProcessingFailureError` |
|`CouldNotCreateParentError`|  `ProcessingFailureError` |
|`DestinationExistsError`|  `ProcessingFailureError` |
|`DestinationFolderLimitedError`|  `ProcessingFailureError` |
|`DestinationParentConflictError`|  `ProcessingFailureError` |
|`DestinationParentDoesNotExistError`|  `ProcessingFailureError` |
|`ExpiredPrivateKeyError`|  `ProcessingFailureError` |
|`ExpiredPublicKeyError`|  `ProcessingFailureError` |
|`ExportFailureError`|  `ProcessingFailureError` |
|`ExportNotReadyError`|  `ProcessingFailureError` |
|`FailedToChangePasswordError`|  `ProcessingFailureError` |
|`FileLockedError`|  `ProcessingFailureError` |
|`FileNotUploadedError`|  `ProcessingFailureError` |
|`FilePendingProcessingError`|  `ProcessingFailureError` |
|`FileProcessingErrorError`|  `ProcessingFailureError` |
|`FileTooBigToDecryptError`|  `ProcessingFailureError` |
|`FileTooBigToEncryptError`|  `ProcessingFailureError` |
|`FileUploadedToWrongRegionError`|  `ProcessingFailureError` |
|`FilenameTooLongError`|  `ProcessingFailureError` |
|`FolderLockedError`|  `ProcessingFailureError` |
|`FolderNotEmptyError`|  `ProcessingFailureError` |
|`HistoryUnavailableError`|  `ProcessingFailureError` |
|`InvalidBundleCodeError`|  `ProcessingFailureError` |
|`InvalidFileTypeError`|  `ProcessingFailureError` |
|`InvalidFilenameError`|  `ProcessingFailureError` |
|`InvalidPriorityColorError`|  `ProcessingFailureError` |
|`InvalidRangeError`|  `ProcessingFailureError` |
|`ModelSaveErrorError`|  `ProcessingFailureError` |
|`MultipleProcessingErrorsError`|  `ProcessingFailureError` |
|`PathTooLongError`|  `ProcessingFailureError` |
|`RecipientAlreadySharedError`|  `ProcessingFailureError` |
|`RemoteServerErrorError`|  `ProcessingFailureError` |
|`ResourceLockedError`|  `ProcessingFailureError` |
|`SubfolderLockedError`|  `ProcessingFailureError` |
|`TwoFactorAuthenticationCodeAlreadySentError`|  `ProcessingFailureError` |
|`TwoFactorAuthenticationCountryBlacklistedError`|  `ProcessingFailureError` |
|`TwoFactorAuthenticationGeneralErrorError`|  `ProcessingFailureError` |
|`TwoFactorAuthenticationMethodUnsupportedErrorError`|  `ProcessingFailureError` |
|`TwoFactorAuthenticationUnsubscribedRecipientError`|  `ProcessingFailureError` |
|`UpdatesNotAllowedForRemotesError`|  `ProcessingFailureError` |
|`DuplicateShareRecipientError`|  `RateLimitedError` |
|`ReauthenticationRateLimitedError`|  `RateLimitedError` |
|`TooManyConcurrentLoginsError`|  `RateLimitedError` |
|`TooManyConcurrentRequestsError`|  `RateLimitedError` |
|`TooManyLoginAttemptsError`|  `RateLimitedError` |
|`TooManyRequestsError`|  `RateLimitedError` |
|`TooManySharesError`|  `RateLimitedError` |
|`AgentUnavailableError`|  `ServiceUnavailableError` |
|`AutomationsUnavailableError`|  `ServiceUnavailableError` |
|`MigrationInProgressError`|  `ServiceUnavailableError` |
|`SiteDisabledError`|  `ServiceUnavailableError` |
|`UploadsUnavailableError`|  `ServiceUnavailableError` |
|`AccountAlreadyExistsError`|  `SiteConfigurationError` |
|`AccountOverdueError`|  `SiteConfigurationError` |
|`NoAccountForSiteError`|  `SiteConfigurationError` |
|`SiteWasRemovedError`|  `SiteConfigurationError` |
|`TrialExpiredError`|  `SiteConfigurationError` |
|`TrialLockedError`|  `SiteConfigurationError` |
|`UserRequestsEnabledRequiredError`|  `SiteConfigurationError` |

## Examples

### File Operations

This SDK allows both file based transfer and data based transfer. Please see the examples below.

#### File Download

The second parameter is optional and will simply use the remote filename by default.

```python
files_sdk.file.download_file("/remote.txt", "local.txt")
```

#### File Upload

The second parameter is optional and will simply use the local filename by default.

```python
files_sdk.file.upload_file("local.txt", "/remote.txt")
```

If the parent directories do not already exist, they can be automatically created by passing
`mkdir_parents` in the `params`.

```python
files_sdk.file.upload_file("local.txt", "/uploads/remote.txt", params={"mkdir_parents": True})
```

#### List Root Folder

```python
for f in files_sdk.folder.list_for("/").auto_paging_iter():
    print(f.type, f.path)
```

#### Writing a File Example (string)

```python
with files_sdk.file.open("foo.txt", 'w') as f:
    f.write("contents")
```

#### Writing a File Example (binary)

```python
with files_sdk.file.open("foo.txt", 'wb') as f:
    f.write(b"contents")
```

#### Reading a File Example (string)

```python
with files_sdk.open("foo.txt", 'r') as f:
    print(f.read())
```

#### Reading a File Example (binary)

```python
with files_sdk.open("foo.txt", 'rb') as f:
    print(f.read())
```

### List Responses and Cursor Paging

List responses for APIs with cursor support will return an iterable object
which contains a single page of records. It has a built-in `auto_paging_iter`
method to iterate through the pages, making the additional API calls
as needed.

#### Iterating with auto_paging_iter

```python
list_obj = files_sdk.folder.list_for('/')

for f in list_obj.auto_paging_iter():
    print(f.type, f.path)
```

#### Iterating Manually

```python
list_obj = files_sdk.folder.list_for('/')

for f in list_obj:
    print(f.type, f.path)

while list_obj.has_next_page:
    list_obj.load_next_page()
    for f in list_obj:
        print(f.type, f.path)
```

### Comparing Case-Insensitive Files and Paths

For related documentation see [Case Sensitivity Documentation](https://www.files.com/docs/files-and-folders/file-system-semantics/case-sensitivity).

```python
if files_sdk.path_util.is_same("Fïłèńämê.Txt", "filename.txt"):
    print("Paths are the same")
```

## Mock Server

Files.com publishes a Files.com API server, which is useful for testing your use of the Files.com
SDKs and other direct integrations against the Files.com API in an integration test environment.

It is a Ruby app that operates as a minimal server for the purpose of testing basic network
operations and JSON encoding for your SDK or API client. It does not maintain state and it does not
deeply inspect your submissions for correctness.

Eventually we will add more features intended for integration testing, such as the ability to
intentionally provoke errors.

Download the server as a Docker image via [Docker Hub](https://hub.docker.com/r/filescom/files-mock-server).

The Source Code is also available on [GitHub](https://github.com/Files-com/files-mock-server).

A README is available on the GitHub link.
