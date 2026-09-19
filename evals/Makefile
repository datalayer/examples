SHELL := /bin/bash

.DEFAULT_GOAL := help

# Every target is named on three axes:
#
#   make evals-<batch|interactive>-<cloudagent|localagent|synthetic>-<cloudplane|localplane>
#
# - mode:   batch runs the fixed, versioned tasks; interactive evaluates live traffic over a window
# - agent:  cloudagent runs on a pool of Datalayer sandboxes (a launch the platform executes);
#           localagent runs on an agent-runtimes server on this machine;
#           synthetic runs no agent at all — deterministic results, to see the reports and the UI
# - plane:  cloudplane is the Datalayer services (the SDK defaults);
#           localplane is `plane local`, every service on localhost, the durable engine `none`
#
# The plane is chosen by construction. cloudplane targets unset every DATALAYER_*_URL so the
# SDK defaults apply; localplane targets pin LOCAL_PLANE_*_URL — names no cluster rc sets — so a
# shell with datalayerrc-prod1 sourced still sends them to the plane on this machine.

LOCAL_PLANE_IAM_URL ?= http://localhost:9700
LOCAL_PLANE_RUNTIMES_URL ?= http://localhost:9500
LOCAL_PLANE_AI_AGENTS_URL ?= http://localhost:4400
LOCAL_PLANE_UI_URL ?= http://localhost:3063
LOCAL_PLANE := env DATALAYER_UI_URL=$(LOCAL_PLANE_UI_URL) DATALAYER_CDN_URL=$(LOCAL_PLANE_UI_URL) DATALAYER_IAM_URL=$(LOCAL_PLANE_IAM_URL) DATALAYER_RUNTIMES_URL=$(LOCAL_PLANE_RUNTIMES_URL) DATALAYER_AI_AGENTS_URL=$(LOCAL_PLANE_AI_AGENTS_URL)
LOCAL_PLANE_FLAGS := --plane local --iam-url $(LOCAL_PLANE_IAM_URL) --runtimes-url $(LOCAL_PLANE_RUNTIMES_URL) --ai-agents-url $(LOCAL_PLANE_AI_AGENTS_URL) --ui-url $(LOCAL_PLANE_UI_URL)
CLOUD_PLANE := env -u DATALAYER_IAM_URL -u DATALAYER_RUNTIMES_URL -u DATALAYER_AI_AGENTS_URL
CLOUD_PLANE_FLAGS := --plane cloud

# The local agent: an agent-runtimes server on this machine, started when none answers.
AGENT_RUNTIME_BASE_URL ?= http://localhost:8765
AGENT_RUNTIME_ID ?= default
LOCAL_AGENT_LOG_LEVEL ?= info
LOCAL_AGENT_FLAGS := --execution-target local --auto-start-local-agent-runtime --local-agent-log-level $(LOCAL_AGENT_LOG_LEVEL) --local-agent-base-url $(AGENT_RUNTIME_BASE_URL) --local-agent-id $(AGENT_RUNTIME_ID)
# The cloud agent: a launch the platform executes on a pool of sandboxes, capped in credits.
# CLOUD_CONCURRENCY is the pool per experiment. A local plane serves each service from one
# process over port-forwards and its IAM answers reservations one at a time, so a pool of
# four per experiment made the operator time out on IAM; one per experiment is what it
# keeps up with (LOCAL_PLANE_CONCURRENCY), the cloud takes the full pool.
CLOUD_CREDITS_LIMIT ?= 100
CLOUD_CONCURRENCY ?= 4
LOCAL_PLANE_CONCURRENCY ?= 1
CLOUD_AGENT_FLAGS := --execution-target cloud --cloud-credits-limit $(CLOUD_CREDITS_LIMIT) --local-agent-base-url $(AGENT_RUNTIME_BASE_URL) --local-agent-id $(AGENT_RUNTIME_ID)
CLOUD_AGENT_CLOUD_PLANE_FLAGS := $(CLOUD_AGENT_FLAGS) --cloud-concurrency $(CLOUD_CONCURRENCY)
CLOUD_AGENT_LOCAL_PLANE_FLAGS := $(CLOUD_AGENT_FLAGS) --cloud-concurrency $(LOCAL_PLANE_CONCURRENCY)

