"""How many parts an upload sends at once, and how large it makes them
when Files.com lets it choose.

An adaptive upload sends more parts at once while measurements show that
helps, fewer after failures, and fewer and waits after the storage service
pushes back with 429, 503 or 504. How it does so depends on where the parts
go: begin_upload's upload_target_class names the kind of storage (s3,
agent_fiw or generic), which tunes the controller and never grants anything
by itself. When it names none of these, an upload whose first answer shows
every part going to one ordinary multipart upload straight to Amazon S3 is
s3, as in the .NET SDK, unless the answer has direct connection information
or the caller kept the SDK from asking for it (see files_sdk.upload).

For Amazon S3, when the caller sets none of UploadTuning's concurrency
settings, the SDK uses the scaled S3 policy of the shared adaptive upload
reference: windows of accepted parts measured by wall time, judged only
when parts kept the target busy, epochs so that one burst of failures
shrinks the target once, and growth up to 150 parts at once, or 1024 once a
fast link has carried enough. UploadStartup chooses how it starts: Default
warms up from one part, probing upwards only as measurements justify, and
Aggressive starts at the policy's start. max_concurrency caps either.
Concurrency settings of the caller's own, adaptive=False and the generic
and agent profiles use the SDK's configurable controller, starting where
its settings say.

Every attempt to send a part holds a permit from the controller for that
attempt alone: a part waiting to be sent again gives its permit back and
waits for a new one, behind any cooldown, like a new part.

Downloads bound to one version of a file admit their ranges through the
same controller, with no startup choice: see files_sdk.download.

UploadTuning names every setting. The defaults of the configurable
controller are conservative choices for Python's threaded I/O, not measured
optimums.

UploadTuning.observer, when set, is called on the uploading thread with an
UploadObservation for each thing worth comparing between runs: how the
upload was planned (and any fallback from the plan it would prefer), each
decision the controller made (growing, shrinking, backpressure and its
cooldown, throughput probes kept or missed, warm-up raises, windows not
measured and why, part-size probes), each wait for room in the
TransferLimiter or for the storage service's cooldown, a sample at most
four times a second of the parts in progress, the read-ahead runway and the
process's memory and CPU time, and at the end a record of the whole upload
for comparing runs. Observations hold numbers and names only: never a path,
URL, header or credential. Without an observer, none of this is collected.
"""

import collections
import dataclasses
import enum
import math
import statistics
import sys
import threading
import time
from typing import Any, Callable

from files_sdk.error import InvalidParameterError

MiB = 1024 * 1024
GiB = 1024 * MiB
TiB = 1024 * GiB

_GENERIC_TIERS = ((8 * GiB, 16 * MiB), (128 * GiB, 32 * MiB), (None, 64 * MiB))
_S3_TIERS = (
    (1 * GiB, 16 * MiB),
    (16 * GiB, 32 * MiB),
    (512 * GiB, 64 * MiB),
    (1 * TiB, 128 * MiB),
    (2 * TiB, 256 * MiB),
    (None, 512 * MiB),
)
# The scaled S3 policy's sizes: 8 MiB through 256 MiB, 16 MiB through 4 GiB,
# 32 MiB through 64 GiB, 64 MiB above.
_SCALED_S3_TIERS = (
    (256 * MiB + 1, 8 * MiB),
    (4 * GiB + 1, 16 * MiB),
    (64 * GiB + 1, 32 * MiB),
    (None, 64 * MiB),
)

LEGACY = "configurable"
"""The policy of the SDK's configurable controller."""

SCALED_S3 = "scaled_s3"
"""The policy the SDK chooses for an automatic upload to Amazon S3."""

SCALED_S3_MAX_CONCURRENCY = 1024
"""The most part attempts the scaled S3 policy has in progress at once."""


class UploadStartup(enum.Enum):
    """How an automatic upload to Amazon S3 starts, when the SDK chooses the
    scaled S3 policy for it.

    DEFAULT starts with one part and adds parts only as measured probes
    justify, by about half at each level that earns it and by one after
    resting; a measured fast link (96 MiB/s) promotes it at once to the
    policy's start. AGGRESSIVE starts at the policy's start, normally 150
    parts, for a caller who knows the link is fast. Either way the upload
    then adapts with the same growth, limits, backoff and retries, so
    Default can reach the same concurrency, only later. Neither raises
    max_concurrency, a TransferLimiter's bounds or a serial-part instruction
    from Files.com, and neither applies to other kinds of storage or to
    tuning with concurrency settings of its own, which starts where those
    settings say.
    """

    DEFAULT = "default"
    AGGRESSIVE = "aggressive"


@dataclasses.dataclass(frozen=True)
class UploadTuning:
    """Settings for how uploads adapt. Leave a field None to use the
    default for the kind of storage an upload goes to; set adaptive=False
    to send max_concurrency parts (4 when it is not given) at once
    throughout. A download takes one too, without the settings only uploads
    use, such as startup and observer (see files_sdk.download).

    Startup: for an upload to Amazon S3 that sets none of the concurrency
    fields below, the SDK chooses its scaled S3 policy, and startup (an
    UploadStartup, DEFAULT when None) chooses how it starts. max_concurrency
    caps that policy too. startup cannot be combined with adaptive=False or
    with any concurrency field, which choose the configurable controller.

    Concurrency (the configurable controller): initial_concurrency parts
    start at once, never fewer than min_concurrency. Every grow_every
    successful parts add grow_step, up to soft_ceiling until at least
    unlock_bytes have been sent at a best throughput of
    unlock_bytes_per_second or more (0 means no soft ceiling), then up to the
    upload's max_concurrency.

    Throughput: every throughput_window parts give a throughput sample.
    Growth is kept only if the next samples improve on the best by
    probe_min_gain_percent, or, above probe_plateau parts at once, by
    probe_gain_per_part_percent for each part added; a sample within
    probe_loss_tolerance_percent of the best also counts. After probe_windows
    samples without that gain, concurrency drops by throughput_shrink_percent
    and holds for hold_windows samples. throughput_window=0 turns probing off.

    Latency: when the time parts take suggests more than latency_queue_high
    parts are waiting in the network, throughput has dropped, and not
    probing, concurrency drops by latency_shrink_percent; growth waits while
    more than latency_growth_queue_high are waiting. 0 turns each off.

    Failures: a failed part drops concurrency by failure_shrink_percent. A
    429, 503 or 504 drops it by backpressure_shrink_percent and stops new
    parts, and parts to send again, for the Retry-After time, or
    backpressure_pause seconds without one. Failures of attempts that began
    before the last drop do not drop it again.

    Streams: up to ready_parts parts, holding at most ready_bytes, are read
    ahead while all parts in progress are busy.

    Part sizes, used only when Files.com allows the upload to choose them:
    part_size_tiers maps an upload's size to a preferred part size, as
    (below this many bytes, part size) pairs with None for the rest. Smaller
    uploads use smaller parts, down to min_part_size, so that there are at
    least workload_parts_per_worker parts for each part sent at once. An
    upload of unknown size starts with unknown_initial_part_size parts and
    doubles them every unknown_grow_every parts up to unknown_max_part_size.
    Under the scaled S3 policy, unless these are given, sizes follow that
    policy's tiers for a workload of at least 16 parts, and each file doubles
    its unread parts' size when its own measured parts show that helps.

    Observation: observer, if given, is called with an UploadObservation as
    described in the module docstring. It runs on the uploading thread, so
    it should return quickly; an exception it raises stops the upload.
    """

    adaptive: bool = True
    initial_concurrency: int | None = None
    min_concurrency: int | None = None
    grow_every: int | None = None
    grow_step: int | None = None
    soft_ceiling: int | None = None
    unlock_bytes: int | None = None
    unlock_bytes_per_second: float | None = None
    throughput_window: int | None = None
    probe_min_gain_percent: float | None = None
    probe_windows: int | None = None
    probe_plateau: int | None = None
    probe_gain_per_part_percent: float | None = None
    probe_loss_tolerance_percent: float | None = None
    throughput_shrink_percent: float | None = None
    hold_windows: int | None = None
    latency_queue_high: float | None = None
    latency_growth_queue_high: float | None = None
    latency_shrink_percent: float | None = None
    failure_shrink_percent: float | None = None
    backpressure_shrink_percent: float | None = None
    backpressure_pause: float | None = None
    ready_parts: int | None = None
    ready_bytes: int | None = None
    part_size_tiers: tuple[tuple[int | None, int], ...] | None = None
    workload_parts_per_worker: int | None = None
    min_part_size: int | None = None
    unknown_initial_part_size: int | None = None
    unknown_max_part_size: int | None = None
    unknown_grow_every: int | None = None
    observer: "Callable[[UploadObservation], None] | None" = dataclasses.field(
        default=None, compare=False
    )
    # After observer, so that the fields before it keep their positions.
    startup: "UploadStartup | None" = None

    def __post_init__(self):
        adaptive: Any = self.adaptive
        if not isinstance(adaptive, bool):
            raise InvalidParameterError("adaptive must be True or False")
        if self.observer is not None and not callable(self.observer):
            raise InvalidParameterError(
                "UploadTuning.observer must be callable"
            )
        for field in dataclasses.fields(self):
            value = getattr(self, field.name)
            if field.name in _UNRULED or value is None:
                continue
            rule = _RULES[field.name]
            if (
                isinstance(value, bool)
                or not isinstance(value, rule.kinds)
                or not rule.valid(value)
            ):
                raise InvalidParameterError(
                    "UploadTuning.{} must be {}".format(
                        field.name, rule.description
                    )
                )
        if self.part_size_tiers is not None:
            _check_tiers(self.part_size_tiers)
        startup: Any = self.startup
        if startup is not None:
            if not isinstance(startup, UploadStartup):
                raise InvalidParameterError(
                    "UploadTuning.startup must be files_sdk.UploadStartup.DEFAULT or files_sdk.UploadStartup.AGGRESSIVE"
                )
            if not self.adaptive:
                raise InvalidParameterError(
                    "UploadTuning.startup chooses how an adaptive upload starts, so it cannot be combined with adaptive=False"
                )
            chosen = [
                name
                for name in _CONCURRENCY_FIELDS
                if getattr(self, name) is not None
            ]
            if chosen:
                raise InvalidParameterError(
                    "UploadTuning.startup cannot be combined with {}, which choose the configurable "
                    "controller and where it starts".format(", ".join(chosen))
                )

    def policy(self, target_class) -> str:
        """The policy an upload to target_class uses: the scaled S3 policy
        for an adaptive upload to S3 whose concurrency the caller left to
        the SDK, otherwise the configurable controller."""
        if (
            target_class == "s3"
            and self.adaptive
            and all(
                getattr(self, name) is None for name in _CONCURRENCY_FIELDS
            )
        ):
            return SCALED_S3
        return LEGACY

    def settings(self, target_class, max_concurrency) -> "_Settings":
        """The settings an upload to target_class uses, with at most
        max_concurrency parts at once. Raises for a combination that cannot
        work, before anything is sent."""
        policy = self.policy(target_class)
        profile = (
            _scaled_s3_profile(max_concurrency)
            if policy == SCALED_S3
            else _profile(target_class)
        )
        values = {
            field.name: (
                getattr(self, field.name)
                if getattr(self, field.name) is not None
                else profile[field.name]
            )
            for field in dataclasses.fields(self)
            if field.name not in _UNRULED
        }
        values["part_size_tiers"] = (
            self.part_size_tiers
            if self.part_size_tiers is not None
            else profile["part_size_tiers"]
        )
        extra: dict[str, Any] = {}
        if policy == SCALED_S3:
            extra = {
                "policy": SCALED_S3,
                "startup": (self.startup or UploadStartup.DEFAULT).value,
                "fast_link_bytes_per_second": _SCALED_FAST_LINK,
                "probe_floor": min(_SCALED_PROBE_FLOOR, max_concurrency),
                "backoff_floor": min(_SCALED_BACKOFF_FLOOR, max_concurrency),
                "explicit_sizes": any(
                    getattr(self, name) is not None for name in _SIZE_FIELDS
                ),
            }
        settings = _Settings(
            adaptive=self.adaptive,
            max_concurrency=max_concurrency,
            target_class=target_class,
            **values,
            **extra,
        )
        settings.check()
        return settings


