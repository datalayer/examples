#!/usr/bin/env python3

"""Minimal cloud batch eval execution example.

Runs the evalset spec as-is against one agentspec in cloud mode via
`agent_runtimes.evals.remote.execute_evalset_spec`.
"""

from __future__ import annotations

import os
from pathlib import Path

from agent_runtimes.evals.remote import execute_evalset_spec, load_evalset_spec, make_client


EVALSET_SPEC_FILE = Path(__file__).with_name("evals_batch.evalset.json")
DEFAULT_AGENTSPEC_IDS = ["example-evals", "example-evals-nocodemode"]


def main() -> None:
    client = make_client()
    account_uid = str(os.environ.get("DATALAYER_ACCOUNT_UID") or "").strip() or None
    billing_entity_uid = (
        str(os.environ.get("DATALAYER_BILLING_ENTITY_UID") or "").strip() or None
    )
    spec = load_evalset_spec(
        EVALSET_SPEC_FILE,
        expected_kind="batch",
        require_cases=True,
    )
    result = execute_evalset_spec(
        client,
        spec=spec,
        agentspec_ids=DEFAULT_AGENTSPEC_IDS,
        create_report=True,
        run_limit=3,
        run_environment="sdk",
        backend_run_environment="sdk",
        execution_target="cloud", # cloud or local
        account_uid=account_uid,
        billing_entity_uid=billing_entity_uid,
        launch_source="python-batch-example-simple",
        log=print,
    )
    print(f"Done. Evalset id: {result.get('evalset_id')}")
    print(
        f"View result on http://localhost:3063/evals/experiments/sdk/{result.get('evalset_id')}"
    )
    report_md = str(result.get("report_markdown_path") or "").strip()
    report_csv = str(result.get("report_csv_path") or "").strip()
    if report_md:
        print(f"Report markdown: {report_md}")
    if report_csv:
        print(f"Report csv: {report_csv}")


if __name__ == "__main__":
    main()
