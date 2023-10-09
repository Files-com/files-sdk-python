from pathlib import Path
import files_sdk.models.account_line_item as account_line_item
import files_sdk.models.action as action
import files_sdk.models.action_notification_export as action_notification_export
import files_sdk.models.action_notification_export_result as action_notification_export_result
import files_sdk.models.action_webhook_failure as action_webhook_failure
import files_sdk.models.api_key as api_key
import files_sdk.models.app as app
import files_sdk.models.as2_incoming_message as as2_incoming_message
import files_sdk.models.as2_outgoing_message as as2_outgoing_message
import files_sdk.models.as2_partner as as2_partner
import files_sdk.models.as2_station as as2_station
import files_sdk.models.auto as auto
import files_sdk.models.automation as automation
import files_sdk.models.automation_run as automation_run
import files_sdk.models.bandwidth_snapshot as bandwidth_snapshot
import files_sdk.models.behavior as behavior
import files_sdk.models.bundle as bundle
import files_sdk.models.bundle_download as bundle_download
import files_sdk.models.bundle_notification as bundle_notification
import files_sdk.models.bundle_recipient as bundle_recipient
import files_sdk.models.bundle_registration as bundle_registration
import files_sdk.models.clickwrap as clickwrap
import files_sdk.models.dns_record as dns_record
import files_sdk.models.email_incoming_message as email_incoming_message
import files_sdk.models.errors as errors
import files_sdk.models.external_event as external_event
import files_sdk.models.file as file
import files_sdk.models.file_action as file_action
import files_sdk.models.file_comment as file_comment
import files_sdk.models.file_comment_reaction as file_comment_reaction
import files_sdk.models.file_migration as file_migration
import files_sdk.models.file_upload_part as file_upload_part
import files_sdk.models.folder as folder
import files_sdk.models.form_field as form_field
import files_sdk.models.form_field_set as form_field_set
import files_sdk.models.gpg_key as gpg_key
import files_sdk.models.group as group
import files_sdk.models.group_user as group_user
import files_sdk.models.history as history
import files_sdk.models.history_export as history_export
import files_sdk.models.history_export_result as history_export_result
import files_sdk.models.image as image
import files_sdk.models.inbox_recipient as inbox_recipient
import files_sdk.models.inbox_registration as inbox_registration
import files_sdk.models.inbox_upload as inbox_upload
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
import files_sdk.models.priority as priority
import files_sdk.models.project as project
import files_sdk.models.public_ip_address as public_ip_address
import files_sdk.models.public_key as public_key
import files_sdk.models.remote_bandwidth_snapshot as remote_bandwidth_snapshot
import files_sdk.models.remote_server as remote_server
import files_sdk.models.remote_server_configuration_file as remote_server_configuration_file
import files_sdk.models.request as request
import files_sdk.models.session as session
import files_sdk.models.settings_change as settings_change
import files_sdk.models.sftp_host_key as sftp_host_key
import files_sdk.models.share_group as share_group
import files_sdk.models.share_group_member as share_group_member
import files_sdk.models.site as site
import files_sdk.models.snapshot as snapshot
import files_sdk.models.sso_strategy as sso_strategy
import files_sdk.models.status as status
import files_sdk.models.style as style
import files_sdk.models.usage_daily_snapshot as usage_daily_snapshot
import files_sdk.models.usage_snapshot as usage_snapshot
import files_sdk.models.user as user
import files_sdk.models.user_cipher_use as user_cipher_use
import files_sdk.models.user_request as user_request
import files_sdk.models.webhook_test as webhook_test