@dataclasses.dataclass(frozen=True)
class _Rule:
    kinds: tuple[type, ...]
    valid: Any
    description: str


def _count(minimum):
    return _Rule(
        (int,),
        lambda v: v >= minimum,
        "an integer of {} or more".format(minimum),
    )


_PERCENT = _Rule(
    (int, float),
    lambda v: math.isfinite(v) and 0 <= v <= 100,
    "a percentage from 0 to 100",
)
_NONNEGATIVE = _Rule(
    (int, float),
    lambda v: math.isfinite(v) and v >= 0,
    "a number of 0 or more",
)
_RULES = {
    "initial_concurrency": _count(1),
    "min_concurrency": _count(1),
    "grow_every": _count(1),
    "grow_step": _count(1),
    "soft_ceiling": _count(0),
    "unlock_bytes": _count(0),
    "unlock_bytes_per_second": _NONNEGATIVE,
    "throughput_window": _count(0),
    "probe_min_gain_percent": _PERCENT,
    "probe_windows": _count(1),
    "probe_plateau": _count(0),
    "probe_gain_per_part_percent": _PERCENT,
    "probe_loss_tolerance_percent": _PERCENT,
    "throughput_shrink_percent": _PERCENT,
    "hold_windows": _count(0),
    "latency_queue_high": _NONNEGATIVE,
    "latency_growth_queue_high": _NONNEGATIVE,
    "latency_shrink_percent": _PERCENT,
    "failure_shrink_percent": _PERCENT,
    "backpressure_shrink_percent": _PERCENT,
    "backpressure_pause": _NONNEGATIVE,
    "ready_parts": _count(0),
    "ready_bytes": _count(0),
    "workload_parts_per_worker": _count(1),
    "min_part_size": _count(1),
    "unknown_initial_part_size": _count(1),
    "unknown_max_part_size": _count(1),
    "unknown_grow_every": _count(1),
}
# Fields checked on their own, and not settings of a profile.
_UNRULED = ("adaptive", "part_size_tiers", "startup", "observer")
# Setting any of these chooses the configurable controller and its start.
_CONCURRENCY_FIELDS = (
    "initial_concurrency",
    "min_concurrency",
    "grow_every",
    "grow_step",
    "soft_ceiling",
    "unlock_bytes",
    "unlock_bytes_per_second",
    "throughput_window",
    "probe_min_gain_percent",
    "probe_windows",
    "probe_plateau",
    "probe_gain_per_part_percent",
    "probe_loss_tolerance_percent",
    "throughput_shrink_percent",
    "hold_windows",
    "latency_queue_high",
    "latency_growth_queue_high",
    "latency_shrink_percent",
    "failure_shrink_percent",
    "backpressure_shrink_percent",
    "backpressure_pause",
)
# Setting any of these fixes how part sizes are chosen.
_SIZE_FIELDS = (
    "part_size_tiers",
    "workload_parts_per_worker",
    "min_part_size",
)


def _check_tiers(tiers):
    message = (
        "UploadTuning.part_size_tiers must be (below bytes, part size) pairs "
        "with increasing sizes, positive part sizes, and None last"
    )
    if not isinstance(tiers, tuple) or not tiers:
        raise InvalidParameterError(message)
    previous = 0
    for index, tier in enumerate(tiers):
        if not isinstance(tier, tuple) or len(tier) != 2:
            raise InvalidParameterError(message)
        below, size = tier
        last = index == len(tiers) - 1
        if isinstance(size, bool) or not isinstance(size, int) or size < 1:
            raise InvalidParameterError(message)
        if last != (below is None):
            raise InvalidParameterError(message)
        if below is not None:
            if (
                isinstance(below, bool)
                or not isinstance(below, int)
                or below <= previous
            ):
                raise InvalidParameterError(message)
            previous = below


# Defaults of the configurable controller by the kind of storage parts go
# to. Provisional: chosen to be safe for Python threads, and not yet
# measured against real targets. A kind of storage is added or re-tuned
# here alone. max_concurrency is the most parts an adaptive upload sends at
# once when the caller does not give max_concurrency; the others are
# UploadTuning's fields. An automatic upload to S3 uses _SCALED_S3 instead.
_BASE = {
    "max_concurrency": 16,
    "initial_concurrency": 4,
    "min_concurrency": 1,
    "grow_every": 4,
    "grow_step": 1,
    "soft_ceiling": 0,
    "unlock_bytes": 0,
    "unlock_bytes_per_second": 0.0,
    "throughput_window": 8,
    "probe_min_gain_percent": 5.0,
    "probe_windows": 2,
    "probe_plateau": 0,
    "probe_gain_per_part_percent": 0.0,
    "probe_loss_tolerance_percent": 0.0,
    "throughput_shrink_percent": 25.0,
    "hold_windows": 1,
    "latency_queue_high": 0.0,
    "latency_growth_queue_high": 0.0,
    "latency_shrink_percent": 0.0,
    "failure_shrink_percent": 50.0,
    "backpressure_shrink_percent": 50.0,
    "backpressure_pause": 1.0,
    "ready_parts": 2,
    "ready_bytes": 64 * MiB,
    "part_size_tiers": _GENERIC_TIERS,
    "workload_parts_per_worker": 2,
    "min_part_size": 8 * MiB,
    "unknown_initial_part_size": 8 * MiB,
    "unknown_max_part_size": 32 * MiB,
    "unknown_grow_every": 128,
}
_PROFILES = {
    "generic": {**_BASE},
    "agent_fiw": {
        **_BASE,
        "max_concurrency": 8,
        "initial_concurrency": 2,
        "grow_every": 8,
        "soft_ceiling": 4,
        "unlock_bytes": 1 * GiB,
        "unlock_bytes_per_second": 32.0 * MiB,
        "probe_min_gain_percent": 10.0,
        "hold_windows": 2,
    },
    "s3": {
        **_BASE,
        "max_concurrency": 32,
        "initial_concurrency": 8,
        "min_concurrency": 2,
        "grow_every": 8,
        "grow_step": 2,
        "soft_ceiling": 16,
        "unlock_bytes": 4 * GiB,
        "unlock_bytes_per_second": 64.0 * MiB,
        "throughput_window": 16,
        "probe_min_gain_percent": 3.0,
        "probe_plateau": 24,
        "probe_gain_per_part_percent": 0.5,
        "probe_loss_tolerance_percent": 2.0,
        "throughput_shrink_percent": 10.0,
        "latency_queue_high": 24.0,
        "latency_growth_queue_high": 16.0,
        "latency_shrink_percent": 10.0,
        "failure_shrink_percent": 35.0,
        "backpressure_shrink_percent": 20.0,
        "backpressure_pause": 0.0,
        "ready_parts": 4,
        "ready_bytes": 128 * MiB,
        "part_size_tiers": _S3_TIERS,
        "workload_parts_per_worker": 4,
    },
}
TARGET_CLASSES = tuple(_PROFILES)

