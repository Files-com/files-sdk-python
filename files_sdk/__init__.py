from pathlib import Path

# Each public name is imported as itself ("import X as X"), which is how
# type checkers know the package means to export it (see py.typed).
from files_sdk.models import account_line_item as account_line_item
from files_sdk.models import action as action
from files_sdk.models import action_log as action_log
from files_sdk.models import (
    action_notification_export as action_notification_export,
)
from files_sdk.models import (
    action_notification_export_result as action_notification_export_result,
)
from files_sdk.models import agent_node as agent_node
from files_sdk.models import agent_node_connection as agent_node_connection
from files_sdk.models import agent_node_instance as agent_node_instance
from files_sdk.models import agent_push_update as agent_push_update
from files_sdk.models import (
    ai_assistant_personality as ai_assistant_personality,
)
from files_sdk.models import ai_task as ai_task
from files_sdk.models import api_key as api_key
from files_sdk.models import api_request_log as api_request_log
from files_sdk.models import app as app
from files_sdk.models import as2_incoming_message as as2_incoming_message
from files_sdk.models import as2_outgoing_message as as2_outgoing_message
from files_sdk.models import as2_partner as as2_partner
from files_sdk.models import as2_station as as2_station
from files_sdk.models import auto as auto
from files_sdk.models import automation as automation
from files_sdk.models import (
    automation_authoring_schema as automation_authoring_schema,
)
from files_sdk.models import (
    automation_execution_node as automation_execution_node,
)
from files_sdk.models import automation_log as automation_log
from files_sdk.models import automation_run as automation_run
from files_sdk.models import bandwidth_snapshot as bandwidth_snapshot
from files_sdk.models import behavior as behavior
from files_sdk.models import bundle as bundle
from files_sdk.models import bundle_action as bundle_action
from files_sdk.models import bundle_download as bundle_download
from files_sdk.models import bundle_notification as bundle_notification
from files_sdk.models import bundle_path as bundle_path
from files_sdk.models import bundle_recipient as bundle_recipient
from files_sdk.models import bundle_registration as bundle_registration
from files_sdk.models import chat_message as chat_message
from files_sdk.models import chat_session as chat_session
from files_sdk.models import (
    child_site_management_policy as child_site_management_policy,
)
from files_sdk.models import clickwrap as clickwrap
from files_sdk.models import custom_domain as custom_domain
from files_sdk.models import (
    desktop_configuration_profile as desktop_configuration_profile,
)
from files_sdk.models import direct_connection_info as direct_connection_info
from files_sdk.models import dns_record as dns_record
from files_sdk.models import email_incoming_message as email_incoming_message
from files_sdk.models import email_log as email_log
from files_sdk.models import errors as errors
from files_sdk.models import event_channel as event_channel
from files_sdk.models import event_delivery_attempt as event_delivery_attempt
from files_sdk.models import event_record as event_record
from files_sdk.models import event_subscription as event_subscription
from files_sdk.models import event_target as event_target
from files_sdk.models import (
    exavault_api_request_log as exavault_api_request_log,
)
from files_sdk.models import expectation as expectation
from files_sdk.models import expectation_evaluation as expectation_evaluation
from files_sdk.models import expectation_incident as expectation_incident
from files_sdk.models import external_event as external_event
from files_sdk.models import file as file
from files_sdk.models import file_action as file_action
from files_sdk.models import file_comment as file_comment
from files_sdk.models import file_comment_reaction as file_comment_reaction
from files_sdk.models import file_migration as file_migration
from files_sdk.models import file_migration_log as file_migration_log
from files_sdk.models import file_upload_part as file_upload_part
from files_sdk.models import folder as folder
from files_sdk.models import form_field as form_field
from files_sdk.models import form_field_set as form_field_set
from files_sdk.models import ftp_action_log as ftp_action_log
from files_sdk.models import gpg_key as gpg_key
from files_sdk.models import group as group
from files_sdk.models import group_user as group_user
from files_sdk.models import history as history
from files_sdk.models import history_export as history_export
from files_sdk.models import history_export_result as history_export_result
from files_sdk.models import holiday_calendar as holiday_calendar
from files_sdk.models import holiday_region as holiday_region
from files_sdk.models import image as image
from files_sdk.models import inbound_s3_log as inbound_s3_log
from files_sdk.models import inbox_recipient as inbox_recipient
from files_sdk.models import inbox_registration as inbox_registration
from files_sdk.models import inbox_upload as inbox_upload
from files_sdk.models import (
    integration_centric_profile as integration_centric_profile,
)
from files_sdk.models import invoice as invoice
from files_sdk.models import invoice_line_item as invoice_line_item
from files_sdk.models import ip_address as ip_address
from files_sdk.models import key_lifecycle_rule as key_lifecycle_rule
from files_sdk.models import lock as lock
from files_sdk.models import metadata_category as metadata_category
from files_sdk.models import notification as notification
from files_sdk.models import outbound_connection_log as outbound_connection_log
from files_sdk.models import partner as partner
from files_sdk.models import partner_channel as partner_channel
from files_sdk.models import (
    partner_channel_template as partner_channel_template,
)
from files_sdk.models import partner_connection as partner_connection
from files_sdk.models import partner_site as partner_site
from files_sdk.models import partner_site_request as partner_site_request
from files_sdk.models import payment as payment
from files_sdk.models import payment_line_item as payment_line_item
from files_sdk.models import pending_work_event as pending_work_event
from files_sdk.models import permission as permission
from files_sdk.models import preview as preview
from files_sdk.models import (
    public_hosting_request_log as public_hosting_request_log,
)
from files_sdk.models import public_ip_address as public_ip_address
from files_sdk.models import public_key as public_key
from files_sdk.models import (
    remote_bandwidth_snapshot as remote_bandwidth_snapshot,
)
from files_sdk.models import remote_mount_backend as remote_mount_backend
from files_sdk.models import remote_server as remote_server
from files_sdk.models import (
    remote_server_configuration_file as remote_server_configuration_file,
)
from files_sdk.models import (
    remote_server_credential as remote_server_credential,
)
from files_sdk.models import request as request
from files_sdk.models import restore as restore
from files_sdk.models import schedule as schedule
from files_sdk.models import scheduled_export as scheduled_export
from files_sdk.models import scim_log as scim_log
from files_sdk.models import secret as secret
from files_sdk.models import session as session
from files_sdk.models import settings_change as settings_change
from files_sdk.models import sftp_action_log as sftp_action_log
from files_sdk.models import sftp_host_key as sftp_host_key
from files_sdk.models import share_group as share_group
from files_sdk.models import share_group_member as share_group_member
from files_sdk.models import siem_http_destination as siem_http_destination
from files_sdk.models import (
    siem_http_destination_event as siem_http_destination_event,
)
from files_sdk.models import site as site
from files_sdk.models import site_subdomain_redirect as site_subdomain_redirect
from files_sdk.models import snapshot as snapshot
from files_sdk.models import sso_event as sso_event
from files_sdk.models import sso_strategy as sso_strategy
from files_sdk.models import status as status
from files_sdk.models import style as style
from files_sdk.models import sync as sync
from files_sdk.models import sync_log as sync_log
from files_sdk.models import sync_run as sync_run
from files_sdk.models import sync_run_live_transfer as sync_run_live_transfer
from files_sdk.models import usage_by_top_level_dir as usage_by_top_level_dir
from files_sdk.models import usage_daily_snapshot as usage_daily_snapshot
from files_sdk.models import usage_snapshot as usage_snapshot
from files_sdk.models import user as user
from files_sdk.models import (
    user_additional_email_recipient as user_additional_email_recipient,
)
from files_sdk.models import user_cipher_use as user_cipher_use
from files_sdk.models import user_lifecycle_rule as user_lifecycle_rule
from files_sdk.models import user_request as user_request
from files_sdk.models import user_security_event as user_security_event
from files_sdk.models import user_sftp_client_use as user_sftp_client_use
from files_sdk.models import web_dav_action_log as web_dav_action_log
from files_sdk.models import webhook_test as webhook_test
from files_sdk.models import workspace as workspace
from files_sdk.models import zip_list_entry as zip_list_entry

