import concurrent.futures
import heapq
import io
import logging
import os
import random
import sys
import tempfile
import threading
import time
import unittest
from pathlib import Path
from unittest import mock

import files_sdk
import requests
from files_sdk.adaptive import (
    Controller,
    UploadStartup,
    UploadTuning,
    _SizeFeedback,
    process_resources,
)
from files_sdk.error import (
    APIConnectionError,
    APIError,
    InvalidParameterError,
    InvalidRequestError,
    OperationCancelledError,
)
from files_sdk.lifetime import CancellationToken, Lifetime
from tests.download_fixtures import S3_ORIGIN
from tests.upload_fixtures import UploadService

KiB = 1024
MiB = 1024 * KiB


class FakeClock:
    def __init__(self):
        self.now = 1000.0

    def __call__(self):
        return self.now


class TestController(unittest.TestCase):
    """The adaptive controller, fed attempts on a fake clock."""

    def setUp(self):
        self.clock = FakeClock()
        patcher = mock.patch("files_sdk.adaptive.time.monotonic", self.clock)
        patcher.start()
        self.addCleanup(patcher.stop)

    def controller(self, max_concurrency=16, **tuning):
        return Controller(
            UploadTuning(**tuning).settings("generic", max_concurrency)
        )

    def succeed(self, controller, parts, seconds=0.1, size=1000):
        for _ in range(parts):
            self.clock.now += seconds / controller.target
            controller.record(success=True, seconds=seconds, size=size)

    def scaled(self, max_concurrency=1024, startup=None):
        """The controller of an automatic upload to S3."""
        return Controller(
            UploadTuning(startup=startup).settings("s3", max_concurrency)
        )

    def rounds(self, controller, count, seconds, size):
        """count rounds in which as many attempts as the controller admits
        start together, take seconds and are accepted. Returns the target
        after each round."""
        targets = []
        for _ in range(count):
            permits = []
            while controller.admit(permits.append):
                pass
            for permit in permits:
                permit.begin()
            self.clock.now += seconds
            for permit in permits:
                permit.end(200, None, size)
            targets.append(controller.target)
        return targets

    def traffic(self, controller, plan, running, until):
        """Attempts against controller, ending at their own times, until
        until() holds: each (sizer, share, bytes per second) of plan keeps
        up to share attempts of its sizer's size in flight, each lasting
        size / bytes per second; share and bytes per second may be functions
        of nothing, asked as attempts start. running carries the attempts in
        flight from one call to the next. Returns how many attempts ended."""
        for ended in range(20000):
            if until():
                return ended
            for sizer, share, rate in plan:
                wanted = share() if callable(share) else share
                while (
                    sum(
                        1
                        for _ends, _key, permit, _size in running
                        if permit.sizer is sizer
                    )
                    < wanted
                ):
                    admitted = []
                    if not controller.admit(admitted.append):
                        break
                    permit = admitted[0]
                    permit.sizer = sizer
                    permit.begin()
                    seconds = sizer.size / (rate() if callable(rate) else rate)
                    heapq.heappush(
                        running,
                        (
                            self.clock.now + seconds,
                            id(permit),
                            permit,
                            sizer.size,
                        ),
                    )
            ends, _key, permit, size = heapq.heappop(running)
            self.clock.now = ends
            permit.end(200, None, size)
        self.fail("the attempts never brought about what was awaited")

    def test_it_grows_every_grow_every_successes_up_to_the_cap(self):
        controller = self.controller(
            max_concurrency=6,
            initial_concurrency=2,
            grow_every=3,
            throughput_window=0,
        )
        targets = []
        for _ in range(15):
            self.succeed(controller, 1)
            targets.append(controller.target)
        self.assertEqual(
            [2, 2, 3, 3, 3, 4, 4, 4, 5, 5, 5, 6, 6, 6, 6], targets
        )

    def test_a_soft_ceiling_holds_until_bytes_and_throughput_both_unlock_it(
        self,
    ):
        controller = self.controller(
            max_concurrency=10,
            initial_concurrency=2,
            grow_every=1,
            soft_ceiling=4,
            unlock_bytes=50_000,
            unlock_bytes_per_second=1,
            throughput_window=0,
        )
        self.succeed(controller, 10)
        self.assertEqual(4, controller.target)  # Held: not enough bytes yet.
        self.succeed(controller, 60)
        self.assertEqual(
            4, controller.target
        )  # Bytes, but no throughput sample.
        unlocked = self.controller(
            max_concurrency=10,
            initial_concurrency=2,
            grow_every=1,
            soft_ceiling=4,
            unlock_bytes=50_000,
            unlock_bytes_per_second=1,
            throughput_window=4,
            probe_min_gain_percent=0.0,
        )
        self.succeed(unlocked, 80)
        self.assertEqual(10, unlocked.target)

    def test_failures_shrink_it_but_not_below_the_minimum(self):
        controller = self.controller(
            initial_concurrency=8, min_concurrency=3, failure_shrink_percent=50
        )
        controller.record(success=False, seconds=0.1, size=0)
        self.assertEqual(4, controller.target)
        controller.record(success=False, seconds=0.1, size=0)
        self.assertEqual(3, controller.target)

    def test_backpressure_shrinks_it_pauses_new_parts_and_later_successes_recover(
        self,
    ):
        controller = self.controller(
            initial_concurrency=8,
            grow_every=2,
            backpressure_shrink_percent=50,
            throughput_window=0,
        )
        controller.record(
            success=False, seconds=0.1, size=0, status=429, retry_after=2.0
        )
        self.assertEqual(4, controller.target)
        self.assertEqual(2.0, controller.pause_left())
        self.clock.now += 2.5
        self.assertEqual(0.0, controller.pause_left())
        self.succeed(controller, 10)
        self.assertGreater(controller.target, 4)

    def test_growth_without_throughput_gain_is_taken_back(self):
        controller = self.controller(
            initial_concurrency=4,
            grow_every=1,
            throughput_window=4,
            probe_min_gain_percent=10,
            probe_windows=1,
            throughput_shrink_percent=50,
            hold_windows=0,
        )
        # Throughput never improves as concurrency grows: every added part
        # makes each part slower by the same factor.
        for _ in range(40):
            seconds = 0.1 * controller.target
            self.clock.now += seconds / controller.target
            controller.record(success=True, seconds=seconds, size=1000)
        snapshot = controller.snapshot()
        self.assertGreater(snapshot["probe_misses"], 0)
        self.assertGreater(snapshot["shrink"], 0)
        self.assertLess(controller.target, 8)

    def test_static_tuning_never_changes_the_target(self):
        controller = Controller(UploadTuning(adaptive=False).settings("s3", 6))
        self.succeed(controller, 50)
        controller.record(success=False, seconds=0.1, size=0, status=503)
        self.assertEqual(6, controller.target)

    def test_a_capped_automatic_s3_upload_warms_up_to_the_cap_or_starts_at_it(
        self,
    ):
        # max_concurrency bounds the scaled S3 policy without replacing it:
        # Default warms up from one part to the capped start, by about half
        # at each level that earns it, and Aggressive starts there. Neither
        # goes above it, and both go on adapting.
        default = self.scaled(12)
        self.assertEqual((1, True), (default.target, default.warm_start))
        targets = self.rounds(default, 40, 0.1, 64 * KiB)
        self.assertEqual([1, 2, 3, 5, 8, 12], sorted(set(targets)))
        self.assertEqual(12, targets[-1])
        self.assertFalse(default.snapshot()["warming"])
        aggressive = self.scaled(12, UploadStartup.AGGRESSIVE)
        self.assertEqual(
            (12, False), (aggressive.target, aggressive.warm_start)
        )
        self.assertEqual({12}, set(self.rounds(aggressive, 40, 0.1, 64 * KiB)))
        # Without a cap: the policy's start of 150, or one for Default.
        self.assertEqual(
            150, self.scaled(startup=UploadStartup.AGGRESSIVE).target
        )
        self.assertEqual(1, self.scaled().target)

    def test_default_keeps_a_warm_raise_only_when_it_earns_its_gain_and_promotes_on_a_fast_link(
        self,
    ):
        # A one-part baseline of 10 MiB/s. Two parts at once then deliver 16
        # MiB/s, at least the 15 MiB/s a raise from one to two must earn, so
        # the raise is kept and the next one tried; or 14 MiB/s, so the
        # target returns to one and rests.
        for seconds_at_two, kept in ((1.25, True), (20 / 14, False)):
            with self.subTest(kept=kept):
                controller = self.scaled()
                heard = controller.watch()
                self.rounds(
                    controller, 3, 1.0, 10 * MiB
                )  # Warming, then the baseline.
                self.assertEqual(2, controller.target)
                self.rounds(
                    controller, 2, seconds_at_two, 10 * MiB
                )  # Its cohort, then a judged window.
                decisions = [entry[0] for entry in heard]
                if kept:
                    self.assertEqual(
                        (["warm_raise", "warm_settled", "warm_raise"], 3),
                        (decisions, controller.target),
                    )
                else:
                    self.assertEqual(
                        (["warm_raise", "warm_withdraw"], 1),
                        (decisions, controller.target),
                    )
                    self.assertTrue(controller.snapshot()["warming"])
        # A first judged window of exactly 96 MiB/s promotes to the start.
        fast = self.scaled()
        heard = fast.watch()
        self.rounds(fast, 1, 1.0, 96 * MiB)
        self.assertEqual(
            (150, ["warm_fast_link"]),
            (fast.target, [entry[0] for entry in heard]),
        )
        # Not from a window the limiter kept from filling the target, however
        # fast its rate: it is not judged, and says why.
        limited = self.scaled()
        heard = limited.watch()
        limited.note_shortfall("limiter")
        self.clock.now += 0.5
        self.rounds(limited, 1, 1.0, 200 * MiB)
        self.assertEqual(
            (1, [("window_not_measured", "limiter")]),
            (limited.target, [(e[0], e[4]) for e in heard]),
        )

    def test_failures_begun_in_one_epoch_shrink_the_target_once_and_every_throttle_extends_the_cooldown(
        self,
    ):
        controller = self.scaled(startup=UploadStartup.AGGRESSIVE)
        heard = controller.watch()
        permits = []
        for _ in range(3):
            controller.admit(permits.append)
        for permit in permits:
            permit.begin()
        self.clock.now += 0.5
        permits[0].end(503, 2.0, MiB)
        self.assertEqual(
            (135, 2.0), (controller.target, controller.pause_left())
        )
        # Begun before that shrink: no further shrink, but a later deadline
        # extends the cooldown, and an earlier one never shortens it.
        permits[1].end(503, 1.0, MiB)
        permits[2].end(503, 5.0, MiB)
        self.assertEqual(
            (135, 5.0), (controller.target, controller.pause_left())
        )
        self.assertFalse(controller.admit(permits.append))
        self.clock.now += 5
        fresh = []
        self.assertTrue(controller.admit(fresh.append))
        fresh[0].begin()
        fresh[0].end(500, None, MiB)
        # Begun in the new epoch: a 35% shrink.
        self.assertEqual(87, controller.target)
        self.assertEqual(
            [
                "backpressure",
                "stale_backpressure",
                "stale_backpressure",
                "failure",
            ],
            [entry[0] for entry in heard],
        )

    def test_completions_during_a_cooldown_measure_nothing_and_a_window_spanning_it_is_not_judged(
        self,
    ):
        controller = self.scaled(16, UploadStartup.AGGRESSIVE)
        heard = controller.watch()
        running = []
        while controller.admit(running.append):
            pass
        for permit in running:
            permit.begin()
        self.clock.now += 0.1
        controller.record(
            success=False, seconds=0.1, size=0, status=503, retry_after=2.0
        )
        self.assertEqual(14, controller.target)
        heard.clear()
        # The 16 attempts already running are accepted during the cooldown.
        for permit in running:
            permit.end(200, None, MiB)
        self.clock.now += 2.0
        # A window needs 32 answers: none of those 16 counts.
        self.rounds(controller, 2, 0.1, MiB)
        self.assertEqual([], list(heard))
        self.rounds(controller, 1, 0.1, MiB)
        self.assertEqual(
            [("window_not_measured", "cooldown")],
            [(e[0], e[4]) for e in heard],
        )

    def test_a_part_sent_again_waits_for_a_fresh_permit_ahead_of_new_parts(
        self,
    ):
        # Two permits. The first part's attempt fails and gives its permit
        # back, so a new part takes it; sending the first part again then
        # waits for a permit, ahead of any new part, and stops waiting when
        # its operation is cancelled.
        controller = self.controller(
            initial_concurrency=2, max_concurrency=2, failure_shrink_percent=0
        )
        first, second, third = [], [], []
        self.assertTrue(controller.admit(first.append))
        self.assertTrue(controller.admit(second.append))
        first[0].begin()
        first[0].end(500, None, 100)
        self.assertTrue(controller.admit(third.append))
        acquired = threading.Event()

        def send_again():
            first[0].acquire(Lifetime(CancellationToken()))
            acquired.set()

        thread = threading.Thread(target=send_again)
        thread.start()
        self.addCleanup(thread.join, 5)
        self.assertFalse(acquired.wait(0.3))
        second[0].begin()
        second[0].end(200, None, 100)
        self.assertFalse(controller.admit([].append))
        self.assertTrue(acquired.wait(5))
        self.assertTrue(first[0].held)
        third[0].begin()
        third[0].end(500, None, 100)
        fourth = []
        self.assertTrue(controller.admit(fourth.append))
        token = CancellationToken()
        cancelled = []

        def wait_until_cancelled():
            try:
                third[0].acquire(Lifetime(CancellationToken(), token))
            except OperationCancelledError as error:
                cancelled.append(error)

        waiter = threading.Thread(target=wait_until_cancelled)
        waiter.start()
        token.cancel()
        waiter.join(5)
        self.assertEqual((1, False), (len(cancelled), third[0].held))
        fourth[0].release()
        self.assertTrue(controller.admit([].append))

    def test_a_file_keeps_larger_parts_only_for_more_goodput_at_an_unchanged_share(
        self,
    ):
        # At its cap of four parts at once, concurrency holds. A file sends
        # 8 MiB parts four at a time, each attempt at 10 MiB/s: 40 MiB/s.
        # After two windows of its own it tries 16 MiB parts, and another
        # file, which sent nothing yet, cannot probe meanwhile. Four at a
        # time at 12 MiB/s each (48 MiB/s) earns the 10% gain; at 10 MiB/s
        # each it does not, and the size goes back after two windows. When
        # the other file takes three of the four places, the file's 16 MiB
        # parts go one at a time at 12 MiB/s each: each attempt is faster,
        # but the file delivers far less at a quarter of the share, so its
        # baseline no longer applies and the size goes back. And a file at
        # one place, beside a file that cannot take larger parts at the
        # other three, has its baseline at 10 MiB/s; at 16 MiB that file
        # yields it a second place for a quarter of the time, so it delivers
        # 25% more with no attempt faster. Its share was one for most of
        # each window, but more places are no gain: the size goes back.
        def quarter():
            # The first quarter of every 6.4 s.
            return self.clock.now % 6.4 < 1.6

        alone = [("mine", 4, 10 * MiB)]
        cases = (
            ("kept", alone, [("mine", 4, 12 * MiB)], "size_kept", 16 * MiB),
            (
                "not earned",
                alone,
                [("mine", 4, 10 * MiB)],
                "size_returned",
                8 * MiB,
            ),
            (
                "share lost",
                alone,
                [("other", 3, 40 * MiB), ("mine", 1, 12 * MiB)],
                "size_returned",
                8 * MiB,
            ),
            (
                "extra places",
                [("fixed", 3, 40 * MiB), ("mine", 1, 10 * MiB)],
                [
                    ("fixed", lambda: 2 if quarter() else 3, 40 * MiB),
                    ("mine", lambda: 2 if quarter() else 1, 10 * MiB),
                ],
                "size_returned",
                8 * MiB,
            ),
        )
        for name, baseline, probe, decision, size in cases:
            with self.subTest(name):
                controller = self.scaled(4, UploadStartup.AGGRESSIVE)
                heard = controller.watch()
                files = {
                    "mine": _SizeFeedback(controller, 8 * MiB, 64 * MiB),
                    "other": _SizeFeedback(controller, 8 * MiB, 64 * MiB),
                    # A file whose grant allows no larger parts.
                    "fixed": _SizeFeedback(controller, 8 * MiB, 8 * MiB),
                }
                for sizer in files.values():
                    controller.add_sizer(sizer)
                mine, other = files["mine"], files["other"]
                running = []
                plan = [
                    (files[file], share, rate)
                    for file, share, rate in baseline
                ]
                self.traffic(
                    controller,
                    plan,
                    running,
                    lambda mine=mine: mine.probe is not None,
                )
                self.assertEqual((16 * MiB, 8 * MiB), (mine.size, other.size))
                plan = [
                    (files[file], share, rate) for file, share, rate in probe
                ]
                self.traffic(
                    controller,
                    plan,
                    running,
                    lambda mine=mine: mine.probe is None,
                )
                sizes = [
                    entry[0] for entry in heard if entry[0].startswith("size_")
                ]
                self.assertEqual(
                    (["size_probe", decision], size), (sizes[:2], mine.size)
                )
                if decision == "size_returned":
                    self.assertEqual(4, mine.hold)
                self.assertEqual(4, controller.target)

    def test_a_warm_up_s_first_rest_tries_no_part_size_and_a_size_experiment_judges_no_concurrency(
        self,
    ):
        # Default and uncapped, one file, which delivers 10 MiB/s at any
        # concurrency: each warm raise is withdrawn, and a rest of two
        # windows of 32 answers follows. The file's size matures at most
        # once per window the controller judges, so the first rest, whose
        # hold window is its first, tries no larger size; the second rest's
        # hold window does. The larger size earns nothing and goes back
        # after two windows of its own. Its answers judge nothing and the
        # rest waits for it: the next raise comes after two whole windows
        # of answers after it.
        controller = self.scaled()
        heard = controller.watch()
        mine = _SizeFeedback(controller, 8 * MiB, 64 * MiB)
        controller.add_sizer(mine)
        plan = [(mine, 64, lambda: 10 * MiB / controller.target)]
        running = []
        self.traffic(
            controller,
            plan,
            running,
            lambda: heard and heard[-1][0] == "size_returned",
        )
        self.assertEqual(
            [
                "warm_raise",
                "warm_withdraw",
                "warm_raise",
                "warm_withdraw",
                "size_probe",
                "size_returned",
            ],
            [entry[0] for entry in heard],
        )
        answers = self.traffic(
            controller, plan, running, lambda: heard[-1][0] == "warm_raise"
        )
        self.assertGreaterEqual(answers, 64)
        self.assertEqual((8 * MiB, 2), (mine.size, controller.target))

    def test_the_scaled_policy_grows_withdraws_rejected_probes_holds_and_backs_off_from_queueing(
        self,
    ):
        # Aggressive and uncapped, so it starts at 150. Its first window, of
        # 1 GiB parts taking 1 s each, is a fast link (its floor is 150) and
        # carries 150 GiB, which unlocks growth above the soft ceiling.
        controller = self.scaled(startup=UploadStartup.AGGRESSIVE)
        heard = controller.watch()
        GiB = 1024 * MiB

        def window(seconds, size):
            return self.rounds(controller, 1, seconds, size)[0]

        self.assertEqual(154, window(1.0, GiB))
        # Four more parts but less throughput, beyond the 2% tolerated: after
        # two windows the probe is withdrawn by 8%, to 141, but not below the
        # fast link's floor of 150. Then a window of hold.
        self.assertEqual(154, window(1.05, GiB))
        self.assertEqual(150, window(1.05, GiB))
        self.assertEqual(150, window(1.0, GiB))
        # Each raise of four earns its 1% and is kept: 154 to 194.
        targets = [window(1.0, GiB) for _ in range(22)]
        self.assertEqual((154, 194), (targets[0], targets[-1]))
        self.assertEqual(198, window(1.0, GiB))
        window(1.05, GiB)
        self.assertEqual(182, window(1.05, GiB))
        self.assertEqual(182, window(1.0, GiB))
        # 1 MiB parts taking 1 s each: answers take 1024 times as long per
        # byte as the fastest window, so the queue estimate is above 160,
        # and throughput declined: withdraw 8%, then hold at the new level.
        self.assertEqual(167, window(1.0, MiB))
        self.assertEqual(167, window(1.0, MiB))
        # A decline of 0.5% with the queue estimate above 160 withdraws
        # again.
        self.assertEqual(153, window(1.005, MiB))
        decisions = [entry[0] for entry in heard]
        self.assertEqual(["grow", "probe_miss", "probe_revert"], decisions[:3])
        self.assertEqual(["grow", "probe_kept"] * 11, decisions[3:25])
        self.assertEqual(
            [
                "grow",
                "probe_miss",
                "probe_revert",
                "latency_backoff",
                "latency_backoff",
            ],
            decisions[25:],
        )

    def test_windows_whose_permits_wait_on_slow_bodies_are_not_judged_and_clean_ones_grow_again(
        self,
    ):
        # Aggressive and uncapped: a fast first window raises 150 to 154,
        # and the next keeps the raise. Then each attempt's headers arrive
        # after 1 s on the network and its body 1 s later, when its permit
        # goes back: for half of each window the permits fill the target
        # with nothing on the network. Those windows are not judged, say
        # why and grow nothing; once bodies are quick again, the next window
        # grows the target.
        controller = self.scaled(startup=UploadStartup.AGGRESSIVE)
        heard = controller.watch()

        def window(body):
            permits = []
            while controller.admit(permits.append):
                pass
            for permit in permits:
                permit.begin()
            self.clock.now += 1.0
            for permit in permits:
                permit.answered(200, None)
            self.clock.now += body
            for permit in permits:
                permit.end(200, None, 1024 * MiB)
            return controller.target

        self.assertEqual(
            [154, 154, 154, 154, 158],
            [window(body) for body in (0.0, 0.0, 1.0, 1.0, 0.0)],
        )
        held = ("window_not_measured", "held off network")
        self.assertEqual(
            [("grow", None), ("probe_kept", None), held, held, ("grow", None)],
            [(entry[0], entry[4]) for entry in heard],
        )

    def test_a_download_s_local_writes_are_off_the_network_and_out_of_its_durations(
        self,
    ):
        # A download's attempt is on the network until its body has arrived,
        # except while it writes what it received to a local file. A fast
        # first window raises 150 to 154. In the next, each attempt spends
        # 1 s on the network and 1 s writing: that window is not judged and
        # says why, so the raise is neither kept nor rejected for the disk's
        # sake. The window after, without writes, keeps it. Every attempt
        # lasted its 1 s on the network: the writes are not in its duration.
        controller = self.scaled(startup=UploadStartup.AGGRESSIVE)
        heard = controller.watch()

        def window(writing):
            permits = []
            while controller.admit(permits.append):
                pass
            for permit in permits:
                permit.begin()
            self.clock.now += 0.5
            for permit in permits:
                permit.writing(True)
            self.clock.now += writing
            for permit in permits:
                permit.writing(False)
            self.clock.now += 0.5
            for permit in permits:
                permit.answered(206)
                permit.end(206, None, 1024 * MiB)
            return controller.target

        self.assertEqual(
            [154, 154, 154], [window(writing) for writing in (0.0, 1.0, 0.0)]
        )
        self.assertEqual(
            [
                ("grow", None),
                ("window_not_measured", "local destination writes"),
                ("probe_kept", None),
            ],
            [(entry[0], entry[4]) for entry in heard],
        )
        attempts = controller.snapshot()["attempts"]
        self.assertEqual(
            (458, 458.0), (attempts["accepted"], attempts["seconds"])
        )


