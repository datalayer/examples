# Copyright (c) 2025-2026 Datalayer, Inc.
#
# BSD 3-Clause License

"""Launch a sandbox of a User Environment, pinned to a version (PLAN_ENV.md E1-26).

    ENVIRONMENT=ada/geospatial-analysis VERSION=1 python launch.py

Without `VERSION` the promoted version runs, which is what you want unless you
were asked for a particular one: a sandbox keeps the version it started with,
so pinning matters for reproducing a result and not for everyday work.
"""

from __future__ import annotations

import os
import sys


def main() -> int:
    environment = (os.environ.get("ENVIRONMENT") or "").strip()
    if not environment:
        print("Set ENVIRONMENT to 'account/name' or the environment's uid.", file=sys.stderr)
        return 2
    version = (os.environ.get("VERSION") or "").strip()
    minutes = int(os.environ.get("MINUTES_LIMIT") or 10)

    from agent_runtimes.client import AgentClient

    client = AgentClient()
    answer = client.create_runtime(
        environment=environment,
        # A number is a version number and a string is a version uid: the
        # platform reads the two differently, so neither is turned into the
        # other here.
        version=int(version) if version.isdigit() else (version or None),
        time_reservation=minutes,
    )
    runtime = getattr(answer, "runtime", None) or answer
    uid = getattr(runtime, "uid", None) or (runtime.get("uid") if isinstance(runtime, dict) else "")
    running = getattr(runtime, "environment", None) or (
        runtime.get("environment") if isinstance(runtime, dict) else {}
    )
    print(f"Runtime {uid} runs {environment}" + (f" version {version}" if version else " (promoted)"))
    if running:
        print(f"  environment: {running}")
    print("  Stop it with: datalayer runtimes terminate " + str(uid))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
