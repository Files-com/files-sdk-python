import builtins  # noqa: F401
from typing import Any, Mapping  # noqa: F401
from files_sdk.api import (  # noqa: F401
    LEGACY,
    LegacyScope,
    Operation,
    copy_params,
    decode_record,
    path_value,
)
from files_sdk.api_client import unexpected_response_error  # noqa: F401
from files_sdk.context import RequestOptions  # noqa: F401
from files_sdk.list_obj import ListObj
from files_sdk.error import (  # noqa: F401
    InvalidParameterError,
    MissingParameterError,
    NotImplementedError,
)


class Partner:
    """A partner record from the Files.com API.

    An attribute the API did not send is None.

    Attributes:
        allow_bypassing_2fa_policies: boolean - Allow Partner Admins to change Two-Factor Authentication requirements for Partner Users.
        allowed_ips: string - A list of allowed IPs for this Partner. Newline delimited. Partner User IP access is allowed when the IP matches the Partner, User, or Site allowed IP lists.
        allow_credential_changes: boolean - Allow Partner Admins to change or reset credentials for users belonging to this Partner.
        allow_providing_gpg_keys: boolean - Allow Partner Admins to provide GPG keys.
        allow_user_creation: boolean - Allow Partner Admins to create users.
        cc_emails_to_responsible_party: boolean - When `true`, emails sent to Partner users are copied to the responsible User or Group.
        connections: array(object) - Approved Connected Sites relationships for this Partner, in both directions. Empty when this Partner has no connections. Read-only.
        id: int64 - The unique ID of the Partner.
        ai_assistant_personality_id: int64 - AI Assistant Personality ID assigned to this Partner, if any. Users in the Partner inherit it unless a direct per-user assignment overrides it.
        workspace_id: int64 - ID of the Workspace associated with this Partner.
        name: string - The name of the Partner.
        notes: string - Notes about this Partner.
        partner_admin_ids: array(int64) - Array of User IDs that are Partner Admins for this Partner.
        partner_channel_template_id: int64 - ID of the Partner Channel Template assigned to this Partner.
        partnership_role: string - This site's role for this Partner in Connected Sites relationships. `host` is a Partner this site configured. `guest` is a Partner created by approving another site's connection request; it has no root folder and cannot hold users, permissions, or Partner Channels, or host a connection. `host_and_guest` is a configured Partner that is also the guest side of a connection. Promote a `guest` Partner by setting this to `host_and_guest` together with a `root_folder`.
        responsible_group_id: int64 - ID of the Group responsible for this Partner.
        responsible_user_id: int64 - ID of the User responsible for this Partner.
        root_folder: string - The root folder path for this Partner.
        show_partner_channel_home_page: boolean - Show Partner users a simplified home page built from this Partner's Channels.
        tags: string - Comma-separated list of Tags for this Partner. Tags are used for other features, such as UserLifecycleRules, which can target specific tags. Tags must only contain lowercase letters, numbers, and hyphens.
        user_ids: array(int64) - Array of User IDs that belong to this Partner.
    """

    default_attributes = {
        "allow_bypassing_2fa_policies": None,  # boolean - Allow Partner Admins to change Two-Factor Authentication requirements for Partner Users.
        "allowed_ips": None,  # string - A list of allowed IPs for this Partner. Newline delimited. Partner User IP access is allowed when the IP matches the Partner, User, or Site allowed IP lists.
        "allow_credential_changes": None,  # boolean - Allow Partner Admins to change or reset credentials for users belonging to this Partner.
        "allow_providing_gpg_keys": None,  # boolean - Allow Partner Admins to provide GPG keys.
        "allow_user_creation": None,  # boolean - Allow Partner Admins to create users.
        "cc_emails_to_responsible_party": None,  # boolean - When `true`, emails sent to Partner users are copied to the responsible User or Group.
        "connections": None,  # array(object) - Approved Connected Sites relationships for this Partner, in both directions. Empty when this Partner has no connections. Read-only.
        "id": None,  # int64 - The unique ID of the Partner.
        "ai_assistant_personality_id": None,  # int64 - AI Assistant Personality ID assigned to this Partner, if any. Users in the Partner inherit it unless a direct per-user assignment overrides it.
        "workspace_id": None,  # int64 - ID of the Workspace associated with this Partner.
        "name": None,  # string - The name of the Partner.
        "notes": None,  # string - Notes about this Partner.
        "partner_admin_ids": None,  # array(int64) - Array of User IDs that are Partner Admins for this Partner.
        "partner_channel_template_id": None,  # int64 - ID of the Partner Channel Template assigned to this Partner.
        "partnership_role": None,  # string - This site's role for this Partner in Connected Sites relationships. `host` is a Partner this site configured. `guest` is a Partner created by approving another site's connection request; it has no root folder and cannot hold users, permissions, or Partner Channels, or host a connection. `host_and_guest` is a configured Partner that is also the guest side of a connection. Promote a `guest` Partner by setting this to `host_and_guest` together with a `root_folder`.
        "responsible_group_id": None,  # int64 - ID of the Group responsible for this Partner.
        "responsible_user_id": None,  # int64 - ID of the User responsible for this Partner.
        "root_folder": None,  # string - The root folder path for this Partner.
        "show_partner_channel_home_page": None,  # boolean - Show Partner users a simplified home page built from this Partner's Channels.
        "tags": None,  # string - Comma-separated list of Tags for this Partner. Tags are used for other features, such as UserLifecycleRules, which can target specific tags.  Tags must only contain lowercase letters, numbers, and hyphens.
        "user_ids": None,  # array(int64) - Array of User IDs that belong to this Partner.
    }

    # Declared for type checkers and editors: the type the API sends each
    # attribute as, or None. set_attributes stores each value as given,
    # converting only decimals, so a value a caller sets can differ.
    allow_bypassing_2fa_policies: bool | None
    allowed_ips: str | None
    allow_credential_changes: bool | None
    allow_providing_gpg_keys: bool | None
    allow_user_creation: bool | None
    cc_emails_to_responsible_party: bool | None
    connections: builtins.list[dict[str, Any]] | None
    id: int | None
    ai_assistant_personality_id: int | None
    workspace_id: int | None
    name: str | None
    notes: str | None
    partner_admin_ids: builtins.list[int] | None
    partner_channel_template_id: int | None
    partnership_role: str | None
    responsible_group_id: int | None
    responsible_user_id: int | None
    root_folder: str | None
    show_partner_channel_home_page: bool | None
    tags: str | None
    user_ids: builtins.list[int] | None

    # The client and settings this object's operations use: those of the
    # operation or client that made it, or the module's when it starts an
    # operation if neither did.
    _context: Any = None

    def __init__(self, attributes=None, options=None):
        if not isinstance(attributes, dict):
            attributes = {}
        if not isinstance(options, dict):
            options = {}
        self.set_attributes(attributes)
        self.options = dict(options)

    def set_attributes(self, attributes):
        for attribute, default_value in Partner.default_attributes.items():
            value = attributes.get(attribute, default_value)
            setattr(self, attribute, value)

    def get_attributes(self):
        attrs = {
            k: getattr(self, k, None)
            for k in Partner.default_attributes
            if getattr(self, k, None) is not None
        }
        return attrs

    def _scope(self):
        if self._context is not None:
            return self._context
        return LegacyScope(self.options)

    def update(self, params: dict[str, Any] | None = None) -> None:
        """Updates this object in place with the record the server returns, and returns None.

        Parameters:
          ai_assistant_personality_id - int64 - AI Assistant Personality ID assigned to this Partner, if any. Users in the Partner inherit it unless a direct per-user assignment overrides it.
          allowed_ips - string - A list of allowed IPs for this Partner. Newline delimited. Partner User IP access is allowed when the IP matches the Partner, User, or Site allowed IP lists.
          allow_bypassing_2fa_policies - boolean - Allow Partner Admins to change Two-Factor Authentication requirements for Partner Users.
          allow_credential_changes - boolean - Allow Partner Admins to change or reset credentials for users belonging to this Partner.
          allow_providing_gpg_keys - boolean - Allow Partner Admins to provide GPG keys.
          allow_user_creation - boolean - Allow Partner Admins to create users.
          cc_emails_to_responsible_party - boolean - When `true`, emails sent to Partner users are copied to the responsible User or Group.
          notes - string - Notes about this Partner.
          partner_channel_template_id - int64 - ID of the Partner Channel Template assigned to this Partner.
          responsible_group_id - int64 - ID of the Group responsible for this Partner.
          responsible_user_id - int64 - ID of the User responsible for this Partner.
          show_partner_channel_home_page - boolean - Show Partner users a simplified home page built from this Partner's Channels.
          tags - string - Comma-separated list of Tags for this Partner. Tags are used for other features, such as UserLifecycleRules, which can target specific tags.  Tags must only contain lowercase letters, numbers, and hyphens.
          name - string - The name of the Partner.
          partnership_role - string - This site's role for this Partner in Connected Sites relationships. `host` is a Partner this site configured. `guest` is a Partner created by approving another site's connection request; it has no root folder and cannot hold users, permissions, or Partner Channels, or host a connection. `host_and_guest` is a configured Partner that is also the guest side of a connection. Promote a `guest` Partner by setting this to `host_and_guest` together with a `root_folder`.
          root_folder - string - The root folder path for this Partner.
        """
        if not (hasattr(self, "id") and self.id):
            raise MissingParameterError("Current object doesn't have a id")
        params = copy_params(params, {"id": self.id})
        if "id" not in params:
            raise MissingParameterError("Parameter missing: id")
        if "id" in params and (
            not isinstance(params["id"], int) or isinstance(params["id"], bool)
        ):
            raise InvalidParameterError("Bad parameter: id must be an int")
        if "ai_assistant_personality_id" in params and (
            not isinstance(params["ai_assistant_personality_id"], int)
            or isinstance(params["ai_assistant_personality_id"], bool)
        ):
            raise InvalidParameterError(
                "Bad parameter: ai_assistant_personality_id must be an int"
            )
        if "allowed_ips" in params and not isinstance(
            params["allowed_ips"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: allowed_ips must be an str"
            )
        if "allow_bypassing_2fa_policies" in params and isinstance(
            params["allow_bypassing_2fa_policies"],
            (builtins.list, tuple, dict),
        ):
            raise InvalidParameterError(
                "Bad parameter: allow_bypassing_2fa_policies must be an bool"
            )
        if "allow_credential_changes" in params and isinstance(
            params["allow_credential_changes"], (builtins.list, tuple, dict)
        ):
            raise InvalidParameterError(
                "Bad parameter: allow_credential_changes must be an bool"
            )
        if "allow_providing_gpg_keys" in params and isinstance(
            params["allow_providing_gpg_keys"], (builtins.list, tuple, dict)
        ):
            raise InvalidParameterError(
                "Bad parameter: allow_providing_gpg_keys must be an bool"
            )
        if "allow_user_creation" in params and isinstance(
            params["allow_user_creation"], (builtins.list, tuple, dict)
        ):
            raise InvalidParameterError(
                "Bad parameter: allow_user_creation must be an bool"
            )
        if "cc_emails_to_responsible_party" in params and isinstance(
            params["cc_emails_to_responsible_party"],
            (builtins.list, tuple, dict),
        ):
            raise InvalidParameterError(
                "Bad parameter: cc_emails_to_responsible_party must be an bool"
            )
        if "notes" in params and not isinstance(params["notes"], str):
            raise InvalidParameterError("Bad parameter: notes must be an str")
        if "partner_channel_template_id" in params and (
            not isinstance(params["partner_channel_template_id"], int)
            or isinstance(params["partner_channel_template_id"], bool)
        ):
            raise InvalidParameterError(
                "Bad parameter: partner_channel_template_id must be an int"
            )
        if "responsible_group_id" in params and (
            not isinstance(params["responsible_group_id"], int)
            or isinstance(params["responsible_group_id"], bool)
        ):
            raise InvalidParameterError(
                "Bad parameter: responsible_group_id must be an int"
            )
        if "responsible_user_id" in params and (
            not isinstance(params["responsible_user_id"], int)
            or isinstance(params["responsible_user_id"], bool)
        ):
            raise InvalidParameterError(
                "Bad parameter: responsible_user_id must be an int"
            )
        if "show_partner_channel_home_page" in params and isinstance(
            params["show_partner_channel_home_page"],
            (builtins.list, tuple, dict),
        ):
            raise InvalidParameterError(
                "Bad parameter: show_partner_channel_home_page must be an bool"
            )
        if "tags" in params and not isinstance(params["tags"], str):
            raise InvalidParameterError("Bad parameter: tags must be an str")
        if "name" in params and not isinstance(params["name"], str):
            raise InvalidParameterError("Bad parameter: name must be an str")
        if "partnership_role" in params and not isinstance(
            params["partnership_role"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: partnership_role must be an str"
            )
        if "root_folder" in params and not isinstance(
            params["root_folder"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: root_folder must be an str"
            )
        operation = Operation.start(self._scope())
        response = operation.request(
            "PATCH", "/partners/" + path_value(params["id"]), params
        )
        decode_record(response, response.data, self.set_attributes)
        operation.adopt(self)

    def delete(self, params: dict[str, Any] | None = None) -> None:
        if not (hasattr(self, "id") and self.id):
            raise MissingParameterError("Current object doesn't have a id")
        params = copy_params(params, {"id": self.id})
        if "id" not in params:
            raise MissingParameterError("Parameter missing: id")
        if "id" in params and (
            not isinstance(params["id"], int) or isinstance(params["id"], bool)
        ):
            raise InvalidParameterError("Bad parameter: id must be an int")
        operation = Operation.start(self._scope())
        operation.request(
            "DELETE", "/partners/" + path_value(params["id"]), params
        )

    def destroy(self, params: dict[str, Any] | None = None) -> None:
        """The same as delete()."""
        return self.delete(params)

    def save(self) -> None:
        """Update this object on the server if it has an id, or else create
        it, taking in place the record the server returns."""
        if hasattr(self, "id") and self.id:
            self.update(self.get_attributes())
        else:
            new_obj = PartnerResource(self._scope()).create(
                self.get_attributes()
            )
            self.set_attributes(new_obj.get_attributes())
            self._context = new_obj._context


class PartnerResource:
    """Partner operations that use one client's configuration.

    Get one from a client, such as ``client.partner``. Each operation
    takes the same arguments as the module-level function of the same name,
    and its options apply on top of the client's.
    """

    def __init__(self, scope):
        self._scope = scope

    def list(
        self,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> ListObj[Partner]:
        """Parameters:
        cursor - string - Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
        per_page - int64 - Number of records to show per page.  (Max: 10000, 1,000 or less is recommended).
        sort_by - object - If set, sort records by the specified field in either `asc` or `desc` direction. Valid fields are `workspace_id` and `name`.
        filter - object - If set, return records where the specified field is equal to the supplied value. Valid fields are `workspace_id`.
        """
        params = copy_params(params)
        if "cursor" in params and not isinstance(params["cursor"], str):
            raise InvalidParameterError("Bad parameter: cursor must be an str")
        if "per_page" in params and (
            not isinstance(params["per_page"], int)
            or isinstance(params["per_page"], bool)
        ):
            raise InvalidParameterError(
                "Bad parameter: per_page must be an int"
            )
        if "sort_by" in params and not isinstance(params["sort_by"], dict):
            raise InvalidParameterError(
                "Bad parameter: sort_by must be an dict"
            )
        if "filter" in params and not isinstance(params["filter"], dict):
            raise InvalidParameterError(
                "Bad parameter: filter must be an dict"
            )
        operation = Operation.start(self._scope, options)
        return ListObj(Partner, "GET", "/partners", params, operation)

    def all(
        self,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> ListObj[Partner]:
        """The same as list()."""
        return self.list(params, options)

    def find(
        self,
        id: int,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> Partner:
        """Parameters:
        id (required) - int64 - Partner ID.
        """
        return self.__find({"id": id}, params, options)

    def __find(
        self,
        path_values: dict[str, Any],
        params: dict[str, Any] | None,
        options: RequestOptions | Mapping[str, Any] | None,
    ) -> Partner:
        params = copy_params(params, path_values)
        if "id" in params and (
            not isinstance(params["id"], int) or isinstance(params["id"], bool)
        ):
            raise InvalidParameterError("Bad parameter: id must be an int")
        if "id" not in params:
            raise MissingParameterError("Parameter missing: id")
        operation = Operation.start(self._scope, options)
        response = operation.request(
            "GET", "/partners/" + path_value(params["id"]), params
        )
        return operation.decode_model(response, Partner)

    def get(
        self,
        id: int,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> Partner:
        """The same as find()."""
        return self.find(id, params, options)

    def create(
        self,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> Partner:
        """Parameters:
        ai_assistant_personality_id - int64 - AI Assistant Personality ID assigned to this Partner, if any. Users in the Partner inherit it unless a direct per-user assignment overrides it.
        allowed_ips - string - A list of allowed IPs for this Partner. Newline delimited. Partner User IP access is allowed when the IP matches the Partner, User, or Site allowed IP lists.
        allow_bypassing_2fa_policies - boolean - Allow Partner Admins to change Two-Factor Authentication requirements for Partner Users.
        allow_credential_changes - boolean - Allow Partner Admins to change or reset credentials for users belonging to this Partner.
        allow_providing_gpg_keys - boolean - Allow Partner Admins to provide GPG keys.
        allow_user_creation - boolean - Allow Partner Admins to create users.
        cc_emails_to_responsible_party - boolean - When `true`, emails sent to Partner users are copied to the responsible User or Group.
        notes - string - Notes about this Partner.
        partner_channel_template_id - int64 - ID of the Partner Channel Template assigned to this Partner.
        responsible_group_id - int64 - ID of the Group responsible for this Partner.
        responsible_user_id - int64 - ID of the User responsible for this Partner.
        show_partner_channel_home_page - boolean - Show Partner users a simplified home page built from this Partner's Channels.
        tags - string - Comma-separated list of Tags for this Partner. Tags are used for other features, such as UserLifecycleRules, which can target specific tags.  Tags must only contain lowercase letters, numbers, and hyphens.
        name (required) - string - The name of the Partner.
        root_folder (required) - string - The root folder path for this Partner.
        workspace_id - int64 - ID of the Workspace associated with this Partner.
        """
        params = copy_params(params)
        if "ai_assistant_personality_id" in params and (
            not isinstance(params["ai_assistant_personality_id"], int)
            or isinstance(params["ai_assistant_personality_id"], bool)
        ):
            raise InvalidParameterError(
                "Bad parameter: ai_assistant_personality_id must be an int"
            )
        if "allowed_ips" in params and not isinstance(
            params["allowed_ips"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: allowed_ips must be an str"
            )
        if "allow_bypassing_2fa_policies" in params and not isinstance(
            params["allow_bypassing_2fa_policies"], bool
        ):
            raise InvalidParameterError(
                "Bad parameter: allow_bypassing_2fa_policies must be an bool"
            )
        if "allow_credential_changes" in params and not isinstance(
            params["allow_credential_changes"], bool
        ):
            raise InvalidParameterError(
                "Bad parameter: allow_credential_changes must be an bool"
            )
        if "allow_providing_gpg_keys" in params and not isinstance(
            params["allow_providing_gpg_keys"], bool
        ):
            raise InvalidParameterError(
                "Bad parameter: allow_providing_gpg_keys must be an bool"
            )
        if "allow_user_creation" in params and not isinstance(
            params["allow_user_creation"], bool
        ):
            raise InvalidParameterError(
                "Bad parameter: allow_user_creation must be an bool"
            )
        if "cc_emails_to_responsible_party" in params and not isinstance(
            params["cc_emails_to_responsible_party"], bool
        ):
            raise InvalidParameterError(
                "Bad parameter: cc_emails_to_responsible_party must be an bool"
            )
        if "notes" in params and not isinstance(params["notes"], str):
            raise InvalidParameterError("Bad parameter: notes must be an str")
        if "partner_channel_template_id" in params and (
            not isinstance(params["partner_channel_template_id"], int)
            or isinstance(params["partner_channel_template_id"], bool)
        ):
            raise InvalidParameterError(
                "Bad parameter: partner_channel_template_id must be an int"
            )
        if "responsible_group_id" in params and (
            not isinstance(params["responsible_group_id"], int)
            or isinstance(params["responsible_group_id"], bool)
        ):
            raise InvalidParameterError(
                "Bad parameter: responsible_group_id must be an int"
            )
        if "responsible_user_id" in params and (
            not isinstance(params["responsible_user_id"], int)
            or isinstance(params["responsible_user_id"], bool)
        ):
            raise InvalidParameterError(
                "Bad parameter: responsible_user_id must be an int"
            )
        if "show_partner_channel_home_page" in params and not isinstance(
            params["show_partner_channel_home_page"], bool
        ):
            raise InvalidParameterError(
                "Bad parameter: show_partner_channel_home_page must be an bool"
            )
        if "tags" in params and not isinstance(params["tags"], str):
            raise InvalidParameterError("Bad parameter: tags must be an str")
        if "name" in params and not isinstance(params["name"], str):
            raise InvalidParameterError("Bad parameter: name must be an str")
        if "root_folder" in params and not isinstance(
            params["root_folder"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: root_folder must be an str"
            )
        if "workspace_id" in params and (
            not isinstance(params["workspace_id"], int)
            or isinstance(params["workspace_id"], bool)
        ):
            raise InvalidParameterError(
                "Bad parameter: workspace_id must be an int"
            )
        if "name" not in params:
            raise MissingParameterError("Parameter missing: name")
        if "root_folder" not in params:
            raise MissingParameterError("Parameter missing: root_folder")
        operation = Operation.start(self._scope, options)
        response = operation.request("POST", "/partners", params)
        return operation.decode_model(response, Partner)

    def update(
        self,
        id: int,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> Partner:
        """Parameters:
        ai_assistant_personality_id - int64 - AI Assistant Personality ID assigned to this Partner, if any. Users in the Partner inherit it unless a direct per-user assignment overrides it.
        allowed_ips - string - A list of allowed IPs for this Partner. Newline delimited. Partner User IP access is allowed when the IP matches the Partner, User, or Site allowed IP lists.
        allow_bypassing_2fa_policies - boolean - Allow Partner Admins to change Two-Factor Authentication requirements for Partner Users.
        allow_credential_changes - boolean - Allow Partner Admins to change or reset credentials for users belonging to this Partner.
        allow_providing_gpg_keys - boolean - Allow Partner Admins to provide GPG keys.
        allow_user_creation - boolean - Allow Partner Admins to create users.
        cc_emails_to_responsible_party - boolean - When `true`, emails sent to Partner users are copied to the responsible User or Group.
        notes - string - Notes about this Partner.
        partner_channel_template_id - int64 - ID of the Partner Channel Template assigned to this Partner.
        responsible_group_id - int64 - ID of the Group responsible for this Partner.
        responsible_user_id - int64 - ID of the User responsible for this Partner.
        show_partner_channel_home_page - boolean - Show Partner users a simplified home page built from this Partner's Channels.
        tags - string - Comma-separated list of Tags for this Partner. Tags are used for other features, such as UserLifecycleRules, which can target specific tags.  Tags must only contain lowercase letters, numbers, and hyphens.
        name - string - The name of the Partner.
        partnership_role - string - This site's role for this Partner in Connected Sites relationships. `host` is a Partner this site configured. `guest` is a Partner created by approving another site's connection request; it has no root folder and cannot hold users, permissions, or Partner Channels, or host a connection. `host_and_guest` is a configured Partner that is also the guest side of a connection. Promote a `guest` Partner by setting this to `host_and_guest` together with a `root_folder`.
        root_folder - string - The root folder path for this Partner.
        """
        return self.__update({"id": id}, params, options)

    def __update(
        self,
        path_values: dict[str, Any],
        params: dict[str, Any] | None,
        options: RequestOptions | Mapping[str, Any] | None,
    ) -> Partner:
        params = copy_params(params, path_values)
        if "id" in params and (
            not isinstance(params["id"], int) or isinstance(params["id"], bool)
        ):
            raise InvalidParameterError("Bad parameter: id must be an int")
        if "ai_assistant_personality_id" in params and (
            not isinstance(params["ai_assistant_personality_id"], int)
            or isinstance(params["ai_assistant_personality_id"], bool)
        ):
            raise InvalidParameterError(
                "Bad parameter: ai_assistant_personality_id must be an int"
            )
        if "allowed_ips" in params and not isinstance(
            params["allowed_ips"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: allowed_ips must be an str"
            )
        if "allow_bypassing_2fa_policies" in params and not isinstance(
            params["allow_bypassing_2fa_policies"], bool
        ):
            raise InvalidParameterError(
                "Bad parameter: allow_bypassing_2fa_policies must be an bool"
            )
        if "allow_credential_changes" in params and not isinstance(
            params["allow_credential_changes"], bool
        ):
            raise InvalidParameterError(
                "Bad parameter: allow_credential_changes must be an bool"
            )
        if "allow_providing_gpg_keys" in params and not isinstance(
            params["allow_providing_gpg_keys"], bool
        ):
            raise InvalidParameterError(
                "Bad parameter: allow_providing_gpg_keys must be an bool"
            )
        if "allow_user_creation" in params and not isinstance(
            params["allow_user_creation"], bool
        ):
            raise InvalidParameterError(
                "Bad parameter: allow_user_creation must be an bool"
            )
        if "cc_emails_to_responsible_party" in params and not isinstance(
            params["cc_emails_to_responsible_party"], bool
        ):
            raise InvalidParameterError(
                "Bad parameter: cc_emails_to_responsible_party must be an bool"
            )
        if "notes" in params and not isinstance(params["notes"], str):
            raise InvalidParameterError("Bad parameter: notes must be an str")
        if "partner_channel_template_id" in params and (
            not isinstance(params["partner_channel_template_id"], int)
            or isinstance(params["partner_channel_template_id"], bool)
        ):
            raise InvalidParameterError(
                "Bad parameter: partner_channel_template_id must be an int"
            )
        if "responsible_group_id" in params and (
            not isinstance(params["responsible_group_id"], int)
            or isinstance(params["responsible_group_id"], bool)
        ):
            raise InvalidParameterError(
                "Bad parameter: responsible_group_id must be an int"
            )
        if "responsible_user_id" in params and (
            not isinstance(params["responsible_user_id"], int)
            or isinstance(params["responsible_user_id"], bool)
        ):
            raise InvalidParameterError(
                "Bad parameter: responsible_user_id must be an int"
            )
        if "show_partner_channel_home_page" in params and not isinstance(
            params["show_partner_channel_home_page"], bool
        ):
            raise InvalidParameterError(
                "Bad parameter: show_partner_channel_home_page must be an bool"
            )
        if "tags" in params and not isinstance(params["tags"], str):
            raise InvalidParameterError("Bad parameter: tags must be an str")
        if "name" in params and not isinstance(params["name"], str):
            raise InvalidParameterError("Bad parameter: name must be an str")
        if "partnership_role" in params and not isinstance(
            params["partnership_role"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: partnership_role must be an str"
            )
        if "root_folder" in params and not isinstance(
            params["root_folder"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: root_folder must be an str"
            )
        if "id" not in params:
            raise MissingParameterError("Parameter missing: id")
        operation = Operation.start(self._scope, options)
        response = operation.request(
            "PATCH", "/partners/" + path_value(params["id"]), params
        )
        return operation.decode_model(response, Partner)

    def delete(
        self,
        id: int,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> None:
        return self.__delete({"id": id}, params, options)

    def __delete(
        self,
        path_values: dict[str, Any],
        params: dict[str, Any] | None,
        options: RequestOptions | Mapping[str, Any] | None,
    ) -> None:
        params = copy_params(params, path_values)
        if "id" in params and (
            not isinstance(params["id"], int) or isinstance(params["id"], bool)
        ):
            raise InvalidParameterError("Bad parameter: id must be an int")
        if "id" not in params:
            raise MissingParameterError("Parameter missing: id")
        operation = Operation.start(self._scope, options)
        operation.request(
            "DELETE", "/partners/" + path_value(params["id"]), params
        )

    def destroy(
        self,
        id: int,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> None:
        """The same as delete()."""
        return self.delete(id, params, options)

    def new(
        self,
        attributes: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> Partner:
        """A new Partner with attributes, not yet saved, whose
        operations use this resource's client."""
        obj = Partner(attributes, options)
        obj._context = self._scope._context_for(options)
        return obj


_legacy_resource = PartnerResource(LEGACY)


def list(
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> ListObj[Partner]:
    """Parameters:
    cursor - string - Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
    per_page - int64 - Number of records to show per page.  (Max: 10000, 1,000 or less is recommended).
    sort_by - object - If set, sort records by the specified field in either `asc` or `desc` direction. Valid fields are `workspace_id` and `name`.
    filter - object - If set, return records where the specified field is equal to the supplied value. Valid fields are `workspace_id`.
    """
    return _legacy_resource.list(params, options)


def all(
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> ListObj[Partner]:
    """The same as list()."""
    return _legacy_resource.list(params, options)


def find(
    id: int,
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> Partner:
    """Parameters:
    id (required) - int64 - Partner ID.
    """
    return _legacy_resource.find(id, params, options)


def get(
    id: int,
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> Partner:
    """The same as find()."""
    return _legacy_resource.find(id, params, options)


def create(
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> Partner:
    """Parameters:
    ai_assistant_personality_id - int64 - AI Assistant Personality ID assigned to this Partner, if any. Users in the Partner inherit it unless a direct per-user assignment overrides it.
    allowed_ips - string - A list of allowed IPs for this Partner. Newline delimited. Partner User IP access is allowed when the IP matches the Partner, User, or Site allowed IP lists.
    allow_bypassing_2fa_policies - boolean - Allow Partner Admins to change Two-Factor Authentication requirements for Partner Users.
    allow_credential_changes - boolean - Allow Partner Admins to change or reset credentials for users belonging to this Partner.
    allow_providing_gpg_keys - boolean - Allow Partner Admins to provide GPG keys.
    allow_user_creation - boolean - Allow Partner Admins to create users.
    cc_emails_to_responsible_party - boolean - When `true`, emails sent to Partner users are copied to the responsible User or Group.
    notes - string - Notes about this Partner.
    partner_channel_template_id - int64 - ID of the Partner Channel Template assigned to this Partner.
    responsible_group_id - int64 - ID of the Group responsible for this Partner.
    responsible_user_id - int64 - ID of the User responsible for this Partner.
    show_partner_channel_home_page - boolean - Show Partner users a simplified home page built from this Partner's Channels.
    tags - string - Comma-separated list of Tags for this Partner. Tags are used for other features, such as UserLifecycleRules, which can target specific tags.  Tags must only contain lowercase letters, numbers, and hyphens.
    name (required) - string - The name of the Partner.
    root_folder (required) - string - The root folder path for this Partner.
    workspace_id - int64 - ID of the Workspace associated with this Partner.
    """
    return _legacy_resource.create(params, options)


def update(
    id: int,
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> Partner:
    """Parameters:
    ai_assistant_personality_id - int64 - AI Assistant Personality ID assigned to this Partner, if any. Users in the Partner inherit it unless a direct per-user assignment overrides it.
    allowed_ips - string - A list of allowed IPs for this Partner. Newline delimited. Partner User IP access is allowed when the IP matches the Partner, User, or Site allowed IP lists.
    allow_bypassing_2fa_policies - boolean - Allow Partner Admins to change Two-Factor Authentication requirements for Partner Users.
    allow_credential_changes - boolean - Allow Partner Admins to change or reset credentials for users belonging to this Partner.
    allow_providing_gpg_keys - boolean - Allow Partner Admins to provide GPG keys.
    allow_user_creation - boolean - Allow Partner Admins to create users.
    cc_emails_to_responsible_party - boolean - When `true`, emails sent to Partner users are copied to the responsible User or Group.
    notes - string - Notes about this Partner.
    partner_channel_template_id - int64 - ID of the Partner Channel Template assigned to this Partner.
    responsible_group_id - int64 - ID of the Group responsible for this Partner.
    responsible_user_id - int64 - ID of the User responsible for this Partner.
    show_partner_channel_home_page - boolean - Show Partner users a simplified home page built from this Partner's Channels.
    tags - string - Comma-separated list of Tags for this Partner. Tags are used for other features, such as UserLifecycleRules, which can target specific tags.  Tags must only contain lowercase letters, numbers, and hyphens.
    name - string - The name of the Partner.
    partnership_role - string - This site's role for this Partner in Connected Sites relationships. `host` is a Partner this site configured. `guest` is a Partner created by approving another site's connection request; it has no root folder and cannot hold users, permissions, or Partner Channels, or host a connection. `host_and_guest` is a configured Partner that is also the guest side of a connection. Promote a `guest` Partner by setting this to `host_and_guest` together with a `root_folder`.
    root_folder - string - The root folder path for this Partner.
    """
    return _legacy_resource.update(id, params, options)


def delete(
    id: int,
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> None:
    _legacy_resource.delete(id, params, options)


def destroy(
    id: int,
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> None:
    """The same as delete()."""
    return _legacy_resource.delete(id, params, options)


def new(*args, **kwargs) -> Partner:
    return Partner(*args, **kwargs)
