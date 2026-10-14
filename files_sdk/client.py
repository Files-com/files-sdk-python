"""files_sdk.Client: a Files.com client with its own configuration and
connections."""

import dataclasses
from typing import Any, Callable, Iterable, Literal, Mapping

import requests

from files_sdk.context import (
    DEFAULT_BASE_PATH,
    DEFAULT_BASE_URL,
    REGION_POLICIES,
    Context,
    check_delay,
    check_duration,
    check_retries,
    checked_base_url,
    principal,
)
from files_sdk.error import InvalidParameterError
from files_sdk.region import RegionRelocation, development_origins
from files_sdk.transport import Transport
from files_sdk.adaptive import UploadTuning
from files_sdk.upload import TransferLimiter
from files_sdk.models.action_log import ActionLogResource
from files_sdk.models.action_notification_export import (
    ActionNotificationExportResource,
)
from files_sdk.models.action_notification_export_result import (
    ActionNotificationExportResultResource,
)
from files_sdk.models.ai_assistant_personality import (
    AiAssistantPersonalityResource,
)
from files_sdk.models.ai_task import AiTaskResource
from files_sdk.models.api_key import ApiKeyResource
from files_sdk.models.api_request_log import ApiRequestLogResource
from files_sdk.models.app import AppResource
from files_sdk.models.as2_incoming_message import As2IncomingMessageResource
from files_sdk.models.as2_outgoing_message import As2OutgoingMessageResource
from files_sdk.models.as2_partner import As2PartnerResource
from files_sdk.models.as2_station import As2StationResource
from files_sdk.models.automation import AutomationResource
from files_sdk.models.automation_log import AutomationLogResource
from files_sdk.models.automation_run import AutomationRunResource
from files_sdk.models.bandwidth_snapshot import BandwidthSnapshotResource
from files_sdk.models.behavior import BehaviorResource
from files_sdk.models.bundle import BundleResource
from files_sdk.models.bundle_action import BundleActionResource
from files_sdk.models.bundle_download import BundleDownloadResource
from files_sdk.models.bundle_notification import BundleNotificationResource
from files_sdk.models.bundle_recipient import BundleRecipientResource
from files_sdk.models.bundle_registration import BundleRegistrationResource
from files_sdk.models.chat_session import ChatSessionResource
from files_sdk.models.child_site_management_policy import (
    ChildSiteManagementPolicyResource,
)
from files_sdk.models.clickwrap import ClickwrapResource
from files_sdk.models.custom_domain import CustomDomainResource
from files_sdk.models.desktop_configuration_profile import (
    DesktopConfigurationProfileResource,
)
from files_sdk.models.dns_record import DnsRecordResource
from files_sdk.models.email_incoming_message import (
    EmailIncomingMessageResource,
)
from files_sdk.models.email_log import EmailLogResource
from files_sdk.models.event_channel import EventChannelResource
from files_sdk.models.event_delivery_attempt import (
    EventDeliveryAttemptResource,
)
from files_sdk.models.event_record import EventRecordResource
from files_sdk.models.event_subscription import EventSubscriptionResource
from files_sdk.models.event_target import EventTargetResource
from files_sdk.models.exavault_api_request_log import (
    ExavaultApiRequestLogResource,
)
from files_sdk.models.expectation import ExpectationResource
from files_sdk.models.expectation_evaluation import (
    ExpectationEvaluationResource,
)
from files_sdk.models.expectation_incident import ExpectationIncidentResource
from files_sdk.models.external_event import ExternalEventResource
from files_sdk.models.file import FileResource
from files_sdk.models.file_comment import FileCommentResource
from files_sdk.models.file_comment_reaction import FileCommentReactionResource
from files_sdk.models.file_migration import FileMigrationResource
from files_sdk.models.file_migration_log import FileMigrationLogResource
from files_sdk.models.folder import FolderResource
from files_sdk.models.form_field_set import FormFieldSetResource
from files_sdk.models.ftp_action_log import FtpActionLogResource
from files_sdk.models.gpg_key import GpgKeyResource
from files_sdk.models.group import GroupResource
from files_sdk.models.group_user import GroupUserResource
from files_sdk.models.history import HistoryResource
from files_sdk.models.history_export import HistoryExportResource
from files_sdk.models.history_export_result import HistoryExportResultResource
from files_sdk.models.holiday_calendar import HolidayCalendarResource
from files_sdk.models.holiday_region import HolidayRegionResource
from files_sdk.models.inbound_s3_log import InboundS3LogResource
from files_sdk.models.inbox_recipient import InboxRecipientResource
from files_sdk.models.inbox_registration import InboxRegistrationResource
from files_sdk.models.inbox_upload import InboxUploadResource
from files_sdk.models.integration_centric_profile import (
    IntegrationCentricProfileResource,
)
from files_sdk.models.invoice import InvoiceResource
from files_sdk.models.ip_address import IpAddressResource
from files_sdk.models.key_lifecycle_rule import KeyLifecycleRuleResource
from files_sdk.models.lock import LockResource
from files_sdk.models.metadata_category import MetadataCategoryResource
from files_sdk.models.notification import NotificationResource
from files_sdk.models.outbound_connection_log import (
    OutboundConnectionLogResource,
)
from files_sdk.models.partner import PartnerResource
from files_sdk.models.partner_channel import PartnerChannelResource
from files_sdk.models.partner_channel_template import (
    PartnerChannelTemplateResource,
)
from files_sdk.models.partner_site import PartnerSiteResource
from files_sdk.models.partner_site_request import PartnerSiteRequestResource
from files_sdk.models.payment import PaymentResource
from files_sdk.models.pending_work_event import PendingWorkEventResource
from files_sdk.models.permission import PermissionResource
from files_sdk.models.public_hosting_request_log import (
    PublicHostingRequestLogResource,
)
from files_sdk.models.public_key import PublicKeyResource
from files_sdk.models.remote_bandwidth_snapshot import (
    RemoteBandwidthSnapshotResource,
)
from files_sdk.models.remote_mount_backend import RemoteMountBackendResource
from files_sdk.models.remote_server import RemoteServerResource
from files_sdk.models.remote_server_credential import (
    RemoteServerCredentialResource,
)
from files_sdk.models.request import RequestResource
from files_sdk.models.restore import RestoreResource
from files_sdk.models.schedule import ScheduleResource
from files_sdk.models.scheduled_export import ScheduledExportResource
from files_sdk.models.scim_log import ScimLogResource
from files_sdk.models.secret import SecretResource
from files_sdk.models.session import SessionResource
from files_sdk.models.settings_change import SettingsChangeResource
from files_sdk.models.sftp_action_log import SftpActionLogResource
from files_sdk.models.sftp_host_key import SftpHostKeyResource
from files_sdk.models.share_group import ShareGroupResource
from files_sdk.models.siem_http_destination import SiemHttpDestinationResource
from files_sdk.models.siem_http_destination_event import (
    SiemHttpDestinationEventResource,
)
from files_sdk.models.site import SiteResource
from files_sdk.models.site_subdomain_redirect import (
    SiteSubdomainRedirectResource,
)
from files_sdk.models.snapshot import SnapshotResource
from files_sdk.models.sso_event import SsoEventResource
from files_sdk.models.sso_strategy import SsoStrategyResource
from files_sdk.models.style import StyleResource
from files_sdk.models.sync import SyncResource
from files_sdk.models.sync_log import SyncLogResource
from files_sdk.models.sync_run import SyncRunResource
from files_sdk.models.usage_daily_snapshot import UsageDailySnapshotResource
from files_sdk.models.usage_snapshot import UsageSnapshotResource
from files_sdk.models.user import UserResource
from files_sdk.models.user_additional_email_recipient import (
    UserAdditionalEmailRecipientResource,
)
from files_sdk.models.user_cipher_use import UserCipherUseResource
from files_sdk.models.user_lifecycle_rule import UserLifecycleRuleResource
from files_sdk.models.user_request import UserRequestResource
from files_sdk.models.user_security_event import UserSecurityEventResource
from files_sdk.models.user_sftp_client_use import UserSftpClientUseResource
from files_sdk.models.web_dav_action_log import WebDavActionLogResource
from files_sdk.models.webhook_test import WebhookTestResource
from files_sdk.models.workspace import WorkspaceResource


