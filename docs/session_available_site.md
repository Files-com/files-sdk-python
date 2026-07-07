# SessionAvailableSite

## Example SessionAvailableSite Object

```
{
  "id": 1,
  "name": "My Site",
  "domain": "my-custom-domain.com",
  "subdomain": "mysite",
  "logo": {
    "name": "My logo",
    "uri": "https://mysite.files.com/.../my_image.png"
  },
  "color2_top": "#000000",
  "folder_permissions_groups_only": True
}
```

* `id` (int64): Site Id
* `name` (string): Site name
* `domain` (string): Custom domain
* `subdomain` (string): Site subdomain
* `logo` (Image): Branded logo
* `color2_top` (string): Top bar background color
* `folder_permissions_groups_only` (boolean): If true, permissions for this site must be bound to a group (not a user).
