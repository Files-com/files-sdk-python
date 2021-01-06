# Style

## Example Style Object

```
{
  "id": 1,
  "path": "",
  "logo": "https://mysite.files.com/...",
  "thumbnail": ""
}
```

* `id` (int64): Style ID
* `path` (string): Folder path This must be slash-delimited, but it must neither start nor end with a slash. Maximum of 5000 characters.
* `logo`: Logo
* `thumbnail`: Logo thumbnail
* `file` (file): Logo for custom branding.


---

## Show Style

```
files_sdk.style.find(path)
```

### Parameters

* `path` (string): Required - Style path.


---

## Update Style

```
files_sdk.style.update(path, {
  "file": "file"
})
```

### Parameters

* `path` (string): Required - Style path.
* `file` (file): Required - Logo for custom branding.


---

## Delete Style

```
files_sdk.style.delete(path)
```

### Parameters

* `path` (string): Required - Style path.


---

## Update Style

```
style = files_sdk.style.find(1)

style.update({
  "file": "file"
})
```

### Parameters

* `path` (string): Required - Style path.
* `file` (file): Required - Logo for custom branding.


---

## Delete Style

```
style = files_sdk.style.find(1)

style.delete()
```

### Parameters

* `path` (string): Required - Style path.