from files_sdk.models.account_line_item import AccountLineItem
from files_sdk.models.action import Action
from files_sdk.models.action_notification_export import (
    ActionNotificationExport,
)
from files_sdk.models.action_notification_export_result import (
    ActionNotificationExportResult,
)
from files_sdk.models.action_webhook_failure import ActionWebhookFailure
from files_sdk.models.api_key import ApiKey
from files_sdk.models.app import App
from files_sdk.models.as2_incoming_message import As2IncomingMessage
from files_sdk.models.as2_outgoing_message import As2OutgoingMessage
from files_sdk.models.as2_partner import As2Partner
from files_sdk.models.as2_station import As2Station
from files_sdk.models.auto import Auto
from files_sdk.models.automation import Automation
from files_sdk.models.automation_run import AutomationRun
from files_sdk.models.bandwidth_snapshot import BandwidthSnapshot
from files_sdk.models.behavior import Behavior
from files_sdk.models.bundle import Bundle
from files_sdk.models.bundle_download import BundleDownload
from files_sdk.models.bundle_notification import BundleNotification
from files_sdk.models.bundle_recipient import BundleRecipient
from files_sdk.models.bundle_registration import BundleRegistration
from files_sdk.models.clickwrap import Clickwrap
from files_sdk.models.dns_record import DnsRecord
from files_sdk.models.email_incoming_message import EmailIncomingMessage
from files_sdk.models.errors import Errors
from files_sdk.models.external_event import ExternalEvent
from files_sdk.models.file import File
from files_sdk.models.file_action import FileAction
from files_sdk.models.file_comment import FileComment
from files_sdk.models.file_comment_reaction import FileCommentReaction
from files_sdk.models.file_migration import FileMigration
from files_sdk.models.file_upload_part import FileUploadPart
from files_sdk.models.folder import Folder
from files_sdk.models.form_field import FormField
from files_sdk.models.form_field_set import FormFieldSet
from files_sdk.models.gpg_key import GpgKey
from files_sdk.models.group import Group
from files_sdk.models.group_user import GroupUser
from files_sdk.models.history import History
from files_sdk.models.history_export import HistoryExport
from files_sdk.models.history_export_result import HistoryExportResult
from files_sdk.models.image import Image
from files_sdk.models.inbox_recipient import InboxRecipient
from files_sdk.models.inbox_registration import InboxRegistration
from files_sdk.models.inbox_upload import InboxUpload
from files_sdk.models.invoice import Invoice
from files_sdk.models.invoice_line_item import InvoiceLineItem
from files_sdk.models.ip_address import IpAddress
from files_sdk.models.lock import Lock
from files_sdk.models.message import Message
from files_sdk.models.message_comment import MessageComment
from files_sdk.models.message_comment_reaction import MessageCommentReaction
from files_sdk.models.message_reaction import MessageReaction
from files_sdk.models.notification import Notification
from files_sdk.models.payment import Payment
from files_sdk.models.payment_line_item import PaymentLineItem
from files_sdk.models.permission import Permission
from files_sdk.models.preview import Preview
from files_sdk.models.priority import Priority
from files_sdk.models.project import Project
from files_sdk.models.public_ip_address import PublicIpAddress
from files_sdk.models.public_key import PublicKey
from files_sdk.models.remote_bandwidth_snapshot import RemoteBandwidthSnapshot
from files_sdk.models.remote_server import RemoteServer
from files_sdk.models.remote_server_configuration_file import (
    RemoteServerConfigurationFile,
)
from files_sdk.models.request import Request
from files_sdk.models.session import Session
from files_sdk.models.settings_change import SettingsChange
from files_sdk.models.sftp_host_key import SftpHostKey
from files_sdk.models.share_group import ShareGroup
from files_sdk.models.share_group_member import ShareGroupMember
from files_sdk.models.site import Site
from files_sdk.models.snapshot import Snapshot
from files_sdk.models.sso_strategy import SsoStrategy
from files_sdk.models.status import Status
from files_sdk.models.style import Style
from files_sdk.models.usage_daily_snapshot import UsageDailySnapshot
from files_sdk.models.usage_snapshot import UsageSnapshot
from files_sdk.models.user import User
from files_sdk.models.user_cipher_use import UserCipherUse
from files_sdk.models.user_request import UserRequest
from files_sdk.models.webhook_test import WebhookTest

import files_sdk.path_util

the_api_key = ""
session_id = None
base_url = "https://app.files.com"
base_path = "api/rest/v1"
version = "1.2.101"

__version__ = version

initial_network_retry_delay = 0.5
max_network_retry_delay = 2
open_timeout = 30
read_timeout = 80
max_network_retries = 3

console_log_level = "none"

OPTS = ("api_key", "client", "session_id")


def set_api_key(_api_key):
    global the_api_key
    the_api_key = _api_key


def get_api_key():
    global the_api_key
    return the_api_key


def set_session(_session):
    if not _session.id:
        _session.save()
    global session_id
    session_id = _session.id


def open(*args, **kwargs):
    return file.open(*args, **kwargs)


def upload_file(*args, **kwargs):
    return file.upload_file(*args, **kwargs)


def download_file(*args, **kwargs):
    return file.download_file(*args, **kwargs)


def list_for(*args, **kwargs):
    return folder.list_for(*args, **kwargs)