from files_sdk.models.account_line_item import (
    AccountLineItem as AccountLineItem,
)
from files_sdk.models.action import Action as Action
from files_sdk.models.action_log import ActionLog as ActionLog
from files_sdk.models.action_notification_export import (
    ActionNotificationExport as ActionNotificationExport,
)
from files_sdk.models.action_notification_export_result import (
    ActionNotificationExportResult as ActionNotificationExportResult,
)
from files_sdk.models.agent_node import AgentNode as AgentNode
from files_sdk.models.agent_node_connection import (
    AgentNodeConnection as AgentNodeConnection,
)
from files_sdk.models.agent_node_instance import (
    AgentNodeInstance as AgentNodeInstance,
)
from files_sdk.models.agent_push_update import (
    AgentPushUpdate as AgentPushUpdate,
)
from files_sdk.models.ai_assistant_personality import (
    AiAssistantPersonality as AiAssistantPersonality,
)
from files_sdk.models.ai_task import AiTask as AiTask
from files_sdk.models.api_key import ApiKey as ApiKey
from files_sdk.models.api_request_log import ApiRequestLog as ApiRequestLog
from files_sdk.models.app import App as App
from files_sdk.models.as2_incoming_message import (
    As2IncomingMessage as As2IncomingMessage,
)
from files_sdk.models.as2_outgoing_message import (
    As2OutgoingMessage as As2OutgoingMessage,
)
from files_sdk.models.as2_partner import As2Partner as As2Partner
from files_sdk.models.as2_station import As2Station as As2Station
from files_sdk.models.auto import Auto as Auto
from files_sdk.models.automation import Automation as Automation
from files_sdk.models.automation_authoring_schema import (
    AutomationAuthoringSchema as AutomationAuthoringSchema,
)
from files_sdk.models.automation_execution_node import (
    AutomationExecutionNode as AutomationExecutionNode,
)
from files_sdk.models.automation_log import AutomationLog as AutomationLog
from files_sdk.models.automation_run import AutomationRun as AutomationRun
from files_sdk.models.bandwidth_snapshot import (
    BandwidthSnapshot as BandwidthSnapshot,
)
from files_sdk.models.behavior import Behavior as Behavior
from files_sdk.models.bundle import Bundle as Bundle
from files_sdk.models.bundle_action import BundleAction as BundleAction
from files_sdk.models.bundle_download import BundleDownload as BundleDownload
from files_sdk.models.bundle_notification import (
    BundleNotification as BundleNotification,
)
from files_sdk.models.bundle_path import BundlePath as BundlePath
from files_sdk.models.bundle_recipient import (
    BundleRecipient as BundleRecipient,
)
from files_sdk.models.bundle_registration import (
    BundleRegistration as BundleRegistration,
)
from files_sdk.models.chat_message import ChatMessage as ChatMessage
from files_sdk.models.chat_session import ChatSession as ChatSession
from files_sdk.models.child_site_management_policy import (
    ChildSiteManagementPolicy as ChildSiteManagementPolicy,
)
from files_sdk.models.clickwrap import Clickwrap as Clickwrap
from files_sdk.models.custom_domain import CustomDomain as CustomDomain
from files_sdk.models.desktop_configuration_profile import (
    DesktopConfigurationProfile as DesktopConfigurationProfile,
)
from files_sdk.models.direct_connection_info import (
    DirectConnectionInfo as DirectConnectionInfo,
)
from files_sdk.models.dns_record import DnsRecord as DnsRecord
from files_sdk.models.email_incoming_message import (
    EmailIncomingMessage as EmailIncomingMessage,
)
from files_sdk.models.email_log import EmailLog as EmailLog
from files_sdk.models.errors import Errors as Errors
from files_sdk.models.event_channel import EventChannel as EventChannel
from files_sdk.models.event_delivery_attempt import (
    EventDeliveryAttempt as EventDeliveryAttempt,
)
from files_sdk.models.event_record import EventRecord as EventRecord
from files_sdk.models.event_subscription import (
    EventSubscription as EventSubscription,
)
from files_sdk.models.event_target import EventTarget as EventTarget
from files_sdk.models.exavault_api_request_log import (
    ExavaultApiRequestLog as ExavaultApiRequestLog,
)
from files_sdk.models.expectation import Expectation as Expectation
from files_sdk.models.expectation_evaluation import (
    ExpectationEvaluation as ExpectationEvaluation,
)
from files_sdk.models.expectation_incident import (
    ExpectationIncident as ExpectationIncident,
)
from files_sdk.models.external_event import ExternalEvent as ExternalEvent
from files_sdk.models.file import File as File
from files_sdk.models.file_action import FileAction as FileAction
from files_sdk.models.file_comment import FileComment as FileComment
from files_sdk.models.file_comment_reaction import (
    FileCommentReaction as FileCommentReaction,
)
from files_sdk.models.file_migration import FileMigration as FileMigration
from files_sdk.models.file_migration_log import (
    FileMigrationLog as FileMigrationLog,
)
from files_sdk.models.file_upload_part import FileUploadPart as FileUploadPart
from files_sdk.models.folder import Folder as Folder
from files_sdk.models.form_field import FormField as FormField
from files_sdk.models.form_field_set import FormFieldSet as FormFieldSet
from files_sdk.models.ftp_action_log import FtpActionLog as FtpActionLog
from files_sdk.models.gpg_key import GpgKey as GpgKey
from files_sdk.models.group import Group as Group
from files_sdk.models.group_user import GroupUser as GroupUser
from files_sdk.models.history import History as History
from files_sdk.models.history_export import HistoryExport as HistoryExport
from files_sdk.models.history_export_result import (
    HistoryExportResult as HistoryExportResult,
)
from files_sdk.models.holiday_calendar import (
    HolidayCalendar as HolidayCalendar,
)
from files_sdk.models.holiday_region import HolidayRegion as HolidayRegion
from files_sdk.models.image import Image as Image
from files_sdk.models.inbound_s3_log import InboundS3Log as InboundS3Log
from files_sdk.models.inbox_recipient import InboxRecipient as InboxRecipient
from files_sdk.models.inbox_registration import (
    InboxRegistration as InboxRegistration,
)
from files_sdk.models.inbox_upload import InboxUpload as InboxUpload
from files_sdk.models.integration_centric_profile import (
    IntegrationCentricProfile as IntegrationCentricProfile,
)
from files_sdk.models.invoice import Invoice as Invoice
from files_sdk.models.invoice_line_item import (
    InvoiceLineItem as InvoiceLineItem,
)
from files_sdk.models.ip_address import IpAddress as IpAddress
from files_sdk.models.key_lifecycle_rule import (
    KeyLifecycleRule as KeyLifecycleRule,
)
from files_sdk.models.lock import Lock as Lock
from files_sdk.models.metadata_category import (
    MetadataCategory as MetadataCategory,
)
from files_sdk.models.notification import Notification as Notification
from files_sdk.models.outbound_connection_log import (
    OutboundConnectionLog as OutboundConnectionLog,
)
from files_sdk.models.partner import Partner as Partner
from files_sdk.models.partner_channel import PartnerChannel as PartnerChannel
from files_sdk.models.partner_channel_template import (
    PartnerChannelTemplate as PartnerChannelTemplate,
)
from files_sdk.models.partner_connection import (
    PartnerConnection as PartnerConnection,
)
from files_sdk.models.partner_site import PartnerSite as PartnerSite
from files_sdk.models.partner_site_request import (
    PartnerSiteRequest as PartnerSiteRequest,
)
from files_sdk.models.payment import Payment as Payment
from files_sdk.models.payment_line_item import (
    PaymentLineItem as PaymentLineItem,
)
from files_sdk.models.pending_work_event import (
    PendingWorkEvent as PendingWorkEvent,
)
from files_sdk.models.permission import Permission as Permission
from files_sdk.models.preview import Preview as Preview
from files_sdk.models.public_hosting_request_log import (
    PublicHostingRequestLog as PublicHostingRequestLog,
)
from files_sdk.models.public_ip_address import (
    PublicIpAddress as PublicIpAddress,
)
from files_sdk.models.public_key import PublicKey as PublicKey
from files_sdk.models.remote_bandwidth_snapshot import (
    RemoteBandwidthSnapshot as RemoteBandwidthSnapshot,
)
from files_sdk.models.remote_mount_backend import (
    RemoteMountBackend as RemoteMountBackend,
)
from files_sdk.models.remote_server import RemoteServer as RemoteServer
from files_sdk.models.remote_server_configuration_file import (
    RemoteServerConfigurationFile as RemoteServerConfigurationFile,
)
from files_sdk.models.remote_server_credential import (
    RemoteServerCredential as RemoteServerCredential,
)
from files_sdk.models.request import Request as Request
from files_sdk.models.restore import Restore as Restore
from files_sdk.models.schedule import Schedule as Schedule
from files_sdk.models.scheduled_export import (
    ScheduledExport as ScheduledExport,
)
from files_sdk.models.scim_log import ScimLog as ScimLog
from files_sdk.models.secret import Secret as Secret
from files_sdk.models.session import Session as Session
from files_sdk.models.settings_change import SettingsChange as SettingsChange
from files_sdk.models.sftp_action_log import SftpActionLog as SftpActionLog
from files_sdk.models.sftp_host_key import SftpHostKey as SftpHostKey
from files_sdk.models.share_group import ShareGroup as ShareGroup
from files_sdk.models.share_group_member import (
    ShareGroupMember as ShareGroupMember,
)
from files_sdk.models.siem_http_destination import (
    SiemHttpDestination as SiemHttpDestination,
)
from files_sdk.models.siem_http_destination_event import (
    SiemHttpDestinationEvent as SiemHttpDestinationEvent,
)
from files_sdk.models.site import Site as Site
from files_sdk.models.site_subdomain_redirect import (
    SiteSubdomainRedirect as SiteSubdomainRedirect,
)
from files_sdk.models.snapshot import Snapshot as Snapshot
from files_sdk.models.sso_event import SsoEvent as SsoEvent
from files_sdk.models.sso_strategy import SsoStrategy as SsoStrategy
from files_sdk.models.status import Status as Status
from files_sdk.models.style import Style as Style
from files_sdk.models.sync import Sync as Sync
from files_sdk.models.sync_log import SyncLog as SyncLog
from files_sdk.models.sync_run import SyncRun as SyncRun
from files_sdk.models.sync_run_live_transfer import (
    SyncRunLiveTransfer as SyncRunLiveTransfer,
)
from files_sdk.models.usage_by_top_level_dir import (
    UsageByTopLevelDir as UsageByTopLevelDir,
)
from files_sdk.models.usage_daily_snapshot import (
    UsageDailySnapshot as UsageDailySnapshot,
)
from files_sdk.models.usage_snapshot import UsageSnapshot as UsageSnapshot
from files_sdk.models.user import User as User
from files_sdk.models.user_additional_email_recipient import (
    UserAdditionalEmailRecipient as UserAdditionalEmailRecipient,
)
from files_sdk.models.user_cipher_use import UserCipherUse as UserCipherUse
from files_sdk.models.user_lifecycle_rule import (
    UserLifecycleRule as UserLifecycleRule,
)
from files_sdk.models.user_request import UserRequest as UserRequest
from files_sdk.models.user_security_event import (
    UserSecurityEvent as UserSecurityEvent,
)
from files_sdk.models.user_sftp_client_use import (
    UserSftpClientUse as UserSftpClientUse,
)
from files_sdk.models.web_dav_action_log import (
    WebDavActionLog as WebDavActionLog,
)
from files_sdk.models.webhook_test import WebhookTest as WebhookTest
from files_sdk.models.workspace import Workspace as Workspace
from files_sdk.models.zip_list_entry import ZipListEntry as ZipListEntry

