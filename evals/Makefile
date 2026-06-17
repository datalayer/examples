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

# Optional agent spec selection for cloud runtimes. Provide at most one:
#   make evals-batch-cloud AGENTSPEC_ID=example-evals
#   make evals-batch-cloud AGENTSPEC=./my-agent.yaml
AGENTSPEC ?=
AGENTSPEC_ID ?=
AGENTSPEC_FLAG := $(if $(strip $(AGENTSPEC)),--agentspec $(AGENTSPEC),)
AGENTSPEC_ID_FLAG := $(if $(strip $(AGENTSPEC_ID)),--agentspec-id $(AGENTSPEC_ID),)
AGENTSPEC_FLAGS := $(AGENTSPEC_FLAG) $(AGENTSPEC_ID_FLAG)
CLOUD_DEFAULT_ENV_RESET := env -u DATALAYER_IAM_URL -u DATALAYER_RUNTIMES_URL -u DATALAYER_AI_AGENTS_URL

.PHONY: help evals-batch-local evals-batch-cloud evals-batch-cloud-billable-account evals-batch-local-proxy evals-batch-cloud-proxy evals-batch-synthetic evals-batch-synthetic-proxy evals-interactive-local evals-interactive-cloud evals-interactive-local-proxy evals-interactive-cloud-proxy evals-interactive-synthetic evals-interactive-synthetic-proxy

help: ## Show available targets
	@awk 'BEGIN {FS = ":.*##"; print "Usage: make <target>\n"} /^[a-zA-Z_-]+:.*?##/ {printf "%-20s %s\n", $$1, $$2}' $(MAKEFILE_LIST)

evals-batch-local: ## Run batch example in SDK lane using direct endpoints with local agent target
	@python evals_batch_example.py --run-environment sdk --run-status completed --execution-target local --timeout $(EVAL_WATCH_TIMEOUT) --interval $(EVAL_WATCH_INTERVAL) --auto-start-local-agent-runtime --local-agent-log-level $(LOCAL_AGENT_LOG_LEVEL) --iam-url $(DATALAYER_IAM_URL) --runtimes-url $(DATALAYER_RUNTIMES_URL) --ai-agents-url $(DATALAYER_AI_AGENTS_URL) --local-agent-base-url $(AGENT_RUNTIME_BASE_URL) --local-agent-id $(AGENT_RUNTIME_ID) $(SYNTHETIC_FLAG)

evals-batch-cloud: ## Run batch example in SDK lane using direct endpoints with cloud agent target (set SYNTHETIC=1 for synthetic mode)
	@$(CLOUD_DEFAULT_ENV_RESET) python evals_batch_example.py --run-environment sdk --run-status completed --execution-target cloud --cloud-credits-limit $(CLOUD_CREDITS_LIMIT) --timeout $(EVAL_WATCH_TIMEOUT) --interval $(EVAL_WATCH_INTERVAL) --local-agent-base-url $(AGENT_RUNTIME_BASE_URL) --local-agent-id $(AGENT_RUNTIME_ID) $(AGENTSPEC_FLAGS) $(SYNTHETIC_FLAG)

evals-batch-cloud-billable-account: ## Prompt for API key + billable account UID, then run batch cloud example with both flags
	@default_api_key="$${DATALYER_API_KEY:-$${DATALAYER_API_KEY:-}}"; \
	read -e -i "$$default_api_key" -p "API key [$$default_api_key]: " api_key; \
	api_key="$${api_key:-$$default_api_key}"; \
	default_billable_account_uid="$${DATALYER_BILLABLE_ACCOUNT_UID:-$${DATALAYER_BILLABLE_ACCOUNT_UID:-$${DATALYER_API_KEY:-$${DATALAYER_API_KEY:-}}}}"; \
	read -e -i "$$default_billable_account_uid" -p "Billable account uid [$$default_billable_account_uid]: " billable_account_uid; \
	billable_account_uid="$${billable_account_uid:-$$default_billable_account_uid}"; \
	if [[ -z "$$api_key" ]]; then echo "Missing API key. Set DATALAYER_API_KEY (or DATALYER_API_KEY) or enter one."; exit 1; fi; \
	$(CLOUD_DEFAULT_ENV_RESET) python evals_batch_example.py --run-environment sdk --run-status completed --execution-target cloud --cloud-credits-limit $(CLOUD_CREDITS_LIMIT) --timeout $(EVAL_WATCH_TIMEOUT) --interval $(EVAL_WATCH_INTERVAL) --local-agent-base-url $(AGENT_RUNTIME_BASE_URL) --local-agent-id $(AGENT_RUNTIME_ID) --api-key "$$api_key" --billable-account-uid "$$billable_account_uid" $(AGENTSPEC_FLAGS) $(SYNTHETIC_FLAG)

