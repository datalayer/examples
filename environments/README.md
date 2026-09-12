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

Editing the document makes the **next** version — `datalayer envs edit
$ENVIRONMENT@1 --file geospatial.yaml` — and a version never changes once it
is built, so a sandbox started an hour ago keeps running what it started with.
`make env-rollback ENVIRONMENT=$ENVIRONMENT` promotes the version before,
rebuilding nothing.

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
place. **The resolve and the build are not deployed**: `env-resolve` answers
`501`, and a queued build refuses with `DL_ENV_CAPABILITY_UNSUPPORTED`, naming
what is missing. Until they are, `env-create`, `env-validate`, `env-show`,
`env-versions`, `env-promote`, `env-rollback` and `env-rm` are the targets that
do their whole job.

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
