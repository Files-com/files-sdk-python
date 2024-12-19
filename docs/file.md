# File

## Example File Object

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
  "sha1": "a94a8fe5ccb19ba61c4c0873d391e987982fbbd3",
  "sha256": "9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08",
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
* `sha1` (string): File SHA1 checksum. This is sometimes delayed, so if you get a blank response, wait and try again.
* `sha256` (string): File SHA256 checksum. This is sometimes delayed, so if you get a blank response, wait and try again.
* `mime_type` (string): MIME Type.  This is determined by the filename extension and is not stored separately internally.
* `region` (string): Region location
* `permissions` (string): A short string representing the current user's permissions.  Can be `r` (Read),`w` (Write),`d` (Delete), `l` (List) or any combination
* `subfolders_locked?` (boolean): Are subfolders locked and unable to be modified?
* `is_locked` (boolean): Is this folder locked and unable to be modified?
* `download_uri` (string): Link to download file. Provided only in response to a download request.
* `priority_color` (string): Bookmark/priority color of file/folder
* `preview_id` (int64): File preview ID
* `preview` (Preview): File preview
* `action` (string): The action to perform.  Can be `append`, `attachment`, `end`, `upload`, `put`, or may not exist
* `length` (int64): Length of file.
* `mkdir_parents` (boolean): Create parent directories if they do not exist?
* `part` (int64): Part if uploading a part.
* `parts` (int64): How many parts to fetch?
* `ref` (string): 
* `restart` (int64): File byte offset to restart from.
* `structure` (string): If copying folder, copy just the structure?
* `with_rename` (boolean): Allow file rename instead of overwrite?


---

## Download File

```
files_sdk.file.download(path, {
  "with_previews": False,
  "with_priority_color": False
})
```

### Parameters

* `path` (string): Required - Path to operate on.
* `action` (string): Can be blank, `redirect` or `stat`.  If set to `stat`, we will return file information but without a download URL, and without logging a download.  If set to `redirect` we will serve a 302 redirect directly to the file.  This is used for integrations with Zapier, and is not recommended for most integrations.
* `preview_size` (string): Request a preview size.  Can be `small` (default), `large`, `xlarge`, or `pdf`.
* `with_previews` (boolean): Include file preview information?
* `with_priority_color` (boolean): Include file priority color information?


---

## Upload File

```
files_sdk.file.create(path, {
  "length": 1,
  "mkdir_parents": False,
  "part": 1,
  "parts": 1,
  "provided_mtime": "2000-01-01T01:00:00Z",
  "restart": 1,
  "size": 1,
  "with_rename": False
})
```

### Parameters

* `path` (string): Required - Path to operate on.
* `action` (string): The action to perform.  Can be `append`, `attachment`, `end`, `upload`, `put`, or may not exist
* `etags[etag]` (array(string)): etag identifier.
* `etags[part]` (array(int64)): Part number.
* `length` (int64): Length of file.
* `mkdir_parents` (boolean): Create parent directories if they do not exist?
* `part` (int64): Part if uploading a part.
* `parts` (int64): How many parts to fetch?
* `provided_mtime` (string): User provided modification time.
* `ref` (string): 
* `restart` (int64): File byte offset to restart from.
* `size` (int64): Size of file.
* `structure` (string): If copying folder, copy just the structure?
* `with_rename` (boolean): Allow file rename instead of overwrite?


---

## Update File/Folder Metadata

```
files_sdk.file.update(path, {
  "custom_metadata": {"key":"value"},
  "provided_mtime": "2000-01-01T01:00:00Z",
  "priority_color": "red"
})
```

### Parameters

* `path` (string): Required - Path to operate on.
* `custom_metadata` (object): Custom metadata map of keys and values. Limited to 32 keys, 256 characters per key and 1024 characters per value.
* `provided_mtime` (string): Modified time of file.
* `priority_color` (string): Priority/Bookmark color of file.


---

## Delete File/Folder

```
files_sdk.file.delete(path, {
  "recursive": False
})
```

### Parameters

* `path` (string): Required - Path to operate on.
* `recursive` (boolean): If true, will recursively delete folders.  Otherwise, will error on non-empty folders.


---

## Find File/Folder by Path

```
files_sdk.file.find(path, {
  "with_previews": False,
  "with_priority_color": False
})
```

### Parameters

* `path` (string): Required - Path to operate on.
* `preview_size` (string): Request a preview size.  Can be `small` (default), `large`, `xlarge`, or `pdf`.
* `with_previews` (boolean): Include file preview information?
* `with_priority_color` (boolean): Include file priority color information?


