# ZipDownload

## Example ZipDownload Object

```
{
  "download_uri": "/zip/download?z=CODE"
}
```

* `download_uri` (string): URL for downloading the ZIP
* `paths` (array(string)): 
* `bundle_registration_code` (string): 
* `encoded_paths` (array(string)): 


---

## Create a URL that can be used to download a ZIP of several files at once

```
files_sdk.zip_download.create({
  "paths": ["file.txt"],
  "encoded_paths": ["file.txt"]
})
```

### Parameters

* `paths` (array(string)): Required - 
* `bundle_registration_code` (string): 
* `encoded_paths` (array(string)): 