# The scaled S3 policy of the shared adaptive upload reference, in the
# fields it shares with the configurable controller, whose meaning differs:
# throughput_window is the accepted attempts a window needs, grow_every the
# judged windows between raises, throughput_shrink_percent and
# latency_shrink_percent the withdrawal of a rejected probe and the latency
# backoff, and workload_parts_per_worker the parts a whole upload prefers.
_SCALED_S3 = {
    "max_concurrency": SCALED_S3_MAX_CONCURRENCY,
    "initial_concurrency": 150,
    "min_concurrency": 8,
    "grow_every": 1,
    "grow_step": 4,
    "soft_ceiling": 150,
    "unlock_bytes": 64 * GiB,
    "unlock_bytes_per_second": 96.0 * MiB,
    "throughput_window": 32,
    "probe_min_gain_percent": 1.0,
    "probe_windows": 2,
    "probe_plateau": 200,
    "probe_gain_per_part_percent": 0.15,
    "probe_loss_tolerance_percent": 2.0,
    "throughput_shrink_percent": 8.0,
    "hold_windows": 1,
    "latency_queue_high": 160.0,
    "latency_growth_queue_high": 96.0,
    "latency_shrink_percent": 8.0,
    "failure_shrink_percent": 35.0,
    "backpressure_shrink_percent": 10.0,
    "backpressure_pause": 0.0,
    "ready_parts": 4,
    "ready_bytes": 128 * MiB,
    "part_size_tiers": _SCALED_S3_TIERS,
    "workload_parts_per_worker": 16,
    "min_part_size": 1 * MiB,
    "unknown_initial_part_size": 8 * MiB,
    "unknown_max_part_size": 32 * MiB,
    "unknown_grow_every": 128,
}
# A window this fast establishes a fast link; after one, probes up to the
# probe floor need no gain and backoff stops at it.
_SCALED_FAST_LINK = 96.0 * MiB
_SCALED_PROBE_FLOOR = 150
# Latency backoff and a rejected probe stop here (below a fast link).
_SCALED_BACKOFF_FLOOR = 50


def _profile(target_class):
    return _PROFILES.get(target_class, _PROFILES["generic"])


def _scaled_s3_profile(max_concurrency):
    """The scaled S3 policy with max_concurrency clamping its start, minimum
    and soft ceiling."""
    return {
        **_SCALED_S3,
        "initial_concurrency": min(
            _SCALED_S3["initial_concurrency"], max_concurrency
        ),
        "min_concurrency": min(_SCALED_S3["min_concurrency"], max_concurrency),
        "soft_ceiling": min(_SCALED_S3["soft_ceiling"], max_concurrency),
    }


def default_max_concurrency(target_class, tuning=None) -> int:
    """The most parts an adaptive upload to target_class sends at once when
    the caller does not give max_concurrency."""
    if tuning is not None and tuning.policy(target_class) == SCALED_S3:
        return SCALED_S3_MAX_CONCURRENCY
    return _profile(target_class)["max_concurrency"]


@dataclasses.dataclass(frozen=True)
class _Settings:
    """UploadTuning with every field resolved, for one upload."""

    adaptive: bool
    max_concurrency: int
    target_class: str
    initial_concurrency: int
    min_concurrency: int
    grow_every: int
    grow_step: int
    soft_ceiling: int
    unlock_bytes: int
    unlock_bytes_per_second: float
    throughput_window: int
    probe_min_gain_percent: float
    probe_windows: int
    probe_plateau: int
    probe_gain_per_part_percent: float
    probe_loss_tolerance_percent: float
    throughput_shrink_percent: float
    hold_windows: int
    latency_queue_high: float
    latency_growth_queue_high: float
    latency_shrink_percent: float
    failure_shrink_percent: float
    backpressure_shrink_percent: float
    backpressure_pause: float
    ready_parts: int
    ready_bytes: int
    part_size_tiers: tuple[tuple[int | None, int], ...]
    workload_parts_per_worker: int
    min_part_size: int
    unknown_initial_part_size: int
    unknown_max_part_size: int
    unknown_grow_every: int
    policy: str = LEGACY
    # For the scaled S3 policy: "default" or "aggressive".
    startup: str | None = None
    fast_link_bytes_per_second: float = 0.0
    probe_floor: int = 0
    backoff_floor: int = 0
    # Whether the caller fixed how part sizes are chosen.
    explicit_sizes: bool = False

    def check(self):
        problems = []
        if self.adaptive and self.min_concurrency > self.max_concurrency:
            problems.append("min_concurrency is more than max_concurrency")
        if self.soft_ceiling and self.soft_ceiling < self.min_concurrency:
            problems.append("soft_ceiling is less than min_concurrency")
        if self.unknown_initial_part_size > self.unknown_max_part_size:
            problems.append(
                "unknown_initial_part_size is more than unknown_max_part_size"
            )
        if problems:
            raise InvalidParameterError(
                "UploadTuning cannot work: {}".format("; ".join(problems))
            )

    def preferred_part_size(self, size):
        for below, part_size in self.part_size_tiers:
            if below is None or size < below:
                return part_size
        return self.part_size_tiers[-1][1]

    @property
    def size_feedback(self) -> bool:
        """Whether each file learns its part sizes from its own parts."""
        return (
            self.policy == SCALED_S3
            and self.adaptive
            and not self.explicit_sizes
        )


_THROTTLES = (429, 503, 504)

# Seconds a part waiting to be sent again rechecks whether to stop.
_WAIT_SLICE = 0.25

# Part-size feedback (scaled S3): eligible windows at one size before a
# larger one is tried, the gain it must show, the non-earning windows that
# return it, the windows held after, the largest size it tries, and the
# fewest accepted parts a file's window holds.
_SIZE_GROWTH_WINDOWS = 2
_SIZE_GAIN = 0.10
_SIZE_PROBE_WINDOWS = 2
_SIZE_HOLD_WINDOWS = 4
_SIZE_CEILING = 256 * MiB
_SIZE_WINDOW_ANSWERS = 8


class _Permit:
    """Room for one HTTP attempt to send a part, from a Controller. A part's
    first attempt gets its permit as the part is admitted; each later one,
    such as a retry, or an attempt after the part's URL was renewed, waits
    for a fresh one (acquire), so a part waiting to be sent again holds none.
    The attempt is on the network from begin() until answered(), when its
    response's headers arrive (or until end() or release() without them);
    a throttle those headers carry counts then, even if the body fails.
    end() reports how it ended and gives the permit back, and release()
    gives it back without a measurement, safe to repeat.

    A download's attempt is on the network until the last byte of its
    body arrives, so it calls answered() then, or at its headers only for
    a throttle; while it writes what arrived to a local file (writing()),
    it is off the network, and that time is not part of its duration."""

    def __init__(self, controller):
        self.controller = controller
        self.held = True
        self.running = False
        self.sequence = 0
        self.epoch = 0
        self.started_at: float | None = None
        self.answered_at: float | None = None
        # Whether the attempt's response headers already throttled the
        # controller, so its outcome does not teach it again.
        self.throttled = False
        # A download's attempt writing to a local file, since when, and the
        # seconds it spent doing so.
        self.local = False
        self.local_since = 0.0
        self.local_seconds = 0.0
        # The file's part-size feedback, told of each attempt.
        self.sizer: "_SizeFeedback | None" = None

    def acquire(self, lifetime):
        if not self.held:
            self.controller._acquire(self, lifetime)

    def begin(self):
        """The attempt goes to the network now."""
        self.controller._begin(self)

    def answered(self, status=None, retry_after=None):
        """The attempt's response headers have arrived, with status and the
        Retry-After seconds they ask for."""
        self.controller._answered(self, status, retry_after)

    def writing(self, active):
        """A download's attempt starts (active) or stops writing what it
        received to a local file."""
        self.controller._writing(self, active)

    def end(self, status, retry_after, size):
        """The attempt ended with status (None without a response), sending
        size bytes; the permit goes back."""
        self.controller._end(self, status, retry_after, size)

    def release(self):
        self.controller._abandon(self)