from files_sdk.attachment import Attachment as Attachment
from files_sdk.client import Client as Client
from files_sdk.context import CLEAR as CLEAR, RequestOptions as RequestOptions
from files_sdk.lifetime import CancellationToken as CancellationToken
from files_sdk.region import RegionRelocation as RegionRelocation
from files_sdk.adaptive import (
    UploadObservation as UploadObservation,
    UploadStartup as UploadStartup,
    UploadTuning as UploadTuning,
)
from files_sdk.checkpoint import PauseToken as PauseToken
from files_sdk.download import DownloadProgress as DownloadProgress
from files_sdk.download_status import (
    DownloadRequestStatus as DownloadRequestStatus,
)
from files_sdk.jobs import (
    FileOutcome as FileOutcome,
    TransferJobProgress as TransferJobProgress,
    TransferResult as TransferResult,
)
from files_sdk.upload import (
    TransferLimiter as TransferLimiter,
    UploadProgress as UploadProgress,
)
import files_sdk.api
import files_sdk.path_util

# The module-level settings. They apply to the module-level functions,
# such as files_sdk.user.find(), and to the objects those return, as of when
# each operation starts. A files_sdk.Client never reads them.
the_api_key = ""
language = None
session_id = None
source_ip = None
workspace_id = None
base_url = "https://app.files.com"
base_path = "api/rest/v1"
version = "2.0.5"

