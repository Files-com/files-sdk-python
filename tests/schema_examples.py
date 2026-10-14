"""The record attributes whose schema example is a placeholder, not a
value of the attribute's declared type, such as "example" for an object or
["example"] for a list of objects. The mock server answers with those
examples, so the generated tests do not hold these attributes to their
declared types, which the records' annotations follow."""

PLACEHOLDERS: dict[str, set[str]] = {
    "Automation": {"definition"},
    "AutomationAuthoringSchema": {
        "definition_schema",
        "error_families",
        "nodes",
    },
    "AutomationExecutionNode": {
        "inputs",
        "outputs",
        "input_items",
        "output_items",
    },
    "AutomationRun": {"definition", "node_states"},
    "Behavior": {"value"},
    "Bundle": {"requested_upload_slots"},
    "ChildSiteManagementPolicy": {"value"},
    "EventRecord": {"human_fields", "actor", "resources", "payload"},
    "EventSubscription": {"delivery_policy"},
    "EventTarget": {"config", "delivery_policy"},
    "HolidayCalendar": {"definition"},
    "IntegrationCentricProfile": {"expected_remote_servers"},
    "Site": {"managed_site_settings"},
    "Style": {"logo"},
}