class Controller:
    """How many part attempts may be in progress now, for one upload or for
    the compatible uploads of a job sharing it. Each attempt holds a permit
    (see admit and _Permit); workers report each attempt's outcome. Events
    are serialized under one lock and use the monotonic clock; nothing waits
    for the network, reads a source or calls an observer while holding it.

    The configurable controller grows after successes and shrinks after
    failures as UploadTuning describes. The scaled S3 policy measures
    windows of accepted attempts: delivered bytes over wall time, accepted
    attempt durations per byte (L, and the lowest window L, Lmin), attempts
    in flight integrated over the window (I) and the queue estimate
    I * (1 - Lmin / L). An attempt lasts, and is in flight, from its send to
    its response's headers: building and logging the request, waiting for a
    permit and reading the response's body are not part of it. A download's
    attempt lasts until its body has arrived, less the time it spends
    writing to a local file, when it is not in flight either. An attempt
    stopped with its operation is abandoned, never a failure. A window
    closes after max(32, target) accepted
    attempts and at least their mean duration, and is judged only if
    attempts met the target for 75% of its time; otherwise it reports the
    dominant shortfall. Completions during a cooldown measure nothing.
    Each attempt carries the epoch it began in: only a failure from the
    current epoch shrinks the target, which starts a new epoch, while every
    throttle extends the cooldown and restarts measurement."""

    def __init__(self, settings: _Settings, shared=False):
        self.settings = settings
        # Whether a job's uploads share it.
        self.shared = shared
        self._lock = threading.Condition()
        self._scaled = settings.policy == SCALED_S3
        low = min(settings.min_concurrency, settings.max_concurrency)
        self._target = settings.max_concurrency
        if settings.adaptive:
            self._target = max(
                low,
                min(settings.initial_concurrency, settings.max_concurrency),
            )
        self._low = low
        # The scaled policy's start, after max_concurrency.
        self._start = self._target
        # Default startup warms up from one part, where the SDK chose the
        # scaled policy and its start is above one.
        self.warm_start = (
            self._scaled
            and settings.adaptive
            and settings.startup == UploadStartup.DEFAULT.value
            and self._start > 1
        )
        self._warm = self.warm_start
        if self._warm:
            self._target = self._low = 1
        self._pause_until = 0.0
        self._epoch = 0
        self._permits = 0
        self._retry_waiting = 0
        self._network = 0
        # Downloads' attempts writing to a local file, off the network.
        self._local = 0
        self._sequence = 0
        self._running: set[int] = set()
        # The configurable controller.
        self._successes = 0
        self._probing = False
        self._probe_start = 0
        self._probe_misses = 0
        self._hold = 0
        self._window_parts = 0
        self._window_bytes = 0
        self._window_duration = 0.0
        self._window_started = 0.0
        self._best = 0.0
        self._min_seconds_per_byte = 0.0
        self._queue = 0.0
        self.bytes_total = 0
        self.stats = {
            "grow": 0,
            "shrink": 0,
            "failures": 0,
            "backpressure": 0,
            "probe_misses": 0,
            "latency_backoffs": 0,
            "peak": self._target,
        }
        # Attempts: accepted (with their seconds from send to response
        # headers), failed and abandoned; and attempts in flight integrated
        # over time.
        self.attempts = {
            "accepted": 0,
            "failed": 0,
            "abandoned": 0,
            "seconds": 0.0,
            "network_seconds": 0.0,
        }
        # Each observer's queue of (decision, target after it, cooldown
        # seconds, epoch, shortfall, queue estimate).
        self._listeners: list[collections.deque[tuple[Any, ...]]] = []
        # The scaled policy's measurement.
        now = time.monotonic()
        self._last_mark = now
        self._shortfall = "no part ready"
        self._open_window(now)
        self._lmin = 0.0
        self._measured = 0.0
        self._fast = False
        # Judged throughputs at the current target.
        self._level: list[float] = []
        # An ordinary probe: (from, to, misses, reference throughput).
        self._probe: tuple[int, int, int, float] | None = None
        self._steady_hold = 0
        # Warming up.
        self._phase = "warming" if self._warm else None
        self._baseline = 0.0
        self._raise_from = 0
        self._raise_by = 0
        self._after_rest = False
        self._settling = False
        self._cohort: set[int] | None = None
        self._answers = 0
        self._rest = 0
        # Counts rests begun, so a file's window knows it stayed in one.
        self._rests_begun = 0
        # The fastest judged median duration per byte at each target.
        self._medians: dict[int, float] = {}
        self._spread = 0.0
        self._spread_df = 0
        # Part-size feedback: each file's, and the one probing its size; how
        # many size experiments began or ended, and how many windows were
        # judged, which paces how sizes mature.
        self._sizers: list[_SizeFeedback] = []
        self._size_probe: _SizeFeedback | None = None
        self._size_transitions = 0
        self._judged_windows = 0

    @property
    def target(self) -> int:
        return self._target

    def pause_left(self) -> float:
        """Seconds until new parts may start after the storage service
        pushed back, or 0."""
        return max(0.0, self._pause_until - time.monotonic())

    # Permits.

    def admit(self, start) -> bool:
        """Call start(permit) to begin a new part, and return True, if one
        may begin now: no cooldown is running, no part waits to be sent
        again, and fewer attempts than the target hold permits. Otherwise
        return False without calling it. Outcomes take the same lock, so
        backpressure cannot arrive between this check and the start. start
        must only hand the part to a worker; anything that waits belongs
        before admit()."""
        with self._lock:
            if not self._has_room():
                return False
            permit = _Permit(self)
            # Permits held, as well as attempts on the network, tell why a
            # window falls short: count up to now first.
            self._mark(time.monotonic())
            self._permits += 1
            try:
                start(permit)
            except BaseException:
                permit.held = False
                self._permits -= 1
                self._lock.notify_all()
                raise
            return True

    def room(self) -> int:
        """How many more parts may be admitted now."""
        with self._lock:
            if self.pause_left() or self._retry_waiting:
                return 0
            return max(0, self._target - self._permits)

    def wait_for_room(self, timeout):
        """Wait up to timeout seconds for room to admit a part."""
        with self._lock:
            if not self._has_room():
                left = self.pause_left()
                self._lock.wait(min(timeout, left) if left else timeout)

    def note_shortfall(self, reason):
        """Why attempts fall short of the target now, as the uploads see
        it: "limiter" while waiting for room in the TransferLimiter, "no
        part ready" otherwise. A window that is not judged reports the
        reason that lasted longest."""
        with self._lock:
            if reason != self._shortfall:
                self._mark(time.monotonic())
                self._shortfall = reason

    def admission(self) -> tuple[int, bool, bool, int]:
        """The target, whether it is warming up, whether it started warm,
        and the parts waiting to be sent again, observed together."""
        with self._lock:
            return (
                self._target,
                self._warm,
                self.warm_start,
                self._retry_waiting,
            )

    def _has_room(self):
        return (
            not self.pause_left()
            and not self._retry_waiting
            and self._permits < self._target
        )

    def _acquire(self, permit, lifetime):
        stop_waking = lifetime.watch(self._wake)
        try:
            with self._lock:
                self._retry_waiting += 1
                try:
                    while self.pause_left() or self._permits >= self._target:
                        lifetime.check("waiting to send a part again")
                        left = self.pause_left()
                        self._lock.wait(
                            min(left, _WAIT_SLICE) if left else _WAIT_SLICE
                        )
                    lifetime.check("waiting to send a part again")
                finally:
                    self._retry_waiting -= 1
                self._mark(time.monotonic())
                self._permits += 1
                permit.held = True
        finally:
            stop_waking()

    def _wake(self):
        with self._lock:
            self._lock.notify_all()

    def attempts_in_progress(self) -> int:
        """Attempts on the network now: sent, their response headers (a
        download's: its body) not yet arrived, and not writing to a local
        file."""
        with self._lock:
            return self._network

    def _begin(self, permit):
        with self._lock:
            now = time.monotonic()
            self._mark(now)
            self._sequence += 1
            permit.sequence = self._sequence
            permit.epoch = self._epoch
            permit.running = True
            permit.started_at = now
            permit.answered_at = None
            permit.throttled = False
            permit.local = False
            permit.local_seconds = 0.0
            self._network += 1
            self._running.add(permit.sequence)
            if permit.sizer is not None:
                permit.sizer.began(now)
            if (
                self._settling
                and self._cohort is None
                and self._network >= self._target
            ):
                # The raised target has filled: every attempt of this cohort
                # must end before the raise is judged.
                self._cohort = set(self._running)

    def _answered(self, permit, status=None, retry_after=None):
        with self._lock:
            now = time.monotonic()
            if not permit.running:
                return
            permit.answered_at = now
            self._stop_running(permit, now)
            if status in _THROTTLES:
                # The storage service pushed back: its cooldown, and the
                # epoch's one shrink, count now, before the body is read and
                # even if it never arrives. The outcome does not count again.
                permit.throttled = True
                self._failed(True, retry_after, permit.epoch, now)

    def _end(self, permit, status, retry_after, size):
        with self._lock:
            now = time.monotonic()
            self._stop_running(permit, now)
            # An attempt lasts from its send until its response's headers (a
            # download's until its body), less any local writes.
            ended = (
                permit.answered_at if permit.answered_at is not None else now
            )
            seconds = (
                ended - permit.started_at
                if permit.started_at is not None
                else 0.0
            )
            seconds = max(0.0, seconds - permit.local_seconds)
            if status is not None and status < 300:
                self.attempts["accepted"] += 1
                self.attempts["seconds"] += seconds
            else:
                self.attempts["failed"] += 1
            if not permit.throttled:
                self._outcome(
                    status,
                    retry_after,
                    seconds,
                    size,
                    permit.epoch,
                    now,
                    permit.sizer,
                )
            self._give_back(permit)

    def _abandon(self, permit):
        """The attempt, if one is in progress, stopped with its operation,
        or the permit goes back unused: no measurement either way."""
        with self._lock:
            if permit.running:
                self.attempts["abandoned"] += 1
            self._stop_running(permit, time.monotonic())
            self._give_back(permit)

    def _writing(self, permit, active):
        """permit's download attempt starts (active) or stops writing to a
        local file: meanwhile it is off the network, and that time is
        neither the network's nor part of the attempt's duration."""
        with self._lock:
            now = time.monotonic()
            if not permit.running or permit.local == active:
                return
            self._mark(now)
            permit.local = active
            if active:
                permit.local_since = now
                self._network -= 1
                self._local += 1
            else:
                permit.local_seconds += now - permit.local_since
                self._network += 1
                self._local -= 1

    def _stop_running(self, permit, now):
        if not permit.running:
            return
        permit.running = False
        self._mark(now)
        if permit.local:
            # Stopped while writing to a local file, off the network.
            permit.local = False
            self._local -= 1
        else:
            self._network -= 1
        self._running.discard(permit.sequence)
        if permit.sizer is not None:
            permit.sizer.ended(now)
        if self._cohort is not None:
            self._cohort.discard(permit.sequence)
            if self._settling and not self._cohort:
                # The cohort has ended: the raise is judged from a window
                # opened now.
                self._settling = False
                self._cohort = None
                self._open_window(now)

    def _give_back(self, permit):
        if permit.held:
            self._mark(time.monotonic())
            permit.held = False
            self._permits -= 1
            self._lock.notify_all()

    # Outcomes.

    def record(
        self,
        *,
        success,
        seconds,
        size,
        status=None,
        retry_after=None,
        epoch=None,
    ):
        """One attempt to send a part, without a permit: whether it
        succeeded, how long it took, its size, its HTTP status if it got
        one, and the epoch it began in (None: the current one)."""
        with self._lock:
            now = time.monotonic()
            if success:
                self._succeeded(seconds, size, now, None)
            else:
                self._failed(status in _THROTTLES, retry_after, epoch, now)

    def _outcome(self, status, retry_after, seconds, size, epoch, now, sizer):
        # A refusal other than 429, such as an expired URL, says nothing
        # about how many parts the storage service can take.
        if status is None or status >= 500 or status == 429:
            self._failed(status in _THROTTLES, retry_after, epoch, now)
        elif status < 300:
            self._succeeded(seconds, size, now, sizer)

    def _succeeded(self, seconds, size, now, sizer):
        self.bytes_total += size
        if self.pause_left() or not self.settings.adaptive:
            # A completion during a cooldown measures nothing.
            return
        if not self._scaled:
            self._sample(seconds, size)
            self._grow()
            return
        if sizer is not None:
            transitions = self._size_transitions
            sizer.accepted(size, seconds, now)
            if self._size_transitions != transitions:
                # This answer began or ended a size experiment: measurement
                # restarted after it, without it.
                return
        if self._settling:
            self._answers += 1
            if self._answers >= max(
                self.settings.throughput_window, self._target
            ):
                # Enough answers since the raise: the window now closing may
                # judge it without waiting for the cohort.
                self._settling = False
                self._cohort = None
        self._w_count += 1
        self._w_bytes += size
        self._w_seconds += seconds
        if self._warm and size > 0:
            self._w_per_byte.append(seconds / size)
        self._maybe_close(now)

    def _failed(self, throttle, retry_after, epoch, now):
        settings = self.settings
        if throttle:
            self.stats["backpressure"] += 1
            pause = (
                retry_after
                if retry_after is not None
                else settings.backpressure_pause
            )
            if pause > 0:
                # Never shortens a cooldown already running.
                self._pause_until = max(self._pause_until, now + pause)
        if not settings.adaptive:
            if throttle:
                self._decided("backpressure", self.pause_left())
            return
        if not throttle:
            self.stats["failures"] += 1
        current = epoch is None or epoch == self._epoch
        percent = (
            settings.backpressure_shrink_percent
            if throttle
            else settings.failure_shrink_percent
        )
        if self._scaled:
            if throttle:
                self._open_window(now)
            self._probe = None
            # A failure interrupts a size probe and restarts each file's
            # size measurement.
            self._interrupt_size_probe()
            for sizer in self._sizers:
                sizer.restart()
            if current:
                self._shrink(percent, 1 if self._warm else self._low)
                self._new_epoch(now)
            if self._warm:
                # Any outstanding raise is abandoned; rest at the target
                # failure handling left.
                self._enter_rest()
        else:
            if throttle:
                self._restart_samples()
            if current:
                self._reset_growth()
                self._shrink(percent, self._low)
                self._new_epoch(now)
        label = "backpressure" if throttle else "failure"
        self._decided(
            label if current else "stale_" + label, self.pause_left()
        )

    # All below run with the lock held.

    def _decided(self, decision, cooldown=0.0, shortfall=None, queue=None):
        entry = (
            decision,
            self._target,
            cooldown,
            self._epoch,
            shortfall,
            queue,
        )
        for listener in self._listeners:
            listener.append(entry)

    def _set_target(self, target, now=None):
        if target == self._target:
            return
        self._target = target
        self.stats["peak"] = max(self.stats["peak"], target)
        if self._scaled:
            # A new target opens a new window; a baseline measured at the
            # old one no longer applies.
            self._open_window(time.monotonic() if now is None else now)
            self._level = []
            for sizer in self._sizers:
                sizer.concurrency_changed()

    def _new_epoch(self, now):
        self._epoch += 1
        if self._scaled:
            self._open_window(now)
            self._level = []

    def _reset_growth(self):
        self._successes = 0
        self._probing = False
        self._probe_misses = 0

    def _restart_samples(self):
        self._window_parts = self._window_bytes = 0
        self._window_duration = 0.0

    def _shrink(self, percent, floor):
        if percent <= 0 or self._target <= floor:
            return False
        smaller = int(self._target * (100 - percent) / 100)
        self._set_target(max(floor, min(smaller, self._target - 1)))
        self.stats["shrink"] += 1
        return True

    # The configurable controller.

    def _ceiling(self):
        settings = self.settings
        if (
            not settings.soft_ceiling
            or settings.soft_ceiling >= settings.max_concurrency
        ):
            return settings.max_concurrency
        unlocked = (
            self.bytes_total >= settings.unlock_bytes
            and self._best >= settings.unlock_bytes_per_second
        )
        return settings.max_concurrency if unlocked else settings.soft_ceiling

    def _grow(self):
        settings = self.settings
        self._successes += 1
        if (
            self._successes < settings.grow_every
            or self._probing
            or self._hold
        ):
            return
        self._successes = 0
        ceiling = self._ceiling()
        if self._target >= ceiling:
            return
        if (
            settings.latency_growth_queue_high
            and self._queue > settings.latency_growth_queue_high
        ):
            return
        previous = self._target
        self._set_target(min(ceiling, self._target + settings.grow_step))
        self.stats["grow"] += 1
        if (
            settings.throughput_window
            and settings.probe_min_gain_percent
            and settings.throughput_shrink_percent
        ):
            self._probing = True
            self._probe_start = previous
            self._probe_misses = 0
        self._decided("grow")

    def _sample(self, seconds, size):
        settings = self.settings
        if not settings.throughput_window or size <= 0:
            return
        now = time.monotonic()
        started = now - seconds
        if not self._window_parts or started < self._window_started:
            self._window_started = started
        self._window_parts += 1
        self._window_bytes += size
        self._window_duration += seconds
        if self._window_parts < settings.throughput_window:
            return
        wall = now - self._window_started
        rate = self._window_bytes / wall if wall > 0 else 0.0
        seconds_per_byte = (
            self._window_duration / self._window_bytes
            if self._window_duration
            else 0.0
        )
        self._restart_samples()
        if seconds_per_byte > 0:
            if (
                not self._min_seconds_per_byte
                or seconds_per_byte < self._min_seconds_per_byte
            ):
                self._min_seconds_per_byte = seconds_per_byte
            self._queue = self._target * (
                1 - self._min_seconds_per_byte / seconds_per_byte
            )
        if rate <= 0:
            return
        if self._hold:
            self._hold -= 1
        if not self._best:
            self._best = rate
            return
        if not self._probing:
            dropped = rate < self._best * (
                1 - max(settings.probe_min_gain_percent, 1) / 100
            )
            if (
                settings.latency_queue_high
                and self._queue > settings.latency_queue_high
                and dropped
            ):
                if self._shrink(settings.latency_shrink_percent, self._low):
                    self.stats["latency_backoffs"] += 1
                    self._hold = settings.hold_windows
                    self._successes = 0
                    self._decided("latency_backoff")
                return
            self._best = max(self._best, rate)
            return
        required = settings.probe_min_gain_percent
        if settings.probe_plateau and self._target > settings.probe_plateau:
            added = self._target - max(
                self._probe_start, settings.probe_plateau
            )
            required = max(
                required, added * settings.probe_gain_per_part_percent
            )
        if rate >= self._best * (1 + required / 100):
            self._best = rate
            self._probing = False
            self._decided("probe_kept")
            return
        tolerance = settings.probe_loss_tolerance_percent
        if tolerance and rate >= self._best * (1 - tolerance / 100):
            self._probing = False
            self._decided("probe_kept")
            return
        self._probe_misses += 1
        self.stats["probe_misses"] += 1
        if self._probe_misses < settings.probe_windows:
            self._decided("probe_miss")
            return
        self._probing = False
        self._probe_misses = 0
        if self._shrink(settings.throughput_shrink_percent, self._low):
            self._hold = settings.hold_windows
            self._successes = 0
        self._decided("probe_revert")

    # The scaled S3 policy: measurement.

    def _mark(self, now):
        """Integrate attempts in flight up to now. Time short of the target
        is the cooldown's while one runs; otherwise "local destination
        writes" while a download's attempt writes to a local file; otherwise
        "held off network" while permits fill the target but their attempts
        are not on the network (their responses' bodies still being read,
        say); otherwise the shortfall the transfers last reported."""
        last = self._last_mark
        elapsed = now - last
        if elapsed > 0:
            self.attempts["network_seconds"] += self._network * elapsed
            self._w_occupied += self._network * elapsed
            if self._network >= self._target:
                self._w_full += elapsed
            else:
                cooling = max(0.0, min(now, self._pause_until) - last)
                if cooling:
                    self._w_short["cooldown"] = (
                        self._w_short.get("cooldown", 0.0) + cooling
                    )
                if elapsed > cooling:
                    if self._local:
                        reason = "local destination writes"
                    elif self._permits >= self._target:
                        reason = "held off network"
                    else:
                        reason = self._shortfall
                    self._w_short[reason] = (
                        self._w_short.get(reason, 0.0) + elapsed - cooling
                    )
            self._last_mark = now

    def _open_window(self, now):
        """Start a window at now, discarding the old one's partial
        accumulation."""
        self._mark(now)
        self._w_opened = now
        self._w_count = 0
        self._w_bytes = 0
        self._w_seconds = 0.0
        self._w_occupied = 0.0
        self._w_full = 0.0
        self._w_short: dict[str, float] = {}
        self._w_per_byte: list[float] = []

    def _maybe_close(self, now):
        count = self._w_count
        elapsed = now - self._w_opened
        if not count or elapsed <= 0 or elapsed < self._w_seconds / count:
            return
        target = self._target
        window = self.settings.throughput_window
        if not self._warm:
            if count >= max(window, target):
                self._close(now)
            return
        if self._phase == "warming" or self._settling:
            needed = target
        elif self._phase == "rest":
            needed = max(window, target)
        else:
            needed = max(target, self._samples_needed())
        fast = (
            count >= target
            and self._w_bytes / elapsed
            >= self.settings.fast_link_bytes_per_second
        )
        if count >= needed or fast:
            self._close(now)

    def _close(self, now):
        self._mark(now)
        elapsed = now - self._w_opened
        delivered = self._w_bytes
        rate = delivered / elapsed
        per_byte = self._w_seconds / delivered if delivered else 0.0
        in_flight = self._w_occupied / elapsed
        if per_byte > 0 and (not self._lmin or per_byte < self._lmin):
            self._lmin = per_byte
        self._queue = (
            in_flight * (1 - self._lmin / per_byte) if per_byte > 0 else 0.0
        )
        eligible = self._w_full >= 0.75 * elapsed
        shortfall = (
            max(self._w_short, key=self._w_short.__getitem__)
            if self._w_short
            else self._shortfall
        )
        answers = self._w_per_byte
        settling = self._settling
        self._open_window(now)
        if not eligible:
            self._decided("window_not_measured", shortfall=shortfall)
            return
        self._measured = max(self._measured, rate)
        if self._size_probe is not None:
            # Concurrency holds while a file judges a part size, which also
            # pauses a warm rest; only a fast link changes it.
            if rate >= self.settings.fast_link_bytes_per_second:
                if self._warm:
                    # Promotion returns the size probe to its earlier size.
                    self._promote()
                    return
                self._fast = True
            return
        self._judged_windows += 1
        if self._warm:
            self._warm_window(rate, in_flight, answers, settling)
            return
        self._steady_window(rate, self._queue)

    def _size_changed(self, now):
        """A file began or ended a size experiment: the window under way and
        the level's baseline mixed sizes, so measurement restarts now."""
        self._size_transitions += 1
        self._open_window(now)
        self._level = []

    def _size_probe_allowed(self):
        """Whether concurrency holds so a file may try a larger part size:
        in the hold window of a warm rest (never for a scope several files
        share while warming), or, once warmed, at the ceiling or after a
        withdrawn raise, with no raise being judged."""
        if self._size_probe is not None:
            return False
        if self._warm:
            return (
                not self.shared
                and self._phase == "rest"
                and self._rest < self.settings.hold_windows
            )
        return (
            self._scaled
            and self._probe is None
            and (
                self._steady_hold > 0 or self._target >= self._scaled_ceiling()
            )
        )

    def _size_window_counts(self, opened_in_rest, opened_warm):
        """Whether a file's window that opened during the rest numbered
        opened_in_rest (or outside warming, when opened_warm is False) may
        mature its part size: never while a shared scope warms, and while a
        single file warms only within one rest."""
        if opened_warm != self._warm:
            return False
        if not self._warm:
            return True
        return (
            not self.shared
            and self._phase == "rest"
            and opened_in_rest == self._rests_begun
        )

    def _steady_window(self, rate, queue):
        """Judge a window of the ordinary policy."""
        settings = self.settings
        if rate >= settings.fast_link_bytes_per_second:
            self._fast = True
        if self._probe is not None:
            start, raised, misses, reference = self._probe
            required = settings.probe_min_gain_percent
            if settings.probe_plateau and raised > settings.probe_plateau:
                required = max(
                    required,
                    settings.probe_gain_per_part_percent
                    * (raised - max(start, settings.probe_plateau)),
                )
            tolerance = settings.probe_loss_tolerance_percent
            tolerated = (
                tolerance
                and self._unlocked()
                and start >= settings.soft_ceiling
                and raised <= settings.probe_plateau
                and rate >= reference * (1 - tolerance / 100)
            )
            free = self._fast and raised <= self.settings.probe_floor
            if rate >= reference * (1 + required / 100) or tolerated or free:
                self._probe = None
                self._level = [rate]
                self._decided("probe_kept", queue=queue)
                return
            misses += 1
            self.stats["probe_misses"] += 1
            if misses < settings.probe_windows:
                self._probe = (start, raised, misses, reference)
                self._decided("probe_miss", queue=queue)
                return
            self._probe = None
            # Withdrawn, never above the level before the probe.
            withdrawn = max(
                self._backoff_floor(),
                int(raised * (100 - settings.throughput_shrink_percent) / 100),
            )
            self._set_target(min(start, withdrawn))
            self.stats["shrink"] += 1
            self._steady_hold = settings.hold_windows
            self._decided("probe_revert", queue=queue)
            return
        # Queued work above the backoff threshold with any decline in judged
        # throughput withdraws load.
        declined = bool(self._level) and rate < sum(self._level) / len(
            self._level
        )
        if (
            settings.latency_queue_high
            and queue > settings.latency_queue_high
            and declined
        ):
            floor = self._backoff_floor()
            if self._target > floor:
                self._set_target(
                    max(
                        floor,
                        min(
                            int(
                                self._target
                                * (100 - settings.latency_shrink_percent)
                                / 100
                            ),
                            self._target - 1,
                        ),
                    )
                )
                self.stats["shrink"] += 1
                self.stats["latency_backoffs"] += 1
                self._steady_hold = settings.hold_windows
                self._decided("latency_backoff", queue=queue)
                return
        self._level.append(rate)
        if self._steady_hold:
            self._steady_hold -= 1
            return
        ceiling = self._scaled_ceiling()
        if self._target >= ceiling:
            return
        if (
            settings.latency_growth_queue_high
            and queue > settings.latency_growth_queue_high
        ):
            return
        start = self._target
        reference = sum(self._level) / len(self._level)
        self._set_target(min(ceiling, start + settings.grow_step))
        self._probe = (start, self._target, 0, reference)
        self.stats["grow"] += 1
        self._decided("grow", queue=queue)

    def _unlocked(self):
        settings = self.settings
        return (
            self.bytes_total >= settings.unlock_bytes
            and self._measured >= settings.unlock_bytes_per_second
        )

    def _scaled_ceiling(self):
        settings = self.settings
        if (
            not settings.soft_ceiling
            or settings.soft_ceiling >= settings.max_concurrency
            or self._unlocked()
        ):
            return settings.max_concurrency
        return settings.soft_ceiling

    def _backoff_floor(self):
        settings = self.settings
        floor = settings.backoff_floor
        if self._fast:
            floor = max(floor, settings.probe_floor)
        return max(self._low, min(floor, settings.max_concurrency))

    # The scaled S3 policy: warming up (Default startup).

    def _warm_window(self, rate, in_flight, answers, settling):
        """Judge a window while warming up."""
        settings = self.settings
        spread, degrees = _relative_spread(answers)
        self._spread += spread
        self._spread_df += degrees
        if rate >= settings.fast_link_bytes_per_second:
            self._promote()
            return
        if settling:
            # An unsettled cohort's window judges nothing.
            return
        median = statistics.median(answers) if answers else 0.0
        target = self._target
        if median:
            self._medians[target] = min(
                self._medians.get(target, median), median
            )
        if self._phase == "warming":
            # The first window warms the connection; the next is the baseline.
            self._phase = "baseline"
            return
        if self._phase == "baseline":
            self._baseline = rate
            self._raise_or_rest(in_flight, median)
            return
        if self._phase == "judging":
            start, added = self._raise_from, self._raise_by
            queue = _warm_queue(
                in_flight, self._medians.get(start, 0.0), median
            )
            if (
                rate >= self._baseline * (1 + 0.5 * added / start)
                and queue < 0.5 * added
            ):
                self._decided("warm_settled", queue=queue)
                if target >= self._start:
                    self._end_warm()
                    return
                self._baseline = rate
                self._after_rest = False
                self._raise_or_rest(in_flight, median)
                return
            self._decided("warm_withdraw", queue=queue)
            self._set_target(start)
            self._new_epoch(time.monotonic())
            self._enter_rest()
            return
        # Resting: hold_windows plus grow_every judged windows; only the
        # first hold_windows of them let a file try a larger part size.
        self._rest += 1
        if self._rest < settings.hold_windows + settings.grow_every:
            return
        self._baseline = rate
        self._after_rest = True
        self._raise_or_rest(in_flight, median)

    def _raise_or_rest(self, in_flight, median):
        """From a baseline: raise the target, by about half or by one after
        a rest, unless the baseline is queued, which rests instead."""
        start = self._target
        added = 1 if self._after_rest else max(1, math.ceil(start / 2))
        queue = _warm_queue(in_flight, self._medians.get(start, 0.0), median)
        if queue >= 0.5 * added:
            self._decided("warm_rest", queue=queue)
            self._enter_rest()
            return
        raised = min(self._start, start + added)
        if raised <= start:
            self._end_warm()
            return
        self._set_target(raised)
        self._raise_from, self._raise_by = start, raised - start
        self._phase = "judging"
        self._settling = True
        self._cohort = None
        self._answers = 0
        self._decided("warm_raise", queue=queue)

    def _enter_rest(self):
        self._phase = "rest"
        self._rest = 0
        self._rests_begun += 1
        self._settling = False
        self._cohort = None

    def _promote(self):
        """A fast link: warming ends at the policy's start."""
        self._interrupt_size_probe()
        self._finish_warming()
        self._fast = True
        self._set_target(self._start)
        self._decided("warm_fast_link")

    def _end_warm(self):
        self._finish_warming()
        self._decided("warm_end")

    def _finish_warming(self):
        self._warm = False
        self._phase = None
        self._settling = False
        self._cohort = None
        self._low = min(
            self.settings.min_concurrency, self.settings.max_concurrency
        )
        self._level = []
        self._medians.clear()

    def _samples_needed(self):
        """The answers a window judging a warm baseline or raise needs, from
        the variation observed within judged windows and this one: a
        bounded sampling heuristic, not a confidence guarantee."""
        target = self._target
        if self._phase == "baseline":
            added = 1 if self._after_rest else max(1, math.ceil(target / 2))
            raised = target + added
        else:
            added = max(1, self._raise_by)
            raised = target
        spread, degrees = _relative_spread(self._w_per_byte)
        spread += self._spread
        degrees += self._spread_df
        window = self.settings.throughput_window
        if degrees <= 0 or spread <= 0:
            return 2
        allowance = 2 / (9 * degrees)
        scale = 1 - allowance - 2 * math.sqrt(allowance)
        if scale <= 0:
            return window
        variation = spread / (degrees * scale**3)
        return min(
            window,
            max(
                2, math.ceil(2 * variation * (raised * 2 / (0.5 * added)) ** 2)
            ),
        )

    # Part-size feedback.

    def add_sizer(self, sizer):
        with self._lock:
            self._sizers.append(sizer)

    def remove_sizer(self, sizer):
        with self._lock:
            if sizer in self._sizers:
                self._sizers.remove(sizer)
            if self._size_probe is sizer:
                self._size_probe = None

    def _interrupt_size_probe(self):
        if self._size_probe is not None:
            self._size_probe.interrupt()

    # Observing.

    def watch(self) -> collections.deque[tuple[Any, ...]]:
        """A queue that hears every decision from now on."""
        listener: collections.deque[tuple[Any, ...]] = collections.deque()
        with self._lock:
            self._listeners.append(listener)
        return listener

    def unwatch(self, listener):
        with self._lock:
            if listener in self._listeners:
                self._listeners.remove(listener)

    def snapshot(self) -> dict[str, Any]:
        with self._lock:
            return {
                **self.stats,
                "target": self._target,
                "best_bytes_per_second": (
                    self._measured if self._scaled else self._best
                ),
                "queue_estimate": self._queue,
                "target_class": self.settings.target_class,
                "adaptive": self.settings.adaptive,
                "policy": self.settings.policy,
                "startup": self.settings.startup,
                "warm_start": self.warm_start,
                "warming": self._warm,
                "fast_link": self._fast,
                "epoch": self._epoch,
                "attempts": dict(self.attempts),
            }


