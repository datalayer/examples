# Copyright (c) 2025-2026 Datalayer, Inc.
#
# BSD 3-Clause License

"""Read section 14's SLO table from the OTEL query API (PLAN_ENVS.md E1-25).

    make env-slos
    python slos.py --account <service account uid> --since 7d

Every number the plan's SLO table asks for is a series the platform already
writes: durable's `environments` worker measures the resolve and the build,
Runtimes measures the launch. This reads them back the way the table is
written — a target, a measured number, and whether one meets the other —
rather than the way they are stored.

Two things about the storage are worth knowing before the numbers mean
anything:

- The instruments are **cumulative**: every point carries the running total
  since the exporting process started, not a delta. The latest point of each
  (instance, attributes) series is therefore the whole of it, and the totals
  across instances add up. A pod restart begins a new series rather than
  resetting the old one, which is why the grouping includes the instance.
- A histogram is stored as its buckets, so a percentile here is the bucket a
  percentile falls in, read as its upper bound. With the default bounds
  (0, 5, 10, 25, 50s...) that is coarse on purpose: it answers "under 45
  seconds?" exactly, and "43.2 seconds" never.

The metrics are account-scoped (every point is filed under the account that
exported it), so this asks for the services' own account. A platform admin may
query it; anybody else gets their own, which holds none of these.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from collections import defaultdict
from typing import Any, Iterable, Mapping, Sequence

# The account the platform services export under. Every `environments.*` point
# is filed there, durable's and Runtimes' alike.
SERVICE_ACCOUNT_UID = os.environ.get(
    "DATALAYER_SERVICE_ACCOUNT_UID", "01KCRC6BSR5S2WMJ79PPQ3BGH5"
)

# A build that fails because the document is wrong is not a platform failure,
# and section 14's success rate says so: "excluding user spec errors". These
# are section 10's codes for a spec the platform read and refused.
USER_SPEC_CODES = frozenset(
    {
        "DL_ENV_SPEC_INVALID",
        "DL_ENV_RESOLVE_CONFLICT",
        "DL_ENV_PACKAGE_NOT_FOUND",
        "DL_ENV_PROTECTED_PACKAGE",
        "DL_ENV_APT_PACKAGE_NOT_ALLOWED",
        "DL_ENV_POST_INSTALL_FAILED",
    }
)


def _json(value: Any, fallback: Any) -> Any:
    """Read one of the columns the store keeps as JSON text."""
    if isinstance(value, (list, dict)):
        return value
    if not value:
        return fallback
    try:
        return json.loads(value)
    except (TypeError, ValueError):
        return fallback


def _instance_of(row: Mapping[str, Any]) -> str:
    """The exporting process, so one pod's total is never added to its own."""
    resource = _json(row.get("resource_attributes"), {})
    return str(resource.get("service.instance.id") or row.get("service_name") or "")


def latest_points(rows: Iterable[Mapping[str, Any]]) -> list[dict[str, Any]]:
    """The newest point of every (instance, attributes, start) series.

    Cumulative means the newest point of a series *is* the series, so this is
    the whole history of everything these rows describe, with nothing
    double-counted.
    """
    newest: dict[tuple[str, str, Any], Mapping[str, Any]] = {}
    for row in rows:
        key = (
            _instance_of(row),
            str(row.get("attributes") or "{}"),
            row.get("start_time_unix_nano"),
        )
        seen = newest.get(key)
        if seen is None or int(row.get("timestamp_unix_nano") or 0) > int(
            seen.get("timestamp_unix_nano") or 0
        ):
            newest[key] = row
    return [
        {**row, "attrs": _json(row.get("attributes"), {})} for row in newest.values()
    ]


