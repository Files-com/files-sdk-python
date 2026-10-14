# FileCommentReaction

## Example FileCommentReaction Object

The API sends each `FileCommentReaction` record as JSON, such as:

```json
{
  "id": 1,
  "emoji": "👍"
}
```

* `id` (int64): Reaction ID
* `emoji` (string): Emoji used in the reaction.
* `user_id` (int64): User ID.  Provide a value of `0` to operate the current session's user.
* `file_comment_id` (int64): ID of file comment to attach reaction to.

The functions below use the module's settings. Each is also a method of a client's
`client.file_comment_reaction` resource, such as
`client.file_comment_reaction.create(...)`,
which uses that client's configuration instead.


---

## Create File Comment Reaction

```python
files_sdk.file_comment_reaction.create({
  "user_id": 1,
  "file_comment_id": 1,
  "emoji": "emoji"
})
```

### Parameters

* `user_id` (int64): User ID.  Provide a value of `0` to operate the current session's user.
* `file_comment_id` (int64): Required - ID of file comment to attach reaction to.
* `emoji` (string): Required - Emoji to react with.


---

## Delete File Comment Reaction

```python
files_sdk.file_comment_reaction.delete(id)
```

### Parameters

* `id` (int64): Required - File Comment Reaction ID.


---

## Delete File Comment Reaction

```python
file_comment_reaction = files_sdk.file_comment_reaction.new({"id": id})
file_comment_reaction.delete()
```

### Parameters

* `id` (int64): Required - File Comment Reaction ID.
