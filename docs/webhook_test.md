# WebhookTest

## Example WebhookTest Object

```
{
  "code": 200,
  "message": "",
  "status": "",
  "data": "example",
  "success": True
}
```

* `code` (int64): Status HTTP code
* `message` (string): Error message
* `status` (string): Status message
* `data` (Auto): Additional data
* `success` (boolean): The success status of the webhook test
* `url` (string): URL for testing the webhook.
* `method` (string): HTTP method(GET or POST).
* `encoding` (string): HTTP encoding method.  Can be JSON, XML, or RAW (form data).
* `headers` (object): Additional request headers.
* `body` (object): Additional body parameters.
* `raw_body` (string): raw body text
* `file_as_body` (boolean): Send the file data as the request body?
* `file_form_field` (string): Send the file data as a named parameter in the request POST body
* `action` (string): action for test body
* `use_dedicated_ips` (boolean): Use dedicated IPs for sending the webhook?


---

## Create Webhook Test

```
files_sdk.webhook_test.create({
  "url": "https://www.site.com/...",
  "method": "GET",
  "encoding": "RAW",
  "headers": {"x-test-header":"testvalue"},
  "body": {"test-param":"testvalue"},
  "raw_body": "test body",
  "file_as_body": False,
  "file_form_field": "upload_file_data",
  "use_dedicated_ips": False
})
```

### Parameters

* `url` (string): Required - URL for testing the webhook.
* `method` (string): HTTP method(GET or POST).
* `encoding` (string): HTTP encoding method.  Can be JSON, XML, or RAW (form data).
* `headers` (object): Additional request headers.
* `body` (object): Additional body parameters.
* `raw_body` (string): raw body text
* `file_as_body` (boolean): Send the file data as the request body?
* `file_form_field` (string): Send the file data as a named parameter in the request POST body
* `action` (string): action for test body
* `use_dedicated_ips` (boolean): Use dedicated IPs for sending the webhook?
