import ray


ray.init(address='auto')


def square(x: int) -> int:
    return x * x


remote_square = ray.remote(square)
values = list(range(10))
results = ray.get([remote_square.remote(v) for v in values])
print('Input :', values)
print('Output:', results)
