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


class EventSubscription:
    """A event subscription record from the Files.com API.

    An attribute the API did not send is None.

    Attributes:
        id: int64 - Event Subscription ID
        event_channel_id: int64 - Event Channel ID
        workspace_id: int64 - Workspace ID. 0 means the default workspace or site-wide.
        apply_to_all_workspaces: boolean - If true, this default-workspace subscription applies to events from all workspaces.
        name: string - Event Subscription name.
        subject: string - Custom subject line to use for notification emails.
        message: string - Custom message to include in notification emails.
        message_only: boolean - If true, notification email bodies contain only the custom message, omitting event details and the review button. Requires a custom message, defaults to false, and does not affect non-email targets.
        enabled: boolean - Whether this Event Subscription can dispatch events.
        event_types: array(string) - Event type strings matched by this subscription. Blank means all event types. Valid values: `automation_run.canceled.v1`, `automation_run.failure.v1`, `automation_run.failure_will_retry.v1`, `automation_run.partial_failure.v1`, `automation_run.partial_failure_will_retry.v1`, `automation_run.skipped.v1`, `automation_run.success.v1`, `expectation_evaluation.invalid.v1`, `expectation_evaluation.late.v1`, `expectation_evaluation.missing.v1`, `expectation_evaluation.success.v1`, `expectation_incident.acknowledged.v1`, `expectation_incident.open.v1`, `expectation_incident.resolved.v1`, `expectation_incident.snoozed.v1`, `external_event.client_log.failure.v1`, `external_event.client_log.partial_failure.v1`, `external_event.client_log.skipped.v1`, `external_event.client_log.success.v1`, `pending_work_event.failure.v1`, `pending_work_event.partial_failure.v1`, `pending_work_event.skipped.v1`, `pending_work_event.success.v1`, `siem_http_destination_event.failure.v1`, `siem_http_destination_event.partial_failure.v1`, `siem_http_destination_event.skipped.v1`, `siem_http_destination_event.success.v1`, `sso_event.ldap_login.failure.v1`, `sso_event.ldap_login.partial_failure.v1`, `sso_event.ldap_login.skipped.v1`, `sso_event.ldap_login.success.v1`, `sso_event.ldap_sync.failure.v1`, `sso_event.ldap_sync.partial_failure.v1`, `sso_event.ldap_sync.skipped.v1`, `sso_event.ldap_sync.success.v1`, `sso_event.saml_login.failure.v1`, `sso_event.saml_login.partial_failure.v1`, `sso_event.saml_login.skipped.v1`, `sso_event.saml_login.success.v1`, `sync_run.failure.v1`, `sync_run.partial_failure.v1`, `sync_run.skipped.v1`, `sync_run.success.v1`, `user_security_event.lockout.v1`
        filter: object - Conditions on event fields that an event must meet to be delivered, keyed by dot-notation field path. All conditions must match.
        delivery_policy: object - Event Subscription delivery policy.
        event_target_ids: array(int64) - Event Target IDs this subscription sends to.
        created_at: date-time - Event Subscription create date/time.
        updated_at: date-time - Event Subscription update date/time.
    """

    default_attributes = {
        "id": None,  # int64 - Event Subscription ID
        "event_channel_id": None,  # int64 - Event Channel ID
        "workspace_id": None,  # int64 - Workspace ID. 0 means the default workspace or site-wide.
        "apply_to_all_workspaces": None,  # boolean - If true, this default-workspace subscription applies to events from all workspaces.
        "name": None,  # string - Event Subscription name.
        "subject": None,  # string - Custom subject line to use for notification emails.
        "message": None,  # string - Custom message to include in notification emails.
        "message_only": None,  # boolean - If true, notification email bodies contain only the custom message, omitting event details and the review button. Requires a custom message, defaults to false, and does not affect non-email targets.
        "enabled": None,  # boolean - Whether this Event Subscription can dispatch events.
        "event_types": None,  # array(string) - Event type strings matched by this subscription. Blank means all event types. Valid values: `automation_run.canceled.v1`, `automation_run.failure.v1`, `automation_run.failure_will_retry.v1`, `automation_run.partial_failure.v1`, `automation_run.partial_failure_will_retry.v1`, `automation_run.skipped.v1`, `automation_run.success.v1`, `expectation_evaluation.invalid.v1`, `expectation_evaluation.late.v1`, `expectation_evaluation.missing.v1`, `expectation_evaluation.success.v1`, `expectation_incident.acknowledged.v1`, `expectation_incident.open.v1`, `expectation_incident.resolved.v1`, `expectation_incident.snoozed.v1`, `external_event.client_log.failure.v1`, `external_event.client_log.partial_failure.v1`, `external_event.client_log.skipped.v1`, `external_event.client_log.success.v1`, `pending_work_event.failure.v1`, `pending_work_event.partial_failure.v1`, `pending_work_event.skipped.v1`, `pending_work_event.success.v1`, `siem_http_destination_event.failure.v1`, `siem_http_destination_event.partial_failure.v1`, `siem_http_destination_event.skipped.v1`, `siem_http_destination_event.success.v1`, `sso_event.ldap_login.failure.v1`, `sso_event.ldap_login.partial_failure.v1`, `sso_event.ldap_login.skipped.v1`, `sso_event.ldap_login.success.v1`, `sso_event.ldap_sync.failure.v1`, `sso_event.ldap_sync.partial_failure.v1`, `sso_event.ldap_sync.skipped.v1`, `sso_event.ldap_sync.success.v1`, `sso_event.saml_login.failure.v1`, `sso_event.saml_login.partial_failure.v1`, `sso_event.saml_login.skipped.v1`, `sso_event.saml_login.success.v1`, `sync_run.failure.v1`, `sync_run.partial_failure.v1`, `sync_run.skipped.v1`, `sync_run.success.v1`, `user_security_event.lockout.v1`
        "filter": None,  # object - Conditions on event fields that an event must meet to be delivered, keyed by dot-notation field path. All conditions must match.
        "delivery_policy": None,  # object - Event Subscription delivery policy.
        "event_target_ids": None,  # array(int64) - Event Target IDs this subscription sends to.
        "created_at": None,  # date-time - Event Subscription create date/time.
        "updated_at": None,  # date-time - Event Subscription update date/time.
    }

    # Declared for type checkers and editors: the type the API sends each
    # attribute as, or None. set_attributes stores each value as given,
    # converting only decimals, so a value a caller sets can differ.
    id: int | None
    event_channel_id: int | None
    workspace_id: int | None
    apply_to_all_workspaces: bool | None
    name: str | None
    subject: str | None
    message: str | None
    message_only: bool | None
    enabled: bool | None
    event_types: builtins.list[str] | None
    filter: dict[str, Any] | None
    delivery_policy: dict[str, Any] | None
    event_target_ids: builtins.list[int] | None
    created_at: str | None
    updated_at: str | None

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
        for (
            attribute,
            default_value,
        ) in EventSubscription.default_attributes.items():
            value = attributes.get(attribute, default_value)
            setattr(self, attribute, value)

    def get_attributes(self):
        attrs = {
            k: getattr(self, k, None)
            for k in EventSubscription.default_attributes
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
          event_channel_id - int64 - Event Channel ID
          workspace_id - int64 - Workspace ID. 0 means the default workspace or site-wide.
          apply_to_all_workspaces - boolean - If true, this default-workspace subscription applies to events from all workspaces.
          name - string - Event Subscription name.
          subject - string - Custom subject line to use for notification emails.
          message - string - Custom message to include in notification emails.
          message_only - boolean - If true, notification email bodies contain only the custom message, omitting event details and the review button. Requires a custom message, defaults to false, and does not affect non-email targets.
          enabled - boolean - Whether this Event Subscription can dispatch events.
          event_types - array(string) - Event type strings matched by this subscription. Blank means all event types. Valid values: `automation_run.canceled.v1`, `automation_run.failure.v1`, `automation_run.failure_will_retry.v1`, `automation_run.partial_failure.v1`, `automation_run.partial_failure_will_retry.v1`, `automation_run.skipped.v1`, `automation_run.success.v1`, `expectation_evaluation.invalid.v1`, `expectation_evaluation.late.v1`, `expectation_evaluation.missing.v1`, `expectation_evaluation.success.v1`, `expectation_incident.acknowledged.v1`, `expectation_incident.open.v1`, `expectation_incident.resolved.v1`, `expectation_incident.snoozed.v1`, `external_event.client_log.failure.v1`, `external_event.client_log.partial_failure.v1`, `external_event.client_log.skipped.v1`, `external_event.client_log.success.v1`, `pending_work_event.failure.v1`, `pending_work_event.partial_failure.v1`, `pending_work_event.skipped.v1`, `pending_work_event.success.v1`, `siem_http_destination_event.failure.v1`, `siem_http_destination_event.partial_failure.v1`, `siem_http_destination_event.skipped.v1`, `siem_http_destination_event.success.v1`, `sso_event.ldap_login.failure.v1`, `sso_event.ldap_login.partial_failure.v1`, `sso_event.ldap_login.skipped.v1`, `sso_event.ldap_login.success.v1`, `sso_event.ldap_sync.failure.v1`, `sso_event.ldap_sync.partial_failure.v1`, `sso_event.ldap_sync.skipped.v1`, `sso_event.ldap_sync.success.v1`, `sso_event.saml_login.failure.v1`, `sso_event.saml_login.partial_failure.v1`, `sso_event.saml_login.skipped.v1`, `sso_event.saml_login.success.v1`, `sync_run.failure.v1`, `sync_run.partial_failure.v1`, `sync_run.skipped.v1`, `sync_run.success.v1`, `user_security_event.lockout.v1`
          filter - object - Conditions on event fields that an event must meet to be delivered, keyed by dot-notation field path. All conditions must match.
          delivery_policy - object - Event Subscription delivery policy.
          event_target_ids - array(int64) - Event Target IDs this subscription sends to.
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
        if "event_channel_id" in params and (
            not isinstance(params["event_channel_id"], int)
            or isinstance(params["event_channel_id"], bool)
        ):
            raise InvalidParameterError(
                "Bad parameter: event_channel_id must be an int"
            )
        if "workspace_id" in params and (
            not isinstance(params["workspace_id"], int)
            or isinstance(params["workspace_id"], bool)
        ):
            raise InvalidParameterError(
                "Bad parameter: workspace_id must be an int"
            )
        if "apply_to_all_workspaces" in params and isinstance(
            params["apply_to_all_workspaces"], (builtins.list, tuple, dict)
        ):
            raise InvalidParameterError(
                "Bad parameter: apply_to_all_workspaces must be an bool"
            )
        if "name" in params and not isinstance(params["name"], str):
            raise InvalidParameterError("Bad parameter: name must be an str")
        if "subject" in params and not isinstance(params["subject"], str):
            raise InvalidParameterError(
                "Bad parameter: subject must be an str"
            )
        if "message" in params and not isinstance(params["message"], str):
            raise InvalidParameterError(
                "Bad parameter: message must be an str"
            )
        if "message_only" in params and isinstance(
            params["message_only"], (builtins.list, tuple, dict)
        ):
            raise InvalidParameterError(
                "Bad parameter: message_only must be an bool"
            )
        if "enabled" in params and isinstance(
            params["enabled"], (builtins.list, tuple, dict)
        ):
            raise InvalidParameterError(
                "Bad parameter: enabled must be an bool"
            )
        if "event_types" in params and not isinstance(
            params["event_types"], builtins.list
        ):
            raise InvalidParameterError(
                "Bad parameter: event_types must be an list"
            )
        if "event_target_ids" in params and not isinstance(
            params["event_target_ids"], builtins.list
        ):
            raise InvalidParameterError(
                "Bad parameter: event_target_ids must be an list"
            )
        operation = Operation.start(self._scope())
        response = operation.request(
            "PATCH", "/event_subscriptions/" + path_value(params["id"]), params
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
            "DELETE",
            "/event_subscriptions/" + path_value(params["id"]),
            params,
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
            new_obj = EventSubscriptionResource(self._scope()).create(
                self.get_attributes()
            )
            self.set_attributes(new_obj.get_attributes())
            self._context = new_obj._context


class EventSubscriptionResource:
    """EventSubscription operations that use one client's configuration.

    Get one from a client, such as ``client.event_subscription``. Each operation
    takes the same arguments as the module-level function of the same name,
    and its options apply on top of the client's.
    """

    def __init__(self, scope):
        self._scope = scope

    def list(
        self,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> ListObj[EventSubscription]:
        """Parameters:
        cursor - string - Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
        per_page - int64 - Number of records to show per page.  (Max: 10000, 1,000 or less is recommended).
        sort_by - object - If set, sort records by the specified field in either `asc` or `desc` direction. Valid fields are `name`, `enabled`, `event_channel_id` or `workspace_id`.
        filter - object - If set, return records where the specified field is equal to the supplied value. Valid fields are `enabled`, `event_channel_id` or `workspace_id`. Valid field combinations are `[ enabled, event_channel_id ]`, `[ workspace_id, enabled ]`, `[ workspace_id, event_channel_id ]` or `[ workspace_id, enabled, event_channel_id ]`.
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
        return ListObj(
            EventSubscription, "GET", "/event_subscriptions", params, operation
        )

    def all(
        self,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> ListObj[EventSubscription]:
        """The same as list()."""
        return self.list(params, options)

    def find(
        self,
        id: int,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> EventSubscription:
        """Parameters:
        id (required) - int64 - Event Subscription ID.
        """
        return self.__find({"id": id}, params, options)

    def __find(
        self,
        path_values: dict[str, Any],
        params: dict[str, Any] | None,
        options: RequestOptions | Mapping[str, Any] | None,
    ) -> EventSubscription:
        params = copy_params(params, path_values)
        if "id" in params and (
            not isinstance(params["id"], int) or isinstance(params["id"], bool)
        ):
            raise InvalidParameterError("Bad parameter: id must be an int")
        if "id" not in params:
            raise MissingParameterError("Parameter missing: id")
        operation = Operation.start(self._scope, options)
        response = operation.request(
            "GET", "/event_subscriptions/" + path_value(params["id"]), params
        )
        return operation.decode_model(response, EventSubscription)

    def get(
        self,
        id: int,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> EventSubscription:
        """The same as find()."""
        return self.find(id, params, options)

    def create(
        self,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> EventSubscription:
        """Parameters:
        event_channel_id - int64 - Event Channel ID
        workspace_id - int64 - Workspace ID. 0 means the default workspace or site-wide.
        apply_to_all_workspaces - boolean - If true, this default-workspace subscription applies to events from all workspaces.
        name (required) - string - Event Subscription name.
        subject - string - Custom subject line to use for notification emails.
        message - string - Custom message to include in notification emails.
        message_only - boolean - If true, notification email bodies contain only the custom message, omitting event details and the review button. Requires a custom message, defaults to false, and does not affect non-email targets.
        enabled - boolean - Whether this Event Subscription can dispatch events.
        event_types - array(string) - Event type strings matched by this subscription. Blank means all event types. Valid values: `automation_run.canceled.v1`, `automation_run.failure.v1`, `automation_run.failure_will_retry.v1`, `automation_run.partial_failure.v1`, `automation_run.partial_failure_will_retry.v1`, `automation_run.skipped.v1`, `automation_run.success.v1`, `expectation_evaluation.invalid.v1`, `expectation_evaluation.late.v1`, `expectation_evaluation.missing.v1`, `expectation_evaluation.success.v1`, `expectation_incident.acknowledged.v1`, `expectation_incident.open.v1`, `expectation_incident.resolved.v1`, `expectation_incident.snoozed.v1`, `external_event.client_log.failure.v1`, `external_event.client_log.partial_failure.v1`, `external_event.client_log.skipped.v1`, `external_event.client_log.success.v1`, `pending_work_event.failure.v1`, `pending_work_event.partial_failure.v1`, `pending_work_event.skipped.v1`, `pending_work_event.success.v1`, `siem_http_destination_event.failure.v1`, `siem_http_destination_event.partial_failure.v1`, `siem_http_destination_event.skipped.v1`, `siem_http_destination_event.success.v1`, `sso_event.ldap_login.failure.v1`, `sso_event.ldap_login.partial_failure.v1`, `sso_event.ldap_login.skipped.v1`, `sso_event.ldap_login.success.v1`, `sso_event.ldap_sync.failure.v1`, `sso_event.ldap_sync.partial_failure.v1`, `sso_event.ldap_sync.skipped.v1`, `sso_event.ldap_sync.success.v1`, `sso_event.saml_login.failure.v1`, `sso_event.saml_login.partial_failure.v1`, `sso_event.saml_login.skipped.v1`, `sso_event.saml_login.success.v1`, `sync_run.failure.v1`, `sync_run.partial_failure.v1`, `sync_run.skipped.v1`, `sync_run.success.v1`, `user_security_event.lockout.v1`
        filter - object - Conditions on event fields that an event must meet to be delivered, keyed by dot-notation field path. All conditions must match.
        delivery_policy - object - Event Subscription delivery policy.
        event_target_ids - array(int64) - Event Target IDs this subscription sends to.
        """
        params = copy_params(params)
        if "event_channel_id" in params and (
            not isinstance(params["event_channel_id"], int)
            or isinstance(params["event_channel_id"], bool)
        ):
            raise InvalidParameterError(
                "Bad parameter: event_channel_id must be an int"
            )
        if "workspace_id" in params and (
            not isinstance(params["workspace_id"], int)
            or isinstance(params["workspace_id"], bool)
        ):
            raise InvalidParameterError(
                "Bad parameter: workspace_id must be an int"
            )
        if "apply_to_all_workspaces" in params and not isinstance(
            params["apply_to_all_workspaces"], bool
        ):
            raise InvalidParameterError(
                "Bad parameter: apply_to_all_workspaces must be an bool"
            )
        if "name" in params and not isinstance(params["name"], str):
            raise InvalidParameterError("Bad parameter: name must be an str")
        if "subject" in params and not isinstance(params["subject"], str):
            raise InvalidParameterError(
                "Bad parameter: subject must be an str"
            )
        if "message" in params and not isinstance(params["message"], str):
            raise InvalidParameterError(
                "Bad parameter: message must be an str"
            )
        if "message_only" in params and not isinstance(
            params["message_only"], bool
        ):
            raise InvalidParameterError(
                "Bad parameter: message_only must be an bool"
            )
        if "enabled" in params and not isinstance(params["enabled"], bool):
            raise InvalidParameterError(
                "Bad parameter: enabled must be an bool"
            )
        if "event_types" in params and not isinstance(
            params["event_types"], builtins.list
        ):
            raise InvalidParameterError(
                "Bad parameter: event_types must be an list"
            )
        if "filter" in params and not isinstance(params["filter"], dict):
            raise InvalidParameterError(
                "Bad parameter: filter must be an dict"
            )
        if "delivery_policy" in params and not isinstance(
            params["delivery_policy"], dict
        ):
            raise InvalidParameterError(
                "Bad parameter: delivery_policy must be an dict"
            )
        if "event_target_ids" in params and not isinstance(
            params["event_target_ids"], builtins.list
        ):
            raise InvalidParameterError(
                "Bad parameter: event_target_ids must be an list"
            )
        if "name" not in params:
            raise MissingParameterError("Parameter missing: name")
        operation = Operation.start(self._scope, options)
        response = operation.request("POST", "/event_subscriptions", params)
        return operation.decode_model(response, EventSubscription)

    def update(
        self,
        id: int,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> EventSubscription:
        """Parameters:
        event_channel_id - int64 - Event Channel ID
        workspace_id - int64 - Workspace ID. 0 means the default workspace or site-wide.
        apply_to_all_workspaces - boolean - If true, this default-workspace subscription applies to events from all workspaces.
        name - string - Event Subscription name.
        subject - string - Custom subject line to use for notification emails.
        message - string - Custom message to include in notification emails.
        message_only - boolean - If true, notification email bodies contain only the custom message, omitting event details and the review button. Requires a custom message, defaults to false, and does not affect non-email targets.
        enabled - boolean - Whether this Event Subscription can dispatch events.
        event_types - array(string) - Event type strings matched by this subscription. Blank means all event types. Valid values: `automation_run.canceled.v1`, `automation_run.failure.v1`, `automation_run.failure_will_retry.v1`, `automation_run.partial_failure.v1`, `automation_run.partial_failure_will_retry.v1`, `automation_run.skipped.v1`, `automation_run.success.v1`, `expectation_evaluation.invalid.v1`, `expectation_evaluation.late.v1`, `expectation_evaluation.missing.v1`, `expectation_evaluation.success.v1`, `expectation_incident.acknowledged.v1`, `expectation_incident.open.v1`, `expectation_incident.resolved.v1`, `expectation_incident.snoozed.v1`, `external_event.client_log.failure.v1`, `external_event.client_log.partial_failure.v1`, `external_event.client_log.skipped.v1`, `external_event.client_log.success.v1`, `pending_work_event.failure.v1`, `pending_work_event.partial_failure.v1`, `pending_work_event.skipped.v1`, `pending_work_event.success.v1`, `siem_http_destination_event.failure.v1`, `siem_http_destination_event.partial_failure.v1`, `siem_http_destination_event.skipped.v1`, `siem_http_destination_event.success.v1`, `sso_event.ldap_login.failure.v1`, `sso_event.ldap_login.partial_failure.v1`, `sso_event.ldap_login.skipped.v1`, `sso_event.ldap_login.success.v1`, `sso_event.ldap_sync.failure.v1`, `sso_event.ldap_sync.partial_failure.v1`, `sso_event.ldap_sync.skipped.v1`, `sso_event.ldap_sync.success.v1`, `sso_event.saml_login.failure.v1`, `sso_event.saml_login.partial_failure.v1`, `sso_event.saml_login.skipped.v1`, `sso_event.saml_login.success.v1`, `sync_run.failure.v1`, `sync_run.partial_failure.v1`, `sync_run.skipped.v1`, `sync_run.success.v1`, `user_security_event.lockout.v1`
        filter - object - Conditions on event fields that an event must meet to be delivered, keyed by dot-notation field path. All conditions must match.
        delivery_policy - object - Event Subscription delivery policy.
        event_target_ids - array(int64) - Event Target IDs this subscription sends to.
        """
        return self.__update({"id": id}, params, options)

    def __update(
        self,
        path_values: dict[str, Any],
        params: dict[str, Any] | None,
        options: RequestOptions | Mapping[str, Any] | None,
    ) -> EventSubscription:
        params = copy_params(params, path_values)
        if "id" in params and (
            not isinstance(params["id"], int) or isinstance(params["id"], bool)
        ):
            raise InvalidParameterError("Bad parameter: id must be an int")
        if "event_channel_id" in params and (
            not isinstance(params["event_channel_id"], int)
            or isinstance(params["event_channel_id"], bool)
        ):
            raise InvalidParameterError(
                "Bad parameter: event_channel_id must be an int"
            )
        if "workspace_id" in params and (
            not isinstance(params["workspace_id"], int)
            or isinstance(params["workspace_id"], bool)
        ):
            raise InvalidParameterError(
                "Bad parameter: workspace_id must be an int"
            )
        if "apply_to_all_workspaces" in params and not isinstance(
            params["apply_to_all_workspaces"], bool
        ):
            raise InvalidParameterError(
                "Bad parameter: apply_to_all_workspaces must be an bool"
            )
        if "name" in params and not isinstance(params["name"], str):
            raise InvalidParameterError("Bad parameter: name must be an str")
        if "subject" in params and not isinstance(params["subject"], str):
            raise InvalidParameterError(
                "Bad parameter: subject must be an str"
            )
        if "message" in params and not isinstance(params["message"], str):
            raise InvalidParameterError(
                "Bad parameter: message must be an str"
            )
        if "message_only" in params and not isinstance(
            params["message_only"], bool
        ):
            raise InvalidParameterError(
                "Bad parameter: message_only must be an bool"
            )
        if "enabled" in params and not isinstance(params["enabled"], bool):
            raise InvalidParameterError(
                "Bad parameter: enabled must be an bool"
            )
        if "event_types" in params and not isinstance(
            params["event_types"], builtins.list
        ):
            raise InvalidParameterError(
                "Bad parameter: event_types must be an list"
            )
        if "filter" in params and not isinstance(params["filter"], dict):
            raise InvalidParameterError(
                "Bad parameter: filter must be an dict"
            )
        if "delivery_policy" in params and not isinstance(
            params["delivery_policy"], dict
        ):
            raise InvalidParameterError(
                "Bad parameter: delivery_policy must be an dict"
            )
        if "event_target_ids" in params and not isinstance(
            params["event_target_ids"], builtins.list
        ):
            raise InvalidParameterError(
                "Bad parameter: event_target_ids must be an list"
            )
        if "id" not in params:
            raise MissingParameterError("Parameter missing: id")
        operation = Operation.start(self._scope, options)
        response = operation.request(
            "PATCH", "/event_subscriptions/" + path_value(params["id"]), params
        )
        return operation.decode_model(response, EventSubscription)

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
            "DELETE",
            "/event_subscriptions/" + path_value(params["id"]),
            params,
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
    ) -> EventSubscription:
        """A new EventSubscription with attributes, not yet saved, whose
        operations use this resource's client."""
        obj = EventSubscription(attributes, options)
        obj._context = self._scope._context_for(options)
        return obj


_legacy_resource = EventSubscriptionResource(LEGACY)


def list(
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> ListObj[EventSubscription]:
    """Parameters:
    cursor - string - Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
    per_page - int64 - Number of records to show per page.  (Max: 10000, 1,000 or less is recommended).
    sort_by - object - If set, sort records by the specified field in either `asc` or `desc` direction. Valid fields are `name`, `enabled`, `event_channel_id` or `workspace_id`.
    filter - object - If set, return records where the specified field is equal to the supplied value. Valid fields are `enabled`, `event_channel_id` or `workspace_id`. Valid field combinations are `[ enabled, event_channel_id ]`, `[ workspace_id, enabled ]`, `[ workspace_id, event_channel_id ]` or `[ workspace_id, enabled, event_channel_id ]`.
    """
    return _legacy_resource.list(params, options)


def all(
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> ListObj[EventSubscription]:
    """The same as list()."""
    return _legacy_resource.list(params, options)


def find(
    id: int,
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> EventSubscription:
    """Parameters:
    id (required) - int64 - Event Subscription ID.
    """
    return _legacy_resource.find(id, params, options)


def get(
    id: int,
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> EventSubscription:
    """The same as find()."""
    return _legacy_resource.find(id, params, options)


def create(
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> EventSubscription:
    """Parameters:
    event_channel_id - int64 - Event Channel ID
    workspace_id - int64 - Workspace ID. 0 means the default workspace or site-wide.
    apply_to_all_workspaces - boolean - If true, this default-workspace subscription applies to events from all workspaces.
    name (required) - string - Event Subscription name.
    subject - string - Custom subject line to use for notification emails.
    message - string - Custom message to include in notification emails.
    message_only - boolean - If true, notification email bodies contain only the custom message, omitting event details and the review button. Requires a custom message, defaults to false, and does not affect non-email targets.
    enabled - boolean - Whether this Event Subscription can dispatch events.
    event_types - array(string) - Event type strings matched by this subscription. Blank means all event types. Valid values: `automation_run.canceled.v1`, `automation_run.failure.v1`, `automation_run.failure_will_retry.v1`, `automation_run.partial_failure.v1`, `automation_run.partial_failure_will_retry.v1`, `automation_run.skipped.v1`, `automation_run.success.v1`, `expectation_evaluation.invalid.v1`, `expectation_evaluation.late.v1`, `expectation_evaluation.missing.v1`, `expectation_evaluation.success.v1`, `expectation_incident.acknowledged.v1`, `expectation_incident.open.v1`, `expectation_incident.resolved.v1`, `expectation_incident.snoozed.v1`, `external_event.client_log.failure.v1`, `external_event.client_log.partial_failure.v1`, `external_event.client_log.skipped.v1`, `external_event.client_log.success.v1`, `pending_work_event.failure.v1`, `pending_work_event.partial_failure.v1`, `pending_work_event.skipped.v1`, `pending_work_event.success.v1`, `siem_http_destination_event.failure.v1`, `siem_http_destination_event.partial_failure.v1`, `siem_http_destination_event.skipped.v1`, `siem_http_destination_event.success.v1`, `sso_event.ldap_login.failure.v1`, `sso_event.ldap_login.partial_failure.v1`, `sso_event.ldap_login.skipped.v1`, `sso_event.ldap_login.success.v1`, `sso_event.ldap_sync.failure.v1`, `sso_event.ldap_sync.partial_failure.v1`, `sso_event.ldap_sync.skipped.v1`, `sso_event.ldap_sync.success.v1`, `sso_event.saml_login.failure.v1`, `sso_event.saml_login.partial_failure.v1`, `sso_event.saml_login.skipped.v1`, `sso_event.saml_login.success.v1`, `sync_run.failure.v1`, `sync_run.partial_failure.v1`, `sync_run.skipped.v1`, `sync_run.success.v1`, `user_security_event.lockout.v1`
    filter - object - Conditions on event fields that an event must meet to be delivered, keyed by dot-notation field path. All conditions must match.
    delivery_policy - object - Event Subscription delivery policy.
    event_target_ids - array(int64) - Event Target IDs this subscription sends to.
    """
    return _legacy_resource.create(params, options)


def update(
    id: int,
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> EventSubscription:
    """Parameters:
    event_channel_id - int64 - Event Channel ID
    workspace_id - int64 - Workspace ID. 0 means the default workspace or site-wide.
    apply_to_all_workspaces - boolean - If true, this default-workspace subscription applies to events from all workspaces.
    name - string - Event Subscription name.
    subject - string - Custom subject line to use for notification emails.
    message - string - Custom message to include in notification emails.
    message_only - boolean - If true, notification email bodies contain only the custom message, omitting event details and the review button. Requires a custom message, defaults to false, and does not affect non-email targets.
    enabled - boolean - Whether this Event Subscription can dispatch events.
    event_types - array(string) - Event type strings matched by this subscription. Blank means all event types. Valid values: `automation_run.canceled.v1`, `automation_run.failure.v1`, `automation_run.failure_will_retry.v1`, `automation_run.partial_failure.v1`, `automation_run.partial_failure_will_retry.v1`, `automation_run.skipped.v1`, `automation_run.success.v1`, `expectation_evaluation.invalid.v1`, `expectation_evaluation.late.v1`, `expectation_evaluation.missing.v1`, `expectation_evaluation.success.v1`, `expectation_incident.acknowledged.v1`, `expectation_incident.open.v1`, `expectation_incident.resolved.v1`, `expectation_incident.snoozed.v1`, `external_event.client_log.failure.v1`, `external_event.client_log.partial_failure.v1`, `external_event.client_log.skipped.v1`, `external_event.client_log.success.v1`, `pending_work_event.failure.v1`, `pending_work_event.partial_failure.v1`, `pending_work_event.skipped.v1`, `pending_work_event.success.v1`, `siem_http_destination_event.failure.v1`, `siem_http_destination_event.partial_failure.v1`, `siem_http_destination_event.skipped.v1`, `siem_http_destination_event.success.v1`, `sso_event.ldap_login.failure.v1`, `sso_event.ldap_login.partial_failure.v1`, `sso_event.ldap_login.skipped.v1`, `sso_event.ldap_login.success.v1`, `sso_event.ldap_sync.failure.v1`, `sso_event.ldap_sync.partial_failure.v1`, `sso_event.ldap_sync.skipped.v1`, `sso_event.ldap_sync.success.v1`, `sso_event.saml_login.failure.v1`, `sso_event.saml_login.partial_failure.v1`, `sso_event.saml_login.skipped.v1`, `sso_event.saml_login.success.v1`, `sync_run.failure.v1`, `sync_run.partial_failure.v1`, `sync_run.skipped.v1`, `sync_run.success.v1`, `user_security_event.lockout.v1`
    filter - object - Conditions on event fields that an event must meet to be delivered, keyed by dot-notation field path. All conditions must match.
    delivery_policy - object - Event Subscription delivery policy.
    event_target_ids - array(int64) - Event Target IDs this subscription sends to.
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


def new(*args, **kwargs) -> EventSubscription:
    return EventSubscription(*args, **kwargs)
