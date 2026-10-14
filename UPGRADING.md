# Upgrading to version 2

Version 2 of the `files_com` package keeps the same synchronous API and the
same `files_sdk` import. Most applications need only a supported Python and
up-to-date dependencies. The changes below are the ones that can affect
existing code. To stay on version 1.x until you have made them, require
`Files.com<2`.

## Python 3.11 or newer

Version 2 requires Python 3.11 or newer and is tested on CPython 3.11, 3.12,
3.13 and 3.14. On an older Python, `pip install files_com` installs the newest
1.x release instead. Releases after 2.0 are published only for Python 3.11
and newer.

## Dependency minimums

These are the lowest versions version 2 installs with:

| Package | Minimum | Why |
| --- | --- | --- |
| requests | 2.34.2 | Security fixes, such as keeping `.netrc` credentials with their host |
| urllib3 | 2.8.0 | Security fixes for streamed and compressed downloads |
| idna | 3.15 | Security fix for very long host names |
| certifi | 2026.7.22 | Current trusted certificate authorities |
| charset-normalizer | 3.5.1 | The maintained release version 2 is tested with |
| requests-toolbelt | 1.0.0 | The current release, which binds `files_sdk.source_ip` |

If your application pins an older version of one of these, pip reports a
conflict. Raise that pin rather than installing version 1.x for it. urllib3 2
needs Python's `ssl` module to use OpenSSL 1.1.1 or newer, as CPython 3.11
and newer already require.

Proxy settings (`HTTP_PROXY`, `HTTPS_PROXY`, `NO_PROXY`), custom certificate
bundles (`REQUESTS_CA_BUNDLE`) and `files_sdk.source_ip` work as before.

## Clients

`files_sdk.Client` is new: a client with its own credentials, settings and
connections, which every object it returns keeps using. The module-level
functions and settings work as before. See the Clients page of the
documentation.

## Timeouts and retries

- The default read timeout is 80 seconds (it was 60).
- `max_network_retries` now counts retries after the first attempt, so the
  default of 3 sends a failing request up to 4 times, and 0 sends it once. In
  version 1.x it counted attempts.
- API retries wait 0.1, 0.2 and 0.4 seconds, doubling from
  `initial_network_retry_delay` (now 0.1) up to `max_network_retry_delay`,
  without the random variation version 1.x added.
- Only connection failures, timeouts, 429 and 5xx answers other than 501 are
  retried. Version 1.x also retried other answers, such as 404, and TLS
  certificate failures.
- A request that may change something, such as a create, update or delete, is
  not sent again once it may have reached Files.com: a lost answer or any
  error answer, 429 and 503 included, raises `APIConnectionError` or that
  error, with `remote_outcome_unknown` set, instead of repeating it. Version
  1.x sent it again, which could do it twice. Requests that only ask for
  something are retried as before.
- `APIError` has `remote_outcome_unknown`: `True` for an error answer to a
  request that may have changed something, except Files.com's answer while its
  site is disabled.
- File transfers wait for a 429 or 503 answer's `Retry-After` seconds, up to
  60 seconds at a time.
  Downloads that fail are now retried, range by range when the download is
  bound to one version of the file. A download to a stream that is read
  with one request is retried only until it has written something.
- The request that completes an upload is not sent again once it may have been
  received; a lost answer or an error answer raises with
  `remote_outcome_unknown` set, and resuming does not complete it again.

## Credentials and options

- When both a module API key and a module session are set, requests use the
  API key, as they already did when both were passed to one call. Clear the key
  with `files_sdk.set_api_key("")` to use the session.
- An unknown option now raises `InvalidParameterError` instead of being
  ignored. The `session` option needs a session that has logged in.
- `files_sdk.CLEAR` removes an inherited setting for one call. An empty
  `api_key` or `session_id` option still means the module's setting.

## Objects keep their settings

Objects and lists returned by the module-level functions keep the module
settings of the call that returned them, such as the API key, workspace and
base URL, for their own later requests. Changing a setting affects only later
calls. `files_sdk.close()` closes the module-level connections; objects they
returned can no longer send requests.

## Logging

