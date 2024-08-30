[![Datalayer](https://assets.datalayer.tech/datalayer-25.svg)](https://datalayer.io)

[![Become a Sponsor](https://img.shields.io/static/v1?label=Become%20a%20Sponsor&message=%E2%9D%A4&logo=GitHub&style=flat&color=1ABC9C)](https://github.com/sponsors/datalayer)

# Performance Comparison of CPU and GPU Serial and Parallel Execution

This notebook explores the performance differences between serial and parallel execution on CPU and GPU using PyTorch. We'll compare the execution times of intensive computational tasks performed sequentially on CPU and GPU, as well as in parallel configurations.

We can observe that parallel execution on multiple CPU cores (`Parallel CPU`) outperformed serial GPU (`Serial GPU`), serial CPU (`Serial CPU`) and parallel CPU (`Parallel CPU`) executions for the given workload. This emphasizes the efficiency of utilizing multiple CPU cores.
