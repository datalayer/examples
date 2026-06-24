SHELL := /bin/bash

.DEFAULT_GOAL := help

DATALAYER_IAM_URL ?= http://localhost:9700
DATALAYER_RUNTIMES_URL ?= http://localhost:9500
DATALAYER_AI_AGENTS_URL ?= http://localhost:4400
AGENT_RUNTIME_BASE_URL ?= http://localhost:8765
AGENT_RUNTIME_ID ?= default
LOCAL_AGENT_LOG_LEVEL ?= info
AGENT_EVALS_MODE ?= interactive
AGENT_EVALS_EMIT_LIVE_EVENTS ?= true
EVAL_WATCH_TIMEOUT ?= 60
EVAL_WATCH_INTERVAL ?= 2
CLOUD_CREDITS_LIMIT ?= 100
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
#   make evals-batch-cloud AGENTSPEC_ID=example-evals
#   make evals-batch-cloud AGENTSPEC_IDS="example-evals,example-evals-nocodemode"
#   make evals-batch-cloud AGENTSPEC=./my-agent.yaml
AGENTSPEC ?=
AGENTSPEC_ID ?=
AGENTSPEC_IDS ?=
AGENTSPEC_FLAG := $(if $(strip $(AGENTSPEC)),--agentspec $(AGENTSPEC),)
AGENTSPEC_ID_FLAG := $(if $(strip $(AGENTSPEC_ID)),--agentspec-id $(AGENTSPEC_ID),)
AGENTSPEC_IDS_FLAG := $(if $(strip $(AGENTSPEC_IDS)),--agentspec-ids $(AGENTSPEC_IDS),)
AGENTSPEC_FLAGS := $(AGENTSPEC_FLAG) $(AGENTSPEC_ID_FLAG) $(AGENTSPEC_IDS_FLAG)
CLOUD_DEFAULT_ENV_RESET := env -u DATALAYER_IAM_URL -u DATALAYER_RUNTIMES_URL -u DATALAYER_AI_AGENTS_URL

.PHONY: help evals-batch-simple evals-batch-local evals-batch-cloud evals-batch-cloud-billable-account evals-batch-local-proxy evals-batch-cloud-proxy evals-batch-synthetic evals-batch-synthetic-proxy evals-interactive-local evals-interactive-cloud evals-interactive-local-proxy evals-interactive-cloud-proxy evals-interactive-synthetic evals-interactive-synthetic-proxy

help: ## Show available targets
	@awk 'BEGIN {FS = ":.*##"; print "Usage: make <target>\n"} /^[a-zA-Z_-]+:.*?##/ {printf "%-20s %s\n", $$1, $$2}' $(MAKEFILE_LIST)

evals-batch-simple: ## Minimal cloud batch run via core execute_evalset_spec (single agentspec, no reports)
	@$(CLOUD_DEFAULT_ENV_RESET) python evals_batch_simple.py

evals-batch-local: ## Run batch example in SDK lane with local agent target (runner-backed)
	@python evals_batch_example.py --run-environment sdk --run-status completed --execution-target local --timeout $(EVAL_WATCH_TIMEOUT) --interval $(EVAL_WATCH_INTERVAL) --auto-start-local-agent-runtime --local-agent-log-level $(LOCAL_AGENT_LOG_LEVEL) --iam-url $(DATALAYER_IAM_URL) --runtimes-url $(DATALAYER_RUNTIMES_URL) --ai-agents-url $(DATALAYER_AI_AGENTS_URL) --local-agent-base-url $(AGENT_RUNTIME_BASE_URL) --local-agent-id $(AGENT_RUNTIME_ID) $(BATCH_EVALSET_SPEC_FLAG) $(SYNTHETIC_FLAG)

evals-batch-cloud: ## Run batch example in SDK lane with cloud agent target (runner-backed; set SYNTHETIC=1 for synthetic mode)
	@$(CLOUD_DEFAULT_ENV_RESET) python evals_batch_example.py --run-environment sdk --run-status completed --execution-target cloud --cloud-credits-limit $(CLOUD_CREDITS_LIMIT) --timeout $(EVAL_WATCH_TIMEOUT) --interval $(EVAL_WATCH_INTERVAL) --local-agent-base-url $(AGENT_RUNTIME_BASE_URL) --local-agent-id $(AGENT_RUNTIME_ID) $(BATCH_EVALSET_SPEC_FLAG) $(AGENTSPEC_FLAGS) $(SYNTHETIC_FLAG)