evals-batch-local-proxy: ## Run batch example via local proxy endpoints in SDK lane with local agent target
	@AGENT_EVALS_MODE=$(AGENT_EVALS_MODE) AGENT_EVALS_EMIT_LIVE_EVENTS=$(AGENT_EVALS_EMIT_LIVE_EVENTS) python evals_batch_example.py --run-environment sdk-proxy --run-status completed --execution-target local --timeout $(EVAL_WATCH_TIMEOUT) --interval $(EVAL_WATCH_INTERVAL) --auto-start-local-agent-runtime --local-agent-log-level $(LOCAL_AGENT_LOG_LEVEL) --iam-url $(DATALAYER_IAM_URL) --runtimes-url $(DATALAYER_RUNTIMES_URL) --ai-agents-url $(DATALAYER_AI_AGENTS_URL) --local-agent-base-url $(AGENT_RUNTIME_BASE_URL) --local-agent-id $(AGENT_RUNTIME_ID) $(SYNTHETIC_FLAG)

evals-batch-cloud-proxy: ## Run batch example via local proxy endpoints in SDK lane with cloud target
	@python evals_batch_example.py --run-environment sdk-proxy --run-status completed --execution-target cloud --cloud-credits-limit $(CLOUD_CREDITS_LIMIT) --timeout $(EVAL_WATCH_TIMEOUT) --interval $(EVAL_WATCH_INTERVAL) --iam-url $(DATALAYER_IAM_URL) --runtimes-url $(DATALAYER_RUNTIMES_URL) --ai-agents-url $(DATALAYER_AI_AGENTS_URL) --local-agent-base-url $(AGENT_RUNTIME_BASE_URL) --local-agent-id $(AGENT_RUNTIME_ID) $(AGENTSPEC_FLAGS) $(SYNTHETIC_FLAG)

evals-batch-synthetic: ## Run batch example in SDK lane with synthetic (no-agent) behavior
	@python evals_batch_example.py --run-environment sdk --run-status completed --timeout $(EVAL_WATCH_TIMEOUT) --interval $(EVAL_WATCH_INTERVAL) --iam-url $(DATALAYER_IAM_URL) --runtimes-url $(DATALAYER_RUNTIMES_URL) --ai-agents-url $(DATALAYER_AI_AGENTS_URL) --synthetic

evals-batch-synthetic-proxy: ## Run batch example via local proxy endpoints in SDK lane with synthetic (no-agent) behavior
	@python evals_batch_example.py --run-environment sdk-proxy --run-status completed --timeout $(EVAL_WATCH_TIMEOUT) --interval $(EVAL_WATCH_INTERVAL) --iam-url $(DATALAYER_IAM_URL) --runtimes-url $(DATALAYER_RUNTIMES_URL) --ai-agents-url $(DATALAYER_AI_AGENTS_URL) --synthetic