AGENT_EVALS_MODE ?= interactive
AGENT_EVALS_EMIT_LIVE_EVENTS ?= true
LOCAL_AGENT_ENV := AGENT_EVALS_MODE=$(AGENT_EVALS_MODE) AGENT_EVALS_EMIT_LIVE_EVENTS=$(AGENT_EVALS_EMIT_LIVE_EVENTS)

EVAL_WATCH_TIMEOUT ?= 60
EVAL_WATCH_INTERVAL ?= 2
WATCH_FLAGS := --timeout $(EVAL_WATCH_TIMEOUT) --interval $(EVAL_WATCH_INTERVAL)

SYNTHETIC ?= 0
SYNTHETIC_FLAG := $(if $(filter 1 true yes on,$(SYNTHETIC)),--synthetic,)
SYNTHETIC_AGENTSPEC_IDS ?= example-evals,example-evals-nocodemode
SYNTHETIC_AGENTSPEC_IDS_FLAG := $(if $(strip $(SYNTHETIC_AGENTSPEC_IDS)),--agentspec-ids $(SYNTHETIC_AGENTSPEC_IDS),)
BATCH_EVALSET_SPEC_FILE ?= evals_batch.evalset.json
INTERACTIVE_EVALSET_SPEC_FILE ?= evals_interactive.evalset.json
BATCH_EVALSET_SPEC_FLAG := $(if $(strip $(BATCH_EVALSET_SPEC_FILE)),--evalset-spec-file $(BATCH_EVALSET_SPEC_FILE),)
INTERACTIVE_EVALSET_SPEC_FLAG := $(if $(strip $(INTERACTIVE_EVALSET_SPEC_FILE)),--evalset-spec-file $(INTERACTIVE_EVALSET_SPEC_FILE),)

# Optional agent spec selection for cloud runtimes.
# Multi-agent-spec defaults are handled by the scripts when none is provided.
# Examples:
#   make evals-batch-cloudagent-cloudplane AGENTSPEC_ID=example-evals
#   make evals-batch-cloudagent-cloudplane AGENTSPEC_IDS="example-evals,example-evals-nocodemode"
#   make evals-batch-cloudagent-cloudplane AGENTSPEC=./my-agent.yaml
AGENTSPEC ?=
AGENTSPEC_ID ?=
AGENTSPEC_IDS ?=
AGENTSPEC_FLAG := $(if $(strip $(AGENTSPEC)),--agentspec $(AGENTSPEC),)
AGENTSPEC_ID_FLAG := $(if $(strip $(AGENTSPEC_ID)),--agentspec-id $(AGENTSPEC_ID),)
AGENTSPEC_IDS_FLAG := $(if $(strip $(AGENTSPEC_IDS)),--agentspec-ids $(AGENTSPEC_IDS),)
AGENTSPEC_FLAGS := $(AGENTSPEC_FLAG) $(AGENTSPEC_ID_FLAG) $(AGENTSPEC_IDS_FLAG)

BATCH := python evals_batch_example.py --run-status completed $(WATCH_FLAGS) $(BATCH_EVALSET_SPEC_FLAG)
INTERACTIVE := python evals_interactive_example.py --run-status running $(WATCH_FLAGS) $(INTERACTIVE_EVALSET_SPEC_FLAG)
INTERACTIVE_SYNTHETIC := python evals_interactive_example.py --run-status completed $(WATCH_FLAGS) $(INTERACTIVE_EVALSET_SPEC_FLAG)

