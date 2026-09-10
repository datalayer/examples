#!/usr/bin/env python3

"""Interactive eval example for Datalayer.

Creates one evalset, five experiments, and three runs per experiment using
run_mode=interactive. Local and synthetic paths emit live evaluator events for
Monitoring so interactive behavior is observable in target/evaluator/event views.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import socket
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

from agent_runtimes.client import AgentClient
from agent_runtimes.commands.agents import _load_agent_spec
from agent_runtimes.evals.remote import (
    evaluate_evalset,
    execute_evalset_spec,
    load_evalset_spec,
    make_client,
    watch_runs,
)
from agent_runtimes.evals.report import write_eval_reports


DEFAULT_EVALSET_SPEC_FILE = Path(__file__).with_name('evals_interactive.evalset.json')
DEFAULT_AGENT_SPEC_ID = 'example-evals'
DEFAULT_AGENT_SPEC_IDS = ['example-evals', 'example-evals-nocodemode']
DEFAULT_AGENT_SPEC_NAME_BY_ID = {
    'example-evals': 'Example Evals Agent',
    'example-evals-nocodemode': 'Example Evals Agent (No Codemode)',
}
BASE_EXPERIMENT_COUNT = 5


def _generated_evalset_name(source: str, mode: str) -> str:
    stamp = datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S')
    return f'evalset-{source}-{mode}-{stamp}'


def _run_status_for_index(index: int) -> str:
    return 'running' if index == 0 else ('completed' if index == 1 else 'failed')


def _normalize_no_agent_first_run_status(requested_status: str) -> str:
    normalized = str(requested_status or '').strip().lower()
    if normalized in {'running', 'queued', 'pending'}:
        return 'completed'
    if normalized in {'completed', 'failed', 'cancelled'}:
        return normalized
    return 'completed'


def _resolve_default_agent_spec_id() -> str:
    return DEFAULT_AGENT_SPEC_ID


def _resolve_default_agent_spec_ids() -> list[str]:
    return list(DEFAULT_AGENT_SPEC_IDS)


def _dedupe_preserve_order(values: list[str]) -> list[str]:
    deduped: list[str] = []
    for value in values:
        normalized = value.strip()
        if not normalized or normalized in deduped:
            continue
        deduped.append(normalized)
    return deduped


def _parse_agent_spec_ids(raw: str | None) -> list[str]:
    if not raw:
        return []
    return _dedupe_preserve_order(str(raw).split(','))


def _resolve_agent_spec_variants(args: argparse.Namespace) -> list[dict[str, Any]]:
    selected_ids: list[str] = []
    if args.agent_spec_id:
        selected_ids.append(str(args.agent_spec_id))
    selected_ids.extend(_parse_agent_spec_ids(args.agent_spec_ids))
    selected_ids = _dedupe_preserve_order(selected_ids)

    if args.agent_spec:
        if len(selected_ids) > 1:
            raise RuntimeError('Use --agent-spec with one agent-spec id only.')
        resolved_id = selected_ids[0] if selected_ids else _resolve_default_agent_spec_id()
        loaded_spec = _load_agent_spec(str(args.agent_spec))
        return [
            {
                'id': resolved_id,
                'name': str(loaded_spec.get('name') or DEFAULT_AGENT_SPEC_NAME_BY_ID.get(resolved_id, resolved_id)),
                'spec': loaded_spec,
            }
        ]

    resolved_ids = selected_ids or _resolve_default_agent_spec_ids()
    return [
        {
            'id': spec_id,
            'name': DEFAULT_AGENT_SPEC_NAME_BY_ID.get(spec_id, spec_id),
            'spec': None,
        }
        for spec_id in resolved_ids
    ]


def _is_intentional_failure(index: int, run_status: str) -> bool:
    return index >= 2 and run_status == 'failed'


def _pass_rate_for_index(base_pass_rate: float, index: int, run_seed: str = '') -> float:
    if index == 0:
        target = base_pass_rate - 0.1
    elif index == 1:
        target = base_pass_rate
    else:
        target = base_pass_rate - 0.18
    # Layer a per-run seeded jitter on top so runs within an experiment drift
    # instead of collapsing onto the same quantized pass rate.
    jitter = (_stable_unit('run-pass-rate', run_seed, index) - 0.5) * 0.24 if run_seed else 0.0
    return max(0.0, min(1.0, target + jitter))


def _experiment_pass_rate(
    base_pass_rate: float, experiment_index: int, experiment_id: str = ''
) -> float:
    """Spread experiments around the base pass rate.

    Without this every experiment shares the same base rate and lands on the
    same quantized value (e.g. all 60%). A deterministic per-experiment offset
    gives the dashboard real variation and drift while staying reproducible.
    """
    spread = (
        _stable_unit('experiment-pass-rate', experiment_index, experiment_id) - 0.5
    ) * 0.6
    return max(0.05, min(0.98, base_pass_rate + spread))


def _stable_unit(*parts: object) -> float:
    key = '|'.join(str(part) for part in parts)
    digest = hashlib.sha256(key.encode('utf-8')).hexdigest()
    return int(digest[:12], 16) / float(0xFFFFFFFFFFFF)


def _build_synthetic_pydantic_usage(
    *,
    experiment_id: str,
    run_index: int,
    run_pass_rate: float,
    run_status: str,
    model_name: str,
) -> dict[str, Any]:
    status_factor = 0.45 if run_status in {'failed', 'error'} else 1.0
    request_count = 1 + int(_stable_unit('synthetic-requests', experiment_id, run_index) * 2)
    base_prompt = 210 + int(_stable_unit('synthetic-prompt', experiment_id, run_index) * 95)
    base_completion = 110 + int(_stable_unit('synthetic-completion', experiment_id, run_index) * 80)
    prompt_tokens = max(1, int(base_prompt * status_factor))
    completion_tokens = max(1, int(base_completion * status_factor))
    total_tokens = prompt_tokens + completion_tokens
    credits_consumed = round(total_tokens * 0.000002, 6)
    duration_ms = max(50, int(620 + (1.0 - run_pass_rate) * 720 + request_count * 55))
    return {
        'source': 'synthetic_example',
        'provider': 'synthetic',
        'model': model_name,
        'requests': request_count,
        'prompt_tokens': prompt_tokens,
        'completion_tokens': completion_tokens,
        'total_tokens': total_tokens,
        'credits_consumed': credits_consumed,
        'duration_ms': duration_ms,
        'captured_at': datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z'),
    }


def _case_weight(case: dict[str, Any], idx: int, run_seed: str = '') -> float:
    """Deterministic 'difficulty' weight in [0, 1], stable across runs."""
    metadata = case.get('metadata') or {}
    difficulty = str(metadata.get('difficulty') or '').strip().lower()
    priority = str(metadata.get('priority') or '').strip().lower()
    base = {'easy': 0.20, 'medium': 0.55, 'hard': 0.85}.get(difficulty)
    if base is None:
        base = {'low': 0.25, 'medium': 0.50, 'high': 0.70, 'critical': 0.90}.get(
            priority, 0.50
        )
    case_name = str(case.get('name') or f'case-{idx}')
    # Keep a stable per-case difficulty offset (keyed only on the case, not the
    # run). Per-run variation in *which* cases fail is layered on top of this
    # weight at ranking time in _build_case_results, so harder cases still fail
    # more often on average while individual runs differ.
    order_jitter = (_stable_unit('case-order', case_name, idx) - 0.5) * 0.30
    static_jitter = (idx % 5) * 0.005
    return max(0.01, min(0.99, base + static_jitter + order_jitter))


def _build_case_results(
    cases: list[dict[str, Any]],
    run_pass_rate: float | None,
    run_status: str,
    run_seed: str = '',
    forced_failed_case_names: set[str] | None = None,
) -> list[dict[str, Any]]:
    """Derive per-case outcomes for a single run.

    The number of passing cases tracks the run pass rate. Which cases fail is
    biased toward the hardest cases (highest weight) but also varies per run
    via a run-seeded jitter, so different runs surface different failing cases
    while harder cases still fail more often on average.
    """
    total = len(cases)
    if total == 0 or run_pass_rate is None:
        return []
    bounded = max(0.0, min(1.0, float(run_pass_rate)))
    passed_count = int(round(bounded * total))
    if run_status in {'failed', 'error'}:
        passed_count = min(passed_count, total - 1)
    passed_count = max(0, min(total, passed_count))
    failed_count = total - passed_count
    ranked = sorted(
        range(total),
        key=lambda i: (
            _case_weight(cases[i], i, run_seed)
            + (_stable_unit('run-failure', run_seed, cases[i].get('name') or i, i) - 0.5) * 0.6,
            _stable_unit('rank-tie', run_seed, cases[i].get('name') or i, i),
        ),
        reverse=True,
    )
    failing = set(ranked[:failed_count])
    forced_failed_case_names = forced_failed_case_names or set()
    for idx, case in enumerate(cases):
        case_name = str(case.get('name') or '')
        if case_name and case_name in forced_failed_case_names:
            failing.add(idx)
    if run_status in {'failed', 'error'} and not failing:
        failing.add(ranked[0])
    for candidate_idx in ranked:
        if len(failing) >= failed_count:
            break
        failing.add(candidate_idx)
    results: list[dict[str, Any]] = []
    for idx, case in enumerate(cases):
        metadata = case.get('metadata') or {}
        passed = idx not in failing
        weight = _case_weight(case, idx, run_seed)
        case_name = str(case.get('name') or f'case-{idx}')
        score_jitter = (_stable_unit('case-score', run_seed, case_name, idx) - 0.5) * 0.10
        if passed:
            score = round(min(1.0, max(0.0, 0.82 + (1.0 - weight) * 0.15 + score_jitter)), 4)
        else:
            score = round(min(1.0, max(0.0, 0.45 - weight * 0.25 + score_jitter)), 4)
        results.append(
            {
                'name': case.get('name'),
                'passed': passed,
                'status': 'passed' if passed else 'failed',
                'score': score,
                'category': metadata.get('category'),
                'difficulty': metadata.get('difficulty') or metadata.get('priority'),
            }
        )
    return results


def _expected_case_text(case: dict[str, Any]) -> str:
    return str((case.get('expected_output') or {}).get('text') or '')


def _failing_output_text(case: dict[str, Any]) -> str:
    """Return an output that will *not* satisfy the case under grading."""
    expected_text = _expected_case_text(case)
    input_text = str((case.get('inputs') or {}).get('text') or '')
    if input_text and input_text != expected_text:
        return input_text
    marker = f'{expected_text} (incorrect)'.strip()
    return marker or 'incorrect'


def _build_case_outputs(
    cases: list[dict[str, Any]],
    run_pass_rate: float | None,
    run_status: str,
    run_seed: str = '',
    forced_failed_case_names: set[str] | None = None,
) -> list[dict[str, Any]]:
    """Simulate one agent output per case for grading by the evals API.

    The example only *produces* outputs (good ones for the cases the simulated
    agent gets right, wrong ones for the rest, biased toward harder cases and
    varied per run via ``_build_case_results``). Evaluator execution and
    grading are delegated to ``evaluate_evalset`` so the example never
    re-implements evaluator logic.
    """
    breakdown = _build_case_results(
        cases,
        run_pass_rate,
        run_status,
        run_seed=run_seed,
        forced_failed_case_names=forced_failed_case_names,
    )
    if not breakdown:
        return []
    outputs: list[dict[str, Any]] = []
    for case, outcome in zip(cases, breakdown):
        if outcome.get('passed'):
            outputs.append({'text': _expected_case_text(case)})
        else:
            outputs.append({'text': _failing_output_text(case)})
    return outputs


def _extract_case_prompt(case: dict[str, Any]) -> str:
    inputs = case.get('inputs')
    if isinstance(inputs, dict):
        for key in ('prompt', 'text', 'query', 'message'):
            value = inputs.get(key)
            if isinstance(value, str) and value.strip():
                return value
        try:
            return json.dumps(inputs, ensure_ascii=True)
        except TypeError:
            return str(inputs)
    return ''


def _synthetic_pass_text(case: dict[str, Any]) -> str:
    """Build a plausible passing answer for a case from its expectations.

    Used by synthetic mode (``--synthetic``) so a healthy run shows an
    output that actually satisfies the case assertions, making the contrast
    with a regressed run obvious in the comparison panel.
    """
    expected = case.get('expected_output')
    if isinstance(expected, dict):
        if expected.get('label') == 'refusal':
            return "I can't help with that request."
        if expected.get('format') == 'json':
            keys = expected.get('required_keys') or []
            body = ', '.join(f'"{key}": "..."' for key in keys)
            return '{' + body + '}'
        contains = expected.get('contains')
        if isinstance(contains, list) and contains:
            tokens = ', '.join(str(token) for token in contains)
            return f'Sure — here is a concise answer mentioning {tokens}.'
    return 'Synthetic passing answer.'


def _assert_http_service_reachable(service_name: str, base_url: str) -> None:
    parsed = urlparse(base_url)
    host = parsed.hostname or 'localhost'
    if parsed.port:
        port = parsed.port
    elif parsed.scheme == 'https':
        port = 443
    else:
        port = 80
    try:
        with socket.create_connection((host, port), timeout=2):
            return
    except OSError as exc:
        raise RuntimeError(
            f"{service_name} service is not reachable at {base_url}. "
            "Start local proxies/services first (for example: p pf-local)."
        ) from exc


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description='Create one evalset, experiments for one or more agentspecs, and three runs per experiment in interactive mode.'
    )
    parser.add_argument('--eval-name', default='')
    parser.add_argument(
        '--evalset-spec-file',
        default=str(DEFAULT_EVALSET_SPEC_FILE),
        help='Path to evalset JSON spec (includes schema, cases, and evaluators).',
    )
    parser.add_argument('--run-status', default='running', choices=['queued', 'running', 'completed', 'failed', 'cancelled'])
    parser.add_argument(
        '--plane',
        default='cloud',
        choices=['cloud', 'local'],
        help=(
            'Which Datalayer plane to talk to: cloud, the SDK defaults; '
            'local, a `plane local` on this machine (the --iam-url, --runtimes-url and '
            '--ai-agents-url addresses are checked before anything is created). '
            'The run environment recorded on the platform is sdk either way.'
        ),
    )
    parser.add_argument('--timeout', type=int, default=60)
    parser.add_argument('--interval', type=int, default=2)
    parser.add_argument('--pass-rate', type=float, default=0.85)
    parser.add_argument('--total-cases', type=int, default=10)
    parser.add_argument('--model-name', default='openai:gpt-5-mini')
    parser.add_argument('--prompt-version', default='v1')
    parser.add_argument('--iam-url', default=os.environ.get('DATALAYER_IAM_URL'))
    parser.add_argument('--runtimes-url', default=os.environ.get('DATALAYER_RUNTIMES_URL'))
    parser.add_argument('--ai-agents-url', default=os.environ.get('DATALAYER_AI_AGENTS_URL'))
    parser.add_argument(
        '--billing-entity-uid',
        default=os.environ.get('DATALAYER_BILLING_ENTITY_UID'),
        help='Optional billing entity UID for eval API calls.',
    )
    parser.add_argument(
        '--account-uid',
        default=os.environ.get('DATALAYER_ACCOUNT_UID'),
        help='Optional account UID for eval API calls.',
    )
    parser.add_argument('--ui-url', default=None)
    parser.add_argument('--execution-target', default='cloud', choices=['cloud', 'local'])
    parser.add_argument(
        '--agentspec-id',
        dest='agent_spec_id',
        default=None,
        help='Agent specification id. Defaults to example-evals when omitted.',
    )
    parser.add_argument(
        '--agentspec-ids',
        dest='agent_spec_ids',
        default=None,
        help=(
            'Comma-separated agentspec ids. Defaults to '
            'example-evals,example-evals-nocodemode when omitted.'
        ),
    )
    parser.add_argument(
        '--agentspec',
        dest='agent_spec',
        default=None,
        help=(
            'Agent spec source as YAML/JSON URL or local file path. '
            'When provided, overrides --agentspec-id.'
        ),
    )
    parser.add_argument('--environment-name', default='ai-agents-env')
    parser.add_argument(
        '--cloud-credits-limit',
        type=float,
        default=100.0,
        help='Target credits reservation for cloud runtime creation.',
    )
    parser.add_argument(
        '--cloud-concurrency',
        type=int,
        default=4,
        help=(
            'Sandboxes a cloud launch runs the tasks on, per experiment. A local plane '
            'serves its services from one process each over port-forwards, so one or '
            'two is what it keeps up with; the cloud takes more.'
        ),
    )
    parser.add_argument(
        '--local-agent-base-url',
        default=os.environ.get('AGENT_RUNTIME_BASE_URL', 'http://localhost:8765'),
    )
    parser.add_argument(
        '--local-agent-id',
        default=os.environ.get('AGENT_RUNTIME_ID', 'default'),
    )
    parser.add_argument(
        '--local-agent-log-level',
        default='info',
        choices=['debug', 'info', 'warning', 'error', 'critical'],
        help='Log level for auto-started local agent-runtimes process.',
    )
    parser.add_argument(
        '--auto-start-local-agent-runtime',
        action='store_true',
        help='Start a local agent-runtimes server on a random free port for local execution.',
    )
    parser.add_argument(
        '--synthetic',
        dest='no_agent',
        action='store_true',
        help='Use synthetic eval behavior without invoking an agent.',
    )
    parser.add_argument(
        '--no-auto-report',
        dest='auto_report',
        action='store_false',
        default=True,
        help='Skip automatic markdown report generation at the end of the run.',
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    token = os.environ.get('DATALAYER_API_KEY')
    if not token:
        raise RuntimeError('Set DATALAYER_API_KEY first.')

    billing_entity_uid = str(args.billing_entity_uid or '').strip() or None
    account_uid = str(args.account_uid or '').strip() or None
    if args.agent_spec and args.agent_spec_id and args.agent_spec_ids:
        raise RuntimeError('Use either --agentspec-id or --agentspec-ids with --agentspec, not both.')

    agent_spec_variants = _resolve_agent_spec_variants(args)
    if args.no_agent and len(agent_spec_variants) < 2:
        default_variant_ids = _resolve_default_agent_spec_ids()
        existing_variant_ids = {
            str(variant.get('id') or '').strip()
            for variant in agent_spec_variants
            if str(variant.get('id') or '').strip()
        }
        for variant_id in default_variant_ids:
            if variant_id in existing_variant_ids:
                continue
            agent_spec_variants.append(
                {
                    'id': variant_id,
                    'name': DEFAULT_AGENT_SPEC_NAME_BY_ID.get(variant_id, variant_id),
                    'spec': None,
                }
            )
            existing_variant_ids.add(variant_id)
            if len(agent_spec_variants) >= 2:
                break
        if len(agent_spec_variants) < 2:
            raise RuntimeError('Synthetic mode requires at least two agentspec variants.')
        print(
            'Synthetic mode requires cross-agentspec comparisons; '
            f'auto-expanded to {len(agent_spec_variants)} variants.'
        )
    print(
        'Agentspec variants: '
        + ', '.join(
            f"{variant['id']} ({variant['name']})" for variant in agent_spec_variants
        )
    )
    backend_run_environment = 'sdk'
    pass_rate = min(1.0, max(0.0, float(args.pass_rate)))
    run_count = 3
    total_cases = max(1, int(args.total_cases))

    client = make_client(
        token=token,
        iam_url=args.iam_url,
        runtimes_url=args.runtimes_url,
        ai_agents_url=args.ai_agents_url,
    )
    urls = client.urls

    if args.plane == 'local':
        _assert_http_service_reachable('ai-agents', urls.ai_agents_url)
        if args.execution_target == 'cloud':
            _assert_http_service_reachable('runtimes', urls.runtimes_url)
    datalayer_url = (os.environ.get('DATALAYER_URL') or '').strip().rstrip('/')
    if args.execution_target == 'cloud' and datalayer_url and not args.ui_url:
        ui_url = datalayer_url
    else:
        ui_url = (
            args.ui_url
            or os.environ.get('DATALAYER_UI_URL')
            or ('http://localhost:3063' if 'localhost' in urls.ai_agents_url or '127.0.0.1' in urls.ai_agents_url else urls.ai_agents_url)
        ).rstrip('/')

    mode_label = 'interactive-synthetic' if args.no_agent else 'interactive'
    evalset_spec = load_evalset_spec(
        args.evalset_spec_file, expected_kind='interactive', require_cases=True
    )
    evalset_name = (
        args.eval_name.strip()
        or str(evalset_spec.get('name') or '').strip()
        or _generated_evalset_name('sdk', mode_label)
    )
    evalset_description = str(
        evalset_spec.get('description') or 'Eval created by evals_interactive_example.py'
    )
    cases = [
        case for case in (evalset_spec.get('cases') or [])
        if isinstance(case, dict)
    ]

    if not args.no_agent:
        if args.agent_spec:
            raise RuntimeError(
                'Runner-backed mode does not support inline --agentspec; pass '
                '--agentspec-id/--agentspec-ids instead.'
            )
        agentspec_ids = [str(variant['id']) for variant in agent_spec_variants]
        print(
            f'[runner] Delegating real {args.execution_target} interactive execution to '
            'agent_runtimes.evals.remote.execute_evalset_spec for agentspecs: '
            + ', '.join(agentspec_ids)
        )
        result = execute_evalset_spec(
            client,
            spec=evalset_spec,
            agentspec_ids=agentspec_ids,
            run_limit=run_count,
            run_environment=backend_run_environment,
            environment_name=args.environment_name,
            billing_entity_uid=billing_entity_uid,
            account_uid=account_uid,
            credits_limit=float(args.cloud_credits_limit),
            concurrency=max(1, int(args.cloud_concurrency)),
            evalset_name=evalset_name,
            backend_run_environment=backend_run_environment,
            launch_source='python-interactive-example',
            agent_name=args.local_agent_id,
            execution_target=args.execution_target,
            local_agent_base_url=args.local_agent_base_url,
            auto_start_local_agent_runtime=bool(
                args.auto_start_local_agent_runtime
            ),
            local_agent_log_level=args.local_agent_log_level,
            create_report=bool(args.auto_report),
            log=print,
        )
        runner_evalset_id = str(result.get('evalset_id') or '')
        print(
            f'[runner] Created evalset {runner_evalset_id} '
            f"({result.get('evalset_name')}) with "
            f"{len(result.get('experiment_ids') or [])} experiment(s) and "
            f"{len(result.get('run_ids') or [])} run(s)."
        )
        if result.get('report_markdown_path'):
            print(f"Auto report written: {result.get('report_markdown_path')}")
        if result.get('report_csv_path'):
            print(f"Auto report CSV written: {result.get('report_csv_path')}")
        if args.execution_target == 'cloud' and datalayer_url:
            print(f'Cloud runtime base URL: {datalayer_url}')
        track_ui_base = (os.environ.get('DATALAYER_CDN_URL') or ui_url).strip().rstrip('/')
        print(f'Track in UI: {track_ui_base}/benchmarks/{runner_evalset_id}')
        print('Done.')
        return

    print('[1/3] Creating evalset...')
    evalset_payload = client.evals_create_eval_from_spec(
        spec=evalset_spec,
        name=evalset_name,
        description=evalset_description,
        run_environment=backend_run_environment,
        kind='interactive',
        billing_entity_uid=billing_entity_uid,
        account_uid=account_uid,
    )
    evalset_id = str((evalset_payload.get('evalset') or {}).get('id') or '')
    if not evalset_id:
        raise RuntimeError(f'Unexpected evalset response: {evalset_payload}')
    print(f'Created evalset: {evalset_id} ({evalset_name})')

    print('[2/3] Creating experiments...')
    experiment_specs = [
        {'name': f'interactive-experiment-{index}', 'index': index}
        for index in range(1, BASE_EXPERIMENT_COUNT + 1)
    ]
    experiment_ids: list[tuple[str, str, int, str, str]] = []
    total_experiments = len(experiment_specs) * len(agent_spec_variants)
    created_experiments = 0
    for spec in experiment_specs:
        for variant_index, variant in enumerate(agent_spec_variants, start=1):
            variant_id = str(variant['id'])
            variant_name = str(variant['name'])
            experiment_name = f"{spec['name']}-{variant_id}"
            experiment_payload = client.evals_create_experiment(
                name=experiment_name,
                evalset_id=evalset_id,
                description='Experiment created by evals_interactive_example.py',
                status='draft',
                config={
                    'run_mode': 'interactive',
                    'execution_target': args.execution_target,
                    'no_agent': bool(args.no_agent),
                    'dry_run': bool(args.no_agent),
                    'agent_spec_id': variant_id,
                    'agent_spec_name': variant_name,
                    'agent_spec': {'id': variant_id, 'name': variant_name},
                    'environment_name': args.environment_name,
                    'local_agent_base_url': args.local_agent_base_url,
                    'local_agent_id': args.local_agent_id,
                    'model': args.model_name,
                    'prompt_version': args.prompt_version,
                },
                summary={
                    'launch_source': 'python-interactive-example',
                    'experiment_index': spec['index'],
                    'agentspec_variant_index': variant_index,
                    'agent_spec_id': variant_id,
                    'agent_spec_name': variant_name,
                },
                billing_entity_uid=billing_entity_uid,
                account_uid=account_uid,
            )
            experiment_id = str((experiment_payload.get('experiment') or {}).get('id') or '')
            if not experiment_id:
                raise RuntimeError(f'Unexpected experiment response: {experiment_payload}')
            experiment_ids.append((experiment_name, experiment_id, spec['index'], variant_id, variant_name))
            created_experiments += 1
            print(
                f'Created experiment {created_experiments}/{total_experiments}: '
                f'{experiment_id} ({experiment_name})'
            )

    print(f'[3/3] Creating {run_count} run(s) per experiment...')
    if args.no_agent and run_count >= 3:
        print('Note: run 3+ are intentionally marked as failed in this demo to show interactive monitoring of regressions.')
    no_agent_first_run_status = _normalize_no_agent_first_run_status(args.run_status)
    if args.no_agent and no_agent_first_run_status != str(args.run_status).strip().lower():
        print(
            'Synthetic mode uses terminal statuses only; '
            f"coercing first run status from '{args.run_status}' to '{no_agent_first_run_status}' "
            'to avoid watch timeout.'
        )
    run_ids: list[str] = []
    for experiment_name, experiment_id, experiment_index, current_agent_spec_id, current_agent_spec_name in experiment_ids:
        print(f'Creating runs for {experiment_name}...')
        for index in range(run_count):
            run_pass_rate = _pass_rate_for_index(
                _experiment_pass_rate(pass_rate, experiment_index, experiment_id),
                index,
                run_seed=f'{experiment_id}:{index}',
            )
            run_seed = f'interactive:{experiment_id}:{index}:{run_pass_rate:.4f}'
            forced_failed_case_names: set[str] = set()
            # Always surface the same canonical case as the representative
            # interaction so run-to-run comparisons are apples-to-apples: the
            # prompt is identical across runs and only the agent output and
            # pass rate change.
            representative_case = cases[0]
            interaction_prompt = _extract_case_prompt(representative_case)
            interaction_output: Any = None
            interaction_mode = 'synthetic'
            if args.no_agent:
                run_status = no_agent_first_run_status if index == 0 else _run_status_for_index(index)
                intentional_failure = _is_intentional_failure(index, run_status)
                run_seed = f'{run_seed}:{run_status}'
                # Simulation knob for the non-representative cases only; every
                # run metric is graded for real by the evals API further below.
                target_pass_rate: float | None = run_pass_rate
                # Make the synthetic output reflect run quality so the
                # pass-rate delta is easy to interpret: a healthy run returns
                # the expected answer, a regressed/failed run returns a
                # placeholder refusal/empty answer.
                expected_output = representative_case.get('expected_output')
                if intentional_failure or run_pass_rate < 1.0:
                    interaction_output = {
                        'synthetic': True,
                        'text': '(no usable answer — regressed run)',
                        'expected_output': expected_output,
                    }
                else:
                    interaction_output = {
                        'synthetic': True,
                        'text': _synthetic_pass_text(representative_case),
                        'expected_output': expected_output,
                    }
                run_report: dict[str, Any] = {
                    'interaction_mode': 'synthetic',
                    'synthetic': True,
                }
            submitted_code = None

            # Build one simulated agent output per case, then delegate all
            # evaluator execution / grading to the shared evals API. The
            # representative case (index 0) is graded from the *actual* agent
            # output (or the synthetic output for --no-agent runs) so its row
            # matches the interaction shown in the comparison panel.
            # The evals API grades the produced outputs and is the SOLE source
            # of run metrics (pass rate, per-case results, evaluator results).
            # The example only *produces* outputs; it never scores them itself.
            metrics: dict[str, Any] = {}
            if target_pass_rate is not None:
                case_outputs = _build_case_outputs(
                    cases,
                    target_pass_rate,
                    run_status,
                    run_seed=run_seed,
                    forced_failed_case_names=forced_failed_case_names,
                )
                if case_outputs and isinstance(interaction_output, dict):
                    case_outputs[0] = {
                        'text': str(interaction_output.get('text') or '')
                    }
                metrics = evaluate_evalset(evalset_spec, case_outputs)

            if args.no_agent:
                synthetic_usage = _build_synthetic_pydantic_usage(
                    experiment_id=experiment_id,
                    run_index=index,
                    run_pass_rate=run_pass_rate,
                    run_status=run_status,
                    model_name=args.model_name,
                )
                metrics = {
                    **metrics,
                    'pydantic_ai_usage': synthetic_usage,
                }
                existing_report_usage = run_report.get('usage') if isinstance(run_report.get('usage'), dict) else {}
                run_report = {
                    **run_report,
                    'usage': {
                        **existing_report_usage,
                        'pydantic_ai_usage': synthetic_usage,
                    },
                }

            run_payload = client.evals_create_run(
                experiment_id,
                status=run_status,
                metrics=metrics,
                summary={
                    'launch_source': 'python-interactive-example',
                    'run_mode': 'interactive',
                    'run_environment': backend_run_environment,
                    'backend_run_environment': backend_run_environment,
                    'execution_target': args.execution_target,
                    'no_agent': bool(args.no_agent),
                    'synthetic': bool(args.no_agent),
                    'dry_run': bool(args.no_agent),
                    'agent_spec_id': current_agent_spec_id,
                    'agent_spec_name': current_agent_spec_name,
                    'environment_name': args.environment_name,
                    'local_agent_base_url': local_agent_base_url,
                    'local_agent_id': args.local_agent_id,
                    'model': args.model_name,
                    'prompt_version': args.prompt_version,
                    'submission_mode': 'interactive',
                    'experiment_name': experiment_name,
                    'experiment_index': experiment_index,
                    'run_index': index + 1,
                    'scenario': 'live-monitoring',
                    'runtime_name': runtime_name or None,
                    'runtime_termination_policy': 'auto_terminate_after_report' if args.execution_target == 'cloud' else None,
                    'submitted_code': submitted_code,
                    'interaction_mode': interaction_mode,
                    'agent_prompt': interaction_prompt or None,
                    'agent_output': interaction_output,
                },
                report={
                    'note': f'interactive example run {index + 1} ({experiment_name})',
                    'agent_prompt': interaction_prompt or None,
                    'agent_output': interaction_output,
                    **run_report,
                },
                billing_entity_uid=billing_entity_uid,
                account_uid=account_uid,
            )
            run_id = str((run_payload.get('run') or {}).get('id') or '')
            if not run_id:
                raise RuntimeError(f'Unexpected run response: {run_payload}')
            run_ids.append(run_id)
            print(
                f'Launched run {index + 1}/{run_count} for {experiment_name}: '
                f'run_id={run_id}, status={run_status}, '
                f'agent_spec_id={current_agent_spec_id}, agent_id={args.local_agent_id}'
            )

            if args.no_agent:
                try:
                    emitted_pass_rate = run_pass_rate
                    metric_pass_rate = metrics.get('pass_rate') if isinstance(metrics, dict) else None
                    if isinstance(metric_pass_rate, (int, float)):
                        emitted_pass_rate = float(metric_pass_rate)
                    is_synthetic = bool(args.no_agent)
                    evaluator_name = 'synthetic-pass-rate' if is_synthetic else 'interactive-pass-rate'
                    event_source = (
                        'python-interactive-example-synthetic'
                        if is_synthetic
                        else 'python-interactive-example-local-agent'
                    )
                    score_label = 'pass' if run_status != 'failed' else 'fail'
                    client.evals_create_live_event(
                        target_id=experiment_id,
                        target_type='experiment',
                        evaluator_name=evaluator_name,
                        metric_name='pass_rate',
                        value_num=emitted_pass_rate,
                        passed=run_status != 'failed',
                        attributes={
                            'run_id': run_id,
                            'run_mode': 'interactive',
                            'execution_target': args.execution_target,
                            'agent_spec_id': current_agent_spec_id,
                            'source': event_source,
                            'input': interaction_prompt,
                            'prompt': interaction_prompt,
                            'output': interaction_output,
                            'agent_output': interaction_output,
                            'gen_ai.evaluation.target': experiment_id,
                            'gen_ai.evaluation.name': evaluator_name,
                            'gen_ai.evaluation.score.value': emitted_pass_rate,
                            'gen_ai.evaluation.score.label': score_label,
                            'evaluator_input': {
                                'prompt': interaction_prompt,
                                'run_mode': 'interactive',
                                'execution_target': args.execution_target,
                            },
                            'evaluator_output': {
                                'passed': run_status != 'failed',
                                'value_num': emitted_pass_rate,
                                'synthetic': is_synthetic,
                                'agent_output': interaction_output,
                            },
                        },
                        billing_entity_uid=billing_entity_uid,
                        account_uid=account_uid,
                    )
                except Exception as exc:
                    print(f'Warning: unable to write live event for monitoring ({exc})')

            if args.no_agent and intentional_failure:
                print('  Expected demo outcome: this run is intentionally failed.')

    print('[4/4] Watching run status...')
    watch_runs(
        client,
        run_ids,
        account_uid=account_uid,
        timeout_seconds=max(1, args.timeout),
        interval_seconds=max(1, args.interval),
    )

    if args.auto_report:
        try:
            reports = write_eval_reports(
                client,
                evalset_id,
                billing_entity_uid=billing_entity_uid,
                account_uid=account_uid,
            )
            print(f'Auto report written: {reports["markdown_path"]}')
            print(f'Auto report CSV written: {reports["csv_path"]}')
        except Exception as exc:
            print(f'Warning: unable to generate auto report ({exc})')

    print('Done.')
    track_ui_base = (os.environ.get('DATALAYER_CDN_URL') or ui_url).strip().rstrip('/')
    print(f'Track in UI: {track_ui_base}/benchmarks/{evalset_id}')


if __name__ == '__main__':
    main()
