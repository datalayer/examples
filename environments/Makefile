SHELL := /bin/bash

.DEFAULT_GOAL := help

# One environment, from a document to a sandbox running it (PLAN_ENV.md E1-26).
#
#   make env-create            # the environment and its first draft version
#   make env-resolve           # the lock: every package pinned, with hashes
#   make env-build-datalayer   # one build, for the Datalayer variant, followed
#   make env-try               # a trial sandbox of the built version
#   make env-promote           # make it the version new sandboxes start from
#   make env-launch            # a sandbox of the promoted version
#   make env-rollback          # back to the version before, rebuilding nothing
#
# Every target is `datalayer envs`, which is what the pages call too — there is
# no second API for the examples. The plane is chosen the way the evals
# examples choose it: a cloud target unsets every DATALAYER_*_URL so the SDK's
# defaults apply, and a `-local` one pins the localhost URLs, so a shell with
# datalayerrc-prod1 sourced still reaches the plane on this machine.

ENVIRONMENT_FILE ?= geospatial.yaml
# `account/name`: your handle, or an organization's. `make env-create` prints
# the one it made; set ENVIRONMENT to work on an environment you already have.
ENVIRONMENT ?=
VERSION ?= 1
# The variants to build. Datalayer is the one Datalayer builds itself; modal
# and daytona build at their provider with your own account (D-8).
VARIANT ?= datalayer
OUTPUT ?= table
CREDITS_LIMIT ?= 5

LOCAL_PLANE_IAM_URL ?= http://localhost:9700
LOCAL_PLANE_RUNTIMES_URL ?= http://localhost:9500
CLOUD_PLANE := env -u DATALAYER_IAM_URL -u DATALAYER_RUNTIMES_URL
LOCAL_PLANE := env DATALAYER_IAM_URL=$(LOCAL_PLANE_IAM_URL) DATALAYER_RUNTIMES_URL=$(LOCAL_PLANE_RUNTIMES_URL)

ENVS := datalayer envs
OUT := --output $(OUTPUT)

# The version to act on: `<environment>@<number>`, or a version uid in VERSION.
VERSION_REF = $(if $(findstring @,$(VERSION)),$(VERSION),$(if $(strip $(ENVIRONMENT)),$(ENVIRONMENT)@$(VERSION),$(VERSION)))

define NEEDS_ENVIRONMENT
	@if [[ -z "$(strip $(ENVIRONMENT))" ]]; then \
		echo "Set ENVIRONMENT to the environment this acts on, as 'account/name' or its uid:"; \
		echo "  make $@ ENVIRONMENT=ada/geospatial-analysis"; \
		exit 2; \
	fi
endef

.PHONY: help env-ls env-create env-show env-validate env-resolve env-diff \
	env-build-datalayer env-build env-logs env-try env-promote env-launch \
	env-rollback env-versions env-rm walkthrough

help: ## Show the targets, in the order an environment goes through them
	@awk 'BEGIN {FS = ":.*##"; print "Usage: make <target> [ENVIRONMENT=account/name] [VERSION=1]\n"} /^[a-zA-Z_-]+:.*?##/ {printf "%-26s %s\n", $$1, $$2}' $(MAKEFILE_LIST)

# ---- writing it ----------------------------------------------------------------------

env-ls: ## The environments you can launch, platform and your own
	@$(CLOUD_PLANE) $(ENVS) ls $(OUT)

env-create: ## Create the environment and its first draft version from ENVIRONMENT_FILE
	@$(CLOUD_PLANE) $(ENVS) create --file $(ENVIRONMENT_FILE) $(OUT)

env-validate: ## Read the document and report every finding with its field; builds nothing
	$(NEEDS_ENVIRONMENT)
	@$(CLOUD_PLANE) $(ENVS) validate $(VERSION_REF) $(OUT)

env-show: ## The environment: its versions, the promoted one, who owns it
	$(NEEDS_ENVIRONMENT)
	@$(CLOUD_PLANE) $(ENVS) show $(ENVIRONMENT) $(OUT)

env-versions: ## Its versions, newest first
	$(NEEDS_ENVIRONMENT)
	@$(CLOUD_PLANE) $(ENVS) versions $(ENVIRONMENT) $(OUT)

# ---- resolving and building -----------------------------------------------------------

