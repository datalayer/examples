[![Datalayer](https://assets.datalayer.tech/datalayer-25.svg)](https://datalayer.ai)

[![Become a Sponsor](https://img.shields.io/static/v1?label=Become%20a%20Sponsor&message=%E2%9D%A4&logo=GitHub&style=flat&color=1ABC9C)](https://github.com/sponsors/datalayer)

# Datalayer Evals Examples

This folder is a beginner-friendly starting point for running Evals from Python.

It contains two runnable scripts:

- `evals_batch_example.py`: deterministic eval runs with `run_mode=batch`
- `evals_interactive_example.py`: event-style eval runs with `run_mode=interactive`

## What You Need

- Python 3.10+
- `datalayer_core` installed
- `DATALAYER_API_KEY` exported in your shell

## Quick Start

From this folder:

```bash
make help
```

Run one batch example:

```bash
make evals-batch-synthetic
```

Run one interactive example:

```bash
make evals-interactive-synthetic
```

These synthetic targets are the easiest way to verify your setup first.

## Next: Run Against Agent Targets

After synthetic runs work, you can try agent-backed runs.

Batch with local target:

```bash
make evals-batch-local
```

Interactive with local target:

```bash
make evals-interactive-local
```

Batch with cloud target:

```bash
make evals-batch-cloud
```

Interactive with cloud target:

```bash
make evals-interactive-cloud
```

## Useful Flags

You can also run scripts directly and pass options.

Batch example:

```bash
python evals_batch_example.py --help
```

Interactive example:

```bash
python evals_interactive_example.py --help
```

Common flags you will use:

- `--eval-name <name>`: set the evalset name
- `--run-environment sdk|sdk-proxy`: choose direct SDK or local proxy endpoints
- `--execution-target local|cloud`: choose where the agent execution happens
- `--billable-account-uid <account_uid>`: run eval calls in a specific billable account context
- `--synthetic`: run deterministic test behavior without agent calls
- `--clean`: remove previously created resources for the same eval name

You can also set a default billing context with:

- `DATALAYER_BILLABLE_ACCOUNT_UID`

## All Makefile Targets

- `make help`: print the list of available targets and short descriptions.
- `make evals-batch-local`: run batch mode in sdk lane with a local execution target.
- `make evals-batch-cloud`: run batch mode in sdk lane with a cloud execution target.
- `make evals-batch-local-proxy`: run batch mode in sdk-proxy lane with a local execution target.
- `make evals-batch-cloud-proxy`: run batch mode in sdk-proxy lane with a cloud execution target.
- `make evals-batch-synthetic`: run batch mode in sdk lane with synthetic no-agent behavior.
- `make evals-batch-synthetic-proxy`: run batch mode in sdk-proxy lane with synthetic no-agent behavior.
- `make evals-interactive-local`: run interactive mode in sdk lane with a local execution target.
- `make evals-interactive-cloud`: run interactive mode in sdk lane with a cloud execution target.
- `make evals-interactive-local-proxy`: run interactive mode in sdk-proxy lane with a local execution target.
- `make evals-interactive-cloud-proxy`: run interactive mode in sdk-proxy lane with a cloud execution target.
- `make evals-interactive-synthetic`: run interactive mode in sdk lane with synthetic no-agent behavior.
- `make evals-interactive-synthetic-proxy`: run interactive mode in sdk-proxy lane with synthetic no-agent behavior.

## Where To See Results

- In UI: open `https://datalayer.ai/evals` and select the `SDK` tab.
- In CLI: use `datalayer evals report <evalset_id>`.
- Auto-generated files: by default, each example writes `report-<timestamp>.md` and `report-<timestamp>.csv` at the end of the run.
- Markdown report: contains evalset summary, per-experiment comparison metrics, run deltas, and failure diagnostics when present.
- CSV report: contains run-level rows that are easy to filter, diff, and ingest into spreadsheets or dashboards.

## Troubleshooting

- If authentication fails, verify `DATALAYER_API_KEY` is set.
- If local/proxy runs fail, start required local services first.
- If cloud runs fail, check runtime capacity and service connectivity.

## Related Docs

- UI docs overview: `https://datalayer.ai/docs/evals`
- Evals examples repository: https://github.com/datalayer/examples/tree/main/evals