The `files_sdk` logger has a `NullHandler`, so an application that has not
configured logging no longer sees the SDK's error messages on stderr. The
warning about an option passed in params is logged at WARNING instead of
printed. `console_log_level` also accepts "warning".

## Redirects, `.netrc` files and transfers

The SDK no longer sends credentials from `.netrc` files. A redirect to another
origin now also drops extra headers, cookies and `Authorization`, and a
redirect that would carry a request's body to another origin (a 307 or 308 of
an upload part, or of an API request with parameters) is not followed: it
raises `APIConnectionError` with `remote_outcome_unknown` set, since the
request's own origin received it. When the API is reached over HTTPS, the
SDK accepts only `https://` transfer URLs; another scheme fails the
transfer before anything is sent to it. File transfer requests send the
SDK's `User-Agent`. The sessions the SDK creates,
including the module-level one, keep no cookies that servers set; cookies you
add to such a session yourself, or keep in a session you pass as
`http_session`, are still sent.

## Cancellation

Operations take `cancel_token`, `request_timeout` and `deadline` options, and
raise `OperationCancelledError`, `ClientClosedError` or
`DeadlineExceededError` when they stop.

## Errors

Every API and connection failure raises a subclass of
`files_sdk.error.Error`, so `except files_sdk.error.Error` catches all of
them. Some failures raise a different class than in version 1.x:

| Failure | Version 1.x | Version 2 |
| --- | --- | --- |
| A response that is not a Files.com error object, such as a proxy's HTML page, an empty or malformed body, or JSON that is not an object | `APIError` with the raw body in its message, or `TypeError` | `APIConnectionError` |
| An error object without a recognized string `type` | `KeyError`, `AttributeError` or `files_sdk.error.Error` | `APIError` |
| A download that cannot be decoded, or whose URL cannot be requested | the `requests` exception | `APIConnectionError` |
| An upload stream whose `read()` returns `None` (a non-blocking stream with no data ready) | `TypeError` | `InvalidParameterError`, raised before that part's data is sent |

Upload from a blocking stream, such as a file opened with `open(path, "rb")`.
Error messages no longer include response bodies, and user names, passwords
and signed query strings in URLs in API error text are redacted. An error that
file storage answers for an upload or download names the remote path it was
for instead, as in `HTTP 403 Transfer request failed for the download of
reports/q3.csv`.

## Uploads

- `upload_file()` and the `upload_to_*()` helpers return the `File` the
  upload created instead of `None`, and take `max_concurrency`, `progress`
  and `tuning` keyword arguments. When Files.com allows parallel parts,
  several are sent at once, adapting to the connection; version 1.x always
  sent one at a time. `upload_stream()` is new, for a binary stream of known
  or unknown size.
- The first `begin_upload` request of `upload_file()` and `upload_stream()`
  sends the upload's `size`.
- `params` given to an upload reach the request that completes it as well,
  so `mkdir_parents`, `with_rename` and `custom_metadata` apply to the whole
  upload. Params the SDK sets itself (`ref`, `part`, `parts`, `size`,
  `restart`, `action`, `etags`, `length`) raise `InvalidParameterError`.
- A file that changes while it uploads raises `InvalidRequestError` instead
  of completing with mixed contents.
- A short read from an upload stream no longer ends the upload early, and a
  stream that ends at a part boundary no longer sends an extra empty part.
- A file opened for writing sends what is written a part at a time as parts
  fill, instead of holding all of it until it closes, and asks Files.com for
  its first part at the first write. `flush()` no longer sends data early:
  sending the buffer from the start again on every flush could upload it
  twice. Text written to a file opened with `"w"` is sent as UTF-8.
- Each client bounds its uploads' parts in progress and their buffers with a
  `files_sdk.TransferLimiter`, which clients can share, and adapts them as
  `files_sdk.UploadTuning` says. See the Uploads page of the documentation.

## Downloads

- `download_file()` returns the `File` it downloaded instead of `None`, and
  takes `max_concurrency`, `progress` and `tuning` keyword arguments.
  `download_stream()` is new, for writing a file's content to a binary stream.
