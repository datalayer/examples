[![Datalayer](https://assets.datalayer.tech/datalayer-25.svg)](https://datalayer.io)

[![Become a Sponsor](https://img.shields.io/static/v1?label=Become%20a%20Sponsor&message=%E2%9D%A4&logo=GitHub&style=flat&color=1ABC9C)](https://github.com/sponsors/datalayer)

# Ξ Datalayer Examples

This repository contains Jupyter notebook examples to showcase [Datalayer Run](https://datalayer.run). Datalayer Run allows you to scale Jupyter Kernels from your local JupyterLab on your machine to the cloud, including running your Kernels on GPU.

First, clone this repository.

```bash
git clone https://github.com/datalayer/examples.git datalayer-examples
cd datalayer-examples
```

To try the examples, we recommend creating a very simple conda environment (with Python and JupyterLab) thanks to the following commands.

```bash
ENV_NAME=datalayer-examples
# conda deactivate && conda remove -y --all -n $ENV_NAME # Delete if it already exists.
conda env create --solver=libmamba -n $ENV_NAME -f ./environment.yaml
conda activate $ENV_NAME
jupyter lab
```

Alternatively, you can just install the `datalayer-run` package in your existing environment with `pip install datalayer-run` (this will install JupyterLab version 4.0.3).

Read the [documentation website](https://docs.datalayer.run/docs) to know more how to scale your local notebooks to the cloud.

Don't worry, it is easy 👍. You just need to create an account, click on the `Datalayer Run` tile in the JupyterLab launcher, wait a bit for your Kernels to be ready, and then just assign a Remote Kernel from any Notebook kernel picker.

<div align="center" style="text-align: center">
  <img alt="Datalayer Run Examples" src="https://datalayer-examples.s3.amazonaws.com/datalayer-run-examples/kernel-selector-choice.png" />
</div>

The examples of this repository showcase the execution of code remotely from your local JupyterLab in various case as shown on the following picture.

<div align="center" style="text-align: center">
  <img alt="Datalayer Run Examples" src="https://datalayer-examples.s3.amazonaws.com/datalayer-run-examples/datalayer-run-examples.png" />
</div>

## Examples

1. [Simple Python](#simple-python)
1. [Titanic](#titanic)
1. [CUDA Vector Add](#cuda-vector-add)
1. [cuDF](#cudf)
1. [PyTorch](#pytorch)
1. [YouTube Face Detection](#youtube-face-detection)
1. [LLMA](#llma)

### [Simple Python](https://github.com/datalayer/examples/tree/main/python-simple)

Simple Python example.

### [Titanic](https://github.com/datalayer/examples/tree/main/titanic)

Titanic example.

### [CUDA Vector Add](https://github.com/datalayer/examples/tree/main/vectoradd-gpu)

CUDA vector addition example.

### [cuDF](https://github.com/datalayer/examples/tree/main/cudf-gpu)

cuDF example.

### [PyTorch](https://github.com/datalayer/examples/tree/main/pytorch-gpu)

PyTorch example.

### [YouTube Face Detection](https://github.com/datalayer/examples/tree/main/youtube-face-detection)

Detect faces from this famous video.

<div align="center" style="text-align: center">
  <img alt="YouTube Face Detection" src="https://datalayer-examples.s3.amazonaws.com/datalayer-run-examples/youtube-face-detection.png" />
</div>

### [LLMA](https://github.com/datalayer/examples/tree/main/llama-gpu)

LLMA example.
