# Release

## Example Release Object

```
{
  "version": "1.0.0",
  "description": "The initial release of Files.com Desktop",
  "native_release_packages": [
    {
      "package_link": "https://www.files.com/desktop/download",
      "platform": "win32",
      "architecture": "amd64",
      "extension": "deb",
      "sha256": "example"
    }
  ],
  "title": "Files.com",
  "product": "desktop_v4"
}
```

* `version` (string): Native release version
* `description` (string): Native release description
* `native_release_packages` (array(object)): A list of native release packages
* `title` (string): Native release title
* `product` (string): Native release product
* `version_major` (int64): 
* `version_minor` (int64): 
* `version_patch` (int64): 
* `version_build` (int64): 
* `oem` (string): 


---

## Show information about the latest Desktop app release

```
files_sdk.release.get_latest({
  "product": "desktop_v6",
  "platform": "win32",
  "architecture": "amd64",
  "ext": "exe"
})
```

### Parameters

* `product` (string): 
* `platform` (string): 
* `architecture` (string): 
* `ext` (string): 


---

## Create an application release

```
files_sdk.release.create({
  "title": "Files.com",
  "description": "The initial release of Files.com Desktop",
  "version_major": 1,
  "version_minor": 1,
  "version_patch": 1,
  "version_build": 1,
  "product": "desktop_v4",
  "native_release_packages": [{"package_link":"https://www.files.com/desktop/download","platform":"win32","architecture":"amd64","extension":"deb","sha256":"example"}]
})
```

### Parameters

* `title` (string): 
* `description` (string): 
* `version_major` (int64): 
* `version_minor` (int64): 
* `version_patch` (int64): 
* `version_build` (int64): 
* `oem` (string): 
* `product` (string): 
* `native_release_packages` (array(object)): 