evals-interactive-local: ## Run interactive example in SDK lane using direct endpoints with local agent target
	@python evals_interactive_example.py --run-environment sdk --run-status running --timeout $(EVAL_WATCH_TIMEOUT) --interval $(EVAL_WATCH_INTERVAL) --execution-target local --auto-start-local-agent-runtime --local-agent-log-level $(LOCAL_AGENT_LOG_LEVEL) --iam-url $(DATALAYER_IAM_URL) --runtimes-url $(DATALAYER_RUNTIMES_URL) --ai-agents-url $(DATALAYER_AI_AGENTS_URL) --local-agent-base-url $(AGENT_RUNTIME_BASE_URL) --local-agent-id $(AGENT_RUNTIME_ID) $(SYNTHETIC_FLAG)

evals-interactive-cloud: ## Run interactive example in SDK lane using direct endpoints with cloud agent target (set SYNTHETIC=1 for synthetic mode)
	@$(CLOUD_DEFAULT_ENV_RESET) python evals_interactive_example.py --run-environment sdk --run-status running --execution-target cloud --cloud-credits-limit $(CLOUD_CREDITS_LIMIT) --timeout $(EVAL_WATCH_TIMEOUT) --interval $(EVAL_WATCH_INTERVAL) --local-agent-base-url $(AGENT_RUNTIME_BASE_URL) --local-agent-id $(AGENT_RUNTIME_ID) $(AGENTSPEC_FLAGS) $(SYNTHETIC_FLAG)

evals-interactive-local-proxy: ## Run interactive example via local proxy endpoints in SDK lane with local agent target
	@AGENT_EVALS_MODE=$(AGENT_EVALS_MODE) AGENT_EVALS_EMIT_LIVE_EVENTS=$(AGENT_EVALS_EMIT_LIVE_EVENTS) python evals_interactive_example.py --run-environment sdk-proxy --run-status running --timeout $(EVAL_WATCH_TIMEOUT) --interval $(EVAL_WATCH_INTERVAL) --execution-target local --auto-start-local-agent-runtime --local-agent-log-level $(LOCAL_AGENT_LOG_LEVEL) --iam-url $(DATALAYER_IAM_URL) --runtimes-url $(DATALAYER_RUNTIMES_URL) --ai-agents-url $(DATALAYER_AI_AGENTS_URL) --local-agent-base-url $(AGENT_RUNTIME_BASE_URL) --local-agent-id $(AGENT_RUNTIME_ID) $(SYNTHETIC_FLAG)

evals-interactive-cloud-proxy: ## Run interactive example via local proxy endpoints in SDK lane with cloud target
	@python evals_interactive_example.py --run-environment sdk-proxy --run-status running --execution-target cloud --cloud-credits-limit $(CLOUD_CREDITS_LIMIT) --timeout $(EVAL_WATCH_TIMEOUT) --interval $(EVAL_WATCH_INTERVAL) --iam-url $(DATALAYER_IAM_URL) --runtimes-url $(DATALAYER_RUNTIMES_URL) --ai-agents-url $(DATALAYER_AI_AGENTS_URL) --local-agent-base-url $(AGENT_RUNTIME_BASE_URL) --local-agent-id $(AGENT_RUNTIME_ID) $(AGENTSPEC_FLAGS) $(SYNTHETIC_FLAG)

evals-interactive-synthetic: ## Run interactive example in SDK lane with synthetic (no-agent) behavior
	@python evals_interactive_example.py --run-environment sdk --run-status completed --timeout $(EVAL_WATCH_TIMEOUT) --interval $(EVAL_WATCH_INTERVAL) --iam-url $(DATALAYER_IAM_URL) --runtimes-url $(DATALAYER_RUNTIMES_URL) --ai-agents-url $(DATALAYER_AI_AGENTS_URL) --synthetic

evals-interactive-synthetic-proxy: ## Run interactive example via local proxy endpoints in SDK lane with synthetic (no-agent) behavior
	@python evals_interactive_example.py --run-environment sdk-proxy --run-status completed --timeout $(EVAL_WATCH_TIMEOUT) --interval $(EVAL_WATCH_INTERVAL) --iam-url $(DATALAYER_IAM_URL) --runtimes-url $(DATALAYER_RUNTIMES_URL) --ai-agents-url $(DATALAYER_AI_AGENTS_URL) --synthetic