class TestUploadTuning(unittest.TestCase):
    def test_invalid_settings_are_refused_before_an_upload_starts(self):
        for kwargs in (
            {"initial_concurrency": 0},
            {"grow_every": True},
            {"probe_min_gain_percent": 101},
            {"backpressure_pause": -1},
            {"part_size_tiers": ((10, 5), (5, 6), (None, 7))},
            {"part_size_tiers": ((None, 5), (10, 6))},
            {"adaptive": "yes"},
        ):
            with self.subTest(kwargs=kwargs):
                with self.assertRaises(InvalidParameterError):
                    UploadTuning(**kwargs)

    def test_contradictory_settings_are_refused(self):
        with self.assertRaises(InvalidParameterError):
            UploadTuning(min_concurrency=10).settings("generic", 4)
        with self.assertRaises(InvalidParameterError):
            UploadTuning(
                unknown_initial_part_size=10, unknown_max_part_size=5
            ).settings("generic", 4)

    def test_each_kind_of_storage_has_its_own_defaults(self):
        generic = UploadTuning().settings("generic", 16)
        agent = UploadTuning().settings("agent_fiw", 8)
        self.assertEqual(
            (4, 2), (generic.initial_concurrency, agent.initial_concurrency)
        )
        self.assertEqual(4, agent.soft_ceiling)
        # An automatic upload to S3 uses the scaled S3 policy, with its start,
        # minimum and part sizes; explicit tuning keeps the configurable
        # controller's S3 profile.
        s3 = UploadTuning().settings("s3", 1024)
        self.assertEqual(
            ("scaled_s3", 150, 8),
            (s3.policy, s3.initial_concurrency, s3.min_concurrency),
        )
        self.assertEqual(8 * MiB, s3.preferred_part_size(10 * MiB))
        configured = UploadTuning(grow_every=8).settings("s3", 32)
        self.assertEqual(
            ("configurable", 8),
            (configured.policy, configured.initial_concurrency),
        )
        self.assertEqual(16 * MiB, configured.preferred_part_size(10 * MiB))

    def test_a_startup_choice_is_refused_when_undefined_or_contradicted_but_not_by_a_cap(
        self,
    ):
        for kwargs in (
            {"startup": "aggressive"},
            {"startup": UploadStartup.AGGRESSIVE, "adaptive": False},
            {"startup": UploadStartup.DEFAULT, "initial_concurrency": 4},
            {"startup": UploadStartup.AGGRESSIVE, "backpressure_pause": 1},
        ):
            with self.subTest(kwargs=kwargs):
                with self.assertRaises(InvalidParameterError):
                    UploadTuning(**kwargs)
        # A cap clamps the policy; part sizes are not a contradiction.
        capped = UploadTuning(
            startup=UploadStartup.AGGRESSIVE, min_part_size=MiB
        ).settings("s3", 12)
        self.assertEqual(
            ("scaled_s3", "aggressive", 12, 8),
            (
                capped.policy,
                capped.startup,
                capped.initial_concurrency,
                capped.min_concurrency,
            ),
        )
        # Where the SDK does not choose the scaled policy, it changes nothing.
        generic = UploadTuning(startup=UploadStartup.AGGRESSIVE).settings(
            "generic", 16
        )
        self.assertEqual(
            ("configurable", None, 4),
            (generic.policy, generic.startup, generic.initial_concurrency),
        )


