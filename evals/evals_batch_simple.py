#!/usr/bin/env python3

"""Minimal cloud batch eval execution example.

Runs the evalset spec as-is against one agentspec in cloud mode via
`datalayer_core.evals.execute_evalset_spec`.
"""

from __future__ import annotations

from pathlib import Path

from datalayer_core.evals import execute_evalset_spec, load_evalset_spec, make_client


EVALSET_SPEC_FILE = Path(__file__).with_name("evals_batch.evalset.json")
DEFAULT_AGENTSPEC_ID = "example-evals"


def main() -> None:
    client = make_client()
    spec = load_evalset_spec(
        EVALSET_SPEC_FILE,
        expected_kind="batch",
        require_cases=True,
    )
    result = execute_evalset_spec(
        client,
        spec=spec,
        agentspec_ids=[DEFAULT_AGENTSPEC_ID],
        run_limit=2,
        run_environment="sdk",
        backend_run_environment="sdk",
        execution_target="cloud",
        launch_source="python-batch-example-simple",
        log=print,
    )
    print(f"Done. Evalset id: {result.get('evalset_id')}")
    print(
        f"View result on http://localhost:3063/evals/experiments/sdk/{result.get('evalset_id')}"
    )


if __name__ == "__main__":
    main()
