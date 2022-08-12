# FormField

## Example FormField Object

```
{
  "id": 1,
  "label": "Sample Label",
  "required": True,
  "help_text": "Help Text",
  "field_type": "text",
  "options_for_select": [
    "red",
    "green",
    "blue"
  ],
  "default_option": "red",
  "form_field_set_id": 1
}
```

* `id` (int64): Form field id
* `label` (string): Label to be displayed
* `required` (boolean): Is this a required field?
* `help_text` (string): Help text to be displayed
* `field_type` (string): Type of Field
* `options_for_select` (array): Options to display for radio and dropdown
* `default_option` (string): Default option for radio and dropdown
* `form_field_set_id` (int64): Form field set id
