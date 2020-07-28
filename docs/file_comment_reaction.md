# FileCommentReaction

## Example FileCommentReaction Object

```
{
  "id": 1,
  "emoji": "👍"
}
```

* `id` (int64): Reaction ID
* `emoji` (string): Emoji used in the reaction.
* `user_id` (int64): User ID.  Provide a value of `0` to operate the current session's user.
* `file_comment_id` (int64): ID of file comment to attach reaction to.


---

## Create File Comment Reaction

```
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

```
files_sdk.file_comment_reaction.delete(id)
```

### Parameters

* `id` (int64): Required - File Comment Reaction ID.


---

## Delete File Comment Reaction

```
file_comment_reaction = files_sdk.file_comment_reaction.list_for(path).first

file_comment_reaction.delete()
```

### Parameters

* `id` (int64): Required - File Comment Reaction ID.
