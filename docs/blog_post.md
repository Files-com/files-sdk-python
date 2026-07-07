# BlogPost

## Example BlogPost Object

```
{
  "id": 1,
  "title": "example",
  "content": "example",
  "link": "2000-01-01T01:00:00Z",
  "published_at": "2000-01-01T01:00:00Z"
}
```

* `id` (int64): Blog Post ID
* `title` (string): Blog Post's Title
* `content` (string): Blog Post's Content
* `link` (date-time): Blog Post's Permanent Link
* `published_at` (date-time): Blog Post's Published Date


---

## Show the most recent blog posts from the Files.com blog

```
files_sdk.blog_post.list()
```

### Parameters

* `cursor` (string): Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
* `per_page` (int64): Number of records to show per page.  (Max: 10000, 1,000 or less is recommended).
* `sort_by` (object): If set, sort records by the specified field in either `asc` or `desc` direction. Valid fields are `published_at`.
* `filter` (object): If set, return records where the specified field is equal to the supplied value. Valid fields are `published_at`.
* `filter_gt` (object): If set, return records where the specified field is greater than the supplied value. Valid fields are `published_at`.
* `filter_gteq` (object): If set, return records where the specified field is greater than or equal the supplied value. Valid fields are `published_at`.
* `filter_lt` (object): If set, return records where the specified field is less than the supplied value. Valid fields are `published_at`.
* `filter_lteq` (object): If set, return records where the specified field is less than or equal the supplied value. Valid fields are `published_at`.


---

## Show the most recent blog posts from the Files.com blog

```
files_sdk.blog_post.create_export()
```

### Parameters

* `sort_by` (object): If set, sort records by the specified field in either `asc` or `desc` direction. Valid fields are `published_at`.
* `filter` (object): If set, return records where the specified field is equal to the supplied value. Valid fields are `published_at`.
* `filter_gt` (object): If set, return records where the specified field is greater than the supplied value. Valid fields are `published_at`.
* `filter_gteq` (object): If set, return records where the specified field is greater than or equal the supplied value. Valid fields are `published_at`.
* `filter_lt` (object): If set, return records where the specified field is less than the supplied value. Valid fields are `published_at`.
* `filter_lteq` (object): If set, return records where the specified field is less than or equal the supplied value. Valid fields are `published_at`.
