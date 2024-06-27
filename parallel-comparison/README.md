# Performance comparison of CPU and GPU serial and parallel execution

This notebook explores the performance differences between serial and parallel execution on CPU and GPU using PyTorch. We'll compare the execution times of intensive computational tasks performed sequentially on CPU and GPU, as well as in parallel configurations.

We can observe that parallel execution on multiple CPU cores (`Parallel CPU`) outperformed serial GPU (`Serial GPU`), serial CPU (`Serial CPU`) and parallel CPU (`Parallel CPU`) executions for the given workload. This emphasizes the efficiency of utilizing multiple CPU cores.