def _relative_spread(values):
    """The squared deviations of values from their mean, relative to the
    squared mean, and their degrees of freedom."""
    if len(values) < 2:
        return 0.0, 0
    mean = sum(values) / len(values)
    if mean <= 0:
        return 0.0, 0
    return (
        sum(((value - mean) / mean) ** 2 for value in values),
        len(values) - 1,
    )


def _warm_queue(in_flight, reference, median):
    """The warm queue estimate: attempts in flight times how much slower
    the window's median answer per byte is than the reference."""
    if not reference or not median:
        return 0.0
    return max(0.0, in_flight * (1 - reference / median))


class _SizeFeedback:
    """The part size one file's unread parts take, under the scaled S3
    policy, learned from that file's own accepted parts at its own share of
    the request budget.

    The file measures windows of its own. One opens at an accepted answer,
    which it does not count, and closes after at least
    _SIZE_WINDOW_ANSWERS more (and twice the most attempts the file had in
    flight) and at least their mean duration. Its evidence is the file's
    accepted bytes over the window's wall time. Its share is the number of
    attempts the file had in flight for longest; the window counts only if
    the file had exactly that many for 75% of it and never more, so that
    more of the request budget is never read as a gain, and only outside
    warming, or within one rest of a warm-up the file does not share. A
    window at another share is no baseline for the earlier ones, and a new
    target discards both the baseline and the window under way. A size
    matures with the controller's own window cadence: its count rises at
    most once per window the controller judges, and persists across
    targets.

    After two counted windows at a size, while the controller says
    concurrency holds and no other file of the scope is probing, the unread
    parts are twice as large (at most 256 MiB and what the grant allows),
    and the first answer at that size opens its window. So the first rest
    of a warm-up, whose hold window is its first, cannot start one; a later
    rest can. The size is kept if a window at the same share delivers 10%
    more than the baseline; it is returned after two windows that do not,
    when the file's share changes or it ever has more attempts in flight
    than the baseline's share, or when a failure or fast link interrupts it,
    holding four counted windows after. Starting, keeping and returning a
    size each restart the controller's measurement, so a size experiment's
    answers never judge concurrency. Parts already prepared, and parts sent
    again, keep their size. Called with the controller's lock held, except
    for size, which the planner reads."""

    def __init__(self, controller, size, largest):
        self.controller = controller
        self.size = size
        self.largest = largest
        self.count = 0
        self.level: list[float] = []
        self.level_share: int | None = None
        self.hold = 0
        self.probe: tuple[int, int] | None = None
        self.misses = 0
        self.baseline = 0.0
        # The controller's judged windows when the count last rose.
        self._matured_at = -1
        # This file's attempts on the network now.
        self.running = 0
        self._discard_window()

    def _discard_window(self):
        """Wait for the next accepted answer to open a window."""
        self._opened: float | None = None
        self._last = 0.0
        self._answers = 0
        self._bytes = 0
        self._seconds = 0.0
        self._occupied = 0.0
        self._time_at: dict[int, float] = {}
        self._peak = 0
        self._opened_in_rest = 0
        self._opened_warm = False

    def _open_window(self, now):
        self._discard_window()
        self._opened = self._last = now
        self._peak = self.running
        self._opened_in_rest = self.controller._rests_begun
        self._opened_warm = self.controller._warm

    def _mark(self, now):
        if self._opened is None:
            return
        elapsed = now - self._last
        if elapsed > 0:
            self._occupied += self.running * elapsed
            self._time_at[self.running] = (
                self._time_at.get(self.running, 0.0) + elapsed
            )
            self._last = now

    def began(self, now):
        self._mark(now)
        self.running += 1
        self._peak = max(self._peak, self.running)

    def ended(self, now):
        self._mark(now)
        self.running -= 1

    def accepted(self, size, seconds, now):
        measured = self.probe[1] if self.probe is not None else self.size
        if size != measured:
            return  # Delivered, but no evidence for the size measured.
        if self._opened is None:
            self._open_window(now)
            return
        self._mark(now)
        self._answers += 1
        self._bytes += size
        self._seconds += seconds
        elapsed = now - self._opened
        if (
            self._answers < max(_SIZE_WINDOW_ANSWERS, 2 * self._peak)
            or elapsed <= 0
            or elapsed < self._seconds / self._answers
        ):
            return
        self._judge(now, elapsed)

    def _judge(self, now, elapsed):
        controller = self.controller
        goodput = self._bytes / elapsed
        time_at = self._time_at
        # The share it held longest, exactly and never exceeded.
        share = max(time_at, key=time_at.__getitem__) if time_at else 0
        above = sum(
            seconds for running, seconds in time_at.items() if running > share
        )
        counts = (
            share > 0
            and time_at[share] >= 0.75 * elapsed
            and not above
            and controller._size_window_counts(
                self._opened_in_rest, self._opened_warm
            )
        )
        grew = self.level_share is not None and any(
            running > self.level_share for running in time_at
        )
        # The next window starts at this answer.
        self._open_window(now)
        if self.probe is not None:
            if grew or (counts and share != self.level_share):
                # Its share of the request budget changed: the baseline does
                # not apply to the larger size.
                self._give_back(now)
                return
            if not counts:
                return
            if goodput >= self.baseline * (1 + _SIZE_GAIN):
                self.probe = None
                self.count = 1
                self._matured_at = controller._judged_windows
                self.level = [goodput]
                controller._size_probe = None
                controller._size_changed(now)
                controller._decided("size_kept")
                return
            self.misses += 1
            if self.misses >= _SIZE_PROBE_WINDOWS:
                self._give_back(now)
            return
        if not counts:
            return
        if share != self.level_share:
            self.level = []
            self.level_share = share
        self.level.append(goodput)
        if controller._judged_windows > self._matured_at:
            # At most once per window the controller judges.
            self._matured_at = controller._judged_windows
            self.count += 1
            if self.hold:
                self.hold -= 1
        if (
            self.hold
            or self.count < _SIZE_GROWTH_WINDOWS
            or not controller._size_probe_allowed()
        ):
            return
        larger = min(
            self.size * 2, self.largest, max(_SIZE_CEILING, self.size)
        )
        if larger <= self.size:
            return
        self.baseline = sum(self.level) / len(self.level)
        self.probe = (self.size, larger)
        self.size = larger
        self.misses = 0
        # The first answer at the larger size opens its window.
        self._discard_window()
        controller._size_probe = self
        controller._size_changed(now)
        controller._decided("size_probe")

    def restart(self):
        """Measurement restarts, as after a failure: the window under way is
        discarded."""
        self._discard_window()

    def concurrency_changed(self):
        """The target changed: the baseline and the window under way no
        longer apply, and a larger size being judged goes back; the windows
        counted for the size persist."""
        if self.probe is not None:
            self._give_back()
            return
        self._discard_window()
        self.level = []
        self.level_share = None

    def interrupt(self):
        if self.probe is not None:
            self._give_back()

    def _give_back(self, now=None):
        assert self.probe is not None
        self.size = self.probe[0]
        self.probe = None
        self.hold = _SIZE_HOLD_WINDOWS
        self.level = []
        self.level_share = None
        self._discard_window()
        if self.controller._size_probe is self:
            self.controller._size_probe = None
        self.controller._size_changed(time.monotonic() if now is None else now)
        self.controller._decided("size_returned")