class AdaptiveTestCase(unittest.TestCase):
    def setUp(self):
        scratch = tempfile.TemporaryDirectory()
        self.addCleanup(scratch.cleanup)
        self.scratch = Path(scratch.name)

    def client(self, service, **settings):
        client = files_sdk.Client(
            api_key="key",
            base_url=service.url,
            initial_network_retry_delay=0,
            **settings,
        )
        self.addCleanup(client.close)
        return client

    def local(self, data, name="data.bin"):
        path = self.scratch / name
        path.write_bytes(data)
        return path

    def retry_logged(self):
        """An event set once the SDK logs that it will send a request again:
        by then the failed attempt's outcome has reached the controller, and
        the request waits to be sent again."""
        logged = threading.Event()

        class Retries(logging.Handler):
            def emit(self, record):
                if "Retrying request" in record.getMessage():
                    logged.set()

        handler = Retries(logging.INFO)
        logger = logging.getLogger("files_sdk")
        level = logger.level
        logger.setLevel(logging.INFO)
        logger.addHandler(handler)
        self.addCleanup(logger.setLevel, level)
        self.addCleanup(logger.removeHandler, handler)
        return logged


class TestAdaptiveUploads(AdaptiveTestCase):
    def test_an_adaptive_upload_adds_parts_as_parts_succeed(self):
        service = UploadService(self, part_size=100)
        service.on_put = lambda number: time.sleep(0.01)
        tuning = UploadTuning(
            initial_concurrency=2, grow_every=2, throughput_window=0
        )
        data = random.Random(3).randbytes(6000)

        self.client(service).file.upload_file(
            self.local(data), "a.bin", max_concurrency=6, tuning=tuning
        )

        self.assertEqual(data, service.assembled())
        self.assertGreater(service.max_active, 2)
        self.assertLessEqual(service.max_active, 6)

    def test_the_kind_of_storage_tunes_how_far_an_upload_goes(self):
        # Aggressive startup applies only where the SDK chooses the scaled S3
        # policy: S3 starts at that policy's start, while the agent profile
        # keeps its own start and soft ceiling.
        observed = {}
        tuning = UploadTuning(startup=UploadStartup.AGGRESSIVE)
        for target in ("agent_fiw", "s3"):
            service = UploadService(
                self, part_size=100, grant={"upload_target_class": target}
            )
            service.on_put = lambda number: time.sleep(0.02)
            self.client(service).file.upload_file(
                self.local(bytes(4000), target), "a.bin", tuning=tuning
            )
            observed[target] = service.max_active
        self.assertLessEqual(
            observed["agent_fiw"], 4
        )  # Its soft ceiling, not yet unlocked.
        self.assertGreaterEqual(observed["s3"], 8)

    def test_parts_of_an_ordinary_s3_multipart_upload_show_s3_when_files_com_names_no_kind(
        self,
    ):
        # Files.com names no kind of storage, and every part goes to one
        # ordinary multipart upload straight to Amazon S3, as begin_upload's
        # answer to a request for direct connection information shows it:
        # the upload takes S3's policy, as if named. A kind Files.com names,
        # any direct connection information, a caller who does not let the
        # SDK ask for it, and a URL that signs more than its host keep the
        # generic defaults. The caller's cap and a serial upload stay so.
        def query(
            signed_headers="host", upload_id=lambda number: "multipart-1"
        ):
            return lambda number: (
                "partNumber={}&uploadId={}&X-Amz-Algorithm=AWS4-HMAC-SHA256"
                "&X-Amz-Credential=AKIAEXAMPLE%2F20261012%2Fus-east-1%2Fs3%2Faws4_request"
                "&X-Amz-SignedHeaders={}&X-Amz-Signature=secret".format(
                    number, upload_id(number), signed_headers
                )
            )

        route = {"action": "put/write"}
        generic = ("generic", "configurable")
        cases = (
            (
                "ordinary S3 upload",
                route,
                query(),
                {},
                {},
                ("s3", "scaled_s3"),
            ),
            (
                "named generic",
                {**route, "upload_target_class": "generic"},
                query(),
                {},
                {},
                generic,
            ),
            (
                "direct connection information",
                {**route, "direct_connection_info": {"version": 1}},
                query(),
                {},
                {},
                generic,
            ),
            (
                "not asked for",
                route,
                query(),
                {"with_direct_connection_info": False},
                {},
                generic,
            ),
            (
                "length signed",
                route,
                query("content-length;host"),
                {},
                {},
                generic,
            ),
            (
                "capped and serial",
                {**route, "parallel_parts": False},
                query(),
                {},
                {"max_concurrency": 2},
                ("s3", "scaled_s3"),
            ),
        )
        data = random.Random(5).randbytes(300)
        for label, grant, storage_query, params, options, expected in cases:
            with self.subTest(label):
                service = UploadService(
                    self,
                    part_size=100,
                    grant=grant,
                    storage_query=storage_query,
                )
                service.storage_origin = S3_ORIGIN
                session = service.session()
                self.addCleanup(session.close)
                observed = []
                self.client(service, http_session=session).file.upload_file(
                    self.local(data, label),
                    "a.bin",
                    params=params or None,
                    tuning=UploadTuning(observer=observed.append),
                    **options,
                )
                settings = observed[-1].details["settings"]
                self.assertEqual(data, service.assembled())
                self.assertEqual(
                    expected, (settings["target_class"], settings["policy"])
                )
                self.assertEqual(
                    params.get("with_direct_connection_info", True),
                    service.begins[0]["with_direct_connection_info"],
                )
                if options:
                    self.assertEqual(
                        (2, 1),
                        (settings["max_concurrency"], service.max_active),
                    )
        # begin_upload's first answer can describe several parts, and every
        # one must be of the same S3 upload: a later part of another upload
        # keeps the generic defaults, however ordinary the first part is.
        several = (
            ("several parts of one upload", query(), ("s3", "scaled_s3")),
            (
                "a later part of another upload",
                query(
                    upload_id=lambda number: "multipart-{}".format(
                        min(number, 2)
                    )
                ),
                generic,
            ),
        )
        for label, storage_query, expected in several:
            with self.subTest(label):
                service = UploadService(
                    self,
                    part_size=100,
                    grant=route,
                    storage_query=storage_query,
                )
                service.storage_origin = S3_ORIGIN
                service.initial_parts = 3
                session = service.session()
                self.addCleanup(session.close)
                observed = []
                self.client(service, http_session=session).file.upload_file(
                    self.local(data, label),
                    "a.bin",
                    tuning=UploadTuning(observer=observed.append),
                )
                settings = observed[-1].details["settings"]
                self.assertEqual(data, service.assembled())
                self.assertEqual(
                    expected, (settings["target_class"], settings["policy"])
                )

    def test_throttling_pauses_new_parts_for_the_retry_after_time(self):
        service = UploadService(self, part_size=100)
        service.fail(3, status=429, retry_after=1)
        # Slow enough that most parts are still to go when the 429 is seen.
        service.on_put = lambda number: time.sleep(0.02)
        tuning = UploadTuning(initial_concurrency=4, throughput_window=0)
        data = bytes(2000)

        self.client(service).file.upload_file(
            self.local(data), "a.bin", tuning=tuning
        )

        self.assertEqual(data, service.assembled())
        throttled = [at for at, number in service.put_times if number == 3][0]
        # Parts started before the 429 was seen arrive right after it; no
        # part starts after that until the Retry-After second has passed.
        since = [
            at - throttled
            for at, _number in service.put_times
            if at > throttled
        ]
        self.assertEqual([gap for gap in since if 0.3 < gap < 0.95], [])
        self.assertTrue(any(gap >= 0.95 for gap in since))

    def test_backpressure_while_a_part_is_read_keeps_that_part_from_starting(
        self,
    ):
        # Part 2 is chosen to start while part 1 is in progress, but part 1
        # is answered 503 while part 2's bytes are still being read from the
        # stream. Part 2 must then wait out the Retry-After time instead of
        # starting. With no retries the 503 fails the upload, and part 2's
        # room in the limiter is given back.
        service = UploadService(self, part_size=100)
        service.fail(1, status=503, retry_after=30)
        limiter = files_sdk.TransferLimiter()
        client = self.client(
            service, max_network_retries=0, transfer_limiter=limiter
        )
        part_1_done = threading.Event()
        started = []

        class RecordingExecutor(concurrent.futures.ThreadPoolExecutor):
            # The upload's executor: records each part handed to a worker and
            # says when part 1's worker is done, by then having seen its 503.
            def submit(self, fn, /, *args, **kwargs):
                number = getattr(args[0], "number", None) if args else None
                if number is not None:
                    started.append(number)

                def run():
                    try:
                        return fn(*args, **kwargs)
                    finally:
                        if number == 1:
                            part_1_done.set()

                return super().submit(run)

        class StreamHeldAtPart2(io.BytesIO):
            def read(self, size=-1):
                if self.tell() >= 100:
                    part_1_done.wait(10)
                return super().read(size)

        stream = StreamHeldAtPart2(bytes(300))
        tuning = UploadTuning(adaptive=False)
        with mock.patch.object(
            concurrent.futures, "ThreadPoolExecutor", RecordingExecutor
        ):
            with self.assertRaises(APIError) as caught:
                client.file.upload_stream(
                    stream, "s.bin", 300, max_concurrency=2, tuning=tuning
                )

        self.assertTrue(part_1_done.is_set())
        self.assertEqual(503, caught.exception.http_status)
        self.assertEqual([1], started)
        self.assertEqual(0, limiter.parts_in_use)

    def test_a_part_refused_by_a_smaller_target_starts_once_the_finished_part_is_collected(
        self,
    ):
        # The limiter has one slot. Part 1 is answered 503 with no cooldown
        # and its retry succeeds, but the 503 halves the target to one. Part
        # 2 is read once part 1 has given its slot back, before part 1 is
        # collected, so it is refused and waits ready holding the only slot.
        # The upload must collect part 1 and start part 2, rather than wait
        # for room to read part 3 that only part 2 could free.
        service = UploadService(self, part_size=100)
        service.fail(1, status=503, retry_after=0)
        limiter = files_sdk.TransferLimiter(max_parts=1)
        client = self.client(service, transfer_limiter=limiter)
        part_1_done = threading.Event()
        begins = []
        send = requests.Session.send

        class RecordingExecutor(concurrent.futures.ThreadPoolExecutor):
            # The upload's executor: says when part 1's worker is done with
            # it, having given its limiter slot back.
            def submit(self, fn, /, *args, **kwargs):
                number = getattr(args[0], "number", None) if args else None

                def run():
                    try:
                        return fn(*args, **kwargs)
                    finally:
                        if number == 1:
                            part_1_done.set()

                return super().submit(run)

        def send_once_part_1_is_done(session, request, **kwargs):
            # Holds the request for parts 2 and 3 until part 1 is done, so
            # part 2 gets the slot as soon as it asks.
            if "/file_actions/begin_upload/" in request.url:
                begins.append(request.url)
                if len(begins) > 1:
                    part_1_done.wait(10)
            return send(session, request, **kwargs)

        data = random.Random(5).randbytes(300)
        tuning = UploadTuning(
            initial_concurrency=2,
            min_concurrency=1,
            grow_every=4,
            throughput_window=0,
        )
        options = {"deadline": time.monotonic() + 20}
        with (
            mock.patch.object(
                concurrent.futures, "ThreadPoolExecutor", RecordingExecutor
            ),
            mock.patch.object(
                requests.Session, "send", send_once_part_1_is_done
            ),
        ):
            client.file.upload_stream(
                io.BytesIO(data),
                "s.bin",
                300,
                options,
                max_concurrency=2,
                tuning=tuning,
            )

        self.assertTrue(part_1_done.is_set())
        self.assertGreater(len(begins), 1)
        self.assertEqual(data, service.assembled())
        self.assertEqual([1, 1, 2, 3], sorted(service.puts))
        self.assertEqual(0, limiter.parts_in_use)
        self.assertEqual(0, limiter.bytes_in_use)

    def test_a_part_held_through_a_cooldown_does_not_starve_a_larger_part_of_limiter_bytes(
        self,
    ):
        # Files.com sizes the parts 100, 100, 200 and 300 bytes; the limiter
        # holds three parts but only 450 bytes. Part 1 stays in progress
        # until part 3 arrives. Part 2's 503 starts the default cooldown, and
        # part 2 waits it out, keeping its 100 bytes, to be sent again. Part
        # 3, read once the client has heard that 503, is refused and waits
        # ready holding 200 bytes. Part 4's 300 bytes cannot fit beside
        # parts 1, 2 and 3, nor beside parts 2 and 3. Once the cooldown ends
        # part 2 goes again first and then part 3 starts, rather than the
        # upload waiting for room for part 4 that only starting part 3 could
        # make.
        sizes = {1: 100, 2: 100, 3: 200, 4: 300}
        service = UploadService(
            self, part_size=lambda number: sizes.get(number, 300)
        )
        service.fail(2, status=503)
        service.hold(1)
        service.on_put = lambda number: (
            service.release(1) if number == 3 else None
        )
        limiter = files_sdk.TransferLimiter(max_parts=3, max_bytes=450)
        client = self.client(service, transfer_limiter=limiter)
        part_2_failed = self.retry_logged()

        class StreamHeldAtPart3(io.BytesIO):
            def read(self, size=-1):
                if self.tell() >= 200:
                    part_2_failed.wait(10)
                return super().read(size)

        data = random.Random(7).randbytes(700)
        tuning = UploadTuning(adaptive=False, backpressure_pause=1)
        options = {"deadline": time.monotonic() + 20}
        client.file.upload_stream(
            StreamHeldAtPart3(data),
            "s.bin",
            700,
            options,
            max_concurrency=3,
            tuning=tuning,
        )

        self.assertTrue(part_2_failed.is_set())
        self.assertEqual(data, service.assembled())
        self.assertEqual([1, 2, 2, 3, 4], sorted(service.puts))
        # Part 2 was sent again, and part 3 first sent, only after the cooldown.
        arrivals = [(number, at) for at, number in service.put_times]
        failed_at = [at for number, at in arrivals if number == 2][0]
        later = [
            at - failed_at for number, at in arrivals if number in (2, 3)
        ][1:]
        self.assertTrue(all(gap > 0.5 for gap in later), later)
        self.assertEqual(0, limiter.parts_in_use)
        self.assertEqual(0, limiter.bytes_in_use)

    def test_a_file_part_holds_only_its_copy_buffer_while_a_stream_part_holds_its_bytes(
        self,
    ):
        # A local file's part is read from the file as it is sent, so it
        # holds its copy buffer (64 KiB) in the limiter; sent again, it reads
        # the same bytes again. A stream's part holds its bytes until storage
        # has answered.
        size = 200 * KiB
        data = random.Random(4).randbytes(3 * size)
        service = UploadService(self, part_size=size)
        service.fail(2, status=500)
        limiter = files_sdk.TransferLimiter(max_parts=8, max_bytes=4 * MiB)
        held = []
        service.on_put = lambda number: held.append(limiter.bytes_in_use)
        client = self.client(service, transfer_limiter=limiter)
        tuning = UploadTuning(adaptive=False)

        client.file.upload_file(
            self.local(data), "f.bin", max_concurrency=3, tuning=tuning
        )

        self.assertEqual(data, service.assembled())
        self.assertEqual([data[size : 2 * size]] * 2, service.attempts(2))
        self.assertLessEqual(max(held), 3 * 64 * KiB)
        self.assertEqual((0, 0), (limiter.parts_in_use, limiter.bytes_in_use))
        held.clear()

        client.file.upload_stream(
            io.BytesIO(data),
            "s.bin",
            len(data),
            max_concurrency=3,
            tuning=tuning,
        )

        self.assertGreaterEqual(max(held), size)
        self.assertEqual((0, 0), (limiter.parts_in_use, limiter.bytes_in_use))

    def test_a_stream_is_read_ahead_within_its_runway_while_every_worker_is_busy(
        self,
    ):
        # Two parts are in progress; the runway holds as many more as both
        # of its limits allow.
        for ready_parts, ready_bytes, expected in (
            (3, 250, 400),
            (1, 10_000, 300),
        ):
            with self.subTest(
                ready_parts=ready_parts, ready_bytes=ready_bytes
            ):
                service = UploadService(self, part_size=100)
                held = [service.hold(1), service.hold(2)]
                stream = io.BytesIO(bytes(1000))
                tuning = UploadTuning(
                    adaptive=False,
                    ready_parts=ready_parts,
                    ready_bytes=ready_bytes,
                )
                done = threading.Event()

                def run():
                    try:
                        self.client(service).file.upload_stream(
                            stream,
                            "s.bin",
                            1000,
                            max_concurrency=2,
                            tuning=tuning,
                        )
                    finally:
                        done.set()

                threading.Thread(target=run).start()
                for arrived in held:
                    arrived.wait(5)
                time.sleep(0.2)
                read_while_held = stream.tell()
                service.release(1)
                service.release(2)
                done.wait(10)

                self.assertEqual(expected, read_while_held)
                self.assertEqual(bytes(1000), service.assembled())


