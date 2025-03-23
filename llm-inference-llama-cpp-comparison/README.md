[![Datalayer](https://assets.datalayer.tech/datalayer-25.svg)](https://datalayer.io)

[![Become a Sponsor](https://img.shields.io/static/v1?label=Become%20a%20Sponsor&message=%E2%9D%A4&logo=GitHub&style=flat&color=1ABC9C)](https://github.com/sponsors/datalayer)

# LLM Inference with llama.cpp GPU vs. CPU Inference Comparison

## Overview

This notebook compares the inference performance of the [`DeepSeek-R1-Distill-Llama-8B`](https://huggingface.co/deepseek-ai/DeepSeek-R1-Distill-Llama-8B) model using GPU acceleration and CPU only. It demonstrates the significant speedup achieved with GPU offloading and highlights the benefits of quantization (using the GGUF model format) for memory and performance optimization.

## Key Concepts

- *Distillation*: Smaller models trained to mimic larger ones, improving efficiency.
- *Quantization*: Reduces precision of model weights for faster inference and lower memory usage.
- *llama.cpp*: A lightweight C++ implementation for efficient inference with support for both CPU and GPU.

##  Results

- GPU Inference: 8 seconds (T4 NVIDIA GPU with 16GB GPU memory).
- CPU Inference: 61 seconds (3 CPUs 20GB RAM).

Speedup: **~7-8x faster on GPU.**