def percentile(points: Sequence[Mapping[str, Any]], quantile: float) -> tuple[float | None, int]:
    """The bucket a quantile falls in, as its upper bound, over every point.

    Returns the bound and the number of observations it was taken over; a
    percentile over three builds is a fact about three builds, and the caller
    prints the count beside the number for that reason.
    """
    # Two bucket layouts cannot be added, and a series that changed its edges
    # leaves both behind — every instrument here did, on 2026-09-16, when each
    # started advising edges its own target falls on. The newest layout wins,
    # and what the older ones hold is dropped rather than folded in: an
    # observation in a bucket of (0, 5s] says nothing about one in (0.05,
    # 0.075s], and a percentile over the two together would be a fiction.
    layouts: dict[tuple[float, ...], tuple[list[int], int]] = {}
    for point in points:
        edges = tuple(float(edge) for edge in _json(point.get("explicit_bounds"), []))
        counts = [int(count) for count in _json(point.get("bucket_counts"), [])]
        if not counts:
            continue
        seen, newest = layouts.get(edges, ([0] * len(counts), 0))
        if len(counts) != len(seen):
            continue
        layouts[edges] = (
            [a + b for a, b in zip(seen, counts)],
            max(newest, int(point.get("timestamp_unix_nano") or 0)),
        )
    if not layouts:
        return None, 0
    bounds_tuple = max(layouts, key=lambda edges: layouts[edges][1])
    bounds = list(bounds_tuple)
    totals = layouts[bounds_tuple][0]
    observations = sum(totals)
    if not observations:
        return None, 0
    wanted = quantile * observations
    running = 0
    for index, count in enumerate(totals):
        running += count
        if running >= wanted:
            # The last bucket is unbounded; its "upper bound" is the last edge,
            # which is the honest floor rather than infinity.
            return (bounds[index] if index < len(bounds) else bounds[-1]), observations
    return bounds[-1], observations


def counts_by(points: Iterable[Mapping[str, Any]], *keys: str) -> dict[tuple[str, ...], int]:
    """Sum the points of a counter, grouped by some of their attributes."""
    totals: dict[tuple[str, ...], int] = defaultdict(int)
    for point in points:
        attrs = point.get("attrs") or {}
        value = point.get("value_int")
        if value is None:
            value = point.get("value_double") or 0
        totals[tuple(str(attrs.get(key, "")) for key in keys)] += int(value)
    return dict(totals)


class Otel:
    """The OTEL query API, through the SDK's own client."""

    def __init__(self, account_uid: str, since_nanos: int | None) -> None:
        from agent_runtimes.client import AgentClient

        self._client = AgentClient()._otel_client()
        self._account_uid = account_uid
        self._since = since_nanos

    @property
    def base_url(self) -> str:
        return str(self._client.base_url)

    def points(self, name: str, **filters: Any) -> list[dict[str, Any]]:
        params: dict[str, Any] = {
            "name": name,
            "account_uid": self._account_uid,
            "limit": 100000,
        }
        if self._since is not None:
            params["start"] = self._since
        # The query service answers 500 now and then — a DataFusion failure it
        # does not recognise as the panic it special-cases — and the same
        # question asked again answers. One retry, because a flake that stops
        # a drill reads as a missing metric.
        try:
            answer = self._client._get("/api/otel/v1/metrics/query", params=params)
        except Exception:  # noqa: BLE001 - any transport or status failure
            answer = self._client._get("/api/otel/v1/metrics/query", params=params)
        rows = answer.get("data") or []
        points = latest_points(rows)
        if not filters:
            return points
        return [
            point
            for point in points
            if all(str((point["attrs"] or {}).get(k, "")) == str(v) for k, v in filters.items())
        ]


def _row(metric: str, target: str, measured: str, met: bool | None) -> dict[str, str]:
    mark = {True: "met", False: "MISSED", None: "no data"}[met]
    return {"metric": metric, "target": target, "measured": measured, "verdict": mark}