- A download asks Files.com for a download identity (`with_download_identity`)
  that binds it to one version of the file. With one, several ranges of that
  version are fetched at once, each carrying the headers the identity
  requires: from Amazon S3, as many as an adaptive controller finds useful,
  starting at 150 (`max_concurrency`, up to 1024, caps it, and
  `tuning=files_sdk.UploadTuning(adaptive=False)` keeps it at
  `max_concurrency`, or four); from other storage, four, or `max_concurrency`.
  Without one, a download from Amazon S3 binds itself to a version from
  storage's own answer to its first range, a 206 with a strong ETag that every
  later range must match with `If-Match`, and is then fetched the same way;
  otherwise the file is read in one response, as in version 1.x, never
  assembled from several. See the Downloads page of the documentation.
- `download_file()` writes into a temporary file, in a private directory the
  SDK makes in the local path's directory, and replaces the local path only
  once the whole file has arrived, so a failed download leaves it as it was;
  version 1.x emptied it first and wrote into it. This needs permission to
  create directories in the local path's directory. The new file takes the
  replaced file's permissions, without set-user-ID, set-group-ID or sticky
  bits, and other hard links to the old file keep the old content.
- A download into a stream writes every byte exactly once, however few bytes
  a `write()` takes. A raw stream whose `write()` returns `None` or `0` raises
  `InvalidParameterError`.
- A file that changes while it downloads, or an answer that is not the file,
  raises an error instead of producing mixed or wrong content.