# Asks for the API key (hidden) and an optional billing entity, then runs `$(1)` with both.
define WITH_BILLING_ENTITY
	@default_api_key="$${DATALAYER_API_KEY:-}"; \
	if [[ -n "$$default_api_key" ]]; then \
		read -s -p "API key [hidden; press Enter to use DATALAYER_API_KEY]: " api_key; \
		echo; \
	else \
		read -s -p "API key: " api_key; \
		echo; \
	fi; \
	api_key="$${api_key:-$$default_api_key}"; \
	default_billing_entity_uid="$${DATALAYER_BILLING_ENTITY_UID:-}"; \
	read -e -i "$$default_billing_entity_uid" -p "Billing Entity uid (optional) [$$default_billing_entity_uid]: " billing_entity_uid; \
	billing_entity_uid="$${billing_entity_uid:-$$default_billing_entity_uid}"; \
	billing_flag=""; \
	if [[ -n "$$billing_entity_uid" ]]; then billing_flag="--billing-entity-uid $$billing_entity_uid"; fi; \
	if [[ -z "$$api_key" ]]; then echo "Missing API key. Set DATALAYER_API_KEY or enter one."; exit 1; fi; \
	$(1) --api-key "$$api_key" $$billing_flag
endef

.PHONY: help \
	evals-batch-cloudagent-cloudplane evals-batch-cloudagent-cloudplane-simple evals-batch-cloudagent-cloudplane-billing-entity evals-batch-cloudagent-localplane \
	evals-batch-localagent-cloudplane evals-batch-localagent-localplane evals-batch-localagent-localplane-billing-entity \
	evals-batch-synthetic-cloudplane evals-batch-synthetic-localplane \
	evals-interactive-cloudagent-cloudplane evals-interactive-cloudagent-localplane \
	evals-interactive-localagent-cloudplane evals-interactive-localagent-localplane \
	evals-interactive-synthetic-cloudplane evals-interactive-synthetic-localplane

help: ## Show available targets: make evals-<batch|interactive>-<cloudagent|localagent|synthetic>-<cloudplane|localplane>
	@awk 'BEGIN {FS = ":.*##"; print "Usage: make evals-<batch|interactive>-<cloudagent|localagent|synthetic>-<cloudplane|localplane>\n"} /^[a-zA-Z_-]+:.*?##/ {printf "%-56s %s\n", $$1, $$2}' $(MAKEFILE_LIST)

# ---- batch, cloud agent --------------------------------------------------------------------

evals-batch-cloudagent-cloudplane: ## Batch on a pool of Datalayer sandboxes, against the Datalayer services (SYNTHETIC=1 for synthetic results)
	@$(CLOUD_PLANE) $(BATCH) $(CLOUD_PLANE_FLAGS) $(CLOUD_AGENT_CLOUD_PLANE_FLAGS) $(AGENTSPEC_FLAGS) $(SYNTHETIC_FLAG)

evals-batch-cloudagent-cloudplane-simple: ## The smallest cloud batch run: evals_batch_simple.py, one agentspec, no reports
	@$(CLOUD_PLANE) python evals_batch_simple.py

evals-batch-cloudagent-cloudplane-billing-entity: ## Same as evals-batch-cloudagent-cloudplane, asking for the API key and a billing entity
	$(call WITH_BILLING_ENTITY,$(CLOUD_PLANE) $(BATCH) $(CLOUD_PLANE_FLAGS) $(CLOUD_AGENT_CLOUD_PLANE_FLAGS) $(AGENTSPEC_FLAGS) $(SYNTHETIC_FLAG))

evals-batch-cloudagent-localplane: ## Batch on a pool of sandboxes launched through `plane local` on this machine
	@$(LOCAL_PLANE) $(BATCH) $(LOCAL_PLANE_FLAGS) $(CLOUD_AGENT_LOCAL_PLANE_FLAGS) $(AGENTSPEC_FLAGS) $(SYNTHETIC_FLAG)

# ---- batch, local agent --------------------------------------------------------------------

evals-batch-localagent-cloudplane: ## Batch on an agent-runtimes server on this machine, results written to the Datalayer services
	@$(CLOUD_PLANE) $(LOCAL_AGENT_ENV) $(BATCH) $(CLOUD_PLANE_FLAGS) $(LOCAL_AGENT_FLAGS) $(SYNTHETIC_FLAG)

