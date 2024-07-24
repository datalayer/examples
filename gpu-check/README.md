[![Datalayer](https://assets.datalayer.tech/datalayer-25.svg)](https://datalayer.io)

[![Become a Sponsor](https://img.shields.io/static/v1?label=Become%20a%20Sponsor&message=%E2%9D%A4&logo=GitHub&style=flat&color=1ABC9C)](https://github.com/sponsors/datalayer)

## GPU Sanity Checks

This notebook contains scripts and tests to perform GPU sanity checks using PyTorch and CUDA. The primary goal of these checks is to ensure that the GPU resources meet the expected requirements.

The notebook:

- Validates GPU Count: Ensure that the expected number of GPUs is available for computation.
- Verifie GPU Memory: Check that each GPU has the expected memory capacity to handle the anticipated workload.
- Test Tensor Loading: Validate the ability to load tensors of specified sizes onto each GPU without exceeding memory limits.