@dataclasses.dataclass(frozen=True)
class UploadObservation:
    """One observation of an upload, as UploadTuning.observer receives it.

    kind is "start" (details: how the upload was planned), "decision" (the
    controller's decision, with cooldown seconds for backpressure, the
    epoch after it, the shortfall of a window not measured and the queue
    estimate behind a warm-up or probe decision), "wait" (for room in the
    limiter, for the read-ahead runway, or for the storage service's
    cooldown, with the seconds waited), "sample" (at most four a second,
    with the process's resources) or "finish" (details: the record of the
    whole upload, whatever its outcome, with the settings it used and the
    SDK and Python that ran it). elapsed counts seconds from the upload's
    start; target_concurrency and the counts are those when the observation
    is delivered, which for a decision can be after later decisions:
    decision_target_concurrency is the controller's target immediately after
    that decision, and None for every other kind. parts_in_progress
    counts the upload's parts handed to workers and not yet finished, which
    includes parts waiting to be sent again; attempts_in_progress counts the
    attempts its controller has on the network (for a job, all of its
    files'), each from its send until its response's headers. What an
    upload of its kind does not have is None, never a zero it did not
    measure: an upload of unknown size, sent one part at a time, has no
    read-ahead runway, controller, decisions or throughput samples. The
    uploads of a job share a controller: each hears the decisions made
    while it runs.

    resources, where the platform reports them, has max_rss_bytes (the
    process's peak memory so far), cpu_user_seconds and cpu_system_seconds
    (the process's, not just the upload's).
    """

    kind: str
    elapsed: float
    target_concurrency: int
    parts_in_progress: int
    runway_parts: int | None
    runway_bytes: int | None
    decision: str | None = None
    cooldown: float = 0.0
    wait: str | None = None
    waited: float = 0.0
    resources: dict[str, float] | None = None
    details: dict[str, Any] | None = None
    epoch: int | None = None
    shortfall: str | None = None
    queue_estimate: float | None = None
    attempts_in_progress: int | None = None
    decision_target_concurrency: int | None = None


