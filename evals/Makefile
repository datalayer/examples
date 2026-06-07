SHELL := /bin/bash

.DEFAULT_GOAL := help

LOCAL_IAM_URL ?= http://localhost:9700/api/iam/
LOCAL_RUNTIMES_URL ?= http://localhost:9500/api/runtimes/
LOCAL_AI_AGENTS_URL ?= http://localhost:4400/api/ai-agents/
LOCAL_AGENT_BASE_URL ?= http://localhost:8765
LOCAL_AGENT_ID ?= default
LOCAL_AGENT_LOG_LEVEL ?= info
LOCAL_AGENT_EVALS_MODE ?= interactive
LOCAL_AGENT_EVALS_EMIT_LIVE_EVENTS ?= true
EVAL_WATCH_TIMEOUT ?= 60
EVAL_WATCH_INTERVAL ?= 2
CLOUD_CREDITS_LIMIT ?= 100
SYNTHETIC ?= 0
SYNTHETIC_FLAG := $(if $(filter 1 true yes on,$(SYNTHETIC)),--synthetic,)

# Optional agent spec selection for cloud runtimes. Provide at most one:
#   make evals-batch-cloud AGENTSPEC_ID=example-simple
#   make evals-batch-cloud AGENTSPEC=./my-agent.yaml
AGENTSPEC ?=
AGENTSPEC_ID ?=
AGENTSPEC_FLAG := $(if $(strip $(AGENTSPEC)),--agentspec $(AGENTSPEC),)
AGENTSPEC_ID_FLAG := $(if $(strip $(AGENTSPEC_ID)),--agentspec-id $(AGENTSPEC_ID),)
AGENTSPEC_FLAGS := $(AGENTSPEC_FLAG) $(AGENTSPEC_ID_FLAG)

.PHONY: help evals-batch-local evals-batch-cloud evals-batch-local-proxy evals-batch-cloud-proxy evals-batch-synthetic-proxy evals-interactive-local evals-interactive-cloud evals-interactive-local-proxy evals-interactive-cloud-proxy evals-interactive-synthetic-proxy

help: ## Show available targets
	@awk 'BEGIN {FS = ":.*##"; print "Usage: make <target>\n"} /^[a-zA-Z_-]+:.*?##/ {printf "%-20s %s\n", $$1, $$2}' $(MAKEFILE_LIST)

evals-batch-local: ## Run batch example in SDK lane using direct endpoints with local agent target
	@python evals_batch_example.py --run-environment sdk --run-status completed --execution-target local --timeout $(EVAL_WATCH_TIMEOUT) --interval $(EVAL_WATCH_INTERVAL) --auto-start-local-agent-runtime --local-agent-log-level $(LOCAL_AGENT_LOG_LEVEL) --local-agent-base-url $(LOCAL_AGENT_BASE_URL) --local-agent-id $(LOCAL_AGENT_ID) $(SYNTHETIC_FLAG)

evals-batch-cloud: ## Run batch example in SDK lane using direct endpoints with cloud agent target (set SYNTHETIC=1 for synthetic mode)
	@python evals_batch_example.py --run-environment sdk --run-status completed --execution-target cloud --cloud-credits-limit $(CLOUD_CREDITS_LIMIT) --timeout $(EVAL_WATCH_TIMEOUT) --interval $(EVAL_WATCH_INTERVAL) --local-agent-base-url $(LOCAL_AGENT_BASE_URL) --local-agent-id $(LOCAL_AGENT_ID) $(AGENTSPEC_FLAGS) $(SYNTHETIC_FLAG)

evals-batch-local-proxy: ## Run batch example via local proxy endpoints in SDK lane with local agent target
	@DATALAYER_EVALS_MODE=$(LOCAL_AGENT_EVALS_MODE) DATALAYER_EVALS_EMIT_LIVE_EVENTS=$(LOCAL_AGENT_EVALS_EMIT_LIVE_EVENTS) python evals_batch_example.py --run-environment sdk-proxy --run-status completed --execution-target local --timeout $(EVAL_WATCH_TIMEOUT) --interval $(EVAL_WATCH_INTERVAL) --auto-start-local-agent-runtime --local-agent-log-level $(LOCAL_AGENT_LOG_LEVEL) --local-agent-base-url $(LOCAL_AGENT_BASE_URL) --local-agent-id $(LOCAL_AGENT_ID) $(SYNTHETIC_FLAG)

