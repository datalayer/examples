[![Datalayer](https://assets.datalayer.tech/datalayer-25.svg)](https://datalayer.ai)

[![Become a Sponsor](https://img.shields.io/static/v1?label=Become%20a%20Sponsor&message=%E2%9D%A4&logo=GitHub&style=flat&color=1ABC9C)](https://github.com/sponsors/datalayer)

# ☰ Datalayer Examples

Examples for the modern Datalayer platform: **managed agents for data analysis** with governed execution, durable runtimes, and reproducible outputs.

Use this repository to explore:

1. Notebook-based AI and ML workflows on CPU/GPU
2. CLI-first remote execution and Ray job orchestration
3. Agent-oriented prompt workflows (MCP, Skills, Guardrails...)

Read more on [datalayer.ai](https://datalayer.ai) and in the [documentation](https://datalayer.ai/docs).

## Getting Started

```bash
pip install datalayer
git clone https://github.com/datalayer/examples.git datalayer-examples
cd datalayer-examples
jupyter lab
```

You can run existing notebooks as-is, then attach local or remote runtimes from JupyterLab.

<img alt="Notebook remote execution" src="https://images.datalayer.io/legacy/examples/user-flow-1.png" width="900" />

## Example Catalog

1. [GPU checks](https://github.com/datalayer/examples/tree/main/gpu-check)
2. [PyTorch examples](https://github.com/datalayer/examples/tree/main/pytorch)
3. [LLM with CPU vs GPU performance comparison](https://github.com/datalayer/examples/tree/main/llm-inference-llama-cpp-comparison)
4. [GPU/CPU execution performance comparison](https://github.com/datalayer/examples/tree/main/gpu-vs-cpu)
5. [OpenCV Face Detection](https://github.com/datalayer/examples/tree/main/image-face-detection-opencv)
6. [Image Classifier with fast.ai](https://github.com/datalayer/examples/tree/main/image-classifier-fastai)
7. [Dreambooth](https://github.com/datalayer/examples/tree/main/image-diffusion-dreambooth)
8. [Text Generation with Transformers](https://github.com/datalayer/examples/tree/main/llm-text-generation-transformers)
9. [Sentiment Analysis with Gemma](https://github.com/datalayer/examples/tree/main/sentiment-analysis-gemma)
10. [Mistral Instruction Tuning](https://github.com/datalayer/examples/tree/main/llm-instruct-tuning-mistral)
11. [LLM Inference with llama.cpp + LangChain](https://github.com/datalayer/examples/tree/main/llm-inference-llama-cpp-langchain)
12. [Prompt examples for Jupyter MCP](https://github.com/datalayer/examples/tree/main/prompts)
13. [Ray CLI examples (`datalayer ray`)](https://github.com/datalayer/examples/tree/main/ray)
14. [Evals SDK examples (batch + interactive)](https://github.com/datalayer/examples/tree/main/evals)

## Highlight: PyTorch Examples

The [pytorch](https://github.com/datalayer/examples/tree/main/pytorch) folder includes practical PyTorch baselines, starting with matrix multiplication for CPU/GPU throughput analysis.

It is useful to:

1. validate runtime and CUDA readiness
2. compare CPU and GPU execution characteristics on your setup
3. establish reproducible performance baselines before model training or inference experiments

## Ray CLI Examples

The [ray](https://github.com/datalayer/examples/tree/main/ray) folder contains Python scripts designed to be submitted with the Datalayer Ray CLI (`datalayer ray jobs submit --py @...`).

Included examples:

1. `hello_ray.py`: basic distributed map (`square`) with Ray tasks
2. `pi_monte_carlo.py`: distributed Monte Carlo estimation of pi
3. `actor_counter.py`: stateful actor pattern with multiple counters

## Evals SDK Examples

The [evals](https://github.com/datalayer/examples/tree/main/evals) folder contains SDK examples for both run modes:

1. `evals_batch_example.py`: deterministic case-set execution (`run_mode=batch`)
2. `evals_interactive_example.py`: event/live-window evaluation (`run_mode=interactive`)

Run them with the packaged make targets:

```bash
cd evals
make help
make evals-batch-local
make evals-batch-cloud
make evals-interactive-local
make evals-interactive-cloud
make evals-batch-local-proxy
make evals-interactive-local-proxy
```

## CLI

Datalayer supports remote code execution through the CLI and integrates with managed runtimes and Ray workflows.

See [CLI docs](https://datalayer.ai/docs) and the [Ray examples](https://github.com/datalayer/examples/tree/main/ray) for end-to-end commands.

<details>

<summary><i>CLI Remote Execution</i></summary>

<img alt="CLI remote execution" src="https://images.datalayer.io/legacy/examples/CLI.png" width="800" />

</details>

<details>

<summary><i>Sharing State between Notebook and CLI</i></summary>

<img alt="Remote Notebook Execution" src="https://images.datalayer.io/legacy/examples/SharingState.png" width="800" />

When using the same Kernel, variables defined in a notebook can be reused in the CLI and vice versa.

</details>

## JupyterLab

Datalayer supports **cell-specific runtimes** so you can run specific cells on different compute targets.

This lets you optimize cost and performance, for example by using local CPU for data prep and remote GPU for intensive cells.

<details>

<summary><i>Cell runtime execution</i></summary>

<img alt="Cell Runtime Execution" src="https://assets.datalayer.tech/examples/cell-picker.gif" width="800" />

The remote GPU runtime is used only for the duration of selected cell computation.

</details>
