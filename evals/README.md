[![Datalayer](https://assets.datalayer.tech/datalayer-25.svg)](https://datalayer.ai)

[![Become a Sponsor](https://img.shields.io/static/v1?label=Become%20a%20Sponsor&message=%E2%9D%A4&logo=GitHub&style=flat&color=1ABC9C)](https://github.com/sponsors/datalayer)

# Datalayer Evals Examples

This folder is a beginner-friendly starting point for running Evals from Python.

It supports multi-agentspec runs out of the box so one evalset can be
executed across several agentspec variants and compared in UI and reports.

It contains two runnable scripts:

- `evals_batch_example.py`: deterministic eval runs with `run_mode=batch`
- `evals_interactive_example.py`: event-style eval runs with `run_mode=interactive`

Each script loads its evalset from a colocated JSON spec file:

- `evals_batch.evalset.json`
- `evals_interactive.evalset.json`

Both scripts now include first-class evaluator configuration in the evalset payload:

- per-case `evaluators` arrays (for example
  `{"name": "equals_expected", "arguments": {}}`)
- evalset-level `evalset_evaluators`
- evalset-level `report_evaluators`

This keeps evaluator configuration explicit and aligned with Pydantic evaluator
semantics across case-level and global/report-level checks.

You can point either script at a custom spec with:

- `--evalset-spec-file <path-to.evalset.json>`

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

### Reusable runner

The bespoke cloud path in `evals_batch_example.py` simulates the
non-representative cases to produce a rich comparison dashboard. When you want a
genuine end-to-end run instead, pass `--use-runner` (or use the
`evals-batch-cloud-runner` / `evals-batch-local-runner` targets) to delegate
execution to the shared `datalayer_core.evals.execute_evalset_spec` runner. It
creates one evalset, one experiment per agentspec, executes **every** case for
real against a cloud runtime (one per agentspec) or a local `agent-runtimes`
server, grades the outputs with the evals API, persists one run per execution,
and tears the execution resources down afterwards:

```bash
# Cloud runtimes (one per agentspec):
make evals-batch-cloud-runner

# Local agent-runtimes server (auto-started):
make evals-batch-local-runner

# or directly:
python evals_batch_example.py --execution-target cloud --use-runner \
  --agentspec-ids example-evals,example-evals-nocodemode
python evals_batch_example.py --execution-target local --use-runner \
  --auto-start-local-agent-runtime \
  --agentspec-ids example-evals,example-evals-nocodemode
```

`--use-runner` requires `--execution-target cloud` or `local` and cannot be
combined with `--synthetic` or inline `--agentspec`.


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
- a **Per-Case Outcomes** section: pass rate for every case across all runs,
  plus a per-agentspec breakdown (codemode vs no-codemode)
- within-agentspec pairwise latest-pass deltas
- cross-agentspec pairwise latest-pass deltas
- Heatmaps section (run windows and consecutive deltas)
- per-experiment run timeline + failure diagnostics
- an `Appendix: Run Details` section listing every fetched run; each run block
  now includes a **Per-Case Results** table (pass/fail, score, category,
  difficulty) and each Run ID links straight to the run-details overlay in the UI

The CSV report mirrors this: in addition to `experiment` and `run` rows it now
emits one `case` row per case per run (`case_name`, `case_status`, `case_score`,
`case_category`, `case_difficulty`) so you can pivot results per case.

Canonical semantics for per-case scores, case-vs-report evaluator modeling, and
agent-backed vs synthetic interpretation now live in the UI docs:
[Evals](https://datalayer.ai/docs/evals).

## Understanding the Synthetic Content

The two scripts generate **deterministic, self-explanatory evalsets** so you
can learn how comparisons work without depending on live model output.

### How cases, runs, and experiments relate

Evals are organized as a strict hierarchy. Reading it top-down:

```text
Evalset (e.g. "Text Normalization")
└── Cases               ← the fixed test inputs + expected outputs (shared by every run)
    │                      e.g. uppercase-basic, trim-and-uppercase, unicode-latin
    │
    └── Experiment       ← one agentspec/config under test (e.g. codemode vs no-codemode)
        └── Run          ← one execution of ALL cases at a point in time
            └── Case result   ← pass/fail + score for ONE case in that run
```

Key relationships:

- A **case** is a single test (`inputs` + `expected_output` + `metadata`). The
  set of cases is defined once on the evalset and **does not change** between
  runs — that is what makes runs comparable.
- An **experiment** pins one agentspec/configuration. Every target here creates
  experiments for **two** agentspecs (`example-evals` and
  `example-evals-nocodemode`) so you can compare codemode vs no-codemode.
- A **run** executes the **whole case set** once. Its `pass_rate` is
  `passed_cases / total_cases`, i.e. an aggregate **over the cases**.
- A **case result** is the per-case outcome inside a run: did *this* case pass,
  what score did it get. Aggregating case results **across runs** tells you
  which cases are reliable and which ones regress.

So "per-case metrics" are simply case results rolled up along two axes:
**down a column** (one case across many runs → is it flaky?) and **across a
row** (all cases in one run → which case dragged the pass rate down?).

### The evalsets and their cases

`evals_batch.evalset.json` defines a **Text Normalization** evalset. Every case is
the same kind of task (normalize text to uppercase), so the suite is coherent
and the expected output is unambiguous:

| Case | Input `text` | Expected `text` | What it checks |
|------|--------------|-----------------|----------------|
| `uppercase-basic` | `hello world` | `HELLO WORLD` | Basic transform |
| `trim-and-uppercase` | `  Paris  ` | `PARIS` | Whitespace trimming |
| `punctuation-preserved` | `hello, world!` | `HELLO, WORLD!` | Punctuation kept |
| `numeric-token-preserved` | `Version 2.1` | `VERSION 2.1` | Numbers preserved |
| `unicode-latin` | `cafe` | `CAFE` | Unicode handling |

`evals_interactive.evalset.json` defines a **Live Assistant** evalset where each
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
- In **real (agent-backed)** runs the representative interaction is actually
  executed against the agent. Its real output is then graded against the
  representative case (`_output_fails_case(...)`): if the run failed or the
  output does not satisfy the case, that case is forced to fail in the per-case
  table. This keeps the representative row coherent with the output shown in the
  comparison panel — you never see a "pass" row next to an output that is
  clearly wrong.

### How per-case results are generated (synthetic)

Every run also stores a **per-case breakdown** under `metrics.case_results`, so
the UI run-details overlay and the report show *which* cases passed — not just
the aggregate pass rate. The synthetic generator is deliberately didactic:

- Each case gets a deterministic **difficulty weight** derived from its
  metadata (`difficulty` for batch: easy/medium; `priority` for interactive:
  high/critical/...). Higher weight = harder.
- For a given run pass rate, the number of passing cases tracks that pass rate,
  and the **hardest cases fail first**. So when a run regresses, you can see the
  difficult cases drop out before the easy ones.
- `passed`, `failed`, `total_cases`, and `avg_score` on the run are recomputed
  from these per-case outcomes, so the aggregate always agrees with the table.

This makes the relationship concrete: open two runs of the same experiment and
the per-case tables show the *same cases* with different pass/fail columns — the
exact rows that explain the pass-rate delta.

### Where case scores come from (and why they are stable across runs)

The per-case `score` is generated in `_build_case_results(...)` in
`evals_batch_example.py` (and the matching function in
`evals_interactive_example.py`). It is a **pure function of the case and its
pass/fail outcome**:

- a passing case scores high: `0.82 + (1 - difficulty_weight) * 0.15 + offset`
- a failing case scores low: `0.45 - difficulty_weight * 0.25 + offset`

The `difficulty_weight` and the small `offset` are keyed **only on the case
name** (via `_case_weight(...)` and the `case-score` hash), not on the run. The
practical consequence:

- The **same case keeps the same score in every run** while its pass/fail
  status does not change.
- A case's score only moves when its **outcome flips** (pass→fail or fail→pass),
  because the pass and fail formulas are different. That flip is driven purely
  by the run's pass rate (the example ramps the pass rate down on later runs),
  not by random per-run noise.

So if you compare two runs and see the *same* case with two *different* scores,
that case changed pass/fail status between those runs. If a case stays passing
(or stays failing) in both runs, its score is identical. This is intentional:
the synthetic data is fully reproducible, so run-to-run deltas always trace back
to a concrete pass/fail change rather than to randomness.

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
- `--evalset-spec-file <path>`: load schema/cases/evaluators from a JSON evalset spec file
- `--run-environment sdk|sdk-proxy`: choose direct SDK or local proxy endpoints
- `--execution-target local|cloud`: choose where the agent execution happens
- `--agent-spec-ids <id1,id2,...>`: run the same evalset across multiple agentspec variants
- `--agent-spec-id <id>`: run a single agentspec variant
- `--billable-account-uid <account_uid>`: optional billable account context; omit to use the default account context
- `--synthetic`: run deterministic test behavior without agent calls

To override synthetic target defaults in Makefile-based runs:

- `make evals-batch-synthetic SYNTHETIC_AGENTSPEC_IDS="example-evals,example-evals-nocodemode"`
- `make evals-interactive-synthetic SYNTHETIC_AGENTSPEC_IDS="example-evals,example-evals-nocodemode"`

You can optionally set a default billing context with:

- `DATALAYER_BILLABLE_ACCOUNT_UID`

## All Makefile Targets

- `make help`: print the list of available targets and short descriptions.

Batch:

- `make evals-batch-local`: batch, sdk (direct) lane, local agent target.
- `make evals-batch-cloud`: batch, sdk (direct) lane, cloud target.
- `make evals-batch-cloud-billable-account`: batch, sdk (direct) lane, cloud target; prompts for API key + optional billable account UID (press Enter to skip billing override).
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
