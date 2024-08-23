[![Datalayer](https://assets.datalayer.tech/datalayer-25.svg)](https://datalayer.io)

[![Become a Sponsor](https://img.shields.io/static/v1?label=Become%20a%20Sponsor&message=%E2%9D%A4&logo=GitHub&style=flat&color=1ABC9C)](https://github.com/sponsors/datalayer)

# Transformers Text Generation

Those notebook examples demonstrate how to leverage Datalayer's **GPU kernels** to accelerate text generation using **Gemma** model and the HuggingFace Transformers library.

<img src="https://huggingface.co/datasets/huggingface/brand-assets/resolve/main/hf-logo-with-title.png" width="200"/>

Text generation can be viewed akin to performing inference tasks, where a model interprets input prompts to generate meaningful and contextually appropriate text responses.

## Transformers Text Generation

This notebook uses Gemma-7b and Gemma-7b-it which is the instruct fine-tuned version of Gemma-7b.

## Sentiment Analysis with Gemma

This example demonstrates how you can leverage Datalayer's **Cell Kernels** feature on JupyterLab to offload specific tasks, such as sentiment analysis, to a remote GPU while keeping the rest of your code running locally. By selectively using remote resources, you can optimize both performance and cost. This hybrid approach is perfect for tasks like sentiment analysis via llm where some parts of the code require more computational resources than others.

For a detailed explanation and step-by-step guide on using Cell Kernels, check out our [blog post](https://datalayer.blog/2024/08/23/cell-kernels) on this specific example.

