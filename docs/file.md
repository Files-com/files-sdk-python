# File

## Example File Object

```
{
  "id": 1,
  "path": "path/file.txt",
  "path_absolute": "path/file.txt",
  "created_by_id": 1,
  "created_by_api_key_id": 1,
  "created_by_as2_incoming_message_id": 1,
  "created_by_automation_id": 1,
  "created_by_bundle_registration_id": 1,
  "created_by_inbox_id": 1,
  "created_by_remote_server_id": 1,
  "created_by_sync_id": 1,
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
  "last_modified_by_sync_id": 1,
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
  "remote_server_id": 1,
  "headers": {
    "key": "example value"
  },
  "socks_ips": [
    "example"
  ],
  "internal_download_uri": "example",
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

* `id` (int64): File/Folder ID.  Used only for ExaVault compatibility API.  Do not use for other purposes, as this value will not always be set.
* `path` (string): File/Folder path. This must be slash-delimited, but it must neither start nor end with a slash. Maximum of 5000 characters.
* `path_absolute` (string): File/Folder absolute path for Bundle Trusted Relay use
* `created_by_id` (int64): User ID of the User who created the file/folder
* `created_by_api_key_id` (int64): ID of the API key that created the file/folder
* `created_by_as2_incoming_message_id` (int64): ID of the AS2 Incoming Message that created the file/folder
* `created_by_automation_id` (int64): ID of the Automation that created the file/folder
* `created_by_bundle_registration_id` (int64): ID of the Bundle Registration that created the file/folder
* `created_by_inbox_id` (int64): ID of the Inbox that created the file/folder
* `created_by_remote_server_id` (int64): ID of the Remote Server that created the file/folder
* `created_by_sync_id` (int64): ID of the Sync that created the file/folder
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
* `last_modified_by_sync_id` (int64): ID of the Sync that last modified the file/folder
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
* `remote_server_id` (int64): Used for internal bandwidth tracking
* `headers` (object): Used for internal url management
* `socks_ips` (array(string)): Used for internal url management
* `internal_download_uri` (string): For use with internal services and should also be with headers and socks_ips
* `download_uri` (string): Link to download file. Provided only in response to a download request.
* `priority_color` (string): Bookmark/priority color of file/folder
* `preview_id` (int64): File preview ID
* `preview` (Preview): File preview
* `copy_destination` (string): 
* `move_destination` (string): 
* `action` (string): The action to perform.  Can be `append`, `attachment`, `end`, `upload`, `put`, or may not exist
* `action_attributes` (object): Attributes to pass through for recording the Action.  Used for overriding action types (i.e. representing copy/move)
* `file` (object): 
* `crc32b` (string): 
* `length` (int64): Length of file.
* `mkdir_parents` (boolean): Create parent directories if they do not exist?
* `overwrite` (boolean): Overwrite existing file(s) in the destination?
* `part` (int64): Part if uploading a part.
* `parts` (int64): How many parts to fetch?
* `prefer_spdy` (boolean): 
* `ref` (string): 
* `restart` (int64): File byte offset to restart from.
* `copy_behaviors` (boolean): If copying a folder, also copy supported behaviors to the destination folder tree?
* `structure` (string): If copying folder, copy just the structure?
* `with_rename` (boolean): Allow file rename instead of overwrite?
* `inbox_registration_code` (string): 
* `bundle_registration_code` (string): 
* `buffered_upload` (boolean): If true, and the path refers to a destination not stored on Files.com (such as a remote server mount), the upload will be uploaded first to Files.com before being sent to the remote server mount. This can allow clients to upload using parallel parts to a remote server destination that does not offer parallel parts support natively.


---

## Download File

```
files_sdk.file.download(path, {
  "prefer_spdy": False,
  "with_previews": False,
  "with_priority_color": False,
  "full_document_preview": False
})
```

### Parameters

* `path` (string): Required - Path to operate on.
* `action` (string): Can be blank, `redirect` or `stat`.  If set to `stat`, we will return file information but without a download URL, and without logging a download.  If set to `redirect` we will serve a 302 redirect directly to the file.  This is used for integrations with Zapier, and is not recommended for most integrations.
* `bundle_registration_code` (string): 
* `prefer_spdy` (boolean): 
* `preview_size` (string): Request a preview size.  Can be `small` (default), `large`, `xlarge`, or `pdf`.
* `with_previews` (boolean): Include file preview information?
* `with_priority_color` (boolean): Include file priority color information?
* `full_document_preview` (boolean): If true, always return a proxied download uri


---

## Upload File

```
files_sdk.file.create(path, {
  "crc32": "70976923",
  "length": 1,
  "md5": "17c54824e9931a4688ca032d03f6663c",
  "mkdir_parents": False,
  "overwrite": False,
  "part": 1,
  "parts": 1,
  "prefer_spdy": False,
  "provided_mtime": "2000-01-01T01:00:00Z",
  "restart": 1,
  "sha1": "a94a8fe5ccb19ba61c4c0873d391e987982fbbd3",
  "sha256": "9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08",
  "size": 1,
  "copy_behaviors": False,
  "with_rename": False,
  "buffered_upload": False
})
```

### Parameters

* `path` (string): Required - Path to operate on.
* `copy_destination` (string): 
* `move_destination` (string): 
* `action` (string): The action to perform.  Can be `append`, `attachment`, `end`, `upload`, `put`, or may not exist
* `action_attributes` (object): Attributes to pass through for recording the Action.  Used for overriding action types (i.e. representing copy/move)
* `file` (object): 
* `crc32` (string): 
* `crc32b` (string): 
* `etags[etag]` (array(string)): etag identifier.
* `etags[part]` (array(int64)): Part number.
* `length` (int64): Length of file.
* `md5` (string): 
* `mkdir_parents` (boolean): Create parent directories if they do not exist?
* `overwrite` (boolean): Overwrite existing file(s) in the destination?
* `part` (int64): Part if uploading a part.
* `parts` (int64): How many parts to fetch?
* `prefer_spdy` (boolean): 
* `provided_mtime` (string): User provided modification time.
* `ref` (string): 
* `restart` (int64): File byte offset to restart from.
* `sha1` (string): 
* `sha256` (string): 
* `size` (int64): Size of file.
* `copy_behaviors` (boolean): If copying a folder, also copy supported behaviors to the destination folder tree?
* `structure` (string): If copying folder, copy just the structure?
* `with_rename` (boolean): Allow file rename instead of overwrite?
* `inbox_registration_code` (string): 
* `bundle_registration_code` (string): 
* `buffered_upload` (boolean): If true, and the path refers to a destination not stored on Files.com (such as a remote server mount), the upload will be uploaded first to Files.com before being sent to the remote server mount. This can allow clients to upload using parallel parts to a remote server destination that does not offer parallel parts support natively.


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
* `bundle_registration_code` (string): 


---

## Find File/Folder by ID

```
files_sdk.file.find_id(id, {
  "with_previews": False,
  "with_priority_color": False
})
```

### Parameters

* `id` (int64): Required - File/Folder ID
* `preview_size` (string): Request a preview size.  Can be `small` (default), `large`, `xlarge`, or `pdf`.
* `with_previews` (boolean): Include file preview information?
* `with_priority_color` (boolean): Include file priority color information?


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
* `bundle_registration_code` (string): 


---

## List the contents of a ZIP file

```
files_sdk.file.zip_list_contents(path)
```

### Parameters

* `path` (string): Required - Path to operate on.


---

## Copy File/Folder

```
files_sdk.file.copy(path, {
  "destination": "destination",
  "copy_behaviors": False,
  "structure": False,
  "overwrite": False
})
```

### Parameters

* `path` (string): Required - Path to operate on.
* `destination` (string): Required - Copy destination path.
* `copy_behaviors` (boolean): If copying a folder, also copy supported behaviors to the destination folder tree?
* `structure` (boolean): Copy structure only?
* `overwrite` (boolean): Overwrite existing file(s) in the destination?
* `bundle_registration_code` (string): 


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
* `bundle_registration_code` (string): 


---

## Transform a file and save the output to a destination path

```
files_sdk.file.transform(path, {
  "destination": "destination",
  "transform_type": "transform_type",
  "target_format": "target_format",
  "width": 1,
  "height": 1,
  "overwrite": False
})
```

### Parameters

* `path` (string): Required - Path to operate on.
* `destination` (string): Required - Destination file path for the transformed output.
* `transform_type` (string): Required - Transform type. Supported values are `image_convert`, `document_convert`, and `files_transform_script_execute`.
* `target_format` (string): Required - Destination format to create.
* `script` (string): Files TransformScript source. Required when transform_type is `files_transform_script_execute`.
* `width` (int64): Maximum output width for image_convert.
* `height` (int64): Maximum output height for image_convert.
* `overwrite` (boolean): Overwrite existing file in the destination?


---

## Decrypt a GPG-encrypted file and save it to a destination path

```
files_sdk.file.gpg_decrypt(path, {
  "destination": "destination",
  "gpg_key_partner_id": 1,
  "use_all_private_keys": False,
  "ignore_mdc_error": False,
  "overwrite": False
})
```

### Parameters

* `path` (string): Required - Path to operate on.
* `destination` (string): Required - Destination file path for the decrypted file.
* `gpg_key_ids` (array(int64)): GPG Key IDs to decrypt with. If omitted, every accessible private GPG key in the source workspace is used.
* `gpg_key_partner_id` (int64): Partner ID whose GPG keys should be used for decryption.
* `use_all_private_keys` (boolean): Use every accessible private GPG key in the source workspace for decryption.
* `ignore_mdc_error` (boolean): Ignore errors from the MDC (modification detection code) check.
* `overwrite` (boolean): Overwrite existing file in the destination?


---

## Encrypt a file with GPG and save it to a destination path

```
files_sdk.file.gpg_encrypt(path, {
  "destination": "destination",
  "gpg_key_partner_id": 1,
  "signing_key_id": 1,
  "armor": False,
  "overwrite": False
})
```

### Parameters

* `path` (string): Required - Path to operate on.
* `destination` (string): Required - Destination file path for the encrypted file.
* `gpg_key_ids` (array(int64)): GPG Key IDs to encrypt with.
* `gpg_key_partner_id` (int64): Partner ID whose GPG keys should be used for encryption.
* `signing_key_id` (int64): Optional GPG Key ID to sign with.
* `armor` (boolean): Output ASCII-armored encrypted data.
* `overwrite` (boolean): Overwrite existing file in the destination?


---

## Extract a ZIP file to a destination folder

```
files_sdk.file.unzip(path, {
  "destination": "destination",
  "overwrite": False
})
```

### Parameters

* `path` (string): Required - ZIP file path to extract.
* `destination` (string): Required - Destination folder path for extracted files.
* `filename` (string): Optional single entry filename to extract.
* `overwrite` (boolean): Overwrite existing files in the destination?


---

## Create a ZIP from one or more paths and save it to a destination path

```
files_sdk.file.zip({
  "paths": "paths",
  "destination": "destination",
  "overwrite": False
})
```

### Parameters

* `paths` (array(string)): Required - Paths to include in the ZIP.
* `destination` (string): Required - Destination file path for the ZIP.
* `overwrite` (boolean): Overwrite existing file in the destination?


---

## Begin File Upload

```
files_sdk.file.begin_upload(path, {
  "mkdir_parents": False,
  "part": 1,
  "parts": 1,
  "prefer_spdy": False,
  "ref": "upload-1",
  "restart": 1,
  "size": 1,
  "with_rename": False,
  "buffered_upload": False
})
```

### Parameters

* `path` (string): Required - Path to operate on.
* `mkdir_parents` (boolean): Create parent directories if they do not exist?
* `part` (int64): Part if uploading a part.
* `parts` (int64): How many parts to fetch?
* `prefer_spdy` (boolean): 
* `ref` (string): 
* `restart` (int64): File byte offset to restart from.
* `size` (int64): Total bytes of file being uploaded (include bytes being retained if appending/restarting).
* `with_rename` (boolean): Allow file rename instead of overwrite?
* `action` (string): 
* `bundle_registration_code` (string): 
* `buffered_upload` (boolean): If true, and the path refers to a destination not stored on Files.com (such as a remote server mount), the upload will be uploaded first to Files.com before being sent to the remote server mount. This can allow clients to upload using parallel parts to a remote server destination that does not offer parallel parts support natively.


---

## Download File

```
file = files_sdk.file.find(path)
file.download({
  "prefer_spdy": False,
  "with_previews": False,
  "with_priority_color": False,
  "full_document_preview": False
})
```

### Parameters

* `path` (string): Required - Path to operate on.
* `action` (string): Can be blank, `redirect` or `stat`.  If set to `stat`, we will return file information but without a download URL, and without logging a download.  If set to `redirect` we will serve a 302 redirect directly to the file.  This is used for integrations with Zapier, and is not recommended for most integrations.
* `bundle_registration_code` (string): 
* `prefer_spdy` (boolean): 
* `preview_size` (string): Request a preview size.  Can be `small` (default), `large`, `xlarge`, or `pdf`.
* `with_previews` (boolean): Include file preview information?
* `with_priority_color` (boolean): Include file priority color information?
* `full_document_preview` (boolean): If true, always return a proxied download uri


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
* `bundle_registration_code` (string): 


---

## List the contents of a ZIP file

```
file = files_sdk.file.find(path)
file.zip_list_contents()
```

### Parameters

* `path` (string): Required - Path to operate on.


---

## Copy File/Folder

```
file = files_sdk.file.find(path)
file.copy({
  "destination": "destination",
  "copy_behaviors": False,
  "structure": False,
  "overwrite": False
})
```

### Parameters

* `path` (string): Required - Path to operate on.
* `destination` (string): Required - Copy destination path.
* `copy_behaviors` (boolean): If copying a folder, also copy supported behaviors to the destination folder tree?
* `structure` (boolean): Copy structure only?
* `overwrite` (boolean): Overwrite existing file(s) in the destination?
* `bundle_registration_code` (string): 


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
* `bundle_registration_code` (string): 


---

## Transform a file and save the output to a destination path

```
file = files_sdk.file.find(path)
file.transform({
  "destination": "destination",
  "transform_type": "transform_type",
  "target_format": "target_format",
  "width": 1,
  "height": 1,
  "overwrite": False
})
```

### Parameters

* `path` (string): Required - Path to operate on.
* `destination` (string): Required - Destination file path for the transformed output.
* `transform_type` (string): Required - Transform type. Supported values are `image_convert`, `document_convert`, and `files_transform_script_execute`.
* `target_format` (string): Required - Destination format to create.
* `script` (string): Files TransformScript source. Required when transform_type is `files_transform_script_execute`.
* `width` (int64): Maximum output width for image_convert.
* `height` (int64): Maximum output height for image_convert.
* `overwrite` (boolean): Overwrite existing file in the destination?


---

## Decrypt a GPG-encrypted file and save it to a destination path

```
file = files_sdk.file.find(path)
file.gpg_decrypt({
  "destination": "destination",
  "gpg_key_partner_id": 1,
  "use_all_private_keys": False,
  "ignore_mdc_error": False,
  "overwrite": False
})
```

### Parameters

* `path` (string): Required - Path to operate on.
* `destination` (string): Required - Destination file path for the decrypted file.
* `gpg_key_ids` (array(int64)): GPG Key IDs to decrypt with. If omitted, every accessible private GPG key in the source workspace is used.
* `gpg_key_partner_id` (int64): Partner ID whose GPG keys should be used for decryption.
* `use_all_private_keys` (boolean): Use every accessible private GPG key in the source workspace for decryption.
* `ignore_mdc_error` (boolean): Ignore errors from the MDC (modification detection code) check.
* `overwrite` (boolean): Overwrite existing file in the destination?


---

## Encrypt a file with GPG and save it to a destination path

```
file = files_sdk.file.find(path)
file.gpg_encrypt({
  "destination": "destination",
  "gpg_key_partner_id": 1,
  "signing_key_id": 1,
  "armor": False,
  "overwrite": False
})
```

### Parameters

* `path` (string): Required - Path to operate on.
* `destination` (string): Required - Destination file path for the encrypted file.
* `gpg_key_ids` (array(int64)): GPG Key IDs to encrypt with.
* `gpg_key_partner_id` (int64): Partner ID whose GPG keys should be used for encryption.
* `signing_key_id` (int64): Optional GPG Key ID to sign with.
* `armor` (boolean): Output ASCII-armored encrypted data.
* `overwrite` (boolean): Overwrite existing file in the destination?


---

## Extract a ZIP file to a destination folder

```
file = files_sdk.file.find(path)
file.unzip({
  "destination": "destination",
  "overwrite": False
})
```

### Parameters

* `path` (string): Required - ZIP file path to extract.
* `destination` (string): Required - Destination folder path for extracted files.
* `filename` (string): Optional single entry filename to extract.
* `overwrite` (boolean): Overwrite existing files in the destination?


---

## Begin File Upload

```
file = files_sdk.file.find(path)
file.begin_upload({
  "mkdir_parents": False,
  "part": 1,
  "parts": 1,
  "prefer_spdy": False,
  "ref": "upload-1",
  "restart": 1,
  "size": 1,
  "with_rename": False,
  "buffered_upload": False
})
```

### Parameters

* `path` (string): Required - Path to operate on.
* `mkdir_parents` (boolean): Create parent directories if they do not exist?
* `part` (int64): Part if uploading a part.
* `parts` (int64): How many parts to fetch?
* `prefer_spdy` (boolean): 
* `ref` (string): 
* `restart` (int64): File byte offset to restart from.
* `size` (int64): Total bytes of file being uploaded (include bytes being retained if appending/restarting).
* `with_rename` (boolean): Allow file rename instead of overwrite?
* `action` (string): 
* `bundle_registration_code` (string): 
* `buffered_upload` (boolean): If true, and the path refers to a destination not stored on Files.com (such as a remote server mount), the upload will be uploaded first to Files.com before being sent to the remote server mount. This can allow clients to upload using parallel parts to a remote server destination that does not offer parallel parts support natively.