class TestVariablePartSizes(AdaptiveTestCase):
    LIMITS = {
        "min_nonfinal_bytes": 1 * KiB,
        "max_part_bytes": 8 * KiB,
        "max_parts": 100,
        "max_file_bytes": 1024 * KiB,
    }

    def tuning(self, **settings):
        return UploadTuning(
            adaptive=False,
            part_size_tiers=((None, 4 * KiB),),
            min_part_size=1 * KiB,
            workload_parts_per_worker=1,
            **settings,
        )

    def test_with_a_variable_grant_the_upload_chooses_its_part_sizes(self):
        service = UploadService(
            self, part_size=999, grant={"variable_part_limits": self.LIMITS}
        )
        data = random.Random(4).randbytes(10 * KiB + 5)

        self.client(service).file.upload_file(
            self.local(data), "v.bin", max_concurrency=2, tuning=self.tuning()
        )

        self.assertEqual(data, service.assembled())
        self.assertEqual(
            [4 * KiB, 4 * KiB, 2 * KiB + 5],
            [len(service.part(n)) for n in (1, 2, 3)],
        )

    def test_part_sizes_leave_room_for_the_rest_of_the_file_within_max_parts(
        self,
    ):
        # Three parts: whether the variable limits allow three, or allow 100
        # but Files.com makes only three part numbers available. No grant is
        # asked for beyond them.
        for limits, grant in (
            ({**self.LIMITS, "max_parts": 3}, {}),
            (self.LIMITS, {"available_parts": 3}),
        ):
            with self.subTest(grant=grant):
                service = UploadService(
                    self,
                    part_size=999,
                    grant={"variable_part_limits": limits, **grant},
                )
                data = random.Random(8).randbytes(20 * KiB)

                self.client(service).file.upload_file(
                    self.local(data), "v.bin", tuning=self.tuning()
                )

                lengths = [
                    len(service.part(n)) for n in sorted(service.stored)
                ]
                self.assertEqual(3, len(lengths))
                self.assertEqual(data, service.assembled())
                self.assertTrue(all(length <= 8 * KiB for length in lengths))
                asked = [
                    begin.get("part", 1) + begin.get("parts", 1) - 1
                    for begin in service.begins
                ]
                self.assertLessEqual(max(asked), 3)
        # Two part numbers fit neither 8 KiB parts of its own nor Files.com's
        # 999-byte parts: refused before anything is sent.
        service = UploadService(
            self,
            part_size=999,
            grant={"variable_part_limits": self.LIMITS, "available_parts": 2},
        )
        with self.assertRaises(InvalidRequestError):
            self.client(service).file.upload_file(
                self.local(bytes(20 * KiB)), "v.bin", tuning=self.tuning()
            )
        self.assertEqual([], service.puts)

    def test_a_partial_or_unfitting_grant_leaves_sizes_to_files_com(self):
        partial = {
            name: value
            for name, value in self.LIMITS.items()
            if name != "max_parts"
        }
        too_small = {**self.LIMITS, "max_file_bytes": 1 * KiB}
        for limits in (partial, too_small):
            with self.subTest(limits=limits):
                service = UploadService(
                    self,
                    part_size=3 * KiB,
                    grant={"variable_part_limits": limits},
                )
                self.client(service).file.upload_file(
                    self.local(bytes(7 * KiB)), "v.bin", tuning=self.tuning()
                )
                self.assertEqual(
                    [3 * KiB, 3 * KiB, 1 * KiB],
                    [len(service.part(n)) for n in (1, 2, 3)],
                )

    def test_a_later_grant_that_narrows_the_limits_stops_before_sending_more(
        self,
    ):
        service = UploadService(
            self,
            part_size=999,
            grant={
                "variable_part_limits": self.LIMITS,
                "parallel_parts": False,
            },
        )
        original = service.describe

        def describe(ref, number):
            record = original(ref, number)
            if number >= 2:
                record["variable_part_limits"] = {
                    **self.LIMITS,
                    "max_part_bytes": 2 * KiB,
                }
            return record

        service.describe = describe
        with self.assertRaises(APIConnectionError) as caught:
            self.client(service).file.upload_file(
                self.local(bytes(10 * KiB)), "v.bin", tuning=self.tuning()
            )
        self.assertIn("narrowed", str(caught.exception))
        self.assertEqual([1], service.puts)
        self.assertEqual([], service.finishes)


