# NpsResponse

## Example NpsResponse Object

```
{
  "id": 1,
  "next_step": "example"
}
```

* `id` (int64): NPS response id
* `next_step` (string): 
* `user_id` (int64): User ID.  Provide a value of `0` to operate the current session's user.
* `score` (int64): NPS score
* `skipped` (boolean): NPS skipped
* `comment` (string): NPS comment
* `contact_me` (boolean): NPS contact_me


---

## Create Nps Response

```
files_sdk.nps_response.create({
  "user_id": 1,
  "score": 1,
  "skipped": False
})
```

### Parameters

* `user_id` (int64): User ID.  Provide a value of `0` to operate the current session's user.
* `score` (int64): NPS score
* `skipped` (boolean): NPS skipped


---

## Update Nps Response

```
files_sdk.nps_response.update(id, {
  "comment": "comment",
  "contact_me": False
})
```

### Parameters

* `id` (int64): Required - Nps Response ID.
* `comment` (string): Required - NPS comment
* `contact_me` (boolean): NPS contact_me


---

## Update Nps Response

```
nps_response = nps_response()
nps_response.update({
  "comment": "comment",
  "contact_me": False
})
```

### Parameters

* `id` (int64): Required - Nps Response ID.
* `comment` (string): Required - NPS comment
* `contact_me` (boolean): NPS contact_me
