# PartnerConnection

## Example PartnerConnection Object

```
{
  "id": 1,
  "role": "guest",
  "site_id": 2,
  "site_name": "Acme Site",
  "mount_path": "_/Sites/2"
}
```

* `id` (int64): Relationship ID used with DELETE /partner_sites/:id to disconnect.
* `role` (string): This Partner's role in this connection. A host shares local files with the connected site; a guest accesses files shared by the connected site.
* `site_id` (int64): ID of the connected site.
* `site_name` (string): Name of the connected site.
* `mount_path` (string): File API path to the connected Host's mount on this site when role is guest. Null when role is host. File access remains subject to the caller's permissions and the Host Partner's grants.
