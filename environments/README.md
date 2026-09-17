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

## What does not work yet

The registry, the pages, the CLI and the launch of a promoted version are in
place. The resolve and the build now run on r1: `env-build-datalayer` resolves
the lock, builds the image and pushes it. **The scan that follows does not
finish yet** — the build ends `failed` with `DL_ENV_PROVIDER_ERROR` while the
registry refuses the scan read — so no version reaches `ready`, and `env-try`,
`env-promote` and `env-launch` have nothing of yours to use. Until it does,
`env-create`, `env-validate`, `env-show`, `env-versions`, `env-rollback` and
`env-rm` are the targets that do their whole job. `env-resolve` still answers
`501`: a version is resolved by its build, not on its own.

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