def _checked_verify(verify: Any) -> bool | str:
    """verify, if it is True, False or a CA bundle path. Requests turns
    certificate verification off for any false value, such as "" or None,
    so only the documented values are accepted."""
    if (
        verify is True
        or verify is False
        or (isinstance(verify, str) and verify)
    ):
        return verify
    raise InvalidParameterError(
        "verify must be True, False or the path of a CA bundle or directory"
    )


class Client:
    """A Files.com client with its own configuration and connections.

    Use it as a context manager, or call close() when done::

        with files_sdk.Client(api_key="...") as client:
            user = client.user.find(123)
            for folder_item in client.folder.list_for("/").auto_paging_iter():
                ...

    Each resource, such as ``client.user``, has the operations of the
    module of the same name, and every object they return, and every page
    of a list, keeps using this client and its settings. A client never
    reads the module-level settings such as files_sdk.set_api_key(), and
    changing those later does not affect it.

    Configuration:

    - api_key, session_id or session (a logged-in files_sdk.Session): the
      principal. An API key is used if both are set, unless an operation's
      options say otherwise.
    - workspace_id, language, headers: sent with every API request.
      headers cannot set the Files.com credential or workspace headers.
    - base_url, base_path: where the API is.
    - open_timeout (30) and read_timeout (80): seconds to wait for a
      connection to each address a host name resolves to, and for each read
      of a response. request_timeout: a default limit, in seconds, on each
      whole operation; None for none.
    - max_network_retries (3): how many times a failed request is sent
      again: after a connection that failed before sending it; and, for a
      request that only asks for something (such as a GET) and for file
      transfers, also after a lost answer, a 429 or a 5xx answer other than
      501. A request that may have changed something, such as creating a
      user, is not sent again once it may have reached Files.com: it raises
      APIConnectionError, or the error answered, with remote_outcome_unknown
      set. 0 sends each
      request once. API retries wait initial_network_retry_delay (0.1 s),
      doubling each time up to max_network_retry_delay (2 s).
      max_redirects (30): redirects each request may follow.
    - source_ip: the local address to send from.
    - verify (True, False or a CA bundle path), cert, proxies, trust_env: as
      for requests.Session. By default
      the client verifies certificates and honors the standard proxy and
      CA bundle environment variables, but never sends credentials from a
      .netrc file.
    - http_session: a requests.Session of your own to send every request
      through, instead of one the client creates. The client uses it as
      Requests would, including its adapters and cookie jar, and never
      closes it, so configure proxies, TLS and source addresses on it
      rather than here. The SDK cannot interrupt a request blocked in a
      session it did not create; cancellation and deadlines then take
      effect when the request's own timeouts return. An adapter that
      retries on its own multiplies the SDK's retries and can repeat a
      request the SDK would not, so uploads refuse to start through one,
      since it could complete an upload twice.
    - region_policy ("automatic" or "disabled"), region_handler and
      region_development_origins: how an operation follows Files.com to
      the host a site requires. See the README's Regional Relocation
      section.
    - transfer_limiter: a files_sdk.TransferLimiter bounding the upload
      parts and download ranges this client has in progress, including
      those of directory and file-list transfers, and the bytes buffered
      for them. Give several clients the same one to bound them together;
      one you give is a hard budget the SDK never raises. By default each
      client has its own, of 1024 parts and 128 MiB.
    - upload_tuning: a files_sdk.UploadTuning for this client's uploads;
      by default they adapt as the Uploads page of the documentation
      describes.

    Closing the client stops its operations in progress and closes its
    connections. Objects it returned keep their data but cannot make
    requests afterwards. Closing never logs out a session.
    """

    def __init__(
        self,
        *,
        api_key: str | None = None,
        session_id: str | None = None,
        session: Any = None,
        workspace_id: int | str | None = None,
        language: str | None = None,
        source_ip: str | None = None,
        headers: Mapping[str, str] | None = None,
        base_url: str = DEFAULT_BASE_URL,
        base_path: str = DEFAULT_BASE_PATH,
        open_timeout: float = 30,
        read_timeout: float = 80,
        max_network_retries: int = 3,
        initial_network_retry_delay: float = 0.1,
        max_network_retry_delay: float = 2,
        request_timeout: float | None = None,
        max_redirects: int = 30,
        http_session: requests.Session | None = None,
        verify: bool | str = True,
        cert: str | tuple[str, str] | None = None,
        proxies: Mapping[str, str] | None = None,
        trust_env: bool = True,
        region_policy: Literal["automatic", "disabled"] = "automatic",
        region_handler: (
            Callable[[RegionRelocation], bool | str | None] | None
        ) = None,
        region_development_origins: Iterable[tuple[str, str]] = (),
        transfer_limiter: TransferLimiter | None = None,
        upload_tuning: UploadTuning | None = None,
    ):
        if http_session is not None:
            # The types forbid this, but callers without a type checker get
            # a clear error.
            if not isinstance(
                http_session, requests.Session
            ):  # pyright: ignore[reportUnnecessaryIsInstance]
                raise InvalidParameterError(
                    "http_session must be a requests.Session"
                )
            conflicts = [
                name
                for name, value, default in (
                    ("verify", verify, True),
                    ("cert", cert, None),
                    ("proxies", proxies, None),
                    ("trust_env", trust_env, True),
                )
                if value is not default
            ]
            if conflicts:
                raise InvalidParameterError(
                    "{} cannot be set with http_session. Configure them on "
                    "that session instead.".format(", ".join(conflicts))
                )
        if (
            isinstance(max_redirects, bool)
            or not isinstance(
                max_redirects, int
            )  # pyright: ignore[reportUnnecessaryIsInstance]
            or max_redirects < 0
        ):
            raise InvalidParameterError(
                "max_redirects must be an integer of 0 or more"
            )
        if region_policy not in REGION_POLICIES:
            raise InvalidParameterError(
                "region_policy must be 'automatic' or 'disabled', not {!r}".format(
                    region_policy
                )
            )
        if region_handler is not None and not callable(region_handler):
            raise InvalidParameterError("region_handler must be callable")
        if transfer_limiter is None:
            transfer_limiter = TransferLimiter._client_owned()
        elif not isinstance(
            transfer_limiter, TransferLimiter
        ):  # pyright: ignore[reportUnnecessaryIsInstance]
            raise InvalidParameterError(
                "transfer_limiter must be a files_sdk.TransferLimiter"
            )
        if upload_tuning is not None and not isinstance(
            upload_tuning, UploadTuning
        ):  # pyright: ignore[reportUnnecessaryIsInstance]
            raise InvalidParameterError(
                "upload_tuning must be a files_sdk.UploadTuning"
            )

        transport = Transport(
            http_session,
            verify=_checked_verify(verify),
            cert=cert,
            proxies=proxies,
            trust_env=trust_env,
        )
        context = Context(
            transport=transport,
            client=self,
            base_url=checked_base_url(base_url),
            base_path=base_path,
            open_timeout=check_duration("open_timeout", open_timeout),
            read_timeout=check_duration("read_timeout", read_timeout),
            max_network_retries=check_retries(max_network_retries),
            initial_network_retry_delay=check_delay(
                "initial_network_retry_delay", initial_network_retry_delay
            ),
            max_network_retry_delay=check_delay(
                "max_network_retry_delay", max_network_retry_delay
            ),
            request_timeout=(
                None
                if request_timeout is None
                else check_duration("request_timeout", request_timeout)
            ),
            max_redirects=max_redirects,
            region_policy=region_policy,
            region_handler=region_handler,
            region_development_origins=development_origins(
                region_development_origins
            ),
            transfer_limiter=transfer_limiter,
            upload_tuning=upload_tuning,
        )
        # Both credentials may be kept, so that an operation that clears
        # the key falls back to the session.
        key, session_id = principal(api_key, session_id, session)
        self._context = dataclasses.replace(
            context, api_key=key, session_id=session_id
        ).merged(
            {
                "workspace_id": workspace_id,
                "language": language,
                "source_ip": source_ip,
                "headers": headers,
            }
        )

    @property
    def closed(self) -> bool:
        return self._context.transport.closed

    def close(self) -> None:
        """Stop this client's operations and close its connections. A
        request blocked on the network stops at once, and close() returns
        once they have settled. Calling it again does nothing. A session
        passed as http_session stays open."""
        self._context.transport.close()

    def __enter__(self) -> "Client":
        return self

    def __exit__(self, *exc_info) -> None:
        self.close()

    def __repr__(self):
        state = " closed" if self.closed else ""
        return "<files_sdk.Client {}{}>".format(self._context.base_url, state)

    def _context_for(self, options) -> Context:
        return self._context._context_for(options)

    @property
    def action_log(self) -> ActionLogResource:
        """ActionLog operations that use this client."""
        return ActionLogResource(self)

    @property
    def action_notification_export(self) -> ActionNotificationExportResource:
        """ActionNotificationExport operations that use this client."""
        return ActionNotificationExportResource(self)

    @property
    def action_notification_export_result(
        self,
    ) -> ActionNotificationExportResultResource:
        """ActionNotificationExportResult operations that use this client."""
        return ActionNotificationExportResultResource(self)

    @property
    def ai_assistant_personality(self) -> AiAssistantPersonalityResource:
        """AiAssistantPersonality operations that use this client."""
        return AiAssistantPersonalityResource(self)

    @property
    def ai_task(self) -> AiTaskResource:
        """AiTask operations that use this client."""
        return AiTaskResource(self)

    @property
    def api_key(self) -> ApiKeyResource:
        """ApiKey operations that use this client."""
        return ApiKeyResource(self)

    @property
    def api_request_log(self) -> ApiRequestLogResource:
        """ApiRequestLog operations that use this client."""
        return ApiRequestLogResource(self)

    @property
    def app(self) -> AppResource:
        """App operations that use this client."""
        return AppResource(self)

    @property
    def as2_incoming_message(self) -> As2IncomingMessageResource:
        """As2IncomingMessage operations that use this client."""
        return As2IncomingMessageResource(self)

    @property
    def as2_outgoing_message(self) -> As2OutgoingMessageResource:
        """As2OutgoingMessage operations that use this client."""
        return As2OutgoingMessageResource(self)

    @property
    def as2_partner(self) -> As2PartnerResource:
        """As2Partner operations that use this client."""
        return As2PartnerResource(self)

    @property
    def as2_station(self) -> As2StationResource:
        """As2Station operations that use this client."""
        return As2StationResource(self)

    @property
    def automation(self) -> AutomationResource:
        """Automation operations that use this client."""
        return AutomationResource(self)

    @property
    def automation_log(self) -> AutomationLogResource:
        """AutomationLog operations that use this client."""
        return AutomationLogResource(self)

    @property
    def automation_run(self) -> AutomationRunResource:
        """AutomationRun operations that use this client."""
        return AutomationRunResource(self)

    @property
    def bandwidth_snapshot(self) -> BandwidthSnapshotResource:
        """BandwidthSnapshot operations that use this client."""
        return BandwidthSnapshotResource(self)

    @property
    def behavior(self) -> BehaviorResource:
        """Behavior operations that use this client."""
        return BehaviorResource(self)

    @property
    def bundle(self) -> BundleResource:
        """Bundle operations that use this client."""
        return BundleResource(self)

    @property
    def bundle_action(self) -> BundleActionResource:
        """BundleAction operations that use this client."""
        return BundleActionResource(self)

    @property
    def bundle_download(self) -> BundleDownloadResource:
        """BundleDownload operations that use this client."""
        return BundleDownloadResource(self)

    @property
    def bundle_notification(self) -> BundleNotificationResource:
        """BundleNotification operations that use this client."""
        return BundleNotificationResource(self)

    @property
    def bundle_recipient(self) -> BundleRecipientResource:
        """BundleRecipient operations that use this client."""
        return BundleRecipientResource(self)

    @property
    def bundle_registration(self) -> BundleRegistrationResource:
        """BundleRegistration operations that use this client."""
        return BundleRegistrationResource(self)

    @property
    def chat_session(self) -> ChatSessionResource:
        """ChatSession operations that use this client."""
        return ChatSessionResource(self)

    @property
    def child_site_management_policy(
        self,
    ) -> ChildSiteManagementPolicyResource:
        """ChildSiteManagementPolicy operations that use this client."""
        return ChildSiteManagementPolicyResource(self)

    @property
    def clickwrap(self) -> ClickwrapResource:
        """Clickwrap operations that use this client."""
        return ClickwrapResource(self)

    @property
    def custom_domain(self) -> CustomDomainResource:
        """CustomDomain operations that use this client."""
        return CustomDomainResource(self)

    @property
    def desktop_configuration_profile(
        self,
    ) -> DesktopConfigurationProfileResource:
        """DesktopConfigurationProfile operations that use this client."""
        return DesktopConfigurationProfileResource(self)

    @property
    def dns_record(self) -> DnsRecordResource:
        """DnsRecord operations that use this client."""
        return DnsRecordResource(self)

    @property
    def email_incoming_message(self) -> EmailIncomingMessageResource:
        """EmailIncomingMessage operations that use this client."""
        return EmailIncomingMessageResource(self)

    @property
    def email_log(self) -> EmailLogResource:
        """EmailLog operations that use this client."""
        return EmailLogResource(self)

    @property
    def event_channel(self) -> EventChannelResource:
        """EventChannel operations that use this client."""
        return EventChannelResource(self)

    @property
    def event_delivery_attempt(self) -> EventDeliveryAttemptResource:
        """EventDeliveryAttempt operations that use this client."""
        return EventDeliveryAttemptResource(self)

    @property
    def event_record(self) -> EventRecordResource:
        """EventRecord operations that use this client."""
        return EventRecordResource(self)

    @property
    def event_subscription(self) -> EventSubscriptionResource:
        """EventSubscription operations that use this client."""
        return EventSubscriptionResource(self)

    @property
    def event_target(self) -> EventTargetResource:
        """EventTarget operations that use this client."""
        return EventTargetResource(self)

    @property
    def exavault_api_request_log(self) -> ExavaultApiRequestLogResource:
        """ExavaultApiRequestLog operations that use this client."""
        return ExavaultApiRequestLogResource(self)

    @property
    def expectation(self) -> ExpectationResource:
        """Expectation operations that use this client."""
        return ExpectationResource(self)

    @property
    def expectation_evaluation(self) -> ExpectationEvaluationResource:
        """ExpectationEvaluation operations that use this client."""
        return ExpectationEvaluationResource(self)

    @property
    def expectation_incident(self) -> ExpectationIncidentResource:
        """ExpectationIncident operations that use this client."""
        return ExpectationIncidentResource(self)

    @property
    def external_event(self) -> ExternalEventResource:
        """ExternalEvent operations that use this client."""
        return ExternalEventResource(self)

    @property
    def file(self) -> FileResource:
        """File operations that use this client."""
        return FileResource(self)

    @property
    def file_comment(self) -> FileCommentResource:
        """FileComment operations that use this client."""
        return FileCommentResource(self)

    @property
    def file_comment_reaction(self) -> FileCommentReactionResource:
        """FileCommentReaction operations that use this client."""
        return FileCommentReactionResource(self)

    @property
    def file_migration(self) -> FileMigrationResource:
        """FileMigration operations that use this client."""
        return FileMigrationResource(self)

    @property
    def file_migration_log(self) -> FileMigrationLogResource:
        """FileMigrationLog operations that use this client."""
        return FileMigrationLogResource(self)

    @property
    def folder(self) -> FolderResource:
        """Folder operations that use this client."""
        return FolderResource(self)

    @property
    def form_field_set(self) -> FormFieldSetResource:
        """FormFieldSet operations that use this client."""
        return FormFieldSetResource(self)

    @property
    def ftp_action_log(self) -> FtpActionLogResource:
        """FtpActionLog operations that use this client."""
        return FtpActionLogResource(self)

    @property
    def gpg_key(self) -> GpgKeyResource:
        """GpgKey operations that use this client."""
        return GpgKeyResource(self)

    @property
    def group(self) -> GroupResource:
        """Group operations that use this client."""
        return GroupResource(self)

    @property
    def group_user(self) -> GroupUserResource:
        """GroupUser operations that use this client."""
        return GroupUserResource(self)

    @property
    def history(self) -> HistoryResource:
        """History operations that use this client."""
        return HistoryResource(self)

    @property
    def history_export(self) -> HistoryExportResource:
        """HistoryExport operations that use this client."""
        return HistoryExportResource(self)

    @property
    def history_export_result(self) -> HistoryExportResultResource:
        """HistoryExportResult operations that use this client."""
        return HistoryExportResultResource(self)

    @property
    def holiday_calendar(self) -> HolidayCalendarResource:
        """HolidayCalendar operations that use this client."""
        return HolidayCalendarResource(self)

    @property
    def holiday_region(self) -> HolidayRegionResource:
        """HolidayRegion operations that use this client."""
        return HolidayRegionResource(self)

    @property
    def inbound_s3_log(self) -> InboundS3LogResource:
        """InboundS3Log operations that use this client."""
        return InboundS3LogResource(self)

    @property
    def inbox_recipient(self) -> InboxRecipientResource:
        """InboxRecipient operations that use this client."""
        return InboxRecipientResource(self)

    @property
    def inbox_registration(self) -> InboxRegistrationResource:
        """InboxRegistration operations that use this client."""
        return InboxRegistrationResource(self)

    @property
    def inbox_upload(self) -> InboxUploadResource:
        """InboxUpload operations that use this client."""
        return InboxUploadResource(self)

    @property
    def integration_centric_profile(self) -> IntegrationCentricProfileResource:
        """IntegrationCentricProfile operations that use this client."""
        return IntegrationCentricProfileResource(self)

    @property
    def invoice(self) -> InvoiceResource:
        """Invoice operations that use this client."""
        return InvoiceResource(self)

    @property
    def ip_address(self) -> IpAddressResource:
        """IpAddress operations that use this client."""
        return IpAddressResource(self)

    @property
    def key_lifecycle_rule(self) -> KeyLifecycleRuleResource:
        """KeyLifecycleRule operations that use this client."""
        return KeyLifecycleRuleResource(self)

    @property
    def lock(self) -> LockResource:
        """Lock operations that use this client."""
        return LockResource(self)

    @property
    def metadata_category(self) -> MetadataCategoryResource:
        """MetadataCategory operations that use this client."""
        return MetadataCategoryResource(self)

    @property
    def notification(self) -> NotificationResource:
        """Notification operations that use this client."""
        return NotificationResource(self)

    @property
    def outbound_connection_log(self) -> OutboundConnectionLogResource:
        """OutboundConnectionLog operations that use this client."""
        return OutboundConnectionLogResource(self)

    @property
    def partner(self) -> PartnerResource:
        """Partner operations that use this client."""
        return PartnerResource(self)

    @property
    def partner_channel(self) -> PartnerChannelResource:
        """PartnerChannel operations that use this client."""
        return PartnerChannelResource(self)

    @property
    def partner_channel_template(self) -> PartnerChannelTemplateResource:
        """PartnerChannelTemplate operations that use this client."""
        return PartnerChannelTemplateResource(self)

    @property
    def partner_site(self) -> PartnerSiteResource:
        """PartnerSite operations that use this client."""
        return PartnerSiteResource(self)

    @property
    def partner_site_request(self) -> PartnerSiteRequestResource:
        """PartnerSiteRequest operations that use this client."""
        return PartnerSiteRequestResource(self)

    @property
    def payment(self) -> PaymentResource:
        """Payment operations that use this client."""
        return PaymentResource(self)

    @property
    def pending_work_event(self) -> PendingWorkEventResource:
        """PendingWorkEvent operations that use this client."""
        return PendingWorkEventResource(self)

    @property
    def permission(self) -> PermissionResource:
        """Permission operations that use this client."""
        return PermissionResource(self)

    @property
    def public_hosting_request_log(self) -> PublicHostingRequestLogResource:
        """PublicHostingRequestLog operations that use this client."""
        return PublicHostingRequestLogResource(self)

    @property
    def public_key(self) -> PublicKeyResource:
        """PublicKey operations that use this client."""
        return PublicKeyResource(self)

    @property
    def remote_bandwidth_snapshot(self) -> RemoteBandwidthSnapshotResource:
        """RemoteBandwidthSnapshot operations that use this client."""
        return RemoteBandwidthSnapshotResource(self)

    @property
    def remote_mount_backend(self) -> RemoteMountBackendResource:
        """RemoteMountBackend operations that use this client."""
        return RemoteMountBackendResource(self)

    @property
    def remote_server(self) -> RemoteServerResource:
        """RemoteServer operations that use this client."""
        return RemoteServerResource(self)

    @property
    def remote_server_credential(self) -> RemoteServerCredentialResource:
        """RemoteServerCredential operations that use this client."""
        return RemoteServerCredentialResource(self)

    @property
    def request(self) -> RequestResource:
        """Request operations that use this client."""
        return RequestResource(self)

    @property
    def restore(self) -> RestoreResource:
        """Restore operations that use this client."""
        return RestoreResource(self)

    @property
    def schedule(self) -> ScheduleResource:
        """Schedule operations that use this client."""
        return ScheduleResource(self)

    @property
    def scheduled_export(self) -> ScheduledExportResource:
        """ScheduledExport operations that use this client."""
        return ScheduledExportResource(self)

    @property
    def scim_log(self) -> ScimLogResource:
        """ScimLog operations that use this client."""
        return ScimLogResource(self)

    @property
    def secret(self) -> SecretResource:
        """Secret operations that use this client."""
        return SecretResource(self)

    @property
    def session(self) -> SessionResource:
        """Session operations that use this client."""
        return SessionResource(self)

    @property
    def settings_change(self) -> SettingsChangeResource:
        """SettingsChange operations that use this client."""
        return SettingsChangeResource(self)

    @property
    def sftp_action_log(self) -> SftpActionLogResource:
        """SftpActionLog operations that use this client."""
        return SftpActionLogResource(self)

    @property
    def sftp_host_key(self) -> SftpHostKeyResource:
        """SftpHostKey operations that use this client."""
        return SftpHostKeyResource(self)

    @property
    def share_group(self) -> ShareGroupResource:
        """ShareGroup operations that use this client."""
        return ShareGroupResource(self)

    @property
    def siem_http_destination(self) -> SiemHttpDestinationResource:
        """SiemHttpDestination operations that use this client."""
        return SiemHttpDestinationResource(self)

    @property
    def siem_http_destination_event(self) -> SiemHttpDestinationEventResource:
        """SiemHttpDestinationEvent operations that use this client."""
        return SiemHttpDestinationEventResource(self)

    @property
    def site(self) -> SiteResource:
        """Site operations that use this client."""
        return SiteResource(self)

    @property
    def site_subdomain_redirect(self) -> SiteSubdomainRedirectResource:
        """SiteSubdomainRedirect operations that use this client."""
        return SiteSubdomainRedirectResource(self)

    @property
    def snapshot(self) -> SnapshotResource:
        """Snapshot operations that use this client."""
        return SnapshotResource(self)

    @property
    def sso_event(self) -> SsoEventResource:
        """SsoEvent operations that use this client."""
        return SsoEventResource(self)

    @property
    def sso_strategy(self) -> SsoStrategyResource:
        """SsoStrategy operations that use this client."""
        return SsoStrategyResource(self)

    @property
    def style(self) -> StyleResource:
        """Style operations that use this client."""
        return StyleResource(self)

    @property
    def sync(self) -> SyncResource:
        """Sync operations that use this client."""
        return SyncResource(self)

    @property
    def sync_log(self) -> SyncLogResource:
        """SyncLog operations that use this client."""
        return SyncLogResource(self)

    @property
    def sync_run(self) -> SyncRunResource:
        """SyncRun operations that use this client."""
        return SyncRunResource(self)

    @property
    def usage_daily_snapshot(self) -> UsageDailySnapshotResource:
        """UsageDailySnapshot operations that use this client."""
        return UsageDailySnapshotResource(self)

    @property
    def usage_snapshot(self) -> UsageSnapshotResource:
        """UsageSnapshot operations that use this client."""
        return UsageSnapshotResource(self)

    @property
    def user(self) -> UserResource:
        """User operations that use this client."""
        return UserResource(self)

    @property
    def user_additional_email_recipient(
        self,
    ) -> UserAdditionalEmailRecipientResource:
        """UserAdditionalEmailRecipient operations that use this client."""
        return UserAdditionalEmailRecipientResource(self)

    @property
    def user_cipher_use(self) -> UserCipherUseResource:
        """UserCipherUse operations that use this client."""
        return UserCipherUseResource(self)

    @property
    def user_lifecycle_rule(self) -> UserLifecycleRuleResource:
        """UserLifecycleRule operations that use this client."""
        return UserLifecycleRuleResource(self)

    @property
    def user_request(self) -> UserRequestResource:
        """UserRequest operations that use this client."""
        return UserRequestResource(self)

    @property
    def user_security_event(self) -> UserSecurityEventResource:
        """UserSecurityEvent operations that use this client."""
        return UserSecurityEventResource(self)

    @property
    def user_sftp_client_use(self) -> UserSftpClientUseResource:
        """UserSftpClientUse operations that use this client."""
        return UserSftpClientUseResource(self)

    @property
    def web_dav_action_log(self) -> WebDavActionLogResource:
        """WebDavActionLog operations that use this client."""
        return WebDavActionLogResource(self)

    @property
    def webhook_test(self) -> WebhookTestResource:
        """WebhookTest operations that use this client."""
        return WebhookTestResource(self)

    @property
    def workspace(self) -> WorkspaceResource:
        """Workspace operations that use this client."""
        return WorkspaceResource(self)
