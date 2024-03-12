# Files.com Python Client

The Files.com Python client library provides convenient access to the Files.com API from applications written in the Python language.


## Installation

To install the package:

    pip3 install Files.com


### Requirements

* Python 3.5+
* requests


## Usage

    import files_sdk


### Authentication

There are multiple ways to authenticate to the API.


#### Global API Key

You can set an API key globally, like this:

    files_sdk.set_api_key("my-key")


#### Per-Request API Key

Or, you can pass an API key per-request, in the Options dictionary at the end
of every method.  Like this:

    files_sdk.group.list({}, {"api_key": "my-key"})

That key will automatically be used for any followup actions that occur
on models returned from the API.


#### User Session

Or, you can open a user session by calling `files_sdk.session.create`

    session = files_sdk.session.create({"username": "uname", "password": "pwd"})

Then use it as follows:

    files_sdk.group.list({}, {"session": session})

Or use if for all subsequent API calls globally like this:

    session = files_sdk.session.create({"username": "uname", "password": "pwd"})
    files_sdk.set_session(session)


### Setting Global Options

You can set the following global options directly on the `files_sdk` module:

 * `files_sdk.open_timeout` - open timeout in seconds (default: 30)
 * `files_sdk.read_timeout` - read timeout in seconds (default: 80)
 * `files_sdk.initial_network_retry_delay` - initial retry delay in seconds (default: 0.5)
 * `files_sdk.max_network_retries` - max retries (default: 3)
 * `files_sdk.max_network_retry_delay` - max retry delay in seconds (default: 2)
 * `files_sdk.base_url` - to point this client at an on-premise
   installation of Files.com, set its URL here.
 * `files_sdk.console_log_level` - set to `None`, `info`, or `debug`, this enables printing
   of messages to stderr in addition to normal logging


#### Log Level

This SDK utilizes the standard Python logging framework. It will respect the global log level
and you can set the module specific log level and other logging settings by getting the logger
object in the standard manner as shown below:

    import logging

    logging.getLogger("files_sdk")


### Error Handling

Unexpected errors when attempting to connect to the API inherit from the base level `Error` class. They all contain a `__str__()`
implementation to describe what went wrong.


#### Unable to connect to the API

```python
try:
    for f in files_sdk.folder.list_for("/").auto_paging_iter():
        print(f.type, f.path)
except files_sdk.error.APIConnectionError as e:
    print("Unable to list root folder: " + str(e))
```

Errors from the API inherit from `ApiError`. They all contain more properties to describe the error such as `code`, `headers`, etc.


#### Path does not exist

```python
try:
    for f in files_sdk.folder.list_for("/missing").auto_paging_iter():
        print(f.type, f.path)
except files_sdk.error.FolderNotFoundError as e:
    print(f"Unable to list folder: {e.code}")
```


### File Operations

This SDK allows both file based transfer and data based transfer. Please see the examples below.


#### File Download

The second parameter is optional and will simply use the remote filename by default.

    files_sdk.file.download_file("/remote.txt", "local.txt")


#### File Upload

The second parameter is optional and will simply use the local filename by default.

    files_sdk.file.upload_file("local.txt", "/remote.txt")

If the parent directories do not already exist, they can be automatically created by passing
`mkdir_parents` in the `params`.

    files_sdk.file.upload_file("local.txt", "/uploads/remote.txt", params={"mkdir_parents": True})


#### List root folder

    for f in files_sdk.folder.list_for("/").auto_paging_iter():
        print(f.type, f.path)


#### Writing a file example (string)

    with files_sdk.file.open("foo.txt", 'w') as f:
        f.write("contents")


#### Writing a file example (binary)

    with files_sdk.file.open("foo.txt", 'wb') as f:
        f.write(b"contents")


#### Reading a file example (string)

    with files_sdk.open("foo.txt", 'r') as f:
        print(f.read())


#### Reading a file example (binary)

    with files_sdk.open("foo.txt", 'rb') as f:
        print(f.read())


### List Responses and Cursor Paging

List responses for APIs with cursor support will return an iterable object
which contains a single page of records. It has a built-in `auto_paging_iter`
method to iterate through the pages, making the additional API calls
as needed.


#### Iterating with with auto_paging_iter

    list_obj = files_sdk.folder.list_for('/')

    for f in list_obj.auto_paging_iter():
        print(f.type, f.path)


#### Iterating manually

    list_obj = files_sdk.folder.list_for('/')

    for f in list_obj:
        print(f.type, f.path)

    while list_obj.has_next_page:
        list_obj.load_next_page()
        for f in list_obj:
            print(f.type, f.path)


### Comparing Case insensitive files and paths

For related documentation see [Case Sensitivity Documentation](https://www.files.com/docs/files-and-folders/file-system-semantics/case-sensitivity).

    if files_sdk.path_util.is_same("Fïłèńämê.Txt", "filename.txt"):
        print("Paths are the same")


### Additional Object Documentation

Additional docs are available at https://developers.files.com/ and also
in the `docs/` subdirectory of this directory.


### Pydoc Generated Documentation coming in the future

We hope to add Pydoc documentation to a future release.


## Getting Support

The Files.com team is happy to help with any SDK Integration challenges you
may face.

Just email support@files.com and we'll get the process started.
