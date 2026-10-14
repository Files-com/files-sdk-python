# Status

## Example Status Object

The API sends each `Status` record as JSON, such as:

```json
{
  "code": 200,
  "message": "example",
  "status": "",
  "data": "example",
  "errors": [
    {
      "fields": [

      ],
      "messages": [

      ]
    }
  ],
  "clickwrap_id": 1,
  "clickwrap_body": "example"
}
```

* `code` (int64): Status HTTP code
* `message` (string): Error message
* `status` (string): Status message
* `data` (Auto): Additional data
* `errors` (array(object)): A list of api errors
* `clickwrap_id` (int64): Required Clickwrap id
* `clickwrap_body` (string): Required Clickwrap body