def process_resources() -> dict[str, float] | None:
    """The process's peak memory and CPU time, where the platform says."""
    if sys.platform == "win32":  # It has no resource module.
        return None
    try:
        import resource
    except ImportError:
        return None
    usage = resource.getrusage(resource.RUSAGE_SELF)
    # Linux reports the peak in KiB, macOS in bytes.
    scale = 1 if sys.platform == "darwin" else 1024
    return {
        "max_rss_bytes": float(usage.ru_maxrss * scale),
        "cpu_user_seconds": usage.ru_utime,
        "cpu_system_seconds": usage.ru_stime,
    }


_SAMPLE_INTERVAL = 0.25

_WAITS = ("limiter", "runway", "backpressure")


def knobs(settings) -> dict[str, Any]:
    """An upload's resolved settings, as its observation record reports them."""
    return {
        field.name: (
            [list(tier) for tier in value]
            if field.name == "part_size_tiers"
            else value
        )
        for field in dataclasses.fields(settings)
        for value in (getattr(settings, field.name),)
    }


class Observer:
    """Delivers one upload's observations to UploadTuning.observer, on the
    uploading thread, and keeps the counts its final record reports."""

    def __init__(self, callback, state, waits=_WAITS):
        self.callback = callback
        # A function returning (target, parts in progress, runway parts,
        # runway bytes, attempts in progress) now; the runway is None for an
        # upload without one, and the attempts for one without a controller.
        self.state = state
        self.started = time.monotonic()
        self.sampled_at = 0.0
        self.controller: Controller | None = None
        self._heard: collections.deque[tuple[Any, ...]] | None = None
        self.decisions: collections.Counter[str] = collections.Counter()
        # Only the waits this upload can have.
        self.waits: dict[str, float] = {kind: 0.0 for kind in waits}
        # The settings the upload chose, once it has chosen them.
        self.knobs: dict[str, Any] | None = None
        self.resources_at_start = process_resources()
        self.peak = 0

    def watch(self, controller):
        """Hear controller's decisions."""
        self.controller = controller
        if controller is not None:
            self._heard = controller.watch()

    def _now(self):
        state = self.state()
        self.peak = max(self.peak, state[1])
        return state

    def _emit(self, kind, **fields):
        target, in_progress, runway_parts, runway_bytes, attempts = self._now()
        self.callback(
            UploadObservation(
                kind=kind,
                elapsed=time.monotonic() - self.started,
                target_concurrency=target,
                parts_in_progress=in_progress,
                runway_parts=runway_parts,
                runway_bytes=runway_bytes,
                attempts_in_progress=attempts,
                **fields,
            )
        )

    def start(self, details):
        self._emit("start", details=dict(details))

    def waited(self, kind, seconds):
        if seconds <= 0:
            return
        self.waits[kind] += seconds
        self._emit("wait", wait=kind, waited=seconds)

    def poll(self):
        """Note the upload's state, as it goes and whenever a part starts or
        ends, and deliver the decisions made since, each with the target it
        left, and a sample when one is due."""
        self._now()
        heard = self._heard
        while heard:
            decision, target, cooldown, epoch, shortfall, queue = (
                heard.popleft()
            )
            self.decisions[decision] += 1
            self._emit(
                "decision",
                decision=decision,
                cooldown=cooldown,
                epoch=epoch,
                shortfall=shortfall,
                queue_estimate=queue,
                decision_target_concurrency=target,
            )
        now = time.monotonic()
        if now - self.sampled_at >= _SAMPLE_INTERVAL:
            self.sampled_at = now
            self._emit("sample", resources=process_resources())

    def finish(self, details):
        import platform

        import files_sdk

        controller = self.controller
        try:
            self.poll()
            snapshot = (
                controller.snapshot() if controller is not None else None
            )
            record = {
                "record": 2,
                **details,
                "seconds": round(time.monotonic() - self.started, 6),
                "peak_parts_in_progress": self.peak,
                # Without a controller, the upload sent one part at a time.
                "peak_target_concurrency": (
                    snapshot["peak"] if snapshot is not None else 1
                ),
                "best_bytes_per_second": (
                    snapshot["best_bytes_per_second"]
                    if snapshot is not None
                    else None
                ),
                "decisions": (
                    dict(self.decisions) if controller is not None else None
                ),
                # Its controller's attempts (for a job, all of its files'):
                # accepted, failed and abandoned, the seconds accepted ones
                # took from send to response headers, and attempts in flight
                # integrated over time.
                "attempts": (
                    snapshot["attempts"] if snapshot is not None else None
                ),
                "waits": {
                    kind: (
                        round(self.waits[kind], 6)
                        if kind in self.waits
                        else None
                    )
                    for kind in _WAITS
                },
                "settings": self.knobs,
                "runtime": {
                    "sdk_version": files_sdk.version,
                    "python": platform.python_version(),
                    "implementation": platform.python_implementation(),
                    "platform": sys.platform,
                    "machine": platform.machine(),
                },
                "resources": {
                    "start": self.resources_at_start,
                    "end": process_resources(),
                },
            }
            self._emit("finish", details=record)
        finally:
            if controller is not None and self._heard is not None:
                controller.unwatch(self._heard)


DEFAULT_TUNING = UploadTuning()
