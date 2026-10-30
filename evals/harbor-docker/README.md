# A Harbor benchmark with an agent, a model and a Docker environment

Two tasks, each with a Dockerfile. A custom agent, `agents/answerer.py`, asks its model once and writes the answer in the task's image. Each verifier writes a structured reward: `correct` for the answer, `image` for whether it ran in the image that task's Dockerfile built. Each task keeps what it left in `/logs/artifacts`, and `job.yaml` asks for two attempts.

The agent holds no key and knows one address, the one its sandbox gives it. Pick a model of the catalogue when you import it:

```bash
agent-runtimes evals adapters inspect harbor evals/harbor-docker
agent-runtimes evals adapters import harbor <inspection> --model bedrock:us.anthropic.claude-haiku-4-5
```

A deployment runs its Dockerfiles only where it offers task images (`DATALAYER_HARBOR_ENVIRONMENTS=image`).