---

## Copy File/Folder

```
files_sdk.file.copy(path, {
  "destination": "destination",
  "structure": False,
  "overwrite": False
})
```

### Parameters

* `path` (string): Required - Path to operate on.
* `destination` (string): Required - Copy destination path.
* `structure` (boolean): Copy structure only?
* `overwrite` (boolean): Overwrite existing file(s) in the destination?


---

## Move File/Folder

```
files_sdk.file.move(path, {
  "destination": "destination",
  "overwrite": False
})
```

### Parameters

* `path` (string): Required - Path to operate on.
* `destination` (string): Required - Move destination path.
* `overwrite` (boolean): Overwrite existing file(s) in the destination?


---

## Begin File Upload

```
files_sdk.file.begin_upload(path, {
  "mkdir_parents": False,
  "part": 1,
  "parts": 1,
  "ref": "upload-1",
  "restart": 1,
  "size": 1,
  "with_rename": False
})
```

### Parameters

* `path` (string): Required - Path to operate on.
* `mkdir_parents` (boolean): Create parent directories if they do not exist?
* `part` (int64): Part if uploading a part.
* `parts` (int64): How many parts to fetch?
* `ref` (string): 
* `restart` (int64): File byte offset to restart from.
* `size` (int64): Total bytes of file being uploaded (include bytes being retained if appending/restarting).
* `with_rename` (boolean): Allow file rename instead of overwrite?


---

## Download File

```
file = files_sdk.file.find(path)
file.download({
  "with_previews": False,
  "with_priority_color": False
})
```

### Parameters

* `path` (string): Required - Path to operate on.
* `action` (string): Can be blank, `redirect` or `stat`.  If set to `stat`, we will return file information but without a download URL, and without logging a download.  If set to `redirect` we will serve a 302 redirect directly to the file.  This is used for integrations with Zapier, and is not recommended for most integrations.
* `preview_size` (string): Request a preview size.  Can be `small` (default), `large`, `xlarge`, or `pdf`.
* `with_previews` (boolean): Include file preview information?
* `with_priority_color` (boolean): Include file priority color information?


---

## Update File/Folder Metadata

```
file = files_sdk.file.find(path)
file.update({
  "custom_metadata": {"key":"value"},
  "provided_mtime": "2000-01-01T01:00:00Z",
  "priority_color": "red"
})
```

### Parameters

* `path` (string): Required - Path to operate on.
* `custom_metadata` (object): Custom metadata map of keys and values. Limited to 32 keys, 256 characters per key and 1024 characters per value.
* `provided_mtime` (string): Modified time of file.
* `priority_color` (string): Priority/Bookmark color of file.


---

## Delete File/Folder

```
file = files_sdk.file.find(path)
file.delete({
  "recursive": False
})
```

### Parameters

* `path` (string): Required - Path to operate on.
* `recursive` (boolean): If true, will recursively delete folders.  Otherwise, will error on non-empty folders.


---

## Copy File/Folder

```
file = files_sdk.file.find(path)
file.copy({
  "destination": "destination",
  "structure": False,
  "overwrite": False
})
```

### Parameters

* `path` (string): Required - Path to operate on.
* `destination` (string): Required - Copy destination path.
* `structure` (boolean): Copy structure only?
* `overwrite` (boolean): Overwrite existing file(s) in the destination?


---

## Move File/Folder

```
file = files_sdk.file.find(path)
file.move({
  "destination": "destination",
  "overwrite": False
})
```

### Parameters

* `path` (string): Required - Path to operate on.
* `destination` (string): Required - Move destination path.
* `overwrite` (boolean): Overwrite existing file(s) in the destination?


---

## Begin File Upload

```
file = files_sdk.file.find(path)
file.begin_upload({
  "mkdir_parents": False,
  "part": 1,
  "parts": 1,
  "ref": "upload-1",
  "restart": 1,
  "size": 1,
  "with_rename": False
})
```

### Parameters

* `path` (string): Required - Path to operate on.
* `mkdir_parents` (boolean): Create parent directories if they do not exist?
* `part` (int64): Part if uploading a part.
* `parts` (int64): How many parts to fetch?
* `ref` (string): 
* `restart` (int64): File byte offset to restart from.
* `size` (int64): Total bytes of file being uploaded (include bytes being retained if appending/restarting).
* `with_rename` (boolean): Allow file rename instead of overwrite?