def read_slos(otel: Otel) -> list[dict[str, str]]:
    """Section 14's table, row by row, from what the plane has recorded."""
    rows: list[dict[str, str]] = []

    # 1. Resolve latency (packages source): p50 < 10s, p95 < 45s.
    resolves = [p for p in otel.points("environments.resolve.duration")
                if (p["attrs"] or {}).get("status") == "resolved"]
    p50, seen = percentile(resolves, 0.50)
    p95, _ = percentile(resolves, 0.95)
    rows.append(
        _row(
            "Resolve latency (packages source)",
            "p50 < 10s, p95 < 45s",
            "no resolve recorded" if not seen else f"p50 ≤ {p50:g}s, p95 ≤ {p95:g}s (n={seen})",
            None if not seen else (p50 is not None and p50 <= 10 and p95 is not None and p95 <= 45),
        )
    )

    # 2. Build latency, Datalayer variant, cached base: p50 < 3 min, p95 < 10 min.
    builds = [p for p in otel.points("environments.build.duration")
              if (p["attrs"] or {}).get("variant") == "datalayer"]
    p50, seen = percentile(builds, 0.50)
    p95, _ = percentile(builds, 0.95)
    rows.append(
        _row(
            "Build latency, Datalayer variant",
            "p50 < 3 min, p95 < 10 min",
            "no build recorded" if not seen else f"p50 ≤ {p50:g}s, p95 ≤ {p95:g}s (n={seen})",
            None if not seen else (p50 is not None and p50 <= 180 and p95 is not None and p95 <= 600),
        )
    )

    # 3. Build success rate excluding user spec errors: > 98%.
    totals = counts_by(otel.points("environments.builds"), "status", "code")
    counted = {
        (status, code): n
        for (status, code), n in totals.items()
        if code not in USER_SPEC_CODES
    }
    attempted = sum(counted.values())
    succeeded = sum(n for (status, _), n in counted.items() if status == "succeeded")
    excluded = sum(totals.values()) - attempted
    rate = (succeeded / attempted * 100) if attempted else None
    rows.append(
        _row(
            "Build success rate (excl. user spec errors)",
            "> 98%",
            "no build recorded"
            if rate is None
            else f"{rate:.0f}% ({succeeded}/{attempted}; {excluded} spec errors excluded)",
            None if rate is None else rate > 98,
        )
    )

    # 4. Cold-start delta, user environment vs platform environment: p95 < +5s.
    #    No service observes it: the moment that matters is the first `1+1`
    #    answering in the sandbox, which only the caller sees. `--cold-start`
    #    measures it here instead; nothing about it is in OTEL.
    rows.append(
        _row(
            "Cold-start delta, user vs platform environment",
            "p95 < +5s after warm-up",
            "not an instrument — run with --cold-start",
            None,
        )
    )

    # 5. Artifact resolution (version → immutable ref): p99 < 100ms.
    resolutions = otel.points("environments.artifact.resolution")
    p99, seen = percentile(resolutions, 0.99)
    # The default bounds start at 0 and jump to 5s, so a sub-second p99 reads
    # as "≤ 5s" and says nothing about 100 ms. The sum over the count is the
    # mean, which for this instrument is the number worth printing.
    total = sum(float(p.get("value_double") or 0) for p in resolutions)
    observations = sum(int(p.get("value_int") or 0) for p in resolutions)
    mean_ms = (total / observations * 1000) if observations else None
    rows.append(
        _row(
            "Artifact resolution (version → immutable ref)",
            "p99 < 100ms",
            "no launch recorded"
            if not seen
            else f"p99 ≤ {p99:g}s, mean {mean_ms:.1f}ms (n={observations})",
            None if not seen else (mean_ms is not None and mean_ms < 100),
        )
    )

    # 6. Provider drift detected but unrepaired: 0 at any cycle end.
    reconciled = counts_by(otel.points("environments.artifacts.reconciled"), "outcome")
    drifted = sum(n for (outcome,), n in reconciled.items() if outcome == "drifted")
    rows.append(
        _row(
            "Provider drift detected but unrepaired",
            "0 at any reconciliation cycle end",
            "no reconciliation recorded" if not reconciled else f"{drifted} drifted",
            None if not reconciled else drifted == 0,
        )
    )
    return rows


def extra_series(otel: Otel) -> list[str]:
    """The rest of section 14's list, which has no target but is tracked."""
    lines: list[str] = []
    lookups = counts_by(otel.points("environments.cache.lookups"), "hit")
    hits = sum(n for (hit,), n in lookups.items() if hit == "true")
    looked = sum(lookups.values())
    if looked:
        lines.append(f"cache hit rate: {hits}/{looked}")
    waits = otel.points("environments.build.queue_wait")
    p95, seen = percentile(waits, 0.95)
    if seen:
        lines.append(f"queue latency: p95 ≤ {p95:g}s (n={seen})")
    retries = counts_by(otel.points("environments.build.retries"), "variant")
    if retries:
        lines.append("retries: " + ", ".join(f"{v or '?'}={n}" for (v,), n in retries.items()))
    failures = {
        code: n
        for (status, code), n in counts_by(
            otel.points("environments.builds"), "status", "code"
        ).items()
        if status == "failed" and code
    }
    if failures:
        lines.append("failures by code: " + ", ".join(f"{c}={n}" for c, n in sorted(failures.items())))
    sizes = otel.points("environments.artifact.bytes")
    observed = sum(int(p.get("value_int") or 0) for p in sizes)
    if observed:
        total = sum(float(p.get("value_double") or 0) for p in sizes)
        lines.append(f"artifact size: mean {total / observed / 1e9:.2f} GB (n={observed})")
    refusals = counts_by(otel.points("environments.launch.refusals"), "code")
    if refusals:
        lines.append("launch refusals: " + ", ".join(f"{c or '?'}={n}" for (c,), n in refusals.items()))
    collected = counts_by(otel.points("environments.artifacts.collected"), "outcome")
    if collected:
        lines.append("artifacts collected: " + ", ".join(f"{o or '?'}={n}" for (o,), n in collected.items()))
    return lines


