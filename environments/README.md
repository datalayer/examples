[![Datalayer](https://assets.datalayer.tech/datalayer-25.svg)](https://datalayer.ai)

[![Become a Sponsor](https://img.shields.io/static/v1?label=Become%20a%20Sponsor&message=%E2%9D%A4&logo=GitHub&style=flat&color=1ABC9C)](https://github.com/sponsors/datalayer)

# Datalayer Environments Example

One environment, from a document to a sandbox running it.

A **User Environment** is the Python version, the packages, a few files and
the resources your Code Sandboxes start with. You write it once; it is
resolved once into a lock, and every variant builds from that same lock, so
the Datalayer sandbox and the Modal one install the same versions.

This folder is the smallest complete example:

- [`geospatial.yaml`](./geospatial.yaml) — the environment, commented field by
  field. Every field is in the
  [specification reference](https://datalayer.ai/docs/environments-spec).
- [`Makefile`](./Makefile) — one target per step, each of them `datalayer envs`,
  which is what the pages call too.
- [`launch.py`](./launch.py) — a sandbox of a version, through the Python SDK.

## What you need

- `datalayer` on your `PATH`, from `agent-runtimes`, and `DATALAYER_API_KEY`
  set (or `datalayer login`).
- Nothing else: the resolve and the build run on the platform, not here.

## The flow

```bash
make env-create                                  # the environment and its first draft
# it prints `account/name`; use that below
export ENVIRONMENT=ada/geospatial-analysis

make env-validate ENVIRONMENT=$ENVIRONMENT       # the document read, every finding with its field
make env-resolve  ENVIRONMENT=$ENVIRONMENT       # the lock: every package pinned, with hashes
make env-build-datalayer ENVIRONMENT=$ENVIRONMENT  # one build, its log followed
make env-try      ENVIRONMENT=$ENVIRONMENT       # a trial sandbox, capped in credits
make env-promote  ENVIRONMENT=$ENVIRONMENT       # new sandboxes start from this version now
make env-launch   ENVIRONMENT=$ENVIRONMENT       # a sandbox of it
```

`make walkthrough ENVIRONMENT=$ENVIRONMENT` runs those in order.

### On Daytona, in your own account

A build for Daytona runs in **your** Daytona organization, with the key you
keep as a Datalayer secret — never a shared account — and makes a snapshot
there, sized by the version's size class:

```bash
datalayer secrets create DAYTONA_API_KEY "my Daytona key" <your Daytona key>
make env-build-daytona ENVIRONMENT=$ENVIRONMENT  # the snapshot, built from the same lock
```

It builds from the lock the Datalayer build used, so both install the same
package versions, and the version's package report shows them side by side.

### Other sources

The same targets build the other examples, each named with `ENVIRONMENT_FILE`
when it is created:

| File | Source | What the lock covers |
|---|---|---|
| `geospatial.yaml` | a package list | everything |
| `requirements.yaml` | a `requirements.txt` | everything, solved the way a package list is |
| `pyproject.yaml`, written by `make env-spec-pyproject` | `pyproject/pyproject.toml` and the `uv.lock` you made | everything, as your `uv.lock` says: it is checked and exported, never solved again |
| `conda-geospatial.yaml` | a conda `environment.yml`, `gdal` from conda-forge | the conda layer by hash, the pip layer by version |
| `gpu-torch.yaml` | PyTorch on the CUDA channel, an RTX 4090 on Daytona (`make env-build-gpu-daytona`) | everything |
| `gpu-torch-modal.yaml` | the same, on a Modal L4 (`make env-build-gpu-modal`) | everything |
| `dockerfile.yaml` | your Dockerfile, on an approved base | the declared packages and the kernel stack; what the Dockerfile installs is not locked |
| `image-import.yaml` | an existing image | does not build yet |

A `uv.lock` of your own is never merged with Datalayer's protected pins, so it
has to lock them itself, at the versions the platform needs, or it is refused
naming the one it lacks. `pyproject/pyproject.toml` lists them. One of them,
`jupyter-server==2.21.0+datalayer.1`, is Datalayer's fork, and no package index
serves it: the project takes it from its release by URL
(`[tool.uv.sources]`), which is also what makes `uv` record its hash.

```bash
cd pyproject && uv lock && cd ..
make env-spec-pyproject
make env-create ENVIRONMENT_FILE=pyproject.yaml
```

This document declares `modal` as an optional variant and nothing here builds
it, so the version settles **partially ready** rather than ready — which is
what it should be: the Datalayer variant is built and runs, and nobody has
said anything about Modal. A partially ready version is promoted only with
each unavailable variant named, so nobody promotes one by accident:
`ACKNOWLEDGE` carries them, and defaults to this document's own.

```bash
make env-promote ENVIRONMENT=$ENVIRONMENT ACKNOWLEDGE=modal
```

Until a version is promoted, `make env-launch` has nothing to launch.

A name belongs to one environment per owner, so a second `make env-create`
refuses with `DL_ENV_CONFLICT` rather than making another. To run the flow
again beside the one you have, copy the document, change its
`metadata.name`, and point the target at it:

```bash
make env-create ENVIRONMENT_FILE=my-copy.yaml
```

Editing the document makes the **next** version — `datalayer envs edit
$ENVIRONMENT@1 --file geospatial.yaml` — and a version never changes once it
is built, so a sandbox started an hour ago keeps running what it started with.
`make env-rollback ENVIRONMENT=$ENVIRONMENT` promotes the version before,
rebuilding nothing.

## Making it public

A promoted version can go into the public Library, where anyone can read it,
launch it or fork it:

```bash
make env-publish     ENVIRONMENT=$ENVIRONMENT   # everything that becomes public, listed
make env-publication ENVIRONMENT=$ENVIRONMENT   # what it made public, and whether it still is
make env-unpublish   ENVIRONMENT=$ENVIRONMENT   # withdraw it
```

`env-publish` prints the whole list rather than a confirmation: the spec, the
lock and its package count, the variants and their artifact references, the
scan's verdict, the SBOM, the licenses and the README. A version is made
public once and the snapshot is frozen at that moment, so the list is the
thing to read before saying yes.

Publishing is refused unless every input is public — no build secret, only
public indexes, an approved base, and a Datalayer artifact that passed its
scan. The refusal names which of those it was.

Withdrawing keeps the snapshot, so `env-publish` afterwards restores exactly
what was public, and sandboxes already running the version are untouched.

## How it is going

```bash
make env-slos          # the SLO table: target, measured, and whether one meets the other
```

Every build and every launch is measured, and `slos.py` reads those series
back from the telemetry API — resolve and build latency, the build success
rate, how long a launch takes to turn a version into an immutable reference.
It answers for the whole plane rather than for your environment: the numbers
are the platform's, and yours are in them.

`make help` lists every target. Each takes `OUTPUT=json` or `OUTPUT=yaml`, so
the same commands read well in a terminal and pipe into a script.

## What costs what

A sandbox burns the rate of the size class its version names, per second:
`small` 0.0008, `medium` 0.0016, `large` 0.0032 credits. A build is metered
too, and builds are limited while the feature is in preview — two at once,
120 build-minutes a day, ten versions kept, 50 GiB stored — so a build over a
limit is refused by name before anything is queued.

## What it reaches, and what is left

Builds run on the platform. For `datalayer` the lock is resolved, the image
built, pushed, scanned and signed, and the version reaches `ready`; for
Daytona and Modal the same lock is built in your own account and tried there
before the version is ready. A GPU version builds for Modal
(`gpu-torch-modal.yaml`) or Daytona (`gpu-torch.yaml`, which needs paid GPU
credit at Daytona: its free credit does not cover GPU sandboxes).

A build reaches only the hosts packages come from: PyPI and PyTorch's wheels,
the public conda channels, the Ubuntu and Debian snapshot mirrors, GitHub
releases and the image registries. An index or a channel on a host of your
own fails the build with `403` until the platform allows that host.

The same targets run against `plane local` — every service on this machine —
with the `-local` suffix: `make env-create-local`, `env-resolve-local`,
`env-build-datalayer-local`.

## Where the rest is written down

- [User Environments](https://datalayer.ai/docs/environments-user) — the whole
  flow, what each refusal means, and what is not available yet.
- [Environment specification](https://datalayer.ai/docs/environments-spec) —
  every field, generated from the schema.
- [Environments](https://datalayer.ai/docs/environments) — platform
  environments, and what an environment is.
