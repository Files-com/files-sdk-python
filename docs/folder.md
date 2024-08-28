# Folder

## Example Folder Object

```
{
  "path": "path/file.txt",
  "created_by_id": 1,
  "created_by_api_key_id": 1,
  "created_by_as2_incoming_message_id": 1,
  "created_by_automation_id": 1,
  "created_by_bundle_registration_id": 1,
  "created_by_inbox_id": 1,
  "created_by_remote_server_id": 1,
  "created_by_remote_server_sync_id": 1,
  "custom_metadata": {
    "key": "value"
  },
  "display_name": "file.txt",
  "type": "file",
  "size": 1024,
  "created_at": "2000-01-01T01:00:00Z",
  "last_modified_by_id": 1,
  "last_modified_by_api_key_id": 1,
  "last_modified_by_automation_id": 1,
  "last_modified_by_bundle_registration_id": 1,
  "last_modified_by_remote_server_id": 1,
  "last_modified_by_remote_server_sync_id": 1,
  "mtime": "2000-01-01T01:00:00Z",
  "provided_mtime": "2000-01-01T01:00:00Z",
  "crc32": "70976923",
  "md5": "17c54824e9931a4688ca032d03f6663c",
  "mime_type": "application/octet-stream",
  "region": "us-east-1",
  "permissions": "rwd",
  "subfolders_locked?": True,
  "is_locked": True,
  "download_uri": "https://mysite.files.com/...",
  "priority_color": "red",
  "preview_id": 1,
  "preview": {
    "id": 1,
    "status": "complete",
    "download_uri": "https://mysite.files.com/...",
    "type": "image",
    "size": "large"
  }
}
```

* `path` (string): File/Folder path. This must be slash-delimited, but it must neither start nor end with a slash. Maximum of 5000 characters.
* `created_by_id` (int64): User ID of the User who created the file/folder
* `created_by_api_key_id` (int64): ID of the API key that created the file/folder
* `created_by_as2_incoming_message_id` (int64): ID of the AS2 Incoming Message that created the file/folder
* `created_by_automation_id` (int64): ID of the Automation that created the file/folder
* `created_by_bundle_registration_id` (int64): ID of the Bundle Registration that created the file/folder
* `created_by_inbox_id` (int64): ID of the Inbox that created the file/folder
* `created_by_remote_server_id` (int64): ID of the Remote Server that created the file/folder
* `created_by_remote_server_sync_id` (int64): ID of the Remote Server Sync that created the file/folder
* `custom_metadata` (object): Custom metadata map of keys and values. Limited to 32 keys, 256 characters per key and 1024 characters per value.
* `display_name` (string): File/Folder display name
* `type` (string): Type: `directory` or `file`.
* `size` (int64): File/Folder size
* `created_at` (date-time): File created date/time
* `last_modified_by_id` (int64): User ID of the User who last modified the file/folder
* `last_modified_by_api_key_id` (int64): ID of the API key that last modified the file/folder
* `last_modified_by_automation_id` (int64): ID of the Automation that last modified the file/folder
* `last_modified_by_bundle_registration_id` (int64): ID of the Bundle Registration that last modified the file/folder
* `last_modified_by_remote_server_id` (int64): ID of the Remote Server that last modified the file/folder
* `last_modified_by_remote_server_sync_id` (int64): ID of the Remote Server Sync that last modified the file/folder
* `mtime` (date-time): File last modified date/time, according to the server.  This is the timestamp of the last Files.com operation of the file, regardless of what modified timestamp was sent.
* `provided_mtime` (date-time): File last modified date/time, according to the client who set it.  Files.com allows desktop, FTP, SFTP, and WebDAV clients to set modified at times.  This allows Desktop<->Cloud syncing to preserve modified at times.
* `crc32` (string): File CRC32 checksum. This is sometimes delayed, so if you get a blank response, wait and try again.
* `md5` (string): File MD5 checksum. This is sometimes delayed, so if you get a blank response, wait and try again.
* `mime_type` (string): MIME Type.  This is determined by the filename extension and is not stored separately internally.
* `region` (string): Region location
* `permissions` (string): A short string representing the current user's permissions.  Can be `r` (Read),`w` (Write),`d` (Delete), `l` (List) or any combination
* `subfolders_locked?` (boolean): Are subfolders locked and unable to be modified?
* `is_locked` (boolean): Is this folder locked and unable to be modified?
* `download_uri` (string): Link to download file. Provided only in response to a download request.
* `priority_color` (string): Bookmark/priority color of file/folder
* `preview_id` (int64): File preview ID
* `preview` (Preview): File preview
* `mkdir_parents` (boolean): Create parent directories if they do not exist?


---

## List Folders by path

```
files_sdk.folder.list_for(path, {
  "search_all": True,
  "with_previews": True,
  "with_priority_color": True
})
```

### Parameters

* `cursor` (string): Send cursor to resume an existing list from the point at which you left off.  Get a cursor from an existing list via the X-Files-Cursor-Next header or the X-Files-Cursor-Prev header.
* `per_page` (int64): Number of records to show per page.  (Max: 10,000, 1,000 or less is recommended).
* `path` (string): Required - Path to operate on.
* `filter` (string): If specified, will filter folders/files list by name. Ignores text before last `/`. Wildcards of `*` and `?` are acceptable here.
* `preview_size` (string): Request a preview size.  Can be `small` (default), `large`, `xlarge`, or `pdf`.
* `sort_by` (object): Search by field and direction. Valid fields are `path`, `size`, `modified_at_datetime`, `provided_modified_at`.  Valid directions are `asc` and `desc`.  Defaults to `{"path":"asc"}`.
* `search` (string): If `search_all` is `true`, provide the search string here.  Otherwise, this parameter acts like an alias of `filter`.
* `search_all` (boolean): Search entire site?  If set, we will ignore the folder path provided and search the entire site.  This is the same API used by the search bar in the UI.  Search results are a best effort, not real time, and not guaranteed to match every file.  This field should only be used for ad-hoc (human) searching, and not as part of an automated process.
* `with_previews` (boolean): Include file previews?
* `with_priority_color` (boolean): Include file priority color information?


---

## Create folder

```
files_sdk.folder.create(path, {
  "mkdir_parents": True,
  "provided_mtime": "2000-01-01T01:00:00Z"
})
```

### Parameters

* `path` (string): Required - Path to operate on.
* `mkdir_parents` (boolean): Create parent directories if they do not exist?
* `provided_mtime` (string): User provided modification time.