env-resolve: ## Resolve the version into a lock: every package pinned, with hashes
	$(NEEDS_ENVIRONMENT)
	@$(CLOUD_PLANE) $(ENVS) resolve $(VERSION_REF) $(OUT)

env-diff: ## What changed between two versions' locks (VERSION and BEFORE)
	$(NEEDS_ENVIRONMENT)
	@$(CLOUD_PLANE) $(ENVS) diff $(ENVIRONMENT)@$(or $(BEFORE),1) $(VERSION_REF) $(OUT)

env-build-datalayer: ## Build the version for the Datalayer variant, following its log
	$(NEEDS_ENVIRONMENT)
	@$(CLOUD_PLANE) $(ENVS) build $(VERSION_REF) --variant datalayer --follow $(OUT)

env-build: ## Build it for VARIANT (datalayer, modal, daytona, e2b), following its log
	$(NEEDS_ENVIRONMENT)
	@$(CLOUD_PLANE) $(ENVS) build $(VERSION_REF) --variant $(VARIANT) --follow $(OUT)

env-logs: ## A build's log, by its uid in BUILD
	@if [[ -z "$(strip $(BUILD))" ]]; then echo "Set BUILD to the build's uid: make env-logs BUILD=01..."; exit 2; fi
	@$(CLOUD_PLANE) $(ENVS) logs $(BUILD) --follow $(OUT)

# ---- trying it, and making it the one ------------------------------------------------

env-try: ## A trial sandbox of the built version, capped in credits (CREDITS_LIMIT)
	$(NEEDS_ENVIRONMENT)
	@$(CLOUD_PLANE) $(ENVS) try $(VERSION_REF) --credits-limit $(CREDITS_LIMIT) $(OUT)

env-promote: ## Make this version the one new sandboxes start from
	$(NEEDS_ENVIRONMENT)
	@$(CLOUD_PLANE) $(ENVS) promote $(VERSION_REF) $(OUT)

env-launch: ## A sandbox of the promoted version, through the Python SDK
	$(NEEDS_ENVIRONMENT)
	@$(CLOUD_PLANE) ENVIRONMENT=$(ENVIRONMENT) VERSION=$(VERSION) python launch.py

env-rollback: ## Promote the newest ready version older than the promoted one; rebuilds nothing
	$(NEEDS_ENVIRONMENT)
	@$(CLOUD_PLANE) $(ENVS) rollback $(ENVIRONMENT) $(OUT)

env-rm: ## Delete the environment, once no version is promoted and nothing runs it
	$(NEEDS_ENVIRONMENT)
	@$(CLOUD_PLANE) $(ENVS) rm $(ENVIRONMENT) $(OUT)

# ---- the whole way through ------------------------------------------------------------

walkthrough: ## create, resolve, build, try, promote, launch — the flow, in order
	$(NEEDS_ENVIRONMENT)
	@set -euo pipefail; \
	$(MAKE) env-validate ENVIRONMENT=$(ENVIRONMENT) VERSION=$(VERSION); \
	$(MAKE) env-resolve ENVIRONMENT=$(ENVIRONMENT) VERSION=$(VERSION); \
	$(MAKE) env-build-datalayer ENVIRONMENT=$(ENVIRONMENT) VERSION=$(VERSION); \
	$(MAKE) env-try ENVIRONMENT=$(ENVIRONMENT) VERSION=$(VERSION); \
	$(MAKE) env-promote ENVIRONMENT=$(ENVIRONMENT) VERSION=$(VERSION); \
	$(MAKE) env-launch ENVIRONMENT=$(ENVIRONMENT) VERSION=$(VERSION)

# ---- the same, on `plane local` -------------------------------------------------------

env-create-local: ## env-create against the plane on this machine
	@$(LOCAL_PLANE) $(ENVS) create --file $(ENVIRONMENT_FILE) $(OUT)

env-resolve-local: ## env-resolve against the plane on this machine
	$(NEEDS_ENVIRONMENT)
	@$(LOCAL_PLANE) $(ENVS) resolve $(VERSION_REF) $(OUT)

env-build-datalayer-local: ## env-build-datalayer against the plane on this machine
	$(NEEDS_ENVIRONMENT)
	@$(LOCAL_PLANE) $(ENVS) build $(VERSION_REF) --variant datalayer --follow $(OUT)