evals-batch-localagent-localplane: ## Batch on an agent-runtimes server on this machine, results written to `plane local`
	@$(LOCAL_PLANE) $(LOCAL_AGENT_ENV) $(BATCH) $(LOCAL_PLANE_FLAGS) $(LOCAL_AGENT_FLAGS) $(SYNTHETIC_FLAG)

evals-batch-localagent-localplane-billing-entity: ## Same as evals-batch-localagent-localplane, asking for the API key and a billing entity
	$(call WITH_BILLING_ENTITY,$(LOCAL_PLANE) $(LOCAL_AGENT_ENV) $(BATCH) $(LOCAL_PLANE_FLAGS) $(LOCAL_AGENT_FLAGS) $(SYNTHETIC_FLAG))

# ---- batch, synthetic (no agent) -----------------------------------------------------------

evals-batch-synthetic-cloudplane: ## Batch with deterministic synthetic results and no agent, against the Datalayer services
	@$(CLOUD_PLANE) $(BATCH) $(CLOUD_PLANE_FLAGS) $(SYNTHETIC_AGENTSPEC_IDS_FLAG) --synthetic

evals-batch-synthetic-localplane: ## Batch with deterministic synthetic results and no agent, against `plane local`
	@$(LOCAL_PLANE) $(BATCH) $(LOCAL_PLANE_FLAGS) $(SYNTHETIC_AGENTSPEC_IDS_FLAG) --synthetic

# ---- interactive, cloud agent --------------------------------------------------------------

evals-interactive-cloudagent-cloudplane: ## Interactive on a pool of Datalayer sandboxes, against the Datalayer services (SYNTHETIC=1 for synthetic results)
	@$(CLOUD_PLANE) $(INTERACTIVE) $(CLOUD_PLANE_FLAGS) $(CLOUD_AGENT_CLOUD_PLANE_FLAGS) $(AGENTSPEC_FLAGS) $(SYNTHETIC_FLAG)

evals-interactive-cloudagent-localplane: ## Interactive on a pool of sandboxes launched through `plane local` on this machine
	@$(LOCAL_PLANE) $(INTERACTIVE) $(LOCAL_PLANE_FLAGS) $(CLOUD_AGENT_LOCAL_PLANE_FLAGS) $(AGENTSPEC_FLAGS) $(SYNTHETIC_FLAG)

# ---- interactive, local agent --------------------------------------------------------------

evals-interactive-localagent-cloudplane: ## Interactive on an agent-runtimes server on this machine, results written to the Datalayer services
	@$(CLOUD_PLANE) $(LOCAL_AGENT_ENV) $(INTERACTIVE) $(CLOUD_PLANE_FLAGS) $(LOCAL_AGENT_FLAGS) $(SYNTHETIC_FLAG)

evals-interactive-localagent-localplane: ## Interactive on an agent-runtimes server on this machine, results written to `plane local`
	@$(LOCAL_PLANE) $(LOCAL_AGENT_ENV) $(INTERACTIVE) $(LOCAL_PLANE_FLAGS) $(LOCAL_AGENT_FLAGS) $(SYNTHETIC_FLAG)

# ---- interactive, synthetic (no agent) -----------------------------------------------------

evals-interactive-synthetic-cloudplane: ## Interactive with deterministic synthetic results and no agent, against the Datalayer services
	@$(CLOUD_PLANE) $(INTERACTIVE_SYNTHETIC) $(CLOUD_PLANE_FLAGS) $(SYNTHETIC_AGENTSPEC_IDS_FLAG) --synthetic

evals-interactive-synthetic-localplane: ## Interactive with deterministic synthetic results and no agent, against `plane local`
	@$(LOCAL_PLANE) $(INTERACTIVE_SYNTHETIC) $(LOCAL_PLANE_FLAGS) $(SYNTHETIC_AGENTSPEC_IDS_FLAG) --synthetic
