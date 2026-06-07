import random

import ray


ray.init(address='auto')


@ray.remote
def count_inside(samples: int) -> int:
    inside = 0
    for _ in range(samples):
        x = random.random()
        y = random.random()
        if x * x + y * y <= 1.0:
            inside += 1
    return inside


workers = 16
samples_per_worker = 100_000
inside_total = sum(ray.get([count_inside.remote(samples_per_worker) for _ in range(workers)]))
total_samples = workers * samples_per_worker
pi_estimate = 4.0 * inside_total / total_samples

print('Workers            :', workers)
print('Samples per worker :', samples_per_worker)
print('Total samples      :', total_samples)
print('Estimated pi       :', pi_estimate)
