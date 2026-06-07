import ray


ray.init(address='auto')


@ray.remote
class Counter:
    def __init__(self):
        self.value = 0

    def add(self, amount: int) -> int:
        self.value += amount
        return self.value

    def get(self) -> int:
        return self.value


counters = [Counter.remote() for _ in range(4)]

for step in [1, 2, 3, 4, 5]:
    ray.get([counter.add.remote(step) for counter in counters])

totals = ray.get([counter.get.remote() for counter in counters])
print('Per-actor totals:', totals)
print('Grand total     :', sum(totals))