class TestUnknownSizes(AdaptiveTestCase):
    def test_a_stream_of_unknown_size_goes_one_part_at_a_time(self):
        service = UploadService(self, part_size=4)
        data = b"abcdefghijklm"

        file = self.client(service).file.upload_stream(
            io.BytesIO(data), "u.txt"
        )

        self.assertEqual("u.txt", file.path)
        self.assertEqual(data, service.assembled())
        self.assertEqual(1, service.max_active)
        self.assertNotIn("size", service.begins[0])
        self.assertEqual(len(data), service.finishes[0]["size"])

    def test_a_spooled_stream_uploads_as_a_file_of_known_size_and_leaves_no_file(
        self,
    ):
        service = UploadService(self, part_size=100)
        service.on_put = lambda number: time.sleep(0.01)
        spool = self.scratch / "spool"
        spool.mkdir()
        data = random.Random(5).randbytes(1500)

        self.client(service).file.upload_stream(
            io.BytesIO(data), "s.bin", spool_limit=2000, spool_directory=spool
        )

        self.assertEqual(data, service.assembled())
        self.assertEqual(1500, service.begins[0]["size"])
        self.assertGreater(service.max_active, 1)
        self.assertNotIn("provided_mtime", service.finishes[0])
        self.assertEqual([], os.listdir(spool))

    def test_a_stream_longer_than_its_spool_limit_sends_nothing(self):
        service = UploadService(self)
        spool = self.scratch / "spool"
        spool.mkdir()
        with self.assertRaises(InvalidRequestError) as caught:
            self.client(service).file.upload_stream(
                io.BytesIO(bytes(101)),
                "s.bin",
                spool_limit=100,
                spool_directory=spool,
            )
        self.assertIn("spool_limit of 100 bytes", str(caught.exception))
        self.assertEqual(([], []), (service.begins, os.listdir(spool)))

    def test_unknown_sizes_can_grow_their_parts_when_granted(self):
        limits = {
            "min_nonfinal_bytes": 2,
            "max_part_bytes": 16,
            "max_parts": 100,
            "max_file_bytes": 1000,
        }
        service = UploadService(
            self,
            part_size=999,
            grant={"variable_part_limits": limits, "parallel_parts": False},
        )
        tuning = UploadTuning(
            unknown_initial_part_size=2,
            unknown_max_part_size=8,
            unknown_grow_every=2,
        )
        data = bytes(range(40))

        self.client(service).file.upload_stream(
            io.BytesIO(data), "g.bin", tuning=tuning
        )

        self.assertEqual(data, service.assembled())
        self.assertEqual(
            [2, 2, 4, 4, 8, 8, 8, 4],
            [len(service.part(n)) for n in sorted(service.stored)],
        )

    def test_an_unknown_size_longer_than_the_grant_allows_is_not_completed(
        self,
    ):
        limits = {
            "min_nonfinal_bytes": 2,
            "max_part_bytes": 4,
            "max_parts": 3,
            "max_file_bytes": 1000,
        }
        service = UploadService(
            self,
            part_size=999,
            grant={"variable_part_limits": limits, "parallel_parts": False},
        )
        tuning = UploadTuning(
            unknown_initial_part_size=4, unknown_max_part_size=4
        )
        with self.assertRaises(InvalidRequestError):
            self.client(service).file.upload_stream(
                io.BytesIO(bytes(13)), "g.bin", tuning=tuning
            )
        self.assertEqual([], service.finishes)

    # The smallest lawful grant: one part of at most 4 bytes.
    ONE_PART = {
        "min_nonfinal_bytes": 1,
        "max_part_bytes": 4,
        "max_parts": 1,
        "max_file_bytes": 4,
    }

    def test_an_unknown_size_up_to_exactly_the_grant_s_limit_completes(self):
        for size in (3, 4):
            for expired in (False, True):
                with self.subTest(size=size, renewed=expired):
                    service = UploadService(
                        self,
                        part_size=999,
                        grant={
                            "variable_part_limits": self.ONE_PART,
                            "parallel_parts": False,
                        },
                    )
                    if expired:
                        service.expire_first()
                    data = bytes(range(size))
                    self.client(service).file.upload_stream(
                        io.BytesIO(data), "g.bin"
                    )
                    self.assertEqual(data, service.assembled())
                    self.assertEqual(size, service.finishes[0]["size"])
                    # Only the part it sent was asked for.
                    self.assertEqual(
                        [1] * (2 if expired else 1),
                        [b.get("part", 1) for b in service.begins],
                    )

    def test_one_byte_more_than_the_grant_allows_fails_without_asking_for_more(
        self,
    ):
        service = UploadService(
            self,
            part_size=999,
            grant={
                "variable_part_limits": self.ONE_PART,
                "parallel_parts": False,
            },
        )
        with self.assertRaisesRegex(
            InvalidRequestError, "longer than Files.com allows"
        ):
            self.client(service).file.upload_stream(
                io.BytesIO(bytes(5)), "g.bin"
            )
        self.assertEqual([], service.finishes)
        self.assertEqual([1], [b.get("part", 1) for b in service.begins])

    def test_an_unknown_size_filling_its_last_part_slot_completes_without_another_grant(
        self,
    ):
        for size, completes in ((8, True), (9, False)):
            with self.subTest(size=size):
                service = UploadService(
                    self,
                    part_size=4,
                    grant={"available_parts": 2, "parallel_parts": False},
                )
                data = bytes(range(size))
                if completes:
                    self.client(service).file.upload_stream(
                        io.BytesIO(data), "s.bin"
                    )
                    self.assertEqual(data, service.assembled())
                else:
                    with self.assertRaisesRegex(
                        InvalidRequestError, "longer than Files.com allows"
                    ):
                        self.client(service).file.upload_stream(
                            io.BytesIO(data), "s.bin"
                        )
                    self.assertEqual([], service.finishes)
                self.assertEqual(
                    [1, 2], [b.get("part", 1) for b in service.begins]
                )

    def test_a_stream_ending_with_a_full_part_asks_for_no_part_it_does_not_send(
        self,
    ):
        for route in ("stream", "chunks"):
            with self.subTest(route):
                service = UploadService(
                    self, part_size=4, grant={"parallel_parts": False}
                )
                files = self.client(service).file
                if route == "stream":
                    files.upload_stream(io.BytesIO(b"abcdefgh"), "s.bin")
                    self.assertEqual(b"abcdefgh", service.assembled())
                else:
                    _part, etags, sent = files.upload_chunks(
                        io.BytesIO(b"abcdefgh"), "s.bin"
                    )
                    self.assertEqual((2, 8), (len(etags), sent))
                self.assertEqual(
                    [1, 2], [b.get("part", 1) for b in service.begins]
                )


