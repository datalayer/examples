## GPU sanity checks

This notebook contains scripts and tests to perform GPU sanity checks using PyTorch and CUDA. The primary goal of these checks is to ensure that the GPU resources meet the expected requirements.

The notebook:
- Validate GPU Count: Ensure that the expected number of GPUs is available for computation.
- Verify GPU Memory: Check that each GPU has the expected memory capacity to handle the anticipated workload.
- Test Tensor Loading: Validate the ability to load tensors of specified sizes onto each GPU without exceeding memory limits.
