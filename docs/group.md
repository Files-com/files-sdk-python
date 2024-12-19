# Group

## Example Group Object

```
{
  "id": 1,
  "name": "owners",
  "allowed_ips": "10.0.0.0/8\n127.0.0.1",
  "admin_ids": "1",
  "notes": "example",
  "user_ids": "1",
  "usernames": "example",
  "ftp_permission": True,
  "sftp_permission": True,
  "dav_permission": True,
  "restapi_permission": True,
  "site_id": 1
}
```

* `id` (int64): Group ID
* `name` (string): Group name
* `allowed_ips` (string): A list of allowed IPs if applicable.  Newline delimited
* `admin_ids` (string): Comma-delimited list of user IDs who are group administrators (separated by commas)
* `notes` (string): Notes about this group
* `user_ids` (string): Comma-delimited list of user IDs who belong to this group (separated by commas)
* `usernames` (string): Comma-delimited list of usernames who belong to this group (separated by commas)
* `ftp_permission` (boolean): If true, users in this group can use FTP to login.  This will override a false value of `ftp_permission` on the user level.
* `sftp_permission` (boolean): If true, users in this group can use SFTP to login.  This will override a false value of `sftp_permission` on the user level.
* `dav_permission` (boolean): If true, users in this group can use WebDAV to login.  This will override a false value of `dav_permission` on the user level.
* `restapi_permission` (boolean): If true, users in this group can use the REST API to login.  This will override a false value of `restapi_permission` on the user level.
* `site_id` (int64): Site ID


---

## List Groups

```
files_sdk.group.list({
  "include_parent_site_groups": False
})
```

### Parameters

* `cursor` (string): Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
* `per_page` (int64): Number of records to show per page.  (Max: 10,000, 1,000 or less is recommended).
* `sort_by` (object): If set, sort records by the specified field in either `asc` or `desc` direction. Valid fields are `site_id` and `name`.
* `filter` (object): If set, return records where the specified field is equal to the supplied value. Valid fields are `name`.
* `filter_prefix` (object): If set, return records where the specified field is prefixed by the supplied value. Valid fields are `name`.
* `ids` (string): Comma-separated list of group ids to include in results.
* `include_parent_site_groups` (boolean): Include groups from the parent site.


---

## Show Group

```
files_sdk.group.find(id)
```

### Parameters

* `id` (int64): Required - Group ID.


---

## Create Group

```
files_sdk.group.create({
  "notes": "example",
  "user_ids": "1",
  "admin_ids": "1",
  "ftp_permission": True,
  "sftp_permission": True,
  "dav_permission": True,
  "restapi_permission": True,
  "allowed_ips": "10.0.0.0/8\n127.0.0.1",
  "name": "name"
})
```

### Parameters

* `notes` (string): Group notes.
* `user_ids` (string): A list of user ids. If sent as a string, should be comma-delimited.
* `admin_ids` (string): A list of group admin user ids. If sent as a string, should be comma-delimited.
* `ftp_permission` (boolean): If true, users in this group can use FTP to login.  This will override a false value of `ftp_permission` on the user level.
* `sftp_permission` (boolean): If true, users in this group can use SFTP to login.  This will override a false value of `sftp_permission` on the user level.
* `dav_permission` (boolean): If true, users in this group can use WebDAV to login.  This will override a false value of `dav_permission` on the user level.
* `restapi_permission` (boolean): If true, users in this group can use the REST API to login.  This will override a false value of `restapi_permission` on the user level.
* `allowed_ips` (string): A list of allowed IPs if applicable.  Newline delimited
* `name` (string): Required - Group name.


---

## Update Group

```
files_sdk.group.update(id, {
  "notes": "example",
  "user_ids": "1",
  "admin_ids": "1",
  "ftp_permission": True,
  "sftp_permission": True,
  "dav_permission": True,
  "restapi_permission": True,
  "allowed_ips": "10.0.0.0/8\n127.0.0.1",
  "name": "owners"
})
```

### Parameters

* `id` (int64): Required - Group ID.
* `notes` (string): Group notes.
* `user_ids` (string): A list of user ids. If sent as a string, should be comma-delimited.
* `admin_ids` (string): A list of group admin user ids. If sent as a string, should be comma-delimited.
* `ftp_permission` (boolean): If true, users in this group can use FTP to login.  This will override a false value of `ftp_permission` on the user level.
* `sftp_permission` (boolean): If true, users in this group can use SFTP to login.  This will override a false value of `sftp_permission` on the user level.
* `dav_permission` (boolean): If true, users in this group can use WebDAV to login.  This will override a false value of `dav_permission` on the user level.
* `restapi_permission` (boolean): If true, users in this group can use the REST API to login.  This will override a false value of `restapi_permission` on the user level.
* `allowed_ips` (string): A list of allowed IPs if applicable.  Newline delimited
* `name` (string): Group name.


---

## Delete Group

```
files_sdk.group.delete(id)
```

### Parameters

* `id` (int64): Required - Group ID.


---

## Update Group

```
group = files_sdk.group.find(id)
group.update({
  "notes": "example",
  "user_ids": "1",
  "admin_ids": "1",
  "ftp_permission": True,
  "sftp_permission": True,
  "dav_permission": True,
  "restapi_permission": True,
  "allowed_ips": "10.0.0.0/8\n127.0.0.1",
  "name": "owners"
})
```

### Parameters

* `id` (int64): Required - Group ID.
* `notes` (string): Group notes.
* `user_ids` (string): A list of user ids. If sent as a string, should be comma-delimited.
* `admin_ids` (string): A list of group admin user ids. If sent as a string, should be comma-delimited.
* `ftp_permission` (boolean): If true, users in this group can use FTP to login.  This will override a false value of `ftp_permission` on the user level.
* `sftp_permission` (boolean): If true, users in this group can use SFTP to login.  This will override a false value of `sftp_permission` on the user level.
* `dav_permission` (boolean): If true, users in this group can use WebDAV to login.  This will override a false value of `dav_permission` on the user level.
* `restapi_permission` (boolean): If true, users in this group can use the REST API to login.  This will override a false value of `restapi_permission` on the user level.
* `allowed_ips` (string): A list of allowed IPs if applicable.  Newline delimited
* `name` (string): Group name.


---

## Delete Group

```
group = files_sdk.group.find(id)
group.delete()
```

### Parameters

* `id` (int64): Required - Group ID.