class TestUploadObservation(AdaptiveTestCase):
    def test_an_observer_hears_the_plan_decisions_waits_samples_and_a_record(
        self,
    ):
        service = UploadService(self, part_size=100)
        service.fail(3, status=503, retry_after=0.1)
        service.on_put = lambda number: time.sleep(0.02)
        observed = []
        # Fewer places than parts wanted, so parts wait for room.
        limiter = files_sdk.TransferLimiter(max_parts=2)
        data = random.Random(3).randbytes(3000)
        threads = set()
        tuning = UploadTuning(
            observer=lambda o: (
                threads.add(threading.get_ident()),
                observed.append(o),
            ),
            initial_concurrency=2,
            grow_every=1,
        )

        self.client(service, transfer_limiter=limiter).file.upload_file(
            self.local(data, name="private-name.bin"),
            "secret/dest.bin",
            max_concurrency=4,
            tuning=tuning,
        )

        self.assertEqual(data, service.assembled())
        self.assertEqual(threads, {threading.get_ident()})
        kinds = [o.kind for o in observed]
        self.assertEqual((kinds[0], kinds[-1]), ("start", "finish"))
        self.assertEqual(observed[0].details["plan"], "server")
        self.assertTrue(observed[0].details["parallel"])
        decisions = [o for o in observed if o.kind == "decision"]
        [backpressure] = [o for o in decisions if o.decision == "backpressure"]
        self.assertGreater(backpressure.cooldown, 0)
        self.assertIn("grow", {o.decision for o in decisions})
        self.assertIn(
            "limiter", {o.wait for o in observed if o.kind == "wait"}
        )
        samples = [o for o in observed if o.kind == "sample"]
        self.assertTrue(samples)
        if sys.platform != "win32":
            self.assertGreater(samples[0].resources["max_rss_bytes"], 0)
        record = observed[-1].details
        self.assertEqual(record["outcome"], "completed")
        self.assertEqual(
            (record["parts"], record["bytes_committed"]), (30, 3000)
        )
        self.assertGreaterEqual(record["decisions"]["backpressure"], 1)
        self.assertGreater(record["waits"]["limiter"], 0)
        self.assertIn(max(o.parts_in_progress for o in observed), range(1, 5))
        # Numbers and names only: no path, URL or credential.
        text = repr(observed)
        for private in ("private-name", "secret", "dest.bin", "X-Amz"):
            self.assertNotIn(private, text)

    def test_a_failed_upload_s_record_says_so_and_a_failing_observer_stops_the_upload(
        self,
    ):
        service = UploadService(self, part_size=100)
        service.fail(2, status=500, times=99)
        observed = []
        with self.assertRaises(files_sdk.error.APIError):
            self.client(service, max_network_retries=0).file.upload_file(
                self.local(bytes(500)),
                "f.bin",
                tuning=UploadTuning(observer=observed.append),
            )
        self.assertEqual(observed[-1].details["outcome"], "failed")

        def refuse(observation):
            if observation.kind == "decision":
                raise KeyError("stop")

        service = UploadService(self, part_size=100)
        service.fail(2, status=503)
        with self.assertRaises(KeyError):
            self.client(service).file.upload_file(
                self.local(bytes(500)),
                "g.bin",
                tuning=UploadTuning(observer=refuse),
            )
        self.assertEqual(service.finishes, [])

    def test_an_observer_failing_at_the_end_does_not_change_a_completed_upload(
        self,
    ):
        service = UploadService(self, part_size=100)

        def fail_at_finish(observation):
            if observation.kind == "finish":
                raise KeyError("late")

        with self.assertLogs("files_sdk", "WARNING") as logs:
            file = self.client(service).file.upload_file(
                self.local(bytes(500)),
                "f.bin",
                tuning=UploadTuning(observer=fail_at_finish),
            )
        self.assertEqual(file.path, "f.bin")
        self.assertIn("Upload observer failed", "\n".join(logs.output))

    def test_an_observer_and_a_log_handler_failing_at_the_end_leave_the_upload_s_own_outcome(
        self,
    ):
        refused = []

        class Refuse(logging.Filter):
            def filter(self, record):
                if "Upload observer failed" not in record.getMessage():
                    return True
                refused.append(record.getMessage())
                raise RuntimeError("the log handler's own failure")

        def fail_at_finish(observation):
            if observation.kind == "finish":
                raise KeyError("late")

        logger = logging.getLogger("files_sdk")
        level = logger.level
        logger.setLevel(logging.WARNING)
        logger.addFilter(Refuse())
        self.addCleanup(logger.setLevel, level)
        self.addCleanup(logger.removeFilter, logger.filters[-1])
        tuning = UploadTuning(observer=fail_at_finish)

        service = UploadService(self, part_size=100)
        file = self.client(service).file.upload_file(
            self.local(bytes(500)), "f.bin", tuning=tuning
        )
        self.assertEqual(file.path, "f.bin")

        service = UploadService(self, part_size=100)
        service.fail(2, status=500, times=99)
        with self.assertRaises(files_sdk.error.APIError) as caught:
            self.client(service, max_network_retries=0).file.upload_file(
                self.local(bytes(500)), "g.bin", tuning=tuning
            )
        self.assertEqual(caught.exception.http_status, 500)
        # Both warnings reached the failing handler.
        self.assertEqual(2, len(refused))

    def test_an_unknown_size_upload_is_observed_as_serial(self):
        service = UploadService(self, part_size=4)
        observed = []
        self.client(service).file.upload_stream(
            io.BytesIO(b"abcdefghij"),
            "u.bin",
            tuning=UploadTuning(observer=observed.append),
        )
        kinds = [o.kind for o in observed]
        self.assertEqual(
            (kinds[0], kinds[-1], set(kinds[1:-1]) <= {"sample"}),
            ("start", "finish", True),
        )
        self.assertEqual(observed[0].details["plan"], "serial (unknown size)")
        self.assertEqual(
            (observed[-1].details["outcome"], observed[-1].details["parts"]),
            ("completed", 3),
        )

    def test_an_unknown_size_upload_reports_its_wait_and_the_part_it_is_sending(
        self,
    ):
        # Another upload holds the only place in the limiter while this one
        # starts; each part then takes a while to send.
        service = UploadService(self, part_size=4)
        holding = threading.Event()
        service.on_put = lambda number: (holding.set(), time.sleep(0.3))
        limiter = files_sdk.TransferLimiter(max_parts=1)
        client = self.client(service, transfer_limiter=limiter)
        holder = threading.Thread(
            target=lambda: client.file.upload_stream(
                io.BytesIO(b"abcd"), "holder", size=4, max_concurrency=1
            )
        )
        holder.start()
        self.addCleanup(holder.join)
        self.assertTrue(holding.wait(5))
        observed = []
        client.file.upload_stream(
            io.BytesIO(b"abcdefgh"),
            "observed",
            tuning=UploadTuning(observer=observed.append),
        )
        holder.join(10)

        self.assertEqual(b"abcdefgh", service.completed("observed"))
        [wait] = [o for o in observed if o.kind == "wait"]
        self.assertEqual("limiter", wait.wait)
        self.assertGreater(wait.waited, 0.1)
        sending = [
            o
            for o in observed
            if o.kind == "sample" and o.parts_in_progress == 1
        ]
        self.assertTrue(sending)
        # No runway, controller or throughput sample: None, not zero.
        self.assertEqual(
            {(o.runway_parts, o.runway_bytes) for o in observed},
            {(None, None)},
        )
        record = observed[-1].details
        self.assertEqual(1, record["peak_parts_in_progress"])
        self.assertGreater(record["waits"]["limiter"], 0.1)
        self.assertEqual(
            (None, None),
            (record["waits"]["runway"], record["waits"]["backpressure"]),
        )
        self.assertEqual(
            (None, None),
            (record["decisions"], record["best_bytes_per_second"]),
        )
        self.assertEqual({"granted_part_size": 4}, record["settings"])
        self.assertEqual(files_sdk.version, record["runtime"]["sdk_version"])

    def test_an_observer_that_raises_on_a_limiter_wait_gives_the_place_back(
        self,
    ):
        # Another upload holds the only place in the shared limiter, so the
        # observed upload waits for it; its observer raises on hearing of
        # the wait, after the place was granted. Unknown and known sizes,
        # and the same without raising.
        for size, raising in (
            (None, True),
            (8, True),
            (None, False),
            (8, False),
        ):
            with self.subTest(size=size, raising=raising):
                service = UploadService(self, part_size=4)
                holding, release = threading.Event(), threading.Event()

                def hold(_number, holding=holding, release=release):
                    if not holding.is_set():
                        holding.set()
                        release.wait(5)

                service.on_put = hold
                limiter = files_sdk.TransferLimiter(max_parts=1)
                client = self.client(service, transfer_limiter=limiter)
                holder = threading.Thread(
                    target=lambda client=client: client.file.upload_stream(
                        io.BytesIO(b"abcd"),
                        "holder",
                        size=4,
                        max_concurrency=1,
                    )
                )
                holder.start()
                self.addCleanup(holder.join)
                self.assertTrue(holding.wait(5))
                timer = threading.Timer(0.3, release.set)
                timer.start()
                self.addCleanup(timer.cancel)
                mine = RuntimeError("the observer's own failure")

                def observer(observation, raising=raising, mine=mine):
                    if (
                        raising
                        and observation.kind == "wait"
                        and observation.wait == "limiter"
                    ):
                        raise mine

                source = io.BytesIO(b"abcdefgh")
                try:
                    client.file.upload_stream(
                        source,
                        "observed",
                        size,
                        tuning=UploadTuning(observer=observer),
                    )
                except RuntimeError as error:
                    self.assertIs(mine, error)
                    self.assertTrue(raising)
                    self.assertNotIn("observed", service.completed_paths())
                else:
                    self.assertFalse(raising)
                    self.assertEqual(
                        b"abcdefgh", service.completed("observed")
                    )
                holder.join(10)
                self.assertEqual(
                    (0, 0), (limiter.parts_in_use, limiter.bytes_in_use)
                )
                self.assertFalse(source.closed)
                client.file.upload_stream(
                    io.BytesIO(b"next"), "next", options={"request_timeout": 5}
                )
                self.assertEqual(b"next", service.completed("next"))

    def test_a_record_names_the_settings_and_runtime_it_came_from(self):
        service = UploadService(self, part_size=100)
        observed = []
        tuning = UploadTuning(observer=observed.append, initial_concurrency=3)
        self.client(service).file.upload_file(
            self.local(bytes(500)), "f.bin", tuning=tuning
        )
        record = observed[-1].details
        self.assertEqual(3, record["settings"]["initial_concurrency"])
        self.assertEqual("generic", record["settings"]["target_class"])
        self.assertEqual(sys.platform, record["runtime"]["platform"])
        # A file is not read ahead, so it has no runway to wait for.
        self.assertIsNone(record["waits"]["runway"])
        self.assertEqual({None}, {o.runway_parts for o in observed})

    def test_an_observer_given_by_position_still_observes_the_upload(self):
        # UploadTuning's fields before observer keep their places: a caller
        # passing all of them and then the observer still has its observer.
        service = UploadService(self, part_size=100)
        observed = []
        tuning = UploadTuning(True, *[None] * 29, observed.append)
        self.client(service).file.upload_file(
            self.local(bytes(300)), "f.bin", tuning=tuning
        )
        self.assertEqual(
            ("start", "finish"), (observed[0].kind, observed[-1].kind)
        )
        self.assertEqual("completed", observed[-1].details["outcome"])

    def test_an_attempt_lasts_from_its_send_to_its_response_headers(self):
        # Each request is logged slowly (0.3 s) before it is sent, and
        # storage keeps each part's answer body 0.4 s after its headers:
        # neither is network time, so neither is in the attempts' seconds or
        # in the attempts in flight. Part 2's first answer loses its body
        # after its headers: it fails, is sent again, and its bytes and ETag
        # count once. Or part 1's first answer is a 503 or a 504 asking for a
        # second, and loses its body. The upload has no pause of its own, so
        # only that Retry-After can hold parts back: the client takes it in
        # with the headers, once, and part 1's retry and the new parts 3 and
        # 4 are sent only once that second, counted from then, is over.
        # Without retries, the lost body is the upload's error, and the
        # upload stops without completing.

        class SlowRequestLog(logging.Handler):
            def emit(self, record):
                if record.getMessage().startswith("message=Request "):
                    time.sleep(0.3)

        handler = SlowRequestLog(logging.INFO)
        logger = logging.getLogger("files_sdk")
        level = logger.level
        logger.setLevel(logging.INFO)
        logger.addHandler(handler)
        self.addCleanup(logger.setLevel, level)
        self.addCleanup(logger.removeHandler, handler)
        # The client taking in a throttle's headers, witnessed at the real
        # controller and passed through: the time just before it does, the
        # status and Retry-After it takes in, and each subtest's event, set
        # once the cooldown is in place.
        answered = Controller._answered
        throttles = []
        taken_in = []

        def witness(controller, permit, status=None, retry_after=None):
            before = time.monotonic()
            answered(controller, permit, status, retry_after)
            if status in (503, 504):
                throttles.append((before, status, retry_after))
                taken_in[-1].set()

        patcher = mock.patch.object(Controller, "_answered", witness)
        patcher.start()
        self.addCleanup(patcher.stop)
        for name, lost, answer, retries in (
            ("lost body", 2, {}, 3),
            ("503's lost body", 1, {"status": 503, "retry_after": 1}, 3),
            (
                "503's lost body without retries",
                1,
                {"status": 503, "retry_after": 1},
                0,
            ),
            ("504's lost body", 1, {"status": 504, "retry_after": 1}, 3),
            (
                "504's lost body without retries",
                1,
                {"status": 504, "retry_after": 1},
                0,
            ),
        ):
            with self.subTest(name):
                service = UploadService(self, part_size=100)
                service.slow_body = 0.4
                service.drop_body(lost, **answer)
                throttles.clear()
                taken_in.append(threading.Event())
                if answer:
                    # Storage answers part 2, which may already hold a
                    # place, only once the client has taken in part 1's
                    # throttle, so no place frees for a new part before.
                    service.on_put = lambda number, event=taken_in[
                        -1
                    ]: number != 2 or event.wait(5)
                observed = []
                data = random.Random(6).randbytes(400)
                limiter = files_sdk.TransferLimiter()
                tuning = UploadTuning(
                    adaptive=False,
                    backpressure_pause=0,
                    observer=observed.append,
                )
                client = self.client(
                    service,
                    transfer_limiter=limiter,
                    max_network_retries=retries,
                )

                if retries:
                    client.file.upload_file(
                        self.local(data),
                        "f.bin",
                        max_concurrency=2,
                        tuning=tuning,
                    )
                else:
                    with self.assertRaises(APIConnectionError):
                        client.file.upload_file(
                            self.local(data),
                            "f.bin",
                            max_concurrency=2,
                            tuning=tuning,
                        )
                    self.assertEqual([], service.finishes)
                    self.assertEqual("failed", observed[-1].details["outcome"])
                self.assertEqual(0, observed[-1].attempts_in_progress)
                self.assertEqual(
                    (0, 0), (limiter.parts_in_use, limiter.bytes_in_use)
                )
                decisions = [o for o in observed if o.kind == "decision"]
                if answer:
                    # Taken in once, with the second its headers asked for,
                    # and decided on once, with that cooldown ahead.
                    self.assertEqual(
                        [(answer["status"], 1.0)],
                        [
                            (status, hint)
                            for _before, status, hint in throttles
                        ],
                    )
                    self.assertEqual(
                        ["backpressure"], [o.decision for o in decisions]
                    )
                    self.assertTrue(
                        0 < decisions[0].cooldown <= 1.0, decisions[0].cooldown
                    )
                    # Every attempt sent after part 1's first one, apart from
                    # part 2's (perhaps admitted before), was sent once the
                    # second from the client taking in the throttle was over.
                    deadline = throttles[0][0] + 1.0
                    first, later = set(), []
                    for at, number in service.put_times:
                        if number in (1, 2) and number not in first:
                            first.add(number)
                        else:
                            later.append((at, number))
                    self.assertTrue(
                        all(at >= deadline for at, _number in later),
                        (deadline, later),
                    )
                    if retries:
                        self.assertEqual(
                            [1, 3, 4], sorted(number for _at, number in later)
                        )
                else:
                    self.assertEqual(([], []), (throttles, decisions))
                if not retries:
                    continue

                self.assertEqual(data, service.assembled())
                self.assertEqual(
                    sorted([1, 2, 3, 4, lost]), sorted(service.puts)
                )
                # One completion, with each part's ETag once.
                self.assertEqual(
                    [[1, 2, 3, 4]],
                    [
                        [tag["part"] for tag in finish["etags"]]
                        for finish in service.finishes
                    ],
                )
                record = observed[-1].details
                attempts = record["attempts"]
                self.assertEqual(
                    (4, 1, 0),
                    (
                        attempts["accepted"],
                        attempts["failed"],
                        attempts["abandoned"],
                    ),
                )
                # Five attempts each spent 0.7 s logging or reading a body.
                self.assertLess(attempts["seconds"], 0.5)
                self.assertLess(attempts["network_seconds"], 0.5)
                self.assertEqual(
                    (4, 400), (record["parts"], record["bytes_committed"])
                )

    def test_a_file_part_held_through_a_cooldown_reports_no_runway_wait(self):
        # Part 1 is answered 503 without Retry-After: the default cooldown
        # starts and the target halves, and part 1 waits out the cooldown to
        # be sent again with a fresh permit. The grants for parts 2 to 4 come
        # only once the client has heard that 503, so part 2 is refused as it
        # starts and waits ready through the cooldown, while parts are still
        # to be placed. That part is not read ahead: the upload has no runway
        # and must report no wait for one.
        service = UploadService(self, part_size=100)
        service.fail(1, status=503)
        limiter = files_sdk.TransferLimiter()
        client = self.client(service, transfer_limiter=limiter)
        part_1_failed = self.retry_logged()
        begins = []
        send = requests.Session.send

        def send_once_part_1_failed(session, request, **kwargs):
            # Holds the request for parts 2 to 4 until the client has heard
            # part 1's 503, which started the cooldown.
            if "/file_actions/begin_upload/" in request.url:
                begins.append(request.url)
                if len(begins) > 1:
                    part_1_failed.wait(10)
            return send(session, request, **kwargs)

        observed = []
        data = random.Random(11).randbytes(400)
        tuning = UploadTuning(observer=observed.append)
        with mock.patch.object(
            requests.Session, "send", send_once_part_1_failed
        ):
            client.file.upload_file(
                self.local(data), "f.bin", max_concurrency=2, tuning=tuning
            )

        self.assertTrue(part_1_failed.is_set())
        self.assertGreater(len(begins), 1)
        self.assertEqual(data, service.assembled())
        self.assertEqual([1, 1, 2, 3, 4], sorted(service.puts))
        # Part 1 was sent again, and part 2 first sent, only once the
        # one-second cooldown was over.
        first_at = [at for at, number in service.put_times if number == 1][0]
        later = [
            at - first_at
            for at, number in service.put_times
            if number in (1, 2)
        ][1:]
        self.assertEqual(2, len(later))
        self.assertTrue(all(gap > 0.5 for gap in later), later)
        record = observed[-1].details
        self.assertEqual(
            ("completed", 4, 400),
            (record["outcome"], record["parts"], record["bytes_committed"]),
        )
        [backpressure] = [
            o
            for o in observed
            if o.kind == "decision" and o.decision == "backpressure"
        ]
        self.assertGreater(backpressure.cooldown, 0)
        # Neither a runway nor a wait for one.
        self.assertIsNone(record["waits"]["runway"])
        self.assertNotIn(
            "runway", {o.wait for o in observed if o.kind == "wait"}
        )
        self.assertEqual(
            {(None, None)},
            {(o.runway_parts, o.runway_bytes) for o in observed},
        )
        self.assertEqual((0, 0), (limiter.parts_in_use, limiter.bytes_in_use))

    def test_resources_are_reported_where_the_platform_has_them(self):
        # Without a resource module (Windows has none) a sample reports None
        # rather than failing the upload.
        with mock.patch.dict(sys.modules, {"resource": None}):
            self.assertIsNone(process_resources())
        try:
            import resource  # noqa: F401
        except ImportError:
            self.assertIsNone(process_resources())
        else:
            resources = process_resources()
            self.assertEqual(
                {"max_rss_bytes", "cpu_user_seconds", "cpu_system_seconds"},
                set(resources or {}),
            )

    def test_an_observer_must_be_callable(self):
        with self.assertRaisesRegex(
            InvalidParameterError, "observer must be callable"
        ):
            UploadTuning(observer="print")  # type: ignore[arg-type]


class TestUploadSummary(AdaptiveTestCase):
    def test_a_finished_upload_is_summarised_at_info_without_urls(self):
        service = UploadService(self, part_size=100)
        with self.assertLogs("files_sdk", level=logging.INFO) as logs:
            self.client(service).file.upload_file(
                self.local(bytes(500)), "a.bin"
            )
        summary = [
            record
            for record in logs.records
            if "Upload finished" in record.getMessage()
        ]
        self.assertEqual(1, len(summary))
        text = "\n".join(logs.output)
        self.assertNotIn("X-Amz-Signature", text)
        self.assertNotIn("/storage/", text)


if __name__ == "__main__":
    unittest.main()