__version__ = version

initial_network_retry_delay = 0.1
max_network_retry_delay = 2
open_timeout = 30
read_timeout = 80
max_network_retries = 3

console_log_level = "none"

OPTS = (
    "api_key",
    "client",
    "session_id",
    "source_ip",
    "language",
    "workspace_id",
)


def set_api_key(_api_key):
    global the_api_key
    the_api_key = _api_key


def get_api_key():
    return the_api_key


def set_language(_language):
    global language
    language = _language


def get_language():
    return language


def set_workspace_id(_workspace_id):
    global workspace_id
    workspace_id = _workspace_id


def get_workspace_id():
    return workspace_id


def set_session(_session):
    if not _session.id:
        _session.save()
    global session_id
    session_id = _session.id


def set_source_ip(_source_ip):
    global source_ip
    source_ip = _source_ip


def get_source_ip():
    return source_ip


def close():
    """Stop the module-level functions' operations in progress and close
    their connections. Objects they returned can no longer make requests;
    the next module-level call opens new connections with the settings of
    that time."""
    files_sdk.api.close_legacy_transport()


# The file helpers, as the file module defines them, so their signatures
# and types are the same here.
from files_sdk.models.file import (  # noqa: E402
    open as open,
    upload_file as upload_file,
    upload_stream as upload_stream,
    upload_to_remote_server as upload_to_remote_server,
    copy_to_remote_server as copy_to_remote_server,
    move_to_remote_server as move_to_remote_server,
    upload_to_snapshot as upload_to_snapshot,
    copy_to_snapshot as copy_to_snapshot,
    move_to_snapshot as move_to_snapshot,
    upload_to_child_site as upload_to_child_site,
    copy_to_child_site as copy_to_child_site,
    move_to_child_site as move_to_child_site,
    download_file as download_file,
    download_stream as download_stream,
    upload_directory as upload_directory,
    download_directory as download_directory,
    upload_files as upload_files,
    download_files as download_files,
)
from files_sdk.models.folder import list_for as list_for  # noqa: E402