evals-batch-cloud-billable-account: ## Prompt for API key + optional billable account UID, then run batch cloud example (runner-backed)
	@default_api_key="$${DATALAYER_API_KEY:-}"; \
	read -e -i "$$default_api_key" -p "API key [$$default_api_key]: " api_key; \
	api_key="$${api_key:-$$default_api_key}"; \
	default_billable_account_uid="$${DATALAYER_BILLABLE_ACCOUNT_UID:-}"; \
	read -e -i "$$default_billable_account_uid" -p "Billable account uid (optional) [$$default_billable_account_uid]: " billable_account_uid; \
	billable_account_uid="$${billable_account_uid:-$$default_billable_account_uid}"; \
	billable_flag=""; \
	if [[ -n "$$billable_account_uid" ]]; then billable_flag="--billable-account-uid $$billable_account_uid"; fi; \
	if [[ -z "$$api_key" ]]; then echo "Missing API key. Set DATALAYER_API_KEY or enter one."; exit 1; fi; \
	$(CLOUD_DEFAULT_ENV_RESET) python evals_batch_example.py --run-environment sdk --run-status completed --execution-target cloud --cloud-credits-limit $(CLOUD_CREDITS_LIMIT) --timeout $(EVAL_WATCH_TIMEOUT) --interval $(EVAL_WATCH_INTERVAL) --local-agent-base-url $(AGENT_RUNTIME_BASE_URL) --local-agent-id $(AGENT_RUNTIME_ID) --api-key "$$api_key" $$billable_flag $(BATCH_EVALSET_SPEC_FLAG) $(AGENTSPEC_FLAGS) $(SYNTHETIC_FLAG)

evals-batch-local-proxy: ## Run batch example via local proxy endpoints in SDK lane with local agent target (runner-backed)
	@AGENT_EVALS_MODE=$(AGENT_EVALS_MODE) AGENT_EVALS_EMIT_LIVE_EVENTS=$(AGENT_EVALS_EMIT_LIVE_EVENTS) python evals_batch_example.py --run-environment sdk-proxy --run-status completed --execution-target local --timeout $(EVAL_WATCH_TIMEOUT) --interval $(EVAL_WATCH_INTERVAL) --auto-start-local-agent-runtime --local-agent-log-level $(LOCAL_AGENT_LOG_LEVEL) --iam-url $(DATALAYER_IAM_URL) --runtimes-url $(DATALAYER_RUNTIMES_URL) --ai-agents-url $(DATALAYER_AI_AGENTS_URL) --local-agent-base-url $(AGENT_RUNTIME_BASE_URL) --local-agent-id $(AGENT_RUNTIME_ID) $(BATCH_EVALSET_SPEC_FLAG) $(SYNTHETIC_FLAG)

evals-batch-cloud-proxy: ## Run batch example via local proxy endpoints in SDK lane with cloud target (runner-backed)
	@python evals_batch_example.py --run-environment sdk-proxy --run-status completed --execution-target cloud --cloud-credits-limit $(CLOUD_CREDITS_LIMIT) --timeout $(EVAL_WATCH_TIMEOUT) --interval $(EVAL_WATCH_INTERVAL) --iam-url $(DATALAYER_IAM_URL) --runtimes-url $(DATALAYER_RUNTIMES_URL) --ai-agents-url $(DATALAYER_AI_AGENTS_URL) --local-agent-base-url $(AGENT_RUNTIME_BASE_URL) --local-agent-id $(AGENT_RUNTIME_ID) $(BATCH_EVALSET_SPEC_FLAG) $(AGENTSPEC_FLAGS) $(SYNTHETIC_FLAG)

evals-batch-synthetic: ## Run batch synthetic comparison and emit pydantic usage across example-evals and example-evals-nocodemode
	@$(CLOUD_DEFAULT_ENV_RESET) python evals_batch_example.py --run-environment sdk --run-status completed --timeout $(EVAL_WATCH_TIMEOUT) --interval $(EVAL_WATCH_INTERVAL) $(BATCH_EVALSET_SPEC_FLAG) $(SYNTHETIC_AGENTSPEC_IDS_FLAG) --synthetic

evals-batch-synthetic-proxy: ## Run batch synthetic comparison via sdk-proxy and emit pydantic usage
	@python evals_batch_example.py --run-environment sdk-proxy --run-status completed --timeout $(EVAL_WATCH_TIMEOUT) --interval $(EVAL_WATCH_INTERVAL) --iam-url $(DATALAYER_IAM_URL) --runtimes-url $(DATALAYER_RUNTIMES_URL) --ai-agents-url $(DATALAYER_AI_AGENTS_URL) $(BATCH_EVALSET_SPEC_FLAG) $(SYNTHETIC_AGENTSPEC_IDS_FLAG) --synthetic

