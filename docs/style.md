# Style

## Example Style Object

The API sends each `Style` record as JSON, such as:

```json
{
  "id": 1,
  "path": "example",
  "logo": "https://mysite.files.com/...",
  "logo_click_href": "https://www.example.com",
  "thumbnail": {
    "name": "My logo",
    "uri": "https://mysite.files.com/.../my_image.png"
  }
}
```

* `id` (int64): Style ID
* `path` (string): Folder path. This must be slash-delimited, but it must neither start nor end with a slash. Maximum of 5000 characters.
* `logo` (Image): Logo
* `logo_click_href` (string): URL to open when a public visitor clicks the logo
* `thumbnail` (Image): Logo thumbnail
* `file` (file): Logo for custom branding. Required when creating a new style.

The functions below use the module's settings. Each is also a method of a client's
`client.style` resource, such as
`client.style.find(...)`,
which uses that client's configuration instead.


---

## Show Style

```python
files_sdk.style.find(path)
```

### Parameters

* `path` (string): Required - Style path.


---

## Update Style

```python
files_sdk.style.update(path, {
  "logo_click_href": "https://www.example.com"
})
```

### Parameters

* `path` (string): Required - Style path.
* `file` (file): Logo for custom branding. Required when creating a new style. Pass bytes, a binary stream, a `files_sdk.Attachment` or a JSON file object. See [File Attachments](../README.md#file-attachments).
* `logo_click_href` (string): URL to open when a public visitor clicks the logo.


---

## Delete Style

```python
files_sdk.style.delete(path)
```

### Parameters

* `path` (string): Required - Style path.


---

## Update Style

```python
style = files_sdk.style.find(path)
style.update({
  "logo_click_href": "https://www.example.com"
})
```

### Parameters

* `path` (string): Required - Style path.
* `file` (file): Logo for custom branding. Required when creating a new style. Pass bytes, a binary stream, a `files_sdk.Attachment` or a JSON file object. See [File Attachments](../README.md#file-attachments).
* `logo_click_href` (string): URL to open when a public visitor clicks the logo.


---

## Delete Style

```python
style = files_sdk.style.find(path)
style.delete()
```

### Parameters

* `path` (string): Required - Style path.