- A download read in one response whose storage names the download request
  (`X-Files-Download-Request-Id`), and whose response declares no size, is
  checked against storage's status of that request before it is used. It
  completes when the status reports `completed` with a count equal to the
  bytes received. A status that reports `failed` or `error`, `completed` with
  no count or a different count, any other state or none, or that cannot be
  read (such as storage's 404 for a request it does not know) raises an error
  instead, whatever the size; a stream has already received the bytes. A
  status still `started` is read again, as a failed request is retried (up
  to `max_network_retries` more times), until storage reports an outcome,
  which is then checked the same way; a request still `started` after that
  raises too, so a response cut short before
  storage records its outcome is never taken as complete. A response that
  names no request is used unchecked, as before. When storage also names an
  error answer, its explanation of that error is added to the error raised,
  as a note and as its `download_request_status`.

## Remote files

A file opened with `files_sdk.open()` behaves more like a local file:

- Reading a file that Files.com binds to one version streams it a range at a
  time instead of downloading all of it first; other files are fetched whole,
  into a temporary file of the SDK's own, at the first read. `read()` returns
  the rest of the file, so reading again at the end returns an empty value; in
  version 1.x each `read()` downloaded the file again and returned it with any
  earlier content. `read(size)`, `readline()`, `readlines()`, `readinto()` and
  iterating by line work; in version 1.x `readline()` and `readinto()`
  returned an error object, and `readall()` returned `None`. Text is read as
  UTF-8 with its line endings as they are.
- Once a read fetches the remote file, its `size` is the total from its bound
  version or an unencoded response's `Content-Length`. A missing or encoded
  length leaves `size` as `None`, instead of the size in the API record.
- `open()` raises for a mode it cannot use, before sending anything:
  `io.UnsupportedOperation` for `"a"`, `"x"` and `"+"`, and `ValueError` for
  one it does not understand. In version 1.x an append mode failed when the
  file was closed.
- `seek()`, `tell()`, `truncate()` and `fileno()` raise
  `io.UnsupportedOperation`, and so does using a closed file; it is an
  `OSError`, as before, and also the `ValueError` Python's files raise.
  Closing a closed file does nothing. `writable()` is new; `writeable()`
  still works.
- A file opened for writing whose upload fails ends that upload. After a
  failed `write()`, further writes and `close()` raise `InvalidRequestError`
  and send nothing, but an exception leaving a `with` block, such as that
  failure, is the one raised, and the file is closed. A failed `close()`
  raises its error and closes the file, releasing its buffer; closing it again
  does nothing. A completion that failed may still have taken effect (the
  error's `remote_outcome_unknown` says so), so it is never sent again. Open
  the file again to upload it anew. In version 1.x a failed `close()` left the
  file open with everything written, and closing it again sent it all again,
  which could complete the upload twice.

## New in version 2

These are additions; code that does not use them is not affected.

- Uploads and downloads take a `checkpoint` path to resume from if they stop,
  and a `files_sdk.PauseToken` as `pause_token` to pause them. A checkpoint is
  used only from where no one else can change it: a file of your own in a
  folder that only you or the system can change, by its permissions and, on
  macOS and Windows, its access control list. See Pausing
  and Resuming in the documentation.
- `upload_directory()`, `download_directory()`, `upload_files()` and
  `download_files()` transfer many files at once and return a
  `files_sdk.TransferResult` with each file's outcome. See Directories and
  Many Files in the documentation.
- `folder.walk()` walks a remote folder tree as `os.walk()` walks a local one.
  `copy_and_wait()`, `move_and_wait()`, `delete_and_wait()` and
  `FileAction.wait()` wait for Files.com to finish. See Remote Files and
  Folders in the documentation.
- The package ships its type information (`py.typed`), so type checkers use
  the SDK's annotations, and records' docstrings list their attributes. Each
  attribute is annotated with the type the API sends it as, or `None`: dates
  and times are the text the API sends, and records nested in others are the
  JSON objects they are. The few values the API sends as any JSON value, such
  as a status's `data`, are `Any`. Nothing is converted except decimals, so a
  value you set yourself is stored as you set it.
- `UploadTuning(observer=...)` reports each upload's plan, decisions, waits,
  samples of the process's resources and a final record, for comparing runs.
- Uploads to Amazon S3 without concurrency tuning of their own use the scaled
  S3 policy, warming up from one part; `UploadTuning(startup=files_sdk.UploadStartup.AGGRESSIVE)`
  starts at that policy's start instead. An upload job's files share one
  target and what it learns. See the Uploads page of the documentation.
  When Files.com names no kind of storage, an upload whose first
  `begin_upload` answer shows every part it describes going to one ordinary S3
  multipart upload counts as one to Amazon S3. To tell, the SDK
  asks `begin_upload` for direct connection information unless `params` sets
  `with_direct_connection_info`; with it set to `False`, or with such
  information in the answer, the upload keeps the generic defaults.

## Records and lists

- A record's `update()` and `save()` change that object in place, to the
  server's copy of the record, and return `None`. In version 1.x, `update()`
  returned the response data, and `save()` on an existing record raised
  `AttributeError` after sending the update. Read the record from the object
  itself, or call the module's or a client's `update()`, which returns the
  record.
- An operation leaves the `params` dictionary you pass unchanged; in version
  1.x it added the path and ID values it sent, such as `id`, to it.
- A record's other operations that answer with a record or a list still
  return the response data as it came, and raise `APIConnectionError` if it
  is not a JSON object or array, as the module functions do for the records
  they return.
- Aliases such as `all()` for `list()` return what the operation they stand
  for returns; in version 1.x they returned `None`.
- A list ends at a missing or blank cursor, and `load_next_page()` after the
  last page sends no request. A list that receives a cursor it already
  followed raises `APIConnectionError` instead of fetching the same records
  again.
- `session.destroy()` logs out that session with one request.

## File attachments

Parameters of type file, such as `avatar_file` in `files_sdk.user.update`
or `file` in `files_sdk.style.update`, now send a file. Pass bytes, a binary
stream or a `files_sdk.Attachment`, as the README's File Attachments section
describes. In version 1.x, file content in one of these parameters raised
`APIConnectionError`, reporting a network error, and sent nothing. A JSON
file object such as `{"encoded_content": ..., "filename": ..., "type": ...}`
is still sent as given.

A request with an attachment is sent as `multipart/form-data`, or as JSON
when form fields would change one of its values or the file's name. Its
other parameters keep the values you give them either way. Requests without
an attachment are sent as JSON, as before.

## Remote mount backend decimals

`files_sdk.remote_mount_backend.create` and `update` take `min_free_cpu` and
`min_free_mem` as a `Decimal` or its exact text, such as `"12.5"`, as well as
a float, and send a decimal's digits exactly. A float is sent as the same
JSON number as before, with the precision a float has. Saving a new
`RemoteMountBackend` that has these values set now creates it; in version
1.x it raised `InvalidParameterError`.

## Packaging

The wheel installs only the `files_sdk` package. Earlier wheels also placed
`README.md` and `_VERSION` files directly in `site-packages`. The source
distribution contains the package and its metadata, and no tests.
