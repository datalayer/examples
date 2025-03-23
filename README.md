[![Datalayer](https://assets.datalayer.tech/datalayer-25.svg)](https://datalayer.io)

[![Become a Sponsor](https://img.shields.io/static/v1?label=Become%20a%20Sponsor&message=%E2%9D%A4&logo=GitHub&style=flat&color=1ABC9C)](https://github.com/sponsors/datalayer)

# Ξ Datalayer Examples

This repository contains Jupyter notebook examples showcasing scenarios where [Datalayer](https://datalayer.io) proves highly beneficial.

Datalayer allows you to **scale runtimes** from your local JupyterLab or CLI to the cloud, providing the capability to run your code on **powerful GPU(s) and CPU(s)**. 🚀

The first examples delves into system checks and performance benchmarks to ensure optimal GPU and CPU utilization, the next ones explore typical AI scenarios where scaling proves essential.

💡 Note that you can use any notebook within Datalayer without requiring any code changes.

## Getting started 

```bash
pip install datalayer
git clone https://github.com/datalayer/examples.git datalayer-examples
cd datalayer-examples
jupyter lab
```

Read the [documentation website](https://docs.datalayer.io) to know more about how setup Datalayer.

Don't worry, it is easy 👍 You just need to install the package, open JupyterLab, click on the `Jupyter Runtimes` tile in the JupyterLab launcher, create an account, wait a bit for your Kernels to be ready, and then just assign a Remote Runtime from any Notebook kernel picker.

<img alt="Notebook remote execution" src="https://datalayer-assets.s3.us-west-2.amazonaws.com/examples/user-flow-1.png" width="900" />

1. [GPU sanity checks](#gpu-sanity-checks)
1. [Performance comparison of CPU and GPU serial and parallel execution](#performance-comparison-of-cpu-and-gpu-serial-and-parallel-execution)
1. [Parallel execution performance comparison](#parallel-execution-performance-comparison)
1. [Face detection on YouTube video with OpenCV](#opencv-face-detection)
1. [Image classification model training with fast.ai](#image-classifier-with-fastai)
1. ['Personalized' text-to-image model creation with Dreambooth](#dreambooth)
1. [Text generation using the Transformers library](#text-generation-with-transformers)
1. [Instruction tuning for Mistral 7B on Alpaca dataset](#mistral-instruction-tuning)
1. [LLM Inference with llama.cpp](#llm-inference-with-llama-cpp)

### [GPU sanity checks](https://github.com/datalayer/examples/tree/main/check-gpu)

This notebook contains scripts and tests to perform GPU sanity checks using PyTorch and CUDA. The primary goal of these checks is to **ensure** that the **GPU resources meet the expected requirements**.

### [LLM with CPU and GPU performance comparison](https://github.com/datalayer/examples/tree/main/llm-inference-llama-cpp-comparison)

In this notebook, we compare the inference performance of the [`DeepSeek-R1-Distill-Llama-8B`](https://huggingface.co/deepseek-ai/DeepSeek-R1-Distill-Llama-8B) model using **GPU acceleration** and **CPU only**.

It demonstrates the significant speedup achieved with GPU offloading and highlights the benefits of **quantization** (using the GGUF model format) for memory and performance optimization.

### [Parallel execution performance comparison](https://github.com/datalayer/examples/tree/main/parallel-execution)

Compare the performance with parallel execution.

### [OpenCV Face Detection](https://github.com/datalayer/examples/tree/main/image-face-detection-opencv)

This example utilizes **OpenCV** for **detecting faces** in YouTube videos. It uses a traditional Haar Cascade model, which may have limitations in accuracy compared to modern deep learning-based models. It also utilizes **parallel computing across multiple CPUs** to accelerate face detection and video processing tasks, optimizing performance and efficiency. Datalayer further enhances this capability by enabling seamless scaling across multiple CPUs.

<div style="display: flex;">
    <img src="https://datalayer-assets.s3.us-west-2.amazonaws.com/examples/rick-ashley-1.png" style="width: 20%;">
    <img src="https://datalayer-assets.s3.us-west-2.amazonaws.com/examples/rick-ashley-2.png" style="width: 20%;">
</div>

### [Image Classifier with Fast.ai](https://github.com/datalayer/examples/tree/main/image-classifier-fastai)

This example demonstrates how to build a model that **distinguishes cats from dogs** in pictures using the fast.ai library. Due to the computational demands of training a model, a **GPU is required**. 

<img src="https://miro.medium.com/v2/resize:fit:1400/format:webp/1*rAbCk0T4rksShBcPQjWC0A.gif" width="400"/>

### [Dreambooth](https://github.com/datalayer/examples/tree/main/image-diffusion-dreambooth)

This example uses the Dreambooth method which takes as input a few images (typically 3-5 images suffice) of a subject (e.g., a specific dog) and the corresponding class name (e.g. "dog"), and returns a **fine-tuned/'personalized' text-to-image model** (source: [Dreambooth](https://dreambooth.github.io/)). To do this fune-tuning process, **GPU is required**.

<img src="https://dreambooth.github.io/DreamBooth_files/accessories.png" width="500"/>

### [Text Generation with Transformers](https://github.com/datalayer/examples/tree/main/llm-text-generation-transformers)

Those notebook examples demonstrate how to leverage Datalayer's **GPU kernels** to accelerate text generation using **Gemma** model and the HuggingFace Transformers library.

<img src="https://huggingface.co/datasets/huggingface/brand-assets/resolve/main/hf-logo-with-title.png" width="200"/>

#### [Transformers Text Generation](https://github.com/datalayer/examples/tree/main/llm--text-generation-transformer/llm--text-generation-transformers.ipynb)

This notebook uses Gemma-7b and Gemma-7b-it which is the instruct fine-tuned version of Gemma-7b.

#### [Sentiment Analysis with Gemma](https://github.com/datalayer/examples/tree/main/sentiment-analysis-gemma/sentiment-analysis-gemma.ipynb)

This example demonstrates how you can leverage Datalayer's [**Cell Runtimes**](https://github.com/datalayer/examples?tab=readme-ov-file#cell-kernel) feature on JupyterLab to **offload specific tasks**, such as sentiment analysis, **to a remote GPU** while keeping the rest of your code running locally. By selectively using remote resources, you can **optimize both performance and cost**.

This hybrid approach is perfect for tasks like sentiment analysis via llm where some parts of the code require more computational resources than others. For a detailed explanation and step-by-step guide on using Cell Kernels, check out our [blog post](https://datalayer.blog/2024/08/23/cell-kernels) on this specific example.

### [Mistral Instruction Tuning](https://github.com/datalayer/examples/tree/main/llm-instruct-tuning-mistral)

**Mistral 7B** is a large language model (LLM) that contains 7.3 billion parameters and is one of the most powerful models for its size. However, this base model is not instruction-tuned, meaning it may struggle to follow instructions and perform specific tasks.

By fine-tuning Mistral 7B on the Alpaca dataset using [**torchtune**](https://github.com/pytorch/torchtune), the model will significantly improve its capabilities to perform tasks such as conversation and answering questions accurately. Due to the computational demands of fine-tuning a model, a **GPU is required**.

<img src="https://assets.datalayer.tech/examples/llm-fine-tuning.png" width="500"/>

### [LLM Inference with llama.cpp](https://github.com/datalayer/examples/tree/main/llm-inference-llama-cpp-langchain)

[`llama.cpp`](https://llama-cpp-python.readthedocs.io) library is used for efficient inference with support for GPU.

[LangChain](https://www.langchain.com) is used.

## CLI Execution

Datalayer supports the remote execution of code using the **CLI**. Refer to this [page](https://docs.datalayer.io/cli) for more information.

<details>

<summary><i>CLI Remote Execution</i></summary>

<img alt="CLI remote execution" src="https://datalayer-assets.s3.us-west-2.amazonaws.com/examples/CLI.png" width="800" />

</details>

<details>

<summary><i>Sharing State between Notebook and CLI</i></summary>

<img alt="Remote Notebook Execution" src="https://datalayer-assets.s3.us-west-2.amazonaws.com/examples/SharingState.png" width="800" />

When using the same Kernel, variables defined in a notebook can be used in the CLI and vice versa. This holds also true when using multiple notebooks connected to the same kernel, for example.

</details>

## Cell Runtime

Datalayer offers the possibility to use **cell-specific Runtime**, allowing you to execute specific cells with different kernels.

This feature **optimizes costs** by enabling you to, for example, leverage the local CPU for data preparation and reserving the powerful (and often more expensive) GPU resources for intensive computations. 

<details>

<summary><i>Cell runtime execution</i></summary>

<img alt="Cell Runtime Execution" src="https://assets.datalayer.tech/examples/cell-picker.gif" width="800" />

The remote GPU Runtime is utilized only for the duration of the cell computation, minimizing costs.

</details>
