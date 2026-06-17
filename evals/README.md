[![Datalayer](https://assets.datalayer.tech/datalayer-25.svg)](https://datalayer.ai)

[![Become a Sponsor](https://img.shields.io/static/v1?label=Become%20a%20Sponsor&message=%E2%9D%A4&logo=GitHub&style=flat&color=1ABC9C)](https://github.com/sponsors/datalayer)

# Datalayer Evals Examples

This folder is a beginner-friendly starting point for running Evals from Python.

It supports multi-agentspec runs out of the box so one evalset can be
executed across several agentspec variants and compared in UI and reports.

It contains two runnable scripts:

- `evals_batch_example.py`: deterministic eval runs with `run_mode=batch`
- `evals_interactive_example.py`: event-style eval runs with `run_mode=interactive`

## Target Matrix

Every `make` target is a combination of three axes:

- **Mode**: `batch` vs `interactive`
- **Lane**: direct endpoints (`--run-environment sdk`) vs proxy
  (`--run-environment sdk-proxy`, suffix `-proxy`)
- **Execution target**: `local` (local agent runtime), `cloud` (cloud runtime),
  or `synthetic` (`--no-agent`, deterministic, no live model calls)

### Batch targets

| Target | Lane | Execution target |
|--------|------|------------------|
| `evals-batch-local` | sdk (direct) | local agent |
| `evals-batch-cloud` | sdk (direct) | cloud |
| `evals-batch-cloud-billable-account` | sdk (direct) | cloud (prompts for API key + billable account) |
| `evals-batch-synthetic` | sdk (direct) | synthetic (no agent) |
| `evals-batch-local-proxy` | sdk-proxy | local agent |
| `evals-batch-cloud-proxy` | sdk-proxy | cloud |
| `evals-batch-synthetic-proxy` | sdk-proxy | synthetic (no agent) |

### Interactive targets

| Target | Lane | Execution target |
|--------|------|------------------|
| `evals-interactive-local` | sdk (direct) | local agent |
| `evals-interactive-cloud` | sdk (direct) | cloud |
| `evals-interactive-synthetic` | sdk (direct) | synthetic (no agent) |
| `evals-interactive-local-proxy` | sdk-proxy | local agent |
| `evals-interactive-cloud-proxy` | sdk-proxy | cloud |
| `evals-interactive-synthetic-proxy` | sdk-proxy | synthetic (no agent) |

The `-billable-account` variant is batch-only: it prompts for an API key and a
billable account UID, then runs the cloud batch target with both flags.

## Codemode vs No-Codemode Comparison

Every target runs **one** evalset that is executed against **both**
agentspecs at once:

- `example-evals` agentspec with codemode enabled
- `example-evals-nocodemode` agentspec with codemode disabled.

There is no separate "no-codemode" target to run — both agentspecs are always
given to the same evalset. This creates one experiment per agentspec inside the
same evalset, so the report and UI directly compare codemode against
no-codemode in:

- UI compare views on https://datalayer.evals
- Mardown and CSV reports created with `datalayer evals report`.

To run a single agentspec instead, pass `--agentspec-id <id>` (or
`AGENTSPEC_ID=<id>` with the Makefile).

## What You Need

- Python 3.10+
- `datalayer_core` installed
- `DATALAYER_API_KEY` exported in your shell

## Learning Path

### 1) Validate Setup With Synthetic Runs (Recommended First)

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

These synthetic targets are the fastest way to verify setup because they do not
depend on live agent responses while still exercising report generation and
multi-agentspec comparison paths.

### 2) Run Against Real Agent Targets

After synthetic runs work, move to agent-backed execution.

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

Batch with interactive API key + billable account prompts:

```bash
make evals-batch-cloud-billable-account
```

Interactive with cloud target:

```bash
make evals-interactive-cloud
```

### 3) Read Results

- In UI: open `https://datalayer.ai/evals` and select the `SDK` tab.
- In CLI: run `datalayer evals report <evalset_id>`.
- Auto-generated files: each example writes `report-<timestamp>.md` and
	`report-<timestamp>.csv` by default.

Report highlights now include:

- experiment overview and rankings (latest, drift, stability)
- within-agentspec pairwise latest-pass deltas
- cross-agentspec pairwise latest-pass deltas
- Heatmaps section (run windows and consecutive deltas)
- per-experiment run timeline + failure diagnostics
- an `Appendix: Run Details` section listing every fetched run; each Run ID
  links straight to the run-details overlay in the UI

## Understanding the Synthetic Content

The two scripts generate **deterministic, self-explanatory evalsets** so you
can learn how comparisons work without depending on live model output.

### The evalsets and their cases

`evals_batch_example.py` builds a **Text Normalization** evalset. Every case is
the same kind of task (normalize text to uppercase), so the suite is coherent
and the expected output is unambiguous:

| Case | Input `text` | Expected `text` | What it checks |
|------|--------------|-----------------|----------------|
| `uppercase-basic` | `hello world` | `HELLO WORLD` | Basic transform |
| `trim-and-uppercase` | `  Paris  ` | `PARIS` | Whitespace trimming |
| `punctuation-preserved` | `hello, world!` | `HELLO, WORLD!` | Punctuation kept |
| `numeric-token-preserved` | `Version 2.1` | `VERSION 2.1` | Numbers preserved |
| `unicode-latin` | `cafe` | `CAFE` | Unicode handling |

`evals_interactive_example.py` builds a **Live Assistant** evalset where each
case checks a different agent behavior (greeting latency, safety refusal,
concise answer, JSON formatting). Each case carries assertion-style
`expected_output` (e.g. `contains`, `label: refusal`, `format: json`).

### How runs and the representative interaction work

- An **experiment** runs the **whole case set** repeatedly. Each run reports a
  `pass_rate` over all cases (`passed / total_cases`).
- To keep run-to-run comparison apples-to-apples, every run now surfaces the
  **same canonical case** (`cases[0]`) as its "representative interaction" in
  the comparison panel. So Run A and Run B show the **same prompt**, and only
  the **agent output** and **pass rate** differ.
- In synthetic (`--no-agent`) mode the representative output reflects run
  quality: a healthy run returns the expected answer, while a regressed/failed
  run returns the un-normalized input (batch) or a placeholder refusal
  (interactive). That is why a lower-`pass_rate` run visibly shows a worse
  output next to the same prompt.

### Reading "Pass-rate delta (A - B)"

In the **Compare Runs Within One Experiment** panel you pick run **A** (the run
you are evaluating) and run **B** (the baseline). The delta is `A - B`, in
percentage points:

- **Positive delta** → A passes more cases than B → an **improvement**.
- **Negative delta** → A passes fewer cases than B → a **regression**.
- **Zero** → no change between the two runs.

Because both runs evaluate the identical case set with the identical
representative prompt, the delta isolates exactly one thing: did quality go up
or down between the two runs. The example deliberately ramps the pass rate down
on later runs so you always see a non-trivial delta (and at least one failing
run) to interpret.

To compare **agentspecs** (codemode vs no-codemode) rather than runs, use the
Comparisons panel below the run panel, or read the cross-agentspec delta tables
in `datalayer evals report`.

## Quick Start Commands

If you want the shortest path:

```bash
make help
make evals-batch-synthetic
make evals-interactive-synthetic
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
- `--agentspec-ids <id1,id2,...>`: run the same evalset across multiple agentspec variants
- `--agentspec-id <id>`: run a single agentspec variant (backward-compatible)
- `--billable-account-uid <account_uid>`: run eval calls in a specific billable account context
- `--synthetic`: run deterministic test behavior without agent calls
- `--clean`: remove previously created resources for the same eval name

To override synthetic target defaults in Makefile-based runs:

- `make evals-batch-synthetic SYNTHETIC_AGENTSPEC_IDS="example-evals,example-evals-nocodemode"`
- `make evals-interactive-synthetic SYNTHETIC_AGENTSPEC_IDS="example-evals,example-evals-nocodemode"`

You can also set a default billing context with:

- `DATALAYER_BILLABLE_ACCOUNT_UID`

## All Makefile Targets

- `make help`: print the list of available targets and short descriptions.

Batch:

- `make evals-batch-local`: batch, sdk (direct) lane, local agent target.
- `make evals-batch-cloud`: batch, sdk (direct) lane, cloud target.
- `make evals-batch-cloud-billable-account`: batch, sdk (direct) lane, cloud target; prompts for API key + billable account UID.
- `make evals-batch-synthetic`: batch, sdk (direct) lane, synthetic no-agent behavior.
- `make evals-batch-local-proxy`: batch, sdk-proxy lane, local agent target.
- `make evals-batch-cloud-proxy`: batch, sdk-proxy lane, cloud target.
- `make evals-batch-synthetic-proxy`: batch, sdk-proxy lane, synthetic no-agent behavior.

Interactive:

- `make evals-interactive-local`: interactive, sdk (direct) lane, local agent target.
- `make evals-interactive-cloud`: interactive, sdk (direct) lane, cloud target.
- `make evals-interactive-synthetic`: interactive, sdk (direct) lane, synthetic no-agent behavior.
- `make evals-interactive-local-proxy`: interactive, sdk-proxy lane, local agent target.
- `make evals-interactive-cloud-proxy`: interactive, sdk-proxy lane, cloud target.
- `make evals-interactive-synthetic-proxy`: interactive, sdk-proxy lane, synthetic no-agent behavior.

All targets run both agentspecs (`example-evals` and `example-evals-nocodemode`)
against one evalset so the report and UI show the codemode-vs-no-codemode
comparison.

## Troubleshooting

- If authentication fails, verify `DATALAYER_API_KEY` is set.
- If local/proxy runs fail, start required local services first.
- If cloud runs fail, check runtime capacity and service connectivity.

## Related Docs

- UI docs overview: `https://datalayer.ai/docs/evals`
- Evals examples repository: https://github.com/datalayer/examples/tree/main/evals
