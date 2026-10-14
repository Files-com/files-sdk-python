# Files.com Python Client

The Files.com Python Client provides a direct, high performance integration to Files.com from applications written in Python.

Files.com is the cloud-native, next-gen MFT, SFTP, and secure file-sharing platform that replaces brittle legacy servers with one always-on, secure fabric. Automate mission-critical file flows—across any cloud, protocol, or partner—while supporting human collaboration and eliminating manual work.

With universal SFTP, AS2, HTTPS, and 50+ native connectors backed by military-grade encryption, Files.com unifies governance, visibility, and compliance in a single pane of glass.

The content included here should be enough to get started, but please visit our
[Developer Documentation Website](https://developers.files.com/python/) for the complete documentation.
[examples/getting_started.py](https://github.com/Files-com/files-sdk-python/blob/master/examples/getting_started.py)
is a short, runnable tour of the SDK.

## Introduction

The Files.com Python SDK manages files, folders, users, permissions and other API resources. Start by installing the package, then choose [Authentication](/python/overview/authentication) and a [Client](/python/overview/clients). For file transfers, begin with [Uploads](/python/overview/uploads) or [Downloads](/python/overview/downloads).

The SDK communicates over HTTPS on port 443. Your environment needs outbound access to Files.com and the storage hosts used for transfers.

<div></div>

### Installation

Install the package into the Python environment that runs your application:

```shell
python -m pip install Files.com
```

Python 3.11 or newer is required. The package is tested on CPython 3.11–3.14 and supported on Python versions receiving vendor security updates. On older Python versions, pip installs the last 1.x release, which no longer receives updates.

Version 2 changes retry behavior and transfer return values. Review [UPGRADING.md](https://github.com/Files-com/files-sdk-python/blob/master/UPGRADING.md) when moving an existing integration from 1.x.

<div></div>

### Files.com is Committed to Python

The package supports custom integrations across the Files.com API. Use the resource reference for operation parameters, and the overview guides for [pagination](/python/overview/pagination), [retries](/python/overview/retries) and [cancellation](/python/overview/cancellation).

Explore the [files-sdk-python](https://github.com/Files-com/files-sdk-python) code on GitHub.

### Getting Support

The Files.com Support team provides official support for all of our official Files.com integration tools.

To initiate a support conversation, you can send an [Authenticated Support Request](https://www.files.com/docs/overview/requesting-support) or simply send an E-Mail to support@files.com.

## Authentication

There are two ways to authenticate: API Key authentication and Session-based authentication.

### Authenticate with an API Key

Authenticating with an API key is the recommended authentication method for most scenarios, and is
the method used in the examples on this site.

To use an API Key, first generate an API key from the [web
interface](https://www.files.com/docs/sdk-and-apis/api-keys) or [via the API or an
SDK](https://developers.files.com/python/resources/developers/api-keys).

Note that when using a user-specific API key, if the user is an administrator, you will have full
access to the entire API. If the user is not an administrator, you will only be able to access files
that user can access, and no access will be granted to site administration functions in the API.

```python title="Example Request"
import files_sdk

files_sdk.set_api_key("YOUR_API_KEY")

## Alternatively, you can specify the API key on a per-request basis in the final parameter to any method or initializer.
try:
  files_sdk.user.list(params, {"api_key": "YOUR_API_KEY"})
except files_sdk.error.NotAuthenticatedError as err:
  print(f"Authentication Error Occurred ({type(err).__name__}):", err)
except files_sdk.error.Error as err:
  print(f"Unknown Error Occurred ({type(err).__name__}):", err)
```

Don't forget to replace the placeholder, `YOUR_API_KEY`, with your actual API key.

### Authenticate with a Session

You can also authenticate by creating a user session using the username and
password of an active user. If the user is an administrator, the session will have full access to
all capabilities of Files.com. Sessions created from regular user accounts will only be able to access files that
user can access, and no access will be granted to site administration functions.

Sessions use the exact same session timeout settings as web interface sessions. When a
session times out, simply create a new session and resume where you left off. This process is not
automatically handled by our SDKs because we do not want to store password information in memory without
your explicit consent.

#### Logging In

To create a session, call `files_sdk.session.create()`, or a client's `client.session.create()`, with
the user's username and password.

This returns a session object that can be used to authenticate SDK method calls, including as a
client's `session` setting. Closing a client does not log out its session.

```python title="Example Request"
import files_sdk

try:
  session = files_sdk.session.create({ "username": "motor", "password": "vroom" })
except files_sdk.error.NotAuthenticatedError as err:
  print(f"Authentication Error Occurred ({type(err).__name__}):", err)
except files_sdk.error.Error as err:
  print(f"Unknown Error Occurred ({type(err).__name__}):", err)
```

#### Using a Session

Once a session has been created, you can store the session globally, use the session per object, or use the session per request to authenticate SDK operations.

```python title="Example Request"
import files_sdk

## You may set the returned session to be used by default for subsequent requests.
files_sdk.set_session(session)

try:
  # Alternatively, you can specify the session ID on a per-object basis in the second parameter to a model constructor.
  user = files_sdk.user.User(params, {"session_id": session.id})

  # You may also specify the session ID on a per-request basis in the final parameter to static methods.
  files_sdk.user.find(id, params, {"session_id": session.id})
except files_sdk.error.NotAuthenticatedError as err:
  print(f"Authentication Error Occurred ({type(err).__name__}):", err)
except files_sdk.error.Error as err:
  print(f"Unknown Error Occurred ({type(err).__name__}):", err)
```

#### Logging Out

User sessions can be ended calling the `destroy` method on the `session` object.

```python title="Example Request"
session.destroy()
```

## Configuration

Create a `files_sdk.Client` with the settings it needs. A client never reads the module-level
settings, and its objects keep using it. See [Clients](https://developers.files.com/python/overview/clients) for per-call
options, clients with your own Requests session, and closing.

The module-level functions, such as `files_sdk.user.find()`, use the settings on the `files_sdk`
module instead, as they are when each call starts.

```python title="Example setting"
import files_sdk

client = files_sdk.Client(
  api_key="YOUR_API_KEY",
  base_url="https://SUBDOMAIN.files.com",
  workspace_id=5,
  open_timeout=30,
  read_timeout=80,
  max_network_retries=3,
  request_timeout=None,
)
```

### Client Settings

| Setting | Default | Meaning |
| --- | --- | --- |
| `api_key`, `session_id`, `session` | | The credential. With both, the API key is used. |
| `workspace_id`, `language`, `headers` | | Sent with every API request. |
| `base_url` | `https://app.files.com` | Where the API is. See Base URL below. |
| `open_timeout`, `read_timeout` | 30, 80 | Seconds to wait for a connection to each resolved address, and for each read. |
| `max_network_retries` | 3 | Retries of a failed request; 0 sends it once. |
| `initial_network_retry_delay`, `max_network_retry_delay` | 0.1, 2 | Seconds API retries wait, doubling. |
| `request_timeout` | None | Seconds each operation may take in all. |
| `max_redirects` | 30 | Redirects each request may follow. |
| `source_ip` | | The local address to send from. |
| `verify`, `cert`, `proxies`, `trust_env` | `True`, None, None, `True` | As for `requests.Session`. |
| `http_session` | | Your own `requests.Session` to send through. |
| `transfer_limiter`, `upload_tuning` | A limiter of its own, adaptive | See [Uploads](https://developers.files.com/python/overview/uploads). |
| `region_policy`, `region_handler`, `region_development_origins` | `"automatic"` | See [Regional Relocation](https://developers.files.com/python/overview/regional-relocation). |

[Retries and Timeouts](https://developers.files.com/python/overview/retries) and
[Cancellation and Deadlines](https://developers.files.com/python/overview/cancellation) describe the timing settings.

### Module Settings

#### Base URL

Set this to the full https:// URL of your Files.com subdomain (e.g. `https://MY-SUBDOMAIN.files.com`).
This is not required in most cases, but one benefit of setting it is that it ensures that authentication failures will be logged to your site's API logs.  Without setting this, we won't know which site to associate the authentication failure with, and it won't be logged to your site's API logs.
This is always required if your site is configured to disable global acceleration.
This can also be set to use a mock server in development or CI.
A client takes the same value as its `base_url` setting.

```python title="Example setting"
import files_sdk

files_sdk.base_url = "https://SUBDOMAIN.files.com"
```

#### Log Level

This SDK uses the standard Python logging framework, through the `files_sdk` logger. The SDK
logs nothing until your application configures logging. At INFO it logs each request, response
and retry without credentials or signed URLs; at DEBUG it logs complete requests and responses,
including credentials, signed URLs and file content, so enable DEBUG only where those can be
kept safe.

```python title="Example setting"
import logging

logging.basicConfig()
logging.getLogger("files_sdk").setLevel(logging.INFO)
```

#### Console Log Level

Also prints the SDK's messages at or above this level to stderr, however logging is configured.

Allowed values are:

* "none" (the default)
* "error"
* "warning"
* "info"
* "debug"

```python title="Example setting"
import files_sdk

files_sdk.console_log_level = "info"
```

#### Open Timeout

Seconds to wait for a connection to each address the host name resolves to. The default
value is 30.

```python title="Example setting"
import files_sdk

files_sdk.open_timeout = 60
```

#### Read Timeout

Read timeout in seconds, for each read of a response. The default value is 80.

```python title="Example setting"
import files_sdk

files_sdk.read_timeout = 90
```

#### Initial Network Retry Delay

Seconds before the first retry of an API request, doubling for each later retry. The default
value is 0.1.

```python title="Example setting"
import files_sdk

files_sdk.initial_network_retry_delay = 1
```

#### Maximum Retry Delay

Maximum network retry delay in seconds. The default value is 2.

```python title="Example setting"
import files_sdk

files_sdk.max_network_retry_delay = 5
```

#### Maximum Network Retries

Maximum number of retries after the first attempt. The default value is 3; 0 sends each request
once.

```python title="Example setting"
import files_sdk

files_sdk.max_network_retries = 5
```

#### Source IP

Configure the local IP address from which to send requests.

```python title="Example setting"
import files_sdk

files_sdk.source_ip = '10.1.2.3'
```

## Clients

A `files_sdk.Client` has its own credentials, settings and connections. Each of its resources,
such as `client.user` or `client.file`, has the operations of the module of the same name, and
every object and list they return keeps using that client. A client never reads the module-level
settings, such as `files_sdk.set_api_key()`, so several clients, for different sites or users,
can work side by side.

Use a client as a context manager, or call `close()` when you are done with it. Closing stops its
operations in progress and closes its connections. The objects it returned keep their data, but
can no longer send requests. Closing a client never logs out a session.

`client.user.new(attributes)` makes an unsaved object whose `save()` uses the client.

A record's `update()` and `save()` change that object in place and return `None`. Read the updated attributes from the same object. The client's resource methods, such as `client.user.update(id, params)`, return the updated record.

```python title="Example Request"
import files_sdk

try:
  with files_sdk.Client(api_key="YOUR_API_KEY") as client:
    user = client.user.find(1234)
    user.update({"name": "Pat"})  # Also through this client.
    for item in client.folder.list_for("reports").auto_paging_iter():
      print(item.path)
except files_sdk.error.NotAuthenticatedError as err:
  print(f"Authentication Error Occurred ({type(err).__name__}):", err)
except files_sdk.error.Error as err:
  print(f"Unknown Error Occurred ({type(err).__name__}):", err)
```

### Options for One Call

Every operation takes an `options` dictionary after its parameters, described by
`files_sdk.RequestOptions`. Options apply to that call and to the objects it returns. An option
that is left out, or set to `None`, is inherited from the client. Set it to `files_sdk.CLEAR` to
remove the inherited value instead, such as a client's workspace. `0` and `False` are real
values. An unknown option raises `InvalidParameterError` before anything is sent.

| Option | Meaning |
| --- | --- |
| `api_key`, `session_id`, `session` | The credential to use. `session` is a logged-in `files_sdk.Session`. |
| `workspace_id`, `language` | Sent with each API request. |
| `headers` | Extra headers for API requests, merged with the client's. |
| `source_ip` | The local address to send from. |
| `open_timeout`, `read_timeout`, `max_network_retries` | See [Retries and Timeouts](/python/overview/retries). |
| `request_timeout`, `deadline`, `cancel_token` | See [Cancellation and Deadlines](/python/overview/cancellation). |
| `region_policy` | `"automatic"` or `"disabled"`. See [Regional Relocation](/python/overview/regional-relocation). |
| `client` | For a module-level function, the client to run it with. |

An API key given for a call is used instead of an inherited session, and a session instead of an
inherited API key. When a client or the module settings have both, the API key is used, unless
the call clears it with `CLEAR`. An empty string for `api_key` or `session_id` is treated as
left out.

```python title="Example Request"
import files_sdk

try:
  client = files_sdk.Client(api_key="YOUR_API_KEY", workspace_id=5)
  session = client.session.create({"username": "USERNAME", "password": "PASSWORD"})

  # As that session, in no workspace.
  client.folder.list_for("", {}, {
    "session": session,
    "workspace_id": files_sdk.CLEAR,
  })
except files_sdk.error.NotAuthenticatedError as err:
  print(f"Authentication Error Occurred ({type(err).__name__}):", err)
except files_sdk.error.Error as err:
  print(f"Unknown Error Occurred ({type(err).__name__}):", err)
```

### Module-Level Functions

The module-level functions, such as `files_sdk.user.find()`, use the module settings as they are
when each call starts, and the objects they return keep those settings. Changing a setting
later affects only later calls. `files_sdk.close()` closes the connections the module-level
functions share. Their objects can no longer send requests, and the next call opens new
connections.

### Your Own Requests Session

Pass a `requests.Session` as `http_session` to send every request through it, API and file
transfers alike, with its adapters, proxies, certificates and hooks. The client never closes
it or changes its adapters. Configure proxies, TLS and source addresses on the session itself;
the client refuses its own `verify`, `cert`, `proxies`, `trust_env` and `source_ip` settings with
one.

Requests keeps the session's cookie jar up to date as it would for any request. A session the
client creates for itself keeps no cookies that servers set, so nothing from one request's
credentials carries over to the next. Requests does
not promise that a session is safe to share between threads.

Only the connections a client creates itself can be interrupted, so with your own session a
cancelled or timed-out operation stops when its request returns or times out.

The SDK never sends a request that may have changed something again once it may have reached
Files.com, but an adapter that retries by itself (a `max_retries` other than 0) can, without the
SDK knowing. Uploads refuse to start through such an adapter, since it could complete an upload
twice; for other requests, mount one only if its retries suit them.

```python title="Example Request"
import requests
import files_sdk

try:
  session = requests.Session()
  session.proxies = {"https": "http://proxy.example.com:3128"}
  client = files_sdk.Client(api_key="YOUR_API_KEY", http_session=session)
except files_sdk.error.NotAuthenticatedError as err:
  print(f"Authentication Error Occurred ({type(err).__name__}):", err)
except files_sdk.error.Error as err:
  print(f"Unknown Error Occurred ({type(err).__name__}):", err)
```

### Threads

A client can be used from several threads at once. Each request uses its own connection from the
client's pool, and connections are reused across calls.

Calling `close()` from inside one of the client's own requests, such as from the stream a
download writes to, raises `RuntimeError` instead of waiting for itself.

## Sort and Filter

Several of the Files.com API resources have list operations that return multiple instances of the
resource. The List operations can be sorted and filtered.

### Sorting

To sort the returned data, pass in the ```sort_by``` method argument.

Each resource supports a unique set of valid sort fields and can only be sorted by one field at a
time.

The argument value is a Python dictionary that has a key of the resource field name sort on and a
value of either ```"asc"``` or ```"desc"``` to specify the sort order.

#### Special note about the List Folder Endpoint

For historical reasons, and to maintain compatibility
with a variety of other cloud-based MFT and EFSS services, Folders will always be listed before Files
when listing a Folder.  This applies regardless of the sorting parameters you provide.  These *will* be
used, after the initial sort application of Folders before Files.

```python title="Sort Example"
import files_sdk

try:
  # users sorted by username
  users = files_sdk.user.list({
    "sort_by": { "username": "asc" }
  })
  for user in users.auto_paging_iter():
    print(user.username)
except files_sdk.error.NotAuthenticatedError as err:
  print(f"Authentication Error Occurred ({type(err).__name__}):", err)
except files_sdk.error.Error as err:
  print(f"Unknown Error Occurred ({type(err).__name__}):", err)
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
import files_sdk

try:
  # non admin users
  users = files_sdk.user.list({
    "filter": { "not_site_admin": True }
  })
  for user in users.auto_paging_iter():
    print(user.username)
except files_sdk.error.NotAuthenticatedError as err:
  print(f"Authentication Error Occurred ({type(err).__name__}):", err)
except files_sdk.error.Error as err:
  print(f"Unknown Error Occurred ({type(err).__name__}):", err)
```

```python title="Range Filter Example"
import files_sdk

try:
  # users who have logged in on or after 2024-01-01
  users = files_sdk.user.list({
    "filter_gteq": { "last_login_at": "2024-01-01" }
  })
  for user in users.auto_paging_iter():
    print(user.username)
except files_sdk.error.NotAuthenticatedError as err:
  print(f"Authentication Error Occurred ({type(err).__name__}):", err)
except files_sdk.error.Error as err:
  print(f"Unknown Error Occurred ({type(err).__name__}):", err)
```

```python title="Pattern Filter Example"
import files_sdk

try:
  # users whose usernames start with 'test'
  users = files_sdk.user.list({
    "filter_prefix": { "username": "test" }
  })
  for user in users.auto_paging_iter():
    print(user.username)
except files_sdk.error.NotAuthenticatedError as err:
  print(f"Authentication Error Occurred ({type(err).__name__}):", err)
except files_sdk.error.Error as err:
  print(f"Unknown Error Occurred ({type(err).__name__}):", err)
```

```python title="Combination Filter with Sort Example"
import files_sdk

try:
  # users whose usernames start with 'test' and are not admins
  users = files_sdk.user.list({
    "filter_prefix": { "username": "test" },
    "filter": { "not_site_admin": True },
    "sort_by": { "username": "asc" }
  })
  for user in users.auto_paging_iter():
    print(user.username)
except files_sdk.error.NotAuthenticatedError as err:
  print(f"Authentication Error Occurred ({type(err).__name__}):", err)
except files_sdk.error.Error as err:
  print(f"Unknown Error Occurred ({type(err).__name__}):", err)
```

## Paths

Files.com preserves the spelling of file and folder paths while comparing them using shared case and Unicode rules. Use the SDK comparison helpers when matching paths locally.
<div></div>

### Capitalization

Files.com uses case-insensitive path matching based on its fixed Unicode comparison map.

For example, the following paths have the same comparison key:

| Path Variant                          | Comparison Key              |
|---------------------------------------|------------------------------|
| `Documents/Reports/Q1.pdf`            | `documents/reports/q1.pdf`  |
| `documents/reports/q1.PDF`            | `documents/reports/q1.pdf`  |
| `DOCUMENTS/REPORTS/Q1.PDF`            | `documents/reports/q1.pdf`  |

This behavior applies across:
- API requests
- Folder and file lookup operations
- Automations and workflows

See also: [Case Sensitivity Documentation](https://www.files.com/docs/files-and-folders/case-sensitivity/)

The `path_util.is_same` function in the Files.com SDK is designed to help you determine if two paths on
your native file system would be considered the same on Files.com. This is particularly important
when handling errors related to duplicate file names and when developing tools for folder
synchronization.

```python title="Compare Case-Insensitive Files and Paths"
import files_sdk

if files_sdk.path_util.is_same("Fïłèńämê.Txt", "filename.txt"):
    print("Paths are the same")
```

### Slashes

Use `/` between folder and file names, without leading or trailing slashes. SDK normalization helpers convert backslashes to `/`, remove duplicate separators, and discard exact `.` and `..` components. Discarding `..` leaves the preceding folder name intact.

| Input | Normalized path |
|-------|-----------------|
| `folder/subfolder/file.txt` | `folder/subfolder/file.txt` |
| `/folder/subfolder/file.txt` | `folder/subfolder/file.txt` |
| `folder/subfolder/file.txt/` | `folder/subfolder/file.txt` |
| `//folder//file.txt` | `folder/file.txt` |
| `folder/../file.txt` | `folder/file.txt` |

<div></div>

### Unicode and Path Comparison

Files.com compares paths using a fixed mapping shared by the server and SDKs. It treats case and many accent differences as equivalent: `Résumé.txt` and `resume.txt` identify the same file, as do `q` followed by a combining acute accent and `q`. The mapping also handles other equivalences, such as Hiragana and Katakana. Lowercasing or applying a standard Unicode normalization form alone does not reproduce these rules.

SDK comparison helpers normalize path separators and dot segments, then apply the bundled [versioned comparison map](https://github.com/Files-com/files-sdk-javascript/blob/master/shared/path_comparison.json). The [shared examples](https://github.com/Files-com/files-sdk-javascript/blob/master/shared/comparison_examples.json) give exact comparison results for integrations that implement their own matching. The map uses hexadecimal Unicode scalar values as keys: a missing entry preserves the character, an empty replacement removes it, and other replacements may contain several characters. Apply each replacement once without normalizing or lowercasing the result again.

Use comparison results only for matching. Send the original path spelling in API requests and preserve it for display and local filenames; comparison results can have a different spelling or length.

Trailing whitespace is significant for comparison. `report.txt` and `report.txt ` are different file paths, and SDK helpers preserve spaces, tabs, and newlines. Folder names cannot end in whitespace. See [Unicode Normalization](https://www.files.com/docs/files-and-folders/file-system-semantics/unicode-normalization) for the complete path rules.

<div></div>

## Workspaces

A Workspace groups files, users, groups, Partners, integrations, and workflows within a Files.com Site. An integration can provision a Workspace for a department or project and delegate its operation to a team without making that team Site Administrators. Every Site has a Default Workspace, with ID `0`; additional Workspaces have their own IDs and root folders.

Account membership, request context, and permission grants serve different purposes. Creating an account in a Workspace determines where it belongs. Selecting a Workspace determines which resources a request operates on. A permission grant determines what the caller can do there. Selecting a Workspace never grants access to it.

### Accounts and Administrative Access

A user's or group's `workspace_id` identifies the Workspace the account belongs to. Accounts belonging to a Custom Workspace stay within it. Default Workspace users and groups can receive permissions in one or more Custom Workspaces while keeping their existing accounts in Workspace `0`.

| Account | Workspace Administrator assignment | Scope |
| --- | --- | --- |
| User belonging to a Custom Workspace | Set the user's `workspace_admin` to `true`. | That user's own Custom Workspace. |
| Default Workspace user | Create an `admin` Permission for the user on a Custom Workspace's root folder. | Each Custom Workspace with a root grant. |
| Default Workspace group | Create an `admin` Permission for the group on a Custom Workspace's root folder. | Every member inherits administration of each Workspace with a root grant. |

`workspace_admin` is not a summary of a user's effective administrative access. A Default Workspace user can administer a Custom Workspace through a direct or group root grant while their `workspace_admin` remains `false`. Groups have no `workspace_admin` field. See [Users](https://developers.files.com/python/resources/user-accounts/users) and [Groups](https://developers.files.com/python/resources/user-accounts/groups) for account fields.

An `admin` grant on the **Custom Workspace root** provides full Workspace Administrator authority over its files, users, groups, Partners, workflows, and integrations. An `admin` grant on a subfolder provides Folder Admin authority over that folder and its descendants; it does not provide Workspace administration. Other permission levels provide their corresponding folder access without Workspace administration. [Permissions](https://developers.files.com/python/resources/user-accounts/permissions) defines the levels.

Site Administrators manage cross-Workspace assignments to Default Workspace accounts. Workspace Administrators manage accounts and permissions within their own scope. Site Administrators retain access to every Workspace; adding a Workspace grant does not narrow Site Administrator authority. The [product documentation](https://www.files.com/docs/workspaces/workspace-administrators) explains the administrator's operational scope and site-wide controls.

### Request Context and API Keys

You can include the `X-Files-Workspace-Id` REST header to select a Workspace for a request. SDK request options and CLI configuration send that same selection. When a Workspace is selected, Workspace-scoped resources are listed, created, and changed within that context, and ordinary paths are relative to its root.

A resource's `workspace_id` request field describes the resource's Workspace membership. It is separate from the SDK's Workspace request option or REST header. Creating a Workspace-scoped resource in a Custom Workspace defaults its `workspace_id` to the selected Workspace; a mismatching membership value is rejected with `not-authorized/insufficient-permission-for-params`.

Selecting another Workspace with an API key requires a **Full Access key created in the Default Workspace**. A user key follows that user's current access, including group permissions. A site-wide Full Access key created in the Default Workspace has Site Administrator authority in every Workspace. A Files Only key stays in its creation Workspace, even if its user has cross-Workspace access. Any key created in a Custom Workspace stays within that Workspace. Selecting another context with these confined keys is rejected with `bad-request/invalid-workspace-id-header`.

An account belonging to a Custom Workspace is scoped there when it authenticates normally. For a Default Workspace user, explicitly select the intended Workspace for an integration rather than relying on an interactive login preference. [API Keys](https://developers.files.com/python/resources/developers/api-keys) and [Authentication](https://developers.files.com/python/overview/authentication) cover credentials.

The Files.com Python SDK supports workspace scoping by using the `files_sdk.set_workspace_id` configuration method. Scope a single request by passing `workspace_id` in the request options.

The adjacent scoping example uses a credential authorized for the selected Workspace. A group member uses their own Full Access user key from the Default Workspace; the Site Administrator credential used to assign the grant is not needed for their day-to-day work.

```python title="Example Request"
import files_sdk

files_sdk.set_workspace_id(123)

files_sdk.folder.list_for("", {}, {"workspace_id": 456})
```

### Delegating a Workspace to an Existing Group

An operations team already represented by a Default Workspace group can administer a Custom Workspace through one root Permission. The group and its members stay in the Default Workspace, so the same team can receive different access in other Workspaces.

First retrieve the target [Workspace](https://developers.files.com/python/resources/settings/workspaces) and [Group](https://developers.files.com/python/resources/user-accounts/groups) IDs as a Site Administrator in Workspace `0`. The examples use Workspace `123`, group `456`, and member user `789`; replace them with your own IDs. Confirm that the group belongs to Workspace `0` and that the intended user is a member.

Create the Permission using a Default Workspace Full Access site-wide key or a Full Access user key belonging to a Site Administrator. Keep the request context at `0` and use the qualified root path `_/Workspaces/123`. Set `group_id` to the group's ID, `permission` to `admin`, and `recursive` to `true`. Save the returned Permission `id` for later removal. For an individual Default Workspace user, use `user_id` instead of `group_id`.

For a Default Workspace group, a Site Administrator can also select Workspace `123` and use an empty `path` to grant access to its root. The qualified path in Workspace `0` works for both Default Workspace users and groups and keeps the account scope and target Workspace explicit. Appending a subfolder to the path would grant Folder Admin access instead of Workspace Administrator authority.

After the grant, make a request as the member, using their own credential with Workspace `123` selected, such as listing that Workspace's root folder. That member can work with the Workspace's files and perform Workspace Administrator operations, such as managing its users, Partners, and integrations. A Site Administrator's successful request does not establish that the member has the intended access.

```python title="Grant group administration"
import files_sdk

files_sdk.set_workspace_id(0)
grant = files_sdk.permission.create({
    "path": "_/Workspaces/123",
    "group_id": 456,
    "permission": "admin",
    "recursive": True,
}, {"workspace_id": 0})
print(grant.id)
```

### Permission Inspection and Removal

List the member's Permissions with `user_id` and `include_groups=true` to include grants inherited through group membership. Listing only direct user grants can miss the Permission that provides Workspace administration. In Workspace `0`, the Custom Workspace root appears as `_/Workspaces/123`; in Workspace `123`, paths are relative to that root. Inspect the root path and `permission=admin`, rather than treating the user's `workspace_admin` field as their effective administrative access.

Permission lists show individual grants, rather than a single flag for effective administrative access. Membership in several groups combines their access. A Permission using `group_ids` instead of `group_id` requires membership in all the specified groups; it is not a shorthand for assigning the same grant to several independent groups.

Removing a member ends access received through that group. Deleting the root Permission ends the group's Workspace Administrator grant for every member. These changes leave independent direct and other group grants in place, so review all applicable grants when withdrawing access. Default Workspace user API keys follow those permission changes without being recreated.

Group membership maintained through SCIM follows the same rule. A Group Admin allowed to add members can give those users the group's existing Workspace Administrator access. Choose who manages the group with that authority in mind.

Delete the Permission by its returned `id` as the Site Administrator in Workspace `0`. The removal examples use Permission ID `9001`; replace it with the ID returned by your create request. Permissions are created and deleted, rather than updated in place. If narrower folder access is still needed, assign it explicitly; deleting a broad grant does not restore narrower grants it previously replaced.

```python title="Inspect member grants and remove the group grant"
for item in files_sdk.permission.list(
    {"user_id": "789", "include_groups": True}, {"workspace_id": 0}
):
    print(item.path, item.permission, item.group_id)
files_sdk.permission.delete(9001, {}, {"workspace_id": 0})
```

## Foreign Language Support

The Files.com Python SDK supports localized responses by using the `files_sdk.set_language` configuration method.
When configured, this guides the API in selecting a preferred language for applicable response content.

Language support currently applies to select human-facing fields only, such as notification messages
and error descriptions.

If the specified language is not supported or the value is omitted, the API defaults to English.

```shell title="Example Request"
import files_sdk

files_sdk.set_language('es')
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
import files_sdk

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

```text title="Example SDK Exception Class Inheritance Structure"
files_sdk.error.APIConnectionError -> files_sdk.error.Error -> Exception
```
##### SDK Exception Classes

| Error Class Name| Description |
| --------------- | ------------ |
| `APIConnectionError`| The Files.com API cannot be reached, or its response is malformed or unreliable |
| `DeadlineExceededError`| An `APIConnectionError`: the operation ran out of the time its `request_timeout` or `deadline` allowed |
| `OperationCancelledError`| The operation's `cancel_token` was cancelled |
| `ClientClosedError`| An `OperationCancelledError`: the operation's client was closed |
| `AuthenticationError`| Not enough authentication information has been provided |
| `InvalidRequestError`| The SDK refused to go on, such as for a file that changed while it transferred, a checkpoint it cannot use, or a remote file whose upload already failed |
| `InvalidParameterError`| An `InvalidRequestError`: a passed in parameter or option is invalid |
| `MissingParameterError`| An `InvalidRequestError`: a method parameter is missing |
| `TransferPausedError`| A transfer stopped because its `pause_token` was paused; its `checkpoint` resumes it |
| `FileMigrationError`| A copy or move that was waited for failed or was cancelled; its `migration`, when Files.com made one, says why |
| `NotImplementedError`| The called method has not be implemented by the SDK |

`APIConnectionError`, `DeadlineExceededError` and `OperationCancelledError` have `phase`, the step
that failed, and `remote_outcome_unknown`, which is `True` when the request may already have
reached Files.com.

Local file problems raise Python's own `OSError` subclasses, such as `files_sdk.localfs.AccessNotKept`
when a download cannot keep a replaced file's owner, group or access control list. A remote file
opened with `files_sdk.open()` raises `io.UnsupportedOperation` for what it cannot do, such as
`seek()`, as Python's own files do.

#### API Errors

API errors are errors returned by the Files.com API.  Each exception class inherits from an error group base class.
The error group base class indicates a particular type of error.

```text title="Example API Exception Class Inheritance Structure"
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
|`DestinationSiteMismatchError`|  `BadRequestError` |
|`DoesNotSupportSortingError`|  `BadRequestError` |
|`FolderMustNotBeAFileError`|  `BadRequestError` |
|`FoldersNotAllowedError`|  `BadRequestError` |
|`InternalGeneralErrorError`|  `BadRequestError` |
|`InvalidBodyError`|  `BadRequestError` |
|`InvalidCursorError`|  `BadRequestError` |
|`InvalidCursorTypeForSortError`|  `BadRequestError` |
|`InvalidEtagsError`|  `BadRequestError` |
|`InvalidFilterAliasCombinationError`|  `BadRequestError` |
|`InvalidFilterFieldError`|  `BadRequestError` |
|`InvalidFilterParamError`|  `BadRequestError` |
|`InvalidFilterParamFormatError`|  `BadRequestError` |
|`InvalidFilterParamValueError`|  `BadRequestError` |
|`InvalidInputEncodingError`|  `BadRequestError` |
|`InvalidInterfaceError`|  `BadRequestError` |
|`InvalidOauthProviderError`|  `BadRequestError` |
|`InvalidPathError`|  `BadRequestError` |
|`InvalidReturnToUrlError`|  `BadRequestError` |
|`InvalidSearchQueryError`|  `BadRequestError` |
|`InvalidSortFieldError`|  `BadRequestError` |
|`InvalidSortFilterCombinationError`|  `BadRequestError` |
|`InvalidUploadOffsetError`|  `BadRequestError` |
|`InvalidUploadPartGapError`|  `BadRequestError` |
|`InvalidUploadPartSizeError`|  `BadRequestError` |
|`InvalidWorkspaceIdHeaderError`|  `BadRequestError` |
|`MethodNotAllowedError`|  `BadRequestError` |
|`MultipleSortParamsNotAllowedError`|  `BadRequestError` |
|`NoValidInputParamsError`|  `BadRequestError` |
|`OffsetUploadNotAllowedWithMalwareScanningError`|  `BadRequestError` |
|`PartNumberTooLargeError`|  `BadRequestError` |
|`PathCannotHaveTrailingWhitespaceError`|  `BadRequestError` |
|`ReauthenticationNeededFieldsError`|  `BadRequestError` |
|`RequestBodyTooLargeError`|  `BadRequestError` |
|`RequestParamsContainInvalidCharacterError`|  `BadRequestError` |
|`RequestParamsInvalidError`|  `BadRequestError` |
|`RequestParamsRequiredError`|  `BadRequestError` |
|`SearchAllOnChildPathError`|  `BadRequestError` |
|`UnrecognizedSortIndexError`|  `BadRequestError` |
|`UnsupportedCurrencyError`|  `BadRequestError` |
|`UnsupportedHttpResponseFormatError`|  `BadRequestError` |
|`UnsupportedMediaTypeError`|  `BadRequestError` |
|`UserIdInvalidError`|  `BadRequestError` |
|`UserIdOnUserEndpointError`|  `BadRequestError` |
|`UserRequiredError`|  `BadRequestError` |
|`AdditionalAuthenticationRequiredError`|  `NotAuthenticatedError` |
|`ApiKeySessionsNotSupportedError`|  `NotAuthenticatedError` |
|`AuthenticationRequiredError`|  `NotAuthenticatedError` |
|`BundleRegistrationCodeFailedError`|  `NotAuthenticatedError` |
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
|`ApiKeyOnlyForFileOperationsError`|  `NotAuthorizedError` |
|`ApiKeyOnlyForMobileAppError`|  `NotAuthorizedError` |
|`ApiKeyOnlyForOfficeIntegrationError`|  `NotAuthorizedError` |
|`BillingInformationHiddenError`|  `NotAuthorizedError` |
|`BillingPermissionRequiredError`|  `NotAuthorizedError` |
|`BundleMaximumUsesReachedError`|  `NotAuthorizedError` |
|`BundlePermissionRequiredError`|  `NotAuthorizedError` |
|`CannotAdministerHigherLevelUserError`|  `NotAuthorizedError` |
|`CannotLoginWhileUsingKeyError`|  `NotAuthorizedError` |
|`CantActForOtherUserError`|  `NotAuthorizedError` |
|`ContactAdminForPasswordChangeHelpError`|  `NotAuthorizedError` |
|`FilesAgentFailedAuthorizationError`|  `NotAuthorizedError` |
|`FolderAdminOrBillingPermissionRequiredError`|  `NotAuthorizedError` |
|`FolderAdminPermissionRequiredError`|  `NotAuthorizedError` |
|`FullPermissionRequiredError`|  `NotAuthorizedError` |
|`HistoryPermissionRequiredError`|  `NotAuthorizedError` |
|`InAppAiAssistantUnavailableError`|  `NotAuthorizedError` |
|`InsufficientPermissionForParamsError`|  `NotAuthorizedError` |
|`InsufficientPermissionForSiteError`|  `NotAuthorizedError` |
|`MoverAccessDeniedError`|  `NotAuthorizedError` |
|`MoverPackageRequiredError`|  `NotAuthorizedError` |
|`MustAuthenticateWithApiKeyError`|  `NotAuthorizedError` |
|`NeedAdminPermissionForInboxError`|  `NotAuthorizedError` |
|`NonAdminsMustQueryByFolderOrPathError`|  `NotAuthorizedError` |
|`NotAllowedToCreateBundleError`|  `NotAuthorizedError` |
|`NotEnqueuableSyncError`|  `NotAuthorizedError` |
|`PasswordChangeNotRequiredError`|  `NotAuthorizedError` |
|`PasswordChangeRequiredError`|  `NotAuthorizedError` |
|`PaymentMethodErrorError`|  `NotAuthorizedError` |
|`PreviewOnlyPermissionCannotDownloadError`|  `NotAuthorizedError` |
|`ReadOnlySessionError`|  `NotAuthorizedError` |
|`ReadPermissionRequiredError`|  `NotAuthorizedError` |
|`ReauthenticationFailedError`|  `NotAuthorizedError` |
|`ReauthenticationFailedFinalError`|  `NotAuthorizedError` |
|`ReauthenticationNeededActionError`|  `NotAuthorizedError` |
|`RecaptchaFailedError`|  `NotAuthorizedError` |
|`RemoteDesktopDebugLoggingDisabledError`|  `NotAuthorizedError` |
|`RootFolderBehaviorSiteAdminRequiredError`|  `NotAuthorizedError` |
|`RootFolderBehaviorSkipSiteAdminRequiredError`|  `NotAuthorizedError` |
|`SelfManagedRequiredError`|  `NotAuthorizedError` |
|`SiteAdminOrPartnerAdminPermissionRequiredError`|  `NotAuthorizedError` |
|`SiteAdminOrWorkspaceAdminOrFolderAdminPermissionRequiredError`|  `NotAuthorizedError` |
|`SiteAdminOrWorkspaceAdminOrPartnerAdminOrFolderAdminPermissionRequiredError`|  `NotAuthorizedError` |
|`SiteAdminOrWorkspaceAdminOrPartnerAdminPermissionRequiredError`|  `NotAuthorizedError` |
|`SiteAdminOrWorkspaceAdminPermissionRequiredError`|  `NotAuthorizedError` |
|`SiteAdminRequiredError`|  `NotAuthorizedError` |
|`SiteFilesAreImmutableError`|  `NotAuthorizedError` |
|`TwoFactorAuthenticationRequiredError`|  `NotAuthorizedError` |
|`UserIdWithoutSiteAdminError`|  `NotAuthorizedError` |
|`WriteAndBundlePermissionRequiredError`|  `NotAuthorizedError` |
|`WritePermissionRequiredError`|  `NotAuthorizedError` |
|`ApiKeyNotFoundError`|  `NotFoundError` |
|`BundlePathNotFoundError`|  `NotFoundError` |
|`BundleRegistrationNotFoundError`|  `NotFoundError` |
|`CodeNotFoundError`|  `NotFoundError` |
|`FileNotFoundError`|  `NotFoundError` |
|`FileUploadNotFoundError`|  `NotFoundError` |
|`GroupNotFoundError`|  `NotFoundError` |
|`InboxNotFoundError`|  `NotFoundError` |
|`NestedNotFoundError`|  `NotFoundError` |
|`PlanNotFoundError`|  `NotFoundError` |
|`SiteNotFoundError`|  `NotFoundError` |
|`UserNotFoundError`|  `NotFoundError` |
|`AgentPushUpdateBlockedError`|  `ProcessingFailureError` |
|`AgentUnavailableError`|  `ProcessingFailureError` |
|`AiTaskCannotBeRunManuallyError`|  `ProcessingFailureError` |
|`AlreadyCompletedError`|  `ProcessingFailureError` |
|`AutomationCannotBeRunManuallyError`|  `ProcessingFailureError` |
|`BehaviorNotAllowedOnRemoteServerError`|  `ProcessingFailureError` |
|`BufferedUploadDisabledForThisDestinationError`|  `ProcessingFailureError` |
|`BundleOnlyAllowsPreviewsError`|  `ProcessingFailureError` |
|`BundleOperationRequiresSubfolderError`|  `ProcessingFailureError` |
|`ConfigurationLockedPathError`|  `ProcessingFailureError` |
|`CouldNotCreateParentError`|  `ProcessingFailureError` |
|`DestinationExistsError`|  `ProcessingFailureError` |
|`DestinationFolderLimitedError`|  `ProcessingFailureError` |
|`DestinationParentConflictError`|  `ProcessingFailureError` |
|`DestinationParentDoesNotExistError`|  `ProcessingFailureError` |
|`ExceededRuntimeLimitError`|  `ProcessingFailureError` |
|`ExpectationAlreadyHasOpenWindowError`|  `ProcessingFailureError` |
|`ExpectationNotManualTriggerError`|  `ProcessingFailureError` |
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
|`InvalidSiteError`|  `ProcessingFailureError` |
|`InvalidZipFileError`|  `ProcessingFailureError` |
|`MetadataNotSupportedOnRemotesError`|  `ProcessingFailureError` |
|`ModelSaveErrorError`|  `ProcessingFailureError` |
|`MultipleProcessingErrorsError`|  `ProcessingFailureError` |
|`PathTooLongError`|  `ProcessingFailureError` |
|`RecipientAlreadySharedError`|  `ProcessingFailureError` |
|`RemoteEntryReadOnlyError`|  `ProcessingFailureError` |
|`RemoteServerErrorError`|  `ProcessingFailureError` |
|`ResourceBelongsToParentSiteError`|  `ProcessingFailureError` |
|`ResourceLockedError`|  `ProcessingFailureError` |
|`SubfolderLockedError`|  `ProcessingFailureError` |
|`SyncInProgressError`|  `ProcessingFailureError` |
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
|`AutomationsUnavailableError`|  `ServiceUnavailableError` |
|`LockOperationBusyError`|  `ServiceUnavailableError` |
|`MigrationInProgressError`|  `ServiceUnavailableError` |
|`SearchUnavailableError`|  `ServiceUnavailableError` |
|`SiteDisabledError`|  `ServiceUnavailableError` |
|`UploadsUnavailableError`|  `ServiceUnavailableError` |
|`AccountAlreadyExistsError`|  `SiteConfigurationError` |
|`AccountOverdueError`|  `SiteConfigurationError` |
|`NoAccountForSiteError`|  `SiteConfigurationError` |
|`SiteWasRemovedError`|  `SiteConfigurationError` |
|`TrialExpiredError`|  `SiteConfigurationError` |
|`TrialLockedError`|  `SiteConfigurationError` |
|`UserRequestsEnabledRequiredError`|  `SiteConfigurationError` |

## Retries and Timeouts

`max_network_retries` defaults to 3 retries after the first attempt; 0 disables SDK retries. Reads and retryable
transfer requests can retry temporary failures. Requests that change data are treated more cautiously, as below.

`open_timeout` defaults to 30 seconds for connecting to each resolved address; `read_timeout` defaults to 80 seconds
for each response read. These limit stalls, not total operation duration. Use `request_timeout` or `deadline` for
an overall limit; see [Cancellation and Deadlines](/python/overview/cancellation).

```python title="Choosing Retry and Timeout Settings"
import files_sdk

try:
  with files_sdk.Client(api_key="YOUR_API_KEY", read_timeout=300, max_network_retries=5) as client:
    client.group.create({"name": "Auditors"}, {"max_network_retries": 0})
except files_sdk.error.NotAuthenticatedError as err:
  print(f"Authentication Error Occurred ({type(err).__name__}):", err)
except files_sdk.error.Error as err:
  print(f"Unknown Error Occurred ({type(err).__name__}):", err)
```

### Sending a Request Again

| Request | Retry behavior |
| --- | --- |
| Connection failure before sending | Can retry within the budget. |
| Read, such as `GET` | Also retries timeouts, lost answers, HTTP 429 and 5xx other than 501. |
| Request that may change data | Not replayed once it may have reached Files.com, including after an error response. |
| Upload part or part-URL request | Repeatable requests retry within the transfer rules; accepted parts are not replayed. |
| Download | Bound ranges retry individually; a whole response restarts only while the destination can restart. Already-written stream bytes are never replayed. |

Retries send the same body, including attachments. A mutating request can take effect before an error, even HTTP
429 or 503. `remote_outcome_unknown = True` on `APIConnectionError` or the API error means **check the outcome before
repeating the change**. A site-disabled response (HTTP 422, `service-unavailable/site-disabled`) is the specific
exception: it precedes the change and has a false flag. Do not treat other error statuses or bodies as proof that
nothing happened.

[Regional Relocation](/python/overview/regional-relocation) consumes one retry. TLS certificate failures,
unsupported URLs, excessive redirects, caller-code exceptions and cancellation are not retried. A custom
`http_session` adapter performing retries can still replay requests outside the SDK's policy; see
[Clients](/python/overview/clients).

| Destination | Wait before retry |
| --- | --- |
| Files.com API | 0.1, 0.2, 0.4 seconds by default, doubling from `initial_network_retry_delay` to `max_network_retry_delay` (2 seconds). |
| File transfer after HTTP 429 or 503 | The `Retry-After` delay, up to 60 seconds at a time, or no wait without it. |
| Other retryable transfer failure | 0.1 seconds. |

Retries are logged at INFO with the reason and wait. [Uploads](/python/overview/uploads) and
[Downloads](/python/overview/downloads) describe completion ambiguity and transfer-specific recovery.

### Redirects, Credentials and Proxies

`max_redirects` defaults to 30 per request. API credentials, Workspace and extra headers stay with the configured
API origin. After a redirect changes scheme, host or port, only generic headers remain, even if it later returns.
Signed transfer requests carry none of those API credentials; version-bound downloads have stricter redirect rules.

The SDK never uses `.netrc` credentials. It honors `HTTP_PROXY`, `HTTPS_PROXY`, `NO_PROXY`, `REQUESTS_CA_BUNDLE` and
`CURL_CA_BUNDLE` unless `trust_env=False`. `proxies`, `verify` and `cert` behave as in `requests.Session`.
Certificates are verified unless you disable verification.

## Cancellation and Deadlines

Use one of these options to stop an operation. Without one, it has no overall time limit.

| Option | Limit |
| --- | --- |
| `cancel_token` | A `files_sdk.CancellationToken`; call `cancel()` from another thread. |
| `request_timeout` | Seconds from the operation's start; a client setting applies to each call. |
| `deadline` | An absolute `time.monotonic()` value. |

If both time limits are set, the earlier one applies.

One operation is one call, with its retries, redirects and any regional relocation. A list's
later pages belong to the operation that fetched the first page, so its deadline covers them, and
time spent between pages counts. An upload or download is one operation from its first request
to its last, and so is a file from `open()`, through `close()`; the SDK checks the operation
before it replaces a download's destination or reads more of an upload's source. Later operations
of the objects an operation returned get their own limits.

```python title="Example Request"
import threading
import files_sdk

try:
  token = files_sdk.CancellationToken()
  threading.Timer(10, token.cancel).start()

  files_sdk.upload_file("big.iso", "backups/big.iso", {
    "cancel_token": token,
    "request_timeout": 3600,
  })
except files_sdk.error.NotAuthenticatedError as err:
  print(f"Authentication Error Occurred ({type(err).__name__}):", err)
except files_sdk.error.Error as err:
  print(f"Unknown Error Occurred ({type(err).__name__}):", err)
```

### What Stops at Once

A request waiting for the network on a connection the client created stops at once: while
setting up TLS or a proxy tunnel, sending a request or file part, or waiting for or reading a
response, even one that trickles in slowly. Its connection is closed rather than reused. Waits
between retries stop at once too.

Some waits cannot be interrupted, and the operation stops when they end:

* Looking up a host name.
* Opening a TCP connection, which waits up to `open_timeout` for each address the host name
  resolves to, so a host with several unreachable addresses can take longer in all.
* Your own code, such as a stream an upload reads from or a download writes to.
* Requests through a session you passed as `http_session`, or through a SOCKS proxy, which stop
  when their own timeouts, shortened to the deadline, return.

### Errors

A cancelled operation raises `files_sdk.error.OperationCancelledError`. Its subclass
`ClientClosedError` means the client was closed, before or during the operation. An operation that
runs out of time raises `DeadlineExceededError`, an `APIConnectionError`.

Their `phase` says what the operation was doing, such as `"response"` while waiting for a
response or `"retry wait"`. `remote_outcome_unknown` is `True` when the request may already have
reached Files.com, so what it asked for may have happened. Cancelling does not undo work Files.com
has already done. If a request through your own `http_session` finishes after the operation was
cancelled, the operation still raises, with the unused response in the error's `response`.

```python title="Example Request"
import files_sdk
from files_sdk.error import OperationCancelledError

try:
  files_sdk.file.download_file("reports/q3.csv", "q3.csv", {"request_timeout": 60})
except files_sdk.error.DeadlineExceededError as error:
  print("Timed out while", error.phase)
except OperationCancelledError:
  print("Cancelled")
```

## Regional Relocation

A site can require connections through one host, such as its custom domain or a regional
subdomain. Files.com answers a request that reaches another host with HTTP 403. Its
`not-authenticated/lockout-region-mismatch` error names the host in `data.host` or the
`X-Files-Host` header; a supplied `data.host` takes precedence. The SDK also recognizes the
legacy plain-text HTTP 403 response starting exactly `You have connected to a URL` with
`X-Files-Host`. Both forms raise `LockoutRegionMismatchError` when relocation is refused.

The SDK then sends the operation to that host once, with the same request, when all of these
hold:

* The answer came straight from the operation's current API origin, over HTTPS with the certificate verified,
  not through a redirect or from file storage.
* The host is a DNS name, as a bare name or an `https://` origin without a path, on the default
  port, and not a local name such as `localhost` or an IP address.
* `region_policy` is `"automatic"`, the default, and the `region_handler`, if any, allows it.
* The request has a retry left. The move counts as one of its `max_network_retries`, like a retry
  after a failure, so with `0`, or once earlier failures have used them all, the operation raises
  the error instead.

The new host lasts for the rest of that operation, including a list's later pages and the objects
the operation returns. It never changes the client: its next operation starts at `base_url` again.
A second mismatch raises the error instead of moving again.

### Controlling Relocation

With `region_policy="disabled"`, for a client or a single call, the operation raises the
`LockoutRegionMismatchError`, retaining the response's data and headers.

A `region_handler` is called with a `files_sdk.RegionRelocation` whose `original_origin` and
`target_origin` are the hosts involved and whose `automatic` says whether the SDK would move on
its own. It returns `True` to allow that, `False` to raise the error instead, or an `https://`
origin to send the operation to, which it approves explicitly, even on another port. If it raises,
the operation stops with its exception.

During automatic handling, an iPaaS integration can save an approved `target_origin` in the
handler and use that address as `base_url` for later calls.

```python title="Example Request"
import files_sdk

try:
  def only_our_domains(relocation):
    return relocation.target_origin in ("https://files.example.com", "https://eu.files.example.com")

  client = files_sdk.Client(
    api_key="YOUR_API_KEY",
    base_url="https://files.example.com",
    region_handler=only_our_domains,
  )
except files_sdk.error.NotAuthenticatedError as err:
  print(f"Authentication Error Occurred ({type(err).__name__}):", err)
except files_sdk.error.Error as err:
  print(f"Unknown Error Occurred ({type(err).__name__}):", err)
```

### Local Development

A `base_url` over plain HTTP, or with certificate verification off, never relocates
automatically. To let a development server send the SDK to another, name the exact pair of
origins in `region_development_origins`.

```python title="Example Request"
import files_sdk

client = files_sdk.Client(
  api_key="YOUR_API_KEY",
  base_url="http://localhost:3000",
  region_development_origins=[("http://localhost:3000", "http://localhost:3001")],
)
```

## Pagination

Certain API operations return lists of objects. When the number of objects in the list is large,
the API will paginate the results.

The Files.com Python SDK provides multiple ways to paginate through lists of objects.

### Automatic Pagination

The `auto_paging_iter` method yields every item in the list, loading each following page only
when the items before it have been consumed. Stopping early, such as with `break`, requests no
further pages.

```python title="Example Request"
import files_sdk

try:
  for item in files_sdk.folder.list_for("remote/path/to/folder").auto_paging_iter():
    print(item.type, item.path)
except files_sdk.error.NotAuthenticatedError as err:
  print(f"Authentication Error Occurred ({type(err).__name__}):", err)
except files_sdk.error.Error as err:
  print(f"Unknown Error Occurred ({type(err).__name__}):", err)
```

### Manual Pagination

Iterating a list object yields the items on its current page. `has_next_page` reports whether
another page is available, and `load_next_page` replaces the current page with the next one.
After the last page, `load_next_page` makes no request and keeps the last page in place.

```python title="Example Request"
import files_sdk

try:
  list_obj = files_sdk.folder.list_for("remote/path/to/folder")

  while True:
    for item in list_obj:
      print(item.type, item.path)
    if not list_obj.has_next_page:
      break
    list_obj.load_next_page()
except files_sdk.error.NotAuthenticatedError as err:
  print(f"Authentication Error Occurred ({type(err).__name__}):", err)
except files_sdk.error.Error as err:
  print(f"Unknown Error Occurred ({type(err).__name__}):", err)
```

## Uploads

Uploads adapt automatically, so most applications need only their paths. When Files.com allows parallel parts,
the SDK adjusts how many it sends based on the connection, within your concurrency, memory and connection limits.
Server-required serial uploads and unspooled unknown-length streams remain serial.

`upload_file()` uploads a local file; `upload_stream()` uploads a binary stream. Both return the `File` created.
A file uses a separate handle for each part; a stream is read forward once. Keep the source unchanged until the
call finishes.

`cancel_token`, `request_timeout` and `deadline` cover the whole upload, including completion. See
[Cancellation and Deadlines](/python/overview/cancellation).

```python title="Uploading a File"
import files_sdk

try:
  with files_sdk.Client(api_key="YOUR_API_KEY") as client:
    file = client.file.upload_file("backups/big.iso", "archive/big.iso", params={"mkdir_parents": True})
    print(file.path, file.size)
except files_sdk.error.NotAuthenticatedError as err:
  print(f"Authentication Error Occurred ({type(err).__name__}):", err)
except files_sdk.error.Error as err:
  print(f"Unknown Error Occurred ({type(err).__name__}):", err)
```

### Streams

Streams are read from their current position, never sought, and left open after the uploaded bytes. Short reads
are accumulated; only an empty read means the end. Use a blocking binary stream.

| Choice | Behavior |
| --- | --- |
| `upload_stream(stream, destination, size)` | Reads exactly `size` bytes; an early end fails without completing. |
| Omit `size` | Sends parts serially until the stream ends. Eligible part sizes can grow within server limits. |
| `spool_limit` | Copies the full unknown-length stream to a bounded temporary file first, enabling parallel file-style upload. An oversized stream fails before any upload is sent. |
| `spool_directory` | Chooses the spool folder instead of the system temporary folder. The SDK removes its spool afterward. |

After a full part, one byte of look-ahead determines whether another is needed. An exact boundary can complete with
the maximum allowed parts; excess data raises `InvalidRequestError` without completing. Text streams and a
nonblocking `read()` returning `None` also fail before completion.

```python title="Uploading Part of a Stream"
import files_sdk

try:
  with open("report.csv", "rb") as source:
    source.seek(128)
    files_sdk.upload_stream(source, "reports/report.csv", 4096)
except files_sdk.error.NotAuthenticatedError as err:
  print(f"Authentication Error Occurred ({type(err).__name__}):", err)
except files_sdk.error.Error as err:
  print(f"Unknown Error Occurred ({type(err).__name__}):", err)
```

### Progress

Pass a `progress` function. It receives `files_sdk.UploadProgress` on the calling thread, at most four times a
second and once more after all parts arrive. If it raises, the upload stops its active parts and propagates the
exception. All bytes accepted does not establish upload completion; wait for the upload call to return.

| Field | Meaning |
| --- | --- |
| `bytes_committed` | Bytes in accepted parts, counted once. |
| `bytes_sent` | Network bytes, including retries. |
| `bytes_per_second` | Recent committed-byte rate. |
| `total_bytes` | Upload size. |

```python title="Following Upload Progress"
def report(progress):
  print(f"{progress.bytes_committed} of {progress.total_bytes} bytes")

file = files_sdk.upload_file("video.mp4", "media/video.mp4", progress=report)
```

### Failures

Parts retry with identical bytes under the [transfer retry rules](/python/overview/retries), only when Files.com
allows retries. Accepted parts are not sent again. Expiring addresses are renewed for the same part before use;
addresses refused as expired can be renewed up to twice. Ordinary refusals, including a 403 without an expiry
reason, fail. The SDK recognizes supplied expiry and supported AWS, Files.com, Google and Azure signing fields.

A permanent part failure stops the other parts, waits for them and raises the original error without completing.
For local files, size and modification time are checked around each read and before completion, plus status-change
time off Windows. A changed file raises `InvalidRequestError` instead of completing mixed content.

The final completion request is not replayed once it may have reached Files.com. A lost or error response can leave
`remote_outcome_unknown` set even though the file completed. Check the remote outcome before starting another
upload; [Pausing and Resuming](/python/overview/resuming) covers checkpoint recovery.

### Adapting to the Connection

Default automatic mode adds parts when measurements show an improvement and backs off after failures or
backpressure. HTTP 429, 503 or 504 pauses all new attempts, retries included, through `Retry-After` (at most 60
seconds at a time). A retry or
URL-renewal wait releases its controller place. Cancelled attempts and failures predating the last backoff do not
trigger another backoff. Measurements cover the request through response headers, not waiting time.

`max_concurrency`, from 1 to 1024, caps either startup. Explicit limiter bounds and server-required serial behavior
still apply. `UploadTuning` can be passed per transfer as `tuning`, or per client as `upload_tuning`.

#### Startup and Explicit Tuning

Eligible Amazon S3 uploads use the SDK's scaled policy unless you provide concurrency tuning:

| Choice | Starting behavior |
| --- | --- |
| `UploadStartup.DEFAULT` | Probes from one part. A measured 96 MiB/s window can promote to the policy's initial target. |
| `UploadStartup.AGGRESSIVE` | Starts at the policy's initial target on a connection you already know is fast. |
| `UploadTuning(adaptive=False)` | Fixed `max_concurrency`, or 4 when not specified. |
| Explicit concurrency settings | Uses the configurable controller's supplied start/growth/backoff. |

The scaled policy grows toward 150 parts, and can target up to 1024 after a qualifying fast link has carried 64 GiB.
Only busy measurement windows are judged. Both startups adapt the same way and can reach the same ceiling;
neither overrides caps or changes other destination profiles. Startup cannot be combined with static mode or
explicit concurrency settings. These policy settings are not a throughput guarantee.

#### Part Sizes

Where Files.com permits client-selected sizes, the SDK fits them to the file and concurrency within granted size
and part-count limits. Scaled-policy files try larger unread parts at a stable concurrency share and keep them only
for a 10% throughput gain. Otherwise server-planned sizes apply. If Files.com withdraws or narrows the grant,
the upload stops before sending further parts.

```python title="Optional Upload Tuning"
import files_sdk

try:
  files_sdk.upload_file("backups/big.iso", "archive/big.iso", max_concurrency=16)

  fast_link = files_sdk.UploadTuning(startup=files_sdk.UploadStartup.AGGRESSIVE)
  files_sdk.upload_file("video.mp4", "media/video.mp4", tuning=fast_link)

  steady = files_sdk.UploadTuning(adaptive=False)
  files_sdk.upload_file("nightly.tar", "backups/nightly.tar", max_concurrency=6, tuning=steady)
except files_sdk.error.NotAuthenticatedError as err:
  print(f"Authentication Error Occurred ({type(err).__name__}):", err)
except files_sdk.error.Error as err:
  print(f"Unknown Error Occurred ({type(err).__name__}):", err)
```

### Memory and Connections

`TransferLimiter` shares the budget across clients or transfers without sharing credentials or their learned
concurrency targets. Waiting uploads are admitted in request order; a directory job shares learning separately.

| Resource | Accounting |
| --- | --- |
| Stream part | Retained whole until accepted, so retries resend identical bytes. A part holds what is left of the stream, up to the part size Files.com gives, and at most 5 GiB: a stream part of more fails the upload, before it is read when `size` shows that. `upload_file()` and `spool_limit` send parts from a file instead. |
| Local-file part | Copy buffer of at most 64 KiB. Small parts, or parts of up to 5 GiB under DEBUG logging, are read whole before sending; DEBUG logs content. |
| Client's implicit limiter | 1024 parts and 128 MiB, shared with downloads. Module-level functions share one implicit limiter. |
| Explicit `TransferLimiter()` | Defaults to 32 parts and 256 MiB; the SDK does not raise supplied limits. |
| SDK buffer reservation larger than `max_bytes` | Waits until no other reservation holds buffer room, then is admitted alone. |

The budget covers SDK part buffers, not your stream buffers or HTTP-library memory. Bounded stream read-ahead can
prepare a few parts while active parts are busy.

```python title="Sharing a Transfer Budget"
import files_sdk

limiter = files_sdk.TransferLimiter(max_parts=6, max_bytes=128 * 1024 * 1024)
first = files_sdk.Client(api_key="FIRST_KEY", transfer_limiter=limiter)
second = files_sdk.Client(api_key="SECOND_KEY", transfer_limiter=limiter)
```

### Writing Remote Files

`files_sdk.open(path, "wb")` uploads one part at a time as it fills, and the remainder on close; it holds at most
one part, up to 5 GiB, and a write past that fails the upload. Text mode `"w"` encodes UTF-8. `flush()` cannot
send a short middle part early. A failed write or close sends nothing further. See
[Remote Files and Folders](/python/overview/remote-files), including why leaving a `with` block with an exception
can still complete the bytes already written.

### Diagnostics

Set `UploadTuning.observer` to receive `UploadObservation` on the uploading thread. It covers planning/fallbacks,
controller and part-size decisions, limiter/read-ahead/cooldown waits, samples at most four times a second, and a
final outcome/settings/attempts record with SDK and Python versions.

Unavailable measurements are `None`, not zero: an unknown-size serial stream reports waits and its active part,
but no runway, controller decisions or throughput samples. Observations contain only numbers and names, never
paths, URLs, headers or credentials, and are not collected without an observer. Observer exceptions stop the
upload except in the final notification, where they are logged.

## Downloads

`download_file()` saves a remote file to a local path; `download_stream()` writes it into a binary stream.
Both return the downloaded `File`.

The SDK fetches parallel ranges where storage supports them with reliable version checks, and adjusts concurrency
on eligible storage. It can fall back to a whole response when needed. Start with the paths; no tuning is required. Temporary failures are
retried within a limit, and you can follow the transfer with a progress callback.

`cancel_token`, `request_timeout` and `deadline` cover the operation from obtaining its download URL to the last byte.
See [Cancellation and Deadlines](/python/overview/cancellation).

```python title="Downloading a File"
import files_sdk

try:
  with files_sdk.Client(api_key="YOUR_API_KEY") as client:
    file = client.file.download_file("archive/big.iso", "downloads/big.iso")
    print(file.path, file.size)
except files_sdk.error.NotAuthenticatedError as err:
  print(f"Authentication Error Occurred ({type(err).__name__}):", err)
except files_sdk.error.Error as err:
  print(f"Unknown Error Occurred ({type(err).__name__}):", err)
```

### Local Files

`download_file()` writes to a private temporary file beside the destination, then puts it in place after the full
response is validated. **It replaces an existing destination.** If the destination is a symbolic link, a single-file
download replaces the file it points to; directory downloads instead refuse links. Other hard links to a replaced
file keep the old content.

A failure or cancellation before publication leaves the destination unchanged. With a checkpoint, a complete,
version-bound private stage can sometimes be kept for recovery; see [Pausing and Resuming](/python/overview/resuming).
A partial whole response starts from the beginning on the next call.

Without `local_path`, the file is saved under its own name in the current directory. The SDK needs permission to
create a temporary directory beside the destination. [Local Access and Publication](#local-access-and-publication)
describes platform access rules and failures that prevent replacement.

### Streams

`download_stream(path, stream)` writes from the stream's current position, in order, and leaves it open. It never
seeks, truncates or rewinds. A failure can leave partial content in the stream, and already-written bytes are never
written again. Whole-response retries stop once the stream has accepted bytes.

The stream must be blocking. Partial writes are completed before proceeding. A raw stream returning `None` or `0`
from `write()` raises `InvalidParameterError`; for other writers, `None` means all bytes were accepted. Cancellation
stops before the next write, and your stream's exceptions propagate unchanged.

Ranges fetched ahead are buffered within the client's shared `TransferLimiter`. For a remote file downloaded as
you read it, use `files_sdk.open(path, "r")` or `"rb"`; text uses UTF-8. See
[Remote Files and Folders](/python/overview/remote-files).

```python title="Downloading Into a Stream"
import files_sdk

try:
  with open("report.csv", "ab") as output:
    files_sdk.download_stream("reports/report.csv", output)
except files_sdk.error.NotAuthenticatedError as err:
  print(f"Authentication Error Occurred ({type(err).__name__}):", err)
except files_sdk.error.Error as err:
  print(f"Unknown Error Occurred ({type(err).__name__}):", err)
```

This example appends to the local file. Choose its open mode deliberately; use `download_file()` for staged
replacement.

### Progress

Pass a function as `progress`. It receives `files_sdk.DownloadProgress` on the calling thread, at most four times
a second while bytes arrive, and once more at completion. If it raises, active ranges stop and its exception is
propagated. Mark the operation successful only after the download call returns.

| Field | Meaning |
| --- | --- |
| `bytes_committed` | Complete range bytes, or bytes accepted by the stream. For whole responses, written bytes reset to zero if the response restarts. |
| `bytes_received` | Network bytes, including retries. |
| `total_bytes` | Size from the bound version or response length. For an encoded whole response, the size is known only at the end. |
| `pinned_version` | Whether the download is protected by one verified version, independently of whether it uses ranges or a whole response. |

```python title="Following Download Progress"
def report(progress):
  print(f"{progress.bytes_committed} of {progress.total_bytes} bytes")

file = files_sdk.download_file("reports/report.csv", "report.csv", progress=report)
```

### Failures

Temporary range failures, short responses and overruns are retried as
[Retries and Timeouts](/python/overview/retries) describes. An overrun fails before excess bytes are written.
A failed whole response restarts from byte zero only while the destination can restart; a stream that has taken
bytes cannot.

| Situation | Outcome |
| --- | --- |
| Storage URL expired or expires within a minute | Renewed for the same version, up to twice. Other refusals, including an ordinary 403, fail. |
| Version is gone or changed, including storage HTTP 412 or a changed bound storage tag | A local-file download starts over once with the current version. A stream already holding old-version bytes raises `InvalidRequestError`. |
| Invalid identity, malformed or encoded range, disallowed redirect, missing required bound storage tag, or web-app response | `APIConnectionError` before bytes from that invalid response are written. |
| Storage ignores a range | API-identity downloads reject it; qualified storage-bound downloads may fetch the same version whole, as below. |

URLs are used exactly as Files.com supplies them. Expiry checks recognize the supplied expiry and supported signed-URL
fields for AWS, Files.com, Google and Azure. Source and destination stream exceptions retain their own type.

### Ranges at Once

Version-bound downloads use 8 MiB ranges. Eligible Amazon S3 downloads use the scaled policy: an initial target of
150 ranges, adapting to throughput, failures, throttling and queueing. Downloads have no upload startup choice or
warmup. Other storage with a Files.com-provided identity fetches 4 ranges by default. An endpoint's name selects
tuning; it does not by itself establish a version.

`max_concurrency`, from 1 to 1024, caps the target. `tuning` accepts `files_sdk.UploadTuning`;
`UploadTuning(adaptive=False)` keeps `max_concurrency` ranges (or 4) at once. Custom concurrency settings use the
configurable controller. Upload-only settings such as `startup`, `observer` and part-size options are refused.

Each range reserves buffer space first: a 256 KiB copy buffer for a local file, or the whole range for an ordered
stream. Each network attempt holds a controller place and limiter `max_parts` slot only while active. Retry and
URL-renewal waits release both slots, keep reserved memory, and wait behind cooldowns. HTTP 429, 503 or 504 pauses
new ranges for `Retry-After`, even if reading the error body fails. Measurements exclude local-file write time.

Adaptive files within `download_directory()` or `download_files()` share a controller for that job;
nonadaptive downloads keep independent targets.

### Download Identity

Version protection is automatic. There are two supported sources:

| Source | Binding and checks |
| --- | --- |
| Files.com-provided download identity | `with_download_identity` supplies a token, exact size and required headers. Each range must match the requested bytes and size. Required `If-Match` tags must match any returned strong ETag; a missing response tag remains accepted for compatibility. Renewal with `expected_download_identity` must return the same token and size. |
| Qualified storage response | Without API identity, HTTPS Amazon S3 general-purpose endpoints on the default port can bind from a first valid HTTP 206 range at byte zero: exact unencoded bytes, authoritative size and a strong ETag. Later requests use `If-Match`, validate every range/size/tag and follow no redirect. Renewed URLs must name the same storage object. |

API-identity requests can follow redirects within their original origin, retaining required headers. Cross-origin
redirects fail before sending there. Storage-bound requests follow no redirects. The storage binding's tag, size
and address digest are an SDK record and are never sent to Files.com. This is a qualified conditional-range
protocol, not a guess from equal ETags, sizes or modification times.

Other storage uses one unbound response. On eligible storage, an initial HTTP 200, 416 or redirect also
falls back to a whole response. A valid first range without a strong tag stays unbound: it can serve as the
whole response if it already contains the entire small file; otherwise the SDK fetches the file whole.
Malformed initial range encoding, byte coverage or length raises `APIConnectionError` instead of falling back.
Unbound downloads keep no reusable checkpoint. After storage binding, a missing tag fails validation and a
weak or different tag indicates a changed version, handled as described under Failures.

If qualified storage starts ignoring ranges after binding, the SDK stops other ranges, discards their partial
writes and fetches the whole **same version** with `If-Match`. `pinned_version` remains true. A stream that already
accepted bytes fails instead. A partial whole response restarts; it is not continued mid-response. A complete bound
private local stage may be reused only after checkpoint sync/save and the same identity, privacy, exact-size and
version checks; see [Pausing and Resuming](/python/overview/resuming).

An identity grants no permissions and is not logged at INFO or above. Checkpoints contain the token/size, or the
storage tag/size/resource digest, never credentials, headers or signed URLs. Recovery confirms the version before
reusing bytes; missing ranges are fetched only where storage still honors Range.

### Local Access and Publication

The temporary directory is named `.files_sdk-` plus 32 hexadecimal digits. Its directory and file are owner-only;
on macOS inherited ACLs are removed before writing. On POSIX systems, operations use the opened destination
directory's descriptors, protecting against other users and links replaced during the download, but not programs
running as you. Windows uses paths without that protection.

The replacement keeps existing file permissions without set-user-ID, set-group-ID or sticky bits. POSIX systems
also preserve its owner and group; macOS/Linux preserve its ACL. Inability to keep that access raises
`files_sdk.localfs.AccessNotKept`, an `OSError`, instead of replacing the file. New macOS files receive their parent
folder's inherited ACL at publication; inability to apply it also fails. Windows does not retain a replaced file's
own access-control entries. The destination directory's permissions are unchanged.

## Pausing and Resuming

Set `checkpoint` to a private local path when calling `upload_file()`, `upload_stream()`, `download_file()` or
`download_stream()`. Repeat the same transfer with that checkpoint after an interruption. Uploads reuse accepted
parts; version-bound downloads reuse recorded ranges where storage still honors Range. Successful completion
removes the checkpoint.

Pass a `files_sdk.PauseToken` as `pause_token` to pause: the SDK starts no new parts, lets active parts finish,
saves progress and raises `TransferPausedError`, whose `checkpoint` identifies the state. Cancellation instead
stops active requests immediately and also saves supported checkpoint state.

An unbound download keeps no checkpoint. A partial whole response starts from the beginning on the next call.
A pause before a whole-response fallback can retain earlier ranged progress, but if storage still ignores Range,
that data is discarded and the same version is fetched whole. This is not mid-response continuation.

```python title="Pausing and Continuing an Upload"
import threading
import files_sdk

try:
  pause = files_sdk.PauseToken()
  timer = threading.Timer(60, pause.pause)
  timer.start()
  try:
    files_sdk.upload_file("backup.tar", "archive/backup.tar",
      checkpoint="backup.tar.checkpoint", pause_token=pause)
  except files_sdk.error.TransferPausedError:
    files_sdk.upload_file("backup.tar", "archive/backup.tar", checkpoint="backup.tar.checkpoint")
  finally:
    timer.cancel()
except files_sdk.error.NotAuthenticatedError as err:
  print(f"Authentication Error Occurred ({type(err).__name__}):", err)
except files_sdk.error.Error as err:
  print(f"Unknown Error Occurred ({type(err).__name__}):", err)
```

Only the paused case runs the continuation. A successful first upload is not uploaded again.

### What a Checkpoint Holds

| Transfer | Recorded state |
| --- | --- |
| Upload | Files.com upload reference, planned parts, accepted ETags and whether completion was attempted. |
| API-identity download | Identity token, version size, private stage and written ranges. |
| Storage-bound download | Strong tag, size, storage-resource digest, private stage and written ranges. |

Checkpoints contain no API key, session, headers or signed URL. The SDK obtains addresses again on recovery.
The checkpoint belongs to the same site, Workspace, paths, stream/file and parameters. Credentials are not recorded,
so keep separate checkpoints for different users. A `.lock` file prevents simultaneous use.

Using another transfer's checkpoint raises `InvalidParameterError`; damaged or incompatible state raises
`InvalidRequestError`. Remove the checkpoint to start a fresh transfer only after resolving any uncertain upload
completion, as below.

### Where to Keep Checkpoints

The checkpoint and lock file must be yours and unmodifiable by other users. Their directory and the folders and
links leading to it must be owned by you or the system and protected from other users changing them.

| Platform | Additional trust requirements |
| --- | --- |
| Linux | No group/other write access, except protected sticky directories such as `/tmp`. Path links must belong to you or the system. Owner-only file permissions limit inherited ACL access. |
| macOS | The same path rules, plus refusal of ACL entries allowing others to write, delete, change attributes/access or take ownership. Denials, your own entries and inheritance-only entries are allowed. |
| Windows | Ownership by you, SYSTEM or Administrators; ACLs preventing others changing files or deleting/replacing directory entries. Links and junctions are refused. Private profile folders can qualify. |

Untrusted paths raise `InvalidRequestError` before checkpoint reading or changing transfer files, though a lock
file may already exist. Group-writable directories, including those created with umask 002, fail; use a private
location or remove group write access from the checkpoint directory. An unreadable ACL is refused.

New checkpoints and locks are private from creation. On macOS they are created in an owner-only `.stage` folder
with inherited ACLs removed, then placed at their final names; abandoned staging folders are never read. A macOS
filesystem with ACLs but no hard links cannot create a new lock and fails. On Windows, a directory inheriting
other-user access to new files is refused before creation.

If privacy or identity changes during a transfer, the checkpoint is not saved or removed. The SDK raises
`files_sdk.checkpoint.UntrustedCheckpointError`, an `OSError`, or adds the cleanup problem to the original failure.
A download's private stage gets final destination access from the current process or replaced file, never from
checkpoint-controlled permissions.

### When a Transfer Starts Again

Recovery never combines different source versions. Downloads renew their API identity or confirm the storage-bound
version of the same object before reusing bytes. Missing ranges are fetched only if storage honors Range; otherwise
the same version is fetched from the beginning.

| Situation | Recovery |
| --- | --- |
| Local upload changed or upload expired | Starts a new upload from the beginning. |
| Upload's granted limits no longer allow its plan | Raises before sending more parts. |
| Download version gone; stage missing, replaced or no longer private | A local-file download starts fresh with the current file. An already-written stream raises `InvalidRequestError`. |
| Complete bound local stage saved but not published | May reuse it only after successful checkpoint sync/save and checks of the same private regular file, exact size, storage resource and version. Not every publication failure leaves reusable state. |
| Unbound download or interrupted whole response | Unbound transfers keep no checkpoint; a whole response is fetched again from byte zero. |

When restarting a local download, an old stage still proven to belong to the SDK is removed on POSIX systems;
Windows leaves it in place. Avoid editing transfer files or their private directories during recovery.

#### Upload Completion Can Be Unknown

The SDK saves the final-request record before completing an upload. If that request's answer is lost, unusable or
an error of any status, the upload may already be complete. A later call raises `APIConnectionError` with
`remote_outcome_unknown` instead of completing it again. **Check the remote file before deleting the checkpoint
and starting another upload.**

Completion is retried on recovery only when it is known not to have happened: the request was not sent or Files.com
reported its site disabled. A flush failure prevents the final request; platform durability limits still apply.

### Streams

| Stream | Requirement for recovery |
| --- | --- |
| Upload | Supply identical bytes from the same start, with the same `size` or `spool_limit`. Accepted parts are read and checked again, not resent. Different bytes raise `InvalidRequestError`. |
| Unknown-size upload without spooling | Cannot resume. |
| Download | Position the stream after the previously recorded bytes and support `tell()`. If more bytes were written than recorded, truncate to the size named by the error before continuing. |

These rules apply to supported version-bound ranged recovery, not continuation within a partial whole response.

```python title="Continuing a Download Stream"
import files_sdk

try:
  with open("report.csv", "ab") as output:
    files_sdk.download_stream("reports/report.csv", output, checkpoint="report.checkpoint")
except files_sdk.error.NotAuthenticatedError as err:
  print(f"Authentication Error Occurred ({type(err).__name__}):", err)
except files_sdk.error.Error as err:
  print(f"Unknown Error Occurred ({type(err).__name__}):", err)
```

### Crashes and Power Loss

Checkpoints are saved at most once a second during transfer and when it stops. Each save replaces a complete,
flushed file and flushes its directory where supported. Download data is flushed before the checkpoint records it.
On storage honoring flushes, recent unrecorded progress may be transferred again rather than falsely marked done.
The SDK flushes caller-owned streams, but persisting their data is the caller's responsibility.

An upload cannot send its final request until the checkpoint save and flush succeed. Windows and filesystems unable
to flush directories persist the checkpoint file but not its rename; a power loss can undo the latest save,
including the completion-attempt record.

A complete stage after a crash is not reusable solely because its length matches: checkpoint commitment, private
file identity and source-version confirmation must also pass. Partial whole-response data does not gain a resumable
span. A complete, saved, version-bound local stage may recover under the conditions above.

Supported partial ranged transfers retain a private stage beside the destination, named `.files_sdk-download`
inside a `.files_sdk-` directory with 32 hexadecimal digits. A download stopped before writing anything keeps no
checkpoint or stage. If you abandon a transfer by deleting its checkpoint, remove its retained private directory too.

## Directories and Many Files

`upload_directory(local_path, remote_path)` and `download_directory(remote_path, local_path)` preserve relative
paths and empty folders. `upload_files()` and `download_files()` instead accept `(source, destination)` pairs.

Each returns `TransferResult` with a `FileOutcome` per entry: paths and a `status` of `"completed"`, `"failed"`
(with `error`), `"skipped"` (with `reason`), `"paused"` or `"cancelled"`. **One file failure does not stop the
other files.** Check `result.ok` and `result.failed` rather than treating a returned job result as universal success.

```python title="Uploading a Directory"
import files_sdk

try:
  with files_sdk.Client(api_key="YOUR_API_KEY") as client:
    result = client.file.upload_directory("photos", "backup/photos", max_files=8)
    for outcome in result.failed:
      print(outcome.local_path, outcome.error)
except files_sdk.error.NotAuthenticatedError as err:
  print(f"Authentication Error Occurred ({type(err).__name__}):", err)
except files_sdk.error.Error as err:
  print(f"Unknown Error Occurred ({type(err).__name__}):", err)
```

### Uploading a Directory

Each file uses `upload_file()`. `mkdir_parents` defaults on unless `params` overrides it; parameters apply to every
file. Symlinks and special files are skipped and reported. A changed or replaced source file fails alone.

Discovery walks folders in name order as transfers run, rather than retaining the whole tree. POSIX systems open
each folder from its parent without following links, so a replaced folder cannot redirect the walk outside the tree.

### Downloading a Folder

Discovery lists remote folders a page at a time. Each file uses a staged `download_file()` replacement; missing local
folders and empty remote folders are created.

Directory downloads refuse destination-file or folder links, leaving their targets unchanged. This differs from
single-file downloads, which follow a supplied destination link. POSIX systems publish through opened folders to
prevent replacement links redirecting files outside the tree. Invalid local names and two remote names colliding
locally, such as `Read.txt`/`read.txt` on case-insensitive filesystems, fail for that file alone.

A subfolder listing failure is a separate outcome. Failure to list the requested root raises instead.

```python title="Downloading a Folder"
import files_sdk

try:
  result = files_sdk.download_directory("reports/2026", "local-reports")
  print(len(result.completed), "files")
  for outcome in result.failed:
    print(outcome.remote_path, outcome.error)
except files_sdk.error.NotAuthenticatedError as err:
  print(f"Authentication Error Occurred ({type(err).__name__}):", err)
except files_sdk.error.Error as err:
  print(f"Unknown Error Occurred ({type(err).__name__}):", err)
```

### Limits and Progress

| Setting or behavior | Meaning |
| --- | --- |
| Explicit `max_files` | Caps simultaneous files from 1 to 64. |
| Default file admission | Normally 4. Eligible scaled-policy upload jobs start with 6 and can prepare up to 128 files to feed their target; noneligible jobs settle at 4. |
| Adaptive upload `max_concurrency` | A shared part target per destination profile across the job's files, not a separate target per file. Serial files and caps of one still participate. |
| Adaptive qualified-S3 downloads | Share one range controller/target for that job. Other bound downloads keep their own target, default 4. Unbound files use one response. |
| Static files | Independent per-file `max_concurrency`, or 4. |
| Shared limiter | Bounds resources fairly across jobs/clients but does not share learned targets between jobs. |

Later files in a job use what earlier files learned; a new job or single transfer starts afresh. Files in the same
job use the client's `TransferLimiter`, including requests outside the adaptive target.

A `progress` callback receives `TransferJobProgress` on the calling thread, at most four times a second: completed,
failed and skipped files, discovered files/bytes and whether discovery finished, and bytes transferred.

### Stopping and Resuming

`cancel_token`, `request_timeout`, `deadline` or closing the client stop the whole job, wait for its transfers and
raise. The error's `result` holds outcomes so far. `checkpoint` and `pause_token` apply to the job as in
[Pausing and Resuming](/python/overview/resuming).

The checkpoint records the site, Workspace, source/destination pairs, completed entries and each unfinished
transfer. Completed files are skipped as `"completed before"` only after verification:

| File | Verification |
| --- | --- |
| Upload | Same unchanged local source and the remote file that upload created, checked with Files.com. |
| Download | Same local file and a Files.com-provided download identity confirmed with Files.com. Completed storage-bound and unbound files are downloaded again. |

Changed source/destination pairs transfer again. Unfinished storage-bound files can reuse saved spans after
confirming their version and private stage. Missing ranges resume only where storage honors Range;
otherwise the verified version is fetched whole. An all-completed/skipped job removes its checkpoint; a job with
failures keeps it so a later run can retry those entries.

## Remote Files and Folders

Use `files_sdk.open(path, mode)` to read or write a remote file with Python's familiar file methods. Use a `with` block to close it; closing a writer completes its upload.

| Mode | Content |
| --- | --- |
| `"r"` / `"w"` | Read / write UTF-8 text, preserving line endings. |
| `"rb"` / `"wb"` | Read / write bytes. |

Readers support `read(size)`, `readline()`, `readlines()`, line iteration and binary `readinto()`. At the end they return an empty value. When Files.com binds the file to one version, the reader fetches ranges as needed and holds at most a few MiB. Otherwise its first read caches the whole response in a temporary file, using memory while it is small; closing the reader removes that cache. A changed remote version raises `InvalidRequestError` instead of mixing content. See [Download Identity](/python/overview/downloads#download-identity).

`file.size` is `None` until a read fetches the remote file. It then reports the verified total size: the bound version's size for ranges, or an unencoded whole response's `Content-Length`. An empty file has size `0`. A missing or encoded response length leaves the size `None`, even when the API record reports a size.

```python title="Example Request"
import files_sdk

try:
  with files_sdk.open("logs/app.log") as log:
    for line in log:
      if "ERROR" in line:
        print(line, end="")
except files_sdk.error.NotAuthenticatedError as err:
  print(f"Authentication Error Occurred ({type(err).__name__}):", err)
except files_sdk.error.Error as err:
  print(f"Unknown Error Occurred ({type(err).__name__}):", err)
```

### Writing

A writer sends full parts as they fill and the remaining bytes on close. After successful close, the file object has the uploaded File's attributes.

| Method | Behavior |
| --- | --- |
| `write()` | Returns the number of bytes or characters accepted. |
| `writelines()` | Writes each supplied item. |
| `flush()` | Does not send a short part early; a short middle part would invalidate the upload. |
| `close()` | Completes once, then releases the writer's resources, including when close fails. |

A failed upload sends nothing further. Later writes and close raise `InvalidRequestError`; an exception leaving a `with` block remains the primary exception, and the file closes. A type error before sending, such as writing bytes to a text writer, does not end the upload. If an error has `remote_outcome_unknown=True`, check the destination before uploading again.

A `with` block closes the writer even when your own code raises an exception, completing the bytes already written. To publish only complete content, prepare a local file or stream first and use `upload_file()` or `upload_stream()`. Local-file uploads can send parts in parallel when the destination permits it.

```python title="Example Request"
import files_sdk

try:
  with files_sdk.open("reports/summary.txt", "w") as report:
    report.write("All jobs finished\n")
  print(report.size)
except files_sdk.error.NotAuthenticatedError as err:
  print(f"Authentication Error Occurred ({type(err).__name__}):", err)
except files_sdk.error.Error as err:
  print(f"Unknown Error Occurred ({type(err).__name__}):", err)
```

### What a Remote File Cannot Do

| Operation | Result |
| --- | --- |
| `seek()`, `tell()`, `truncate()`, `fileno()` | Raise `io.UnsupportedOperation`; `seekable()` is `False`. |
| Modes `"a"`, `"x"`, or `"+"` | Raise `io.UnsupportedOperation` before sending a request. |
| An unrecognized mode | Raises `ValueError` before sending a request. |
| Reading a writer, writing a reader, or using a closed file | Raises `io.UnsupportedOperation`. |

`io.UnsupportedOperation` inherits from both `ValueError` and `OSError`, preserving the exception compatibility of Python's files and version 1 of the SDK.

### Walking Folders

`folder.walk(path)` yields each folder's path, child folders and files as `File` objects, from the top down. It lists folders lazily, one page at a time. Remove entries from the yielded folders list to skip their subtrees. One operation covers the walk, so `cancel_token` and `deadline` apply to the entire traversal.

```python title="Example Request"
import files_sdk

try:
  for folder, folders, files in files_sdk.folder.walk("projects"):
    folders[:] = [f for f in folders if not f.path.endswith("/archive")]
    for file in files:
      print(file.path, file.size)
except files_sdk.error.NotAuthenticatedError as err:
  print(f"Authentication Error Occurred ({type(err).__name__}):", err)
except files_sdk.error.Error as err:
  print(f"Unknown Error Occurred ({type(err).__name__}):", err)
```

### Waiting for Copies, Moves and Deletions

`copy()` and `move()` can return a pending `FileAction` before the server finishes. Use a waiting method when subsequent work depends on completion.

| Method | Completion |
| --- | --- |
| `copy_and_wait()`, `move_and_wait()`, or `FileAction.wait()` | Poll the `FileMigration` every second by default (`interval`), call `progress` when supplied, and return the completed migration or `None` for an immediately finished action. |
| `delete_and_wait()` | Waits until the path no longer exists, allowing a replacement upload. |

A failed or cancelled migration raises `files_sdk.error.FileMigrationError`; its `migration` attribute holds the result. Bound waiting with the operation's `cancel_token`, `request_timeout` or `deadline` options.

```python title="Example Request"
import files_sdk

try:
  migration = files_sdk.file.copy_and_wait(
    "projects/2026", {"destination": "archive/2026"},
    {"request_timeout": 600},
  )
except files_sdk.error.NotAuthenticatedError as err:
  print(f"Authentication Error Occurred ({type(err).__name__}):", err)
except files_sdk.error.Error as err:
  print(f"Unknown Error Occurred ({type(err).__name__}):", err)
```

## File Attachments

Attachments configure API objects, such as a user's `avatar_file`, a style's `file` or a behavior's `attachment_file`. To transfer a file to your site's folders, use `files_sdk.upload_file()`.

| Input | Behavior |
| --- | --- |
| Bytes or a binary stream | Sends the supplied content. |
| `files_sdk.Attachment` | Also sets the filename and content type. |
| `Attachment.from_path(path)` | Opens and closes the local file for you. |
| String | Is never treated as a local path. |
| JSON file object | Sends `encoded_content`, `filename` and `type` as supplied. |

The default filename is the stream's basename, or the parameter name when unavailable. The default content type is `application/octet-stream`.

```python title="Example Request"
import files_sdk

try:
  with open("avatar.png", "rb") as picture:
    files_sdk.user.update(1234, {
      "avatar_file": files_sdk.Attachment(picture, content_type="image/png"),
    })

  files_sdk.style.update("marketing/assets", {
    "file": files_sdk.Attachment.from_path("logo.png", content_type="image/png"),
  })
except files_sdk.error.NotAuthenticatedError as err:
  print(f"Authentication Error Occurred ({type(err).__name__}):", err)
except files_sdk.error.Error as err:
  print(f"Unknown Error Occurred ({type(err).__name__}):", err)
```

### Streams and Retries

The SDK borrows your stream from its current position to the end and leaves it open. Keep it unchanged until the call returns.

| Source | Replay for an allowed retry or 307/308 redirect |
| --- | --- |
| Seekable stream | Seeks back to the starting position and sends the same bytes. |
| Nonseekable stream, such as a pipe or `sys.stdin.buffer` | Buffers first: up to 1 MiB in memory, then a temporary file removed when the request ends. |
| `Attachment.from_path()` | Replays only while the original size and modification time remain unchanged. |

Nonseekable buffering is limited to 64 MiB per attachment by default, or its `spool_limit`. A request containing several attachments can buffer each one's allowance. This replay support does not make an otherwise unsafe request eligible for retry; see [Retries](/python/overview/retries).

```python title="Example Request"
import sys

import files_sdk

try:
  files_sdk.user.update(1234, {
    "avatar_file": files_sdk.Attachment(
      sys.stdin.buffer,
      filename="avatar.png",
      content_type="image/png",
      spool_limit=16 * 1024 * 1024,
    ),
  })
except files_sdk.error.NotAuthenticatedError as err:
  print(f"Authentication Error Occurred ({type(err).__name__}):", err)
except files_sdk.error.Error as err:
  print(f"Unknown Error Occurred ({type(err).__name__}):", err)
```

### Other Parameters

Other parameters retain their supplied values. The SDK uses multipart form data when it can preserve every value and the filename exactly; otherwise it sends a JSON file object with streamed base64 content, about one third larger.

JSON is required for `None`, empty lists or objects, numbers or booleans inside an object, lists of objects, or filenames containing `%`, `\`, `/` or `"`, which the API's form parser would change.

The API validates the attachment and parameters normally. The SDK raises `InvalidParameterError` without retrying for a text stream, `read()` returning `None` or ending early, exceeded spool limits, or a changed local file.

```python title="Example Request"
import files_sdk

try:
  with open("watermark.png", "rb") as image:
    files_sdk.behavior.create({
      "path": "shared/previews",
      "behavior": "watermark",
      "attachment_file": files_sdk.Attachment(image, content_type="image/png"),
      "value": {
        "gravity": "SouthWest",
        "max_height_or_width": 20,
        "transparency": 25,
      },
    })
except files_sdk.error.NotAuthenticatedError as err:
  print(f"Authentication Error Occurred ({type(err).__name__}):", err)
except files_sdk.error.Error as err:
  print(f"Unknown Error Occurred ({type(err).__name__}):", err)
```

## Mock Server

Files.com publishes a mock Files.com API server, which is useful for testing your use of the Files.com
SDKs and other direct integrations against the Files.com API in an integration test environment.
It never checks credentials: send any placeholder API key, such as `YOUR_API_KEY`, and never use
real Files.com credentials with it.

The server has two modes, chosen when it starts:

* **Legacy mode** (the default) checks required parameters and parameter types, then returns a fixed
  example response for each API endpoint. It does not maintain state and it does not deeply inspect
  your submissions for correctness, which makes it useful for testing basic network operations and
  JSON encoding for your SDK or API client.
* **Simulation mode** keeps records, files and folders in memory, so a test can create, list, update
  and delete resources, upload a file and download the same bytes, and make chosen requests fail,
  stall or lose their connection on purpose. Requests it does not simulate fail with a clear error
  instead of returning an example response.

<div></div>
### Quick Start with Docker

With [Docker](https://docs.docker.com/get-docker/) installed, start the published image from
[Docker Hub](https://hub.docker.com/r/filescom/files-mock-server) with the command shown. It runs
legacy mode at `http://127.0.0.1:4041`, reachable from your machine only: point your integration's
Files.com API base URL there and use a placeholder API key. Stop it with Ctrl+C; `--rm` removes its
container.

The published image is built for `linux/amd64` only, so the command asks for that platform;
without it, Docker on a machine of another architecture, such as an Apple silicon Mac, looks for
an image the tag does not have. The `latest` tag moves to whichever server was published last,
and `--pull=always` fetches it again each time, so it need not include simulation mode. To run
simulation mode, build the image from the source as below.

```shell title="Start the Mock Server with Docker"
docker run --platform linux/amd64 --rm --pull=always -p 127.0.0.1:4041:4041 filescom/files-mock-server:latest

## In another terminal, with a placeholder API key:
curl -H "X-FilesAPI-Key: YOUR_API_KEY" http://127.0.0.1:4041/api/rest/v1/users
```

### Simulation Mode in Docker

To run exactly the server the source's README describes, simulation mode included, build the image
from a checkout of the source on [GitHub](https://github.com/Files-com/files-mock-server) and run
it by the image ID you record with your test results. Only `linux/amd64` builds of the source have
been checked, so both commands ask for that platform.

Simulation mode listens only on loopback unless told otherwise, so the command binds it to the
container's interfaces with `-b tcp://0.0.0.0:4041` and publishes the port on your machine's
loopback address only. `FILES_MOCK_TRANSFER_ORIGIN` tells it the address your tests use, so the
upload and download URLs it returns point at the published port.

Simulation mode keeps its state only in the server process. Its control endpoints under
`/__files_mock/v1` report when the server is ready, reset it with your fixtures, add fault rules
and return the journal of the requests it received. It refuses work over its limits instead of
truncating it. The README in the source describes all of these, the operations it simulates and
how to configure its limits.

```shell title="Simulation Mode from the Source"
## In a checkout of the source:
docker build --platform linux/amd64 -t files-mock-server:local .
image=$(docker image inspect --format '{{.Id}}' files-mock-server:local)
echo "$image"   # record this ID with your test results
docker run --platform linux/amd64 --rm -e FILES_MOCK_MODE=simulation \
  -e FILES_MOCK_TRANSFER_ORIGIN=http://127.0.0.1:40410 \
  -p 127.0.0.1:40410:4041 "$image" -b tcp://0.0.0.0:4041

## In another terminal:
curl http://127.0.0.1:40410/__files_mock/v1/ready
```

### From the Source with Ruby

Start the server from its source with Ruby and Bundler. `FILES_MOCK_MODE` is read once at startup:
leaving it unset or setting it to `legacy` starts legacy mode, `simulation` starts simulation mode,
and any other value stops startup with an error. Legacy mode listens on port 4041 on all IPv4
interfaces, and simulation mode on `127.0.0.1:4041`.

```shell title="Start the Mock Server with Ruby"
bundle install

## Legacy mode
bundle exec puma

## Simulation mode
FILES_MOCK_MODE=simulation bundle exec puma
```