evals-batch-cloud-proxy: ## Run batch example via local proxy endpoints in SDK lane with cloud target
	@python evals_batch_example.py --run-environment sdk-proxy --run-status completed --execution-target cloud --cloud-credits-limit $(CLOUD_CREDITS_LIMIT) --timeout $(EVAL_WATCH_TIMEOUT) --interval $(EVAL_WATCH_INTERVAL) --local-agent-base-url $(LOCAL_AGENT_BASE_URL) --local-agent-id $(LOCAL_AGENT_ID) $(AGENTSPEC_FLAGS) $(SYNTHETIC_FLAG)

evals-batch-synthetic-proxy: ## Run batch example via local proxy endpoints in SDK lane with synthetic (no-agent) behavior
	@python evals_batch_example.py --run-environment sdk-proxy --run-status completed --timeout $(EVAL_WATCH_TIMEOUT) --interval $(EVAL_WATCH_INTERVAL) --synthetic

evals-interactive-local: ## Run interactive example in SDK lane using direct endpoints with local agent target
	@python evals_interactive_example.py --run-environment sdk --run-status running --timeout $(EVAL_WATCH_TIMEOUT) --interval $(EVAL_WATCH_INTERVAL) --execution-target local --auto-start-local-agent-runtime --local-agent-log-level $(LOCAL_AGENT_LOG_LEVEL) --local-agent-base-url $(LOCAL_AGENT_BASE_URL) --local-agent-id $(LOCAL_AGENT_ID) $(SYNTHETIC_FLAG)

evals-interactive-cloud: ## Run interactive example in SDK lane using direct endpoints with cloud agent target (set SYNTHETIC=1 for synthetic mode)
	@python evals_interactive_example.py --run-environment sdk --run-status running --execution-target cloud --cloud-credits-limit $(CLOUD_CREDITS_LIMIT) --timeout $(EVAL_WATCH_TIMEOUT) --interval $(EVAL_WATCH_INTERVAL) --local-agent-base-url $(LOCAL_AGENT_BASE_URL) --local-agent-id $(LOCAL_AGENT_ID) $(AGENTSPEC_FLAGS) $(SYNTHETIC_FLAG)

evals-interactive-local-proxy: ## Run interactive example via local proxy endpoints in SDK lane with local agent target
	@DATALAYER_EVALS_MODE=$(LOCAL_AGENT_EVALS_MODE) DATALAYER_EVALS_EMIT_LIVE_EVENTS=$(LOCAL_AGENT_EVALS_EMIT_LIVE_EVENTS) python evals_interactive_example.py --run-environment sdk-proxy --run-status running --timeout $(EVAL_WATCH_TIMEOUT) --interval $(EVAL_WATCH_INTERVAL) --execution-target local --auto-start-local-agent-runtime --local-agent-log-level $(LOCAL_AGENT_LOG_LEVEL) --local-agent-base-url $(LOCAL_AGENT_BASE_URL) --local-agent-id $(LOCAL_AGENT_ID) $(SYNTHETIC_FLAG)

evals-interactive-cloud-proxy: ## Run interactive example via local proxy endpoints in SDK lane with cloud target
	@python evals_interactive_example.py --run-environment sdk-proxy --run-status running --execution-target cloud --cloud-credits-limit $(CLOUD_CREDITS_LIMIT) --timeout $(EVAL_WATCH_TIMEOUT) --interval $(EVAL_WATCH_INTERVAL) --local-agent-base-url $(LOCAL_AGENT_BASE_URL) --local-agent-id $(LOCAL_AGENT_ID) $(AGENTSPEC_FLAGS) $(SYNTHETIC_FLAG)

evals-interactive-synthetic-proxy: ## Run interactive example via local proxy endpoints in SDK lane with synthetic (no-agent) behavior
	@python evals_interactive_example.py --run-environment sdk-proxy --run-status completed --timeout $(EVAL_WATCH_TIMEOUT) --interval $(EVAL_WATCH_INTERVAL) --synthetic