evals-interactive-local: ## Run interactive example in SDK lane with local agent target (runner-backed)
	@python evals_interactive_example.py --run-environment sdk --run-status running --timeout $(EVAL_WATCH_TIMEOUT) --interval $(EVAL_WATCH_INTERVAL) --execution-target local --auto-start-local-agent-runtime --local-agent-log-level $(LOCAL_AGENT_LOG_LEVEL) --iam-url $(DATALAYER_IAM_URL) --runtimes-url $(DATALAYER_RUNTIMES_URL) --ai-agents-url $(DATALAYER_AI_AGENTS_URL) --local-agent-base-url $(AGENT_RUNTIME_BASE_URL) --local-agent-id $(AGENT_RUNTIME_ID) $(INTERACTIVE_EVALSET_SPEC_FLAG) $(SYNTHETIC_FLAG)

evals-interactive-cloud: ## Run interactive example in SDK lane with cloud agent target (runner-backed; set SYNTHETIC=1 for synthetic mode)
	@$(CLOUD_DEFAULT_ENV_RESET) python evals_interactive_example.py --run-environment sdk --run-status running --execution-target cloud --cloud-credits-limit $(CLOUD_CREDITS_LIMIT) --timeout $(EVAL_WATCH_TIMEOUT) --interval $(EVAL_WATCH_INTERVAL) --local-agent-base-url $(AGENT_RUNTIME_BASE_URL) --local-agent-id $(AGENT_RUNTIME_ID) $(INTERACTIVE_EVALSET_SPEC_FLAG) $(AGENTSPEC_FLAGS) $(SYNTHETIC_FLAG)

evals-interactive-local-proxy: ## Run interactive example via local proxy endpoints in SDK lane with local agent target (runner-backed)
	@AGENT_EVALS_MODE=$(AGENT_EVALS_MODE) AGENT_EVALS_EMIT_LIVE_EVENTS=$(AGENT_EVALS_EMIT_LIVE_EVENTS) python evals_interactive_example.py --run-environment sdk-proxy --run-status running --timeout $(EVAL_WATCH_TIMEOUT) --interval $(EVAL_WATCH_INTERVAL) --execution-target local --auto-start-local-agent-runtime --local-agent-log-level $(LOCAL_AGENT_LOG_LEVEL) --iam-url $(DATALAYER_IAM_URL) --runtimes-url $(DATALAYER_RUNTIMES_URL) --ai-agents-url $(DATALAYER_AI_AGENTS_URL) --local-agent-base-url $(AGENT_RUNTIME_BASE_URL) --local-agent-id $(AGENT_RUNTIME_ID) $(INTERACTIVE_EVALSET_SPEC_FLAG) $(SYNTHETIC_FLAG)

evals-interactive-cloud-proxy: ## Run interactive example via local proxy endpoints in SDK lane with cloud target (runner-backed)
	@python evals_interactive_example.py --run-environment sdk-proxy --run-status running --execution-target cloud --cloud-credits-limit $(CLOUD_CREDITS_LIMIT) --timeout $(EVAL_WATCH_TIMEOUT) --interval $(EVAL_WATCH_INTERVAL) --iam-url $(DATALAYER_IAM_URL) --runtimes-url $(DATALAYER_RUNTIMES_URL) --ai-agents-url $(DATALAYER_AI_AGENTS_URL) --local-agent-base-url $(AGENT_RUNTIME_BASE_URL) --local-agent-id $(AGENT_RUNTIME_ID) $(INTERACTIVE_EVALSET_SPEC_FLAG) $(AGENTSPEC_FLAGS) $(SYNTHETIC_FLAG)

evals-interactive-synthetic: ## Run interactive synthetic comparison and emit pydantic usage across example-evals and example-evals-nocodemode
	@$(CLOUD_DEFAULT_ENV_RESET) python evals_interactive_example.py --run-environment sdk --run-status completed --timeout $(EVAL_WATCH_TIMEOUT) --interval $(EVAL_WATCH_INTERVAL) $(INTERACTIVE_EVALSET_SPEC_FLAG) $(SYNTHETIC_AGENTSPEC_IDS_FLAG) --synthetic

evals-interactive-synthetic-proxy: ## Run interactive synthetic comparison via sdk-proxy and emit pydantic usage
	@python evals_interactive_example.py --run-environment sdk-proxy --run-status completed --timeout $(EVAL_WATCH_TIMEOUT) --interval $(EVAL_WATCH_INTERVAL) --iam-url $(DATALAYER_IAM_URL) --runtimes-url $(DATALAYER_RUNTIMES_URL) --ai-agents-url $(DATALAYER_AI_AGENTS_URL) $(INTERACTIVE_EVALSET_SPEC_FLAG) $(SYNTHETIC_AGENTSPEC_IDS_FLAG) --synthetic

