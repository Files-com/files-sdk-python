import files_sdk.models.account_line_item as account_line_item
import files_sdk.models.action as action
import files_sdk.models.api_key as api_key
import files_sdk.models.app as app
import files_sdk.models.as2_key as as2_key
import files_sdk.models.auto as auto
import files_sdk.models.automation as automation
import files_sdk.models.bandwidth_snapshot as bandwidth_snapshot
import files_sdk.models.behavior as behavior
import files_sdk.models.bundle as bundle
import files_sdk.models.bundle_download as bundle_download
import files_sdk.models.bundle_recipient as bundle_recipient
import files_sdk.models.clickwrap as clickwrap
import files_sdk.models.dns_record as dns_record
import files_sdk.models.errors as errors
import files_sdk.models.external_event as external_event
import files_sdk.models.file as file
import files_sdk.models.file_action as file_action
import files_sdk.models.file_comment as file_comment
import files_sdk.models.file_comment_reaction as file_comment_reaction
import files_sdk.models.file_part_upload as file_part_upload
import files_sdk.models.folder as folder
import files_sdk.models.group as group
import files_sdk.models.group_user as group_user
import files_sdk.models.history as history
import files_sdk.models.history_export as history_export
import files_sdk.models.history_export_result as history_export_result
import files_sdk.models.image as image
import files_sdk.models.invoice as invoice
import files_sdk.models.invoice_line_item as invoice_line_item
import files_sdk.models.ip_address as ip_address
import files_sdk.models.lock as lock
import files_sdk.models.message as message
import files_sdk.models.message_comment as message_comment
import files_sdk.models.message_comment_reaction as message_comment_reaction
import files_sdk.models.message_reaction as message_reaction
import files_sdk.models.notification as notification
import files_sdk.models.payment as payment
import files_sdk.models.payment_line_item as payment_line_item
import files_sdk.models.permission as permission
import files_sdk.models.preview as preview
import files_sdk.models.project as project
import files_sdk.models.public_ip_address as public_ip_address
import files_sdk.models.public_key as public_key
import files_sdk.models.remote_server as remote_server
import files_sdk.models.request as request
import files_sdk.models.session as session
import files_sdk.models.settings_change as settings_change
import files_sdk.models.site as site
import files_sdk.models.sso_strategy as sso_strategy
import files_sdk.models.status as status
import files_sdk.models.style as style
import files_sdk.models.usage_daily_snapshot as usage_daily_snapshot
import files_sdk.models.usage_snapshot as usage_snapshot
import files_sdk.models.user as user
import files_sdk.models.user_cipher_use as user_cipher_use
import files_sdk.models.user_request as user_request

the_api_key = ""
session_id = None
base_url = "https://app.files.com"
base_path = "api/rest/v1"
version = "1.0"

initial_network_retry_delay = 0.5
max_network_retry_delay = 2
open_timeout = 30
read_timeout = 80
max_network_retries = 3

console_log_level="none"

OPTS = ("api_key", "client", "session_id")

def set_api_key(api_key):
    global the_api_key
    the_api_key = api_key

def get_api_key():
    global the_api_key
    return the_api_key

def set_session(session):
    if not session.id:
        session.save()
    global session_id
    session_id = session.id

def open(*args, **kwargs):
    return file.open(*args, **kwargs)

def upload_file(*args, **kwargs):
    return file.upload_file(*args, **kwargs)

def download_file(*args, **kwargs):
    return file.download_file(*args, **kwargs)

def list_for(*args, **kwargs):
    return folder.list_for(*args, **kwargs)