def measure_cold_start(environment: str, platform_environment: str, runs: int) -> list[str]:
    """Time a launch to its first `1+1`, for a user and a platform environment.

    Section 14's only row no instrument can answer. The moment it is about — a
    sandbox that will run code — is not a moment any service sees: Runtimes
    has answered and the pod is still pulling. So it is measured from here,
    the way the person waiting experiences it, and the delta is what the row
    asks for: a user environment against a platform one, same size class, same
    plane, back to back.
    """
    import time

    from agent_runtimes.client import AgentClient

    client = AgentClient()
    lines: list[str] = []
    taken: dict[str, list[float]] = {}
    for name in (platform_environment, environment):
        deltas: list[float] = []
        for _ in range(runs):
            began = time.monotonic()
            runtime = client.create_runtime(environment=name, time_reservation=5)
            try:
                # `create_runtime` answers as soon as the record exists; the
                # pod may still be pulling. `start()` is what waits for a
                # kernel, and running code is what proves there is one.
                runtime.start()
                runtime.execute("1+1")
                deltas.append(time.monotonic() - began)
            finally:
                try:
                    runtime.stop()
                except Exception:  # noqa: BLE001 - a stop that fails is not a measurement
                    pass
        taken[name] = deltas
        lines.append(f"{name}: " + ", ".join(f"{d:.1f}s" for d in deltas))
    warm = {name: min(deltas) for name, deltas in taken.items() if deltas}
    if len(warm) == 2:
        delta = warm[environment] - warm[platform_environment]
        lines.append(
            f"delta (warmest of each): {delta:+.1f}s against a target of < +5s"
        )
    return lines


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--account", default=SERVICE_ACCOUNT_UID, help="the account the services export under")
    parser.add_argument("--since", default=None, help="only points after this many days, as e.g. 7d")
    parser.add_argument("--json", action="store_true", help="the table as JSON")
    parser.add_argument("--cold-start", action="store_true", help="also measure the cold-start delta, which launches sandboxes")
    parser.add_argument("--environment", default=os.environ.get("ENVIRONMENT", ""), help="the user environment to time")
    parser.add_argument("--platform-environment", default="ai-agents-env", help="the platform environment to time it against")
    parser.add_argument("--runs", type=int, default=3, help="how many launches each, for --cold-start")
    args = parser.parse_args(argv)

    since_nanos = None
    if args.since:
        import time

        days = float(str(args.since).rstrip("dD"))
        since_nanos = int((time.time() - days * 86400) * 1e9)

    otel = Otel(args.account, since_nanos)
    rows = read_slos(otel)

    if args.cold_start:
        if not args.environment:
            print("Set --environment (or ENVIRONMENT) to the user environment to time.", file=sys.stderr)
            return 2
        for line in measure_cold_start(args.environment, args.platform_environment, args.runs):
            print("  " + line)
        return 0

    if args.json:
        print(json.dumps(rows, indent=2))
        return 0

    print(f"Section 14 SLOs, from {otel.base_url}, account {args.account}\n")
    widths = [max(len(row[key]) for row in rows) for key in ("metric", "target", "measured")]
    header = ("Metric", "Target", "Measured", "")
    print("  ".join(h.ljust(w) for h, w in zip(header, widths + [0])).rstrip())
    print("  ".join("-" * w for w in widths + [7]))
    for row in rows:
        print(
            "  ".join(
                [
                    row["metric"].ljust(widths[0]),
                    row["target"].ljust(widths[1]),
                    row["measured"].ljust(widths[2]),
                    row["verdict"],
                ]
            )
        )
    extra = extra_series(otel)
    if extra:
        print("\nAlso tracked (section 14, no target):")
        for line in extra:
            print("  " + line)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
