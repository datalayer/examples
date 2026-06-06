[![Datalayer](https://assets.datalayer.tech/datalayer-25.svg)](https://datalayer.ai)

# Ray CLI Examples

These examples are designed to be submitted with the Datalayer Ray CLI.

## Prerequisites

Before running these examples, make sure you have an account on [Datalayer AI](https://datalayer.ai).

## Create a Cluster

```bash
datalaeyr ray clusters ls
datalayer ray clusters create my-ray --namespace default --worker-replicas 1
datalayer ray clusters ls # my-ray should be added to the list.
datalayer ray clusters get my-ray --namespace default
```

## Example 1: Hello Ray

```bash
JOB_NAME="hello-ray-$(date +%s)"
datalayer ray jobs submit my-ray --namespace default --job-name "${JOB_NAME}" --py @ray/hello_ray.py
datalayer ray jobs monitor "${JOB_NAME}" --namespace default
datalayer ray jobs logs "${JOB_NAME}" --namespace default --tail-lines 200
```

## Example 2: Monte Carlo Pi

```bash
JOB_NAME="pi-monte-carlo-$(date +%s)"
datalayer ray jobs submit my-ray --namespace default --job-name "${JOB_NAME}" --py @ray/pi_monte_carlo.py
datalayer ray jobs monitor "${JOB_NAME}" --namespace default
datalayer ray jobs logs "${JOB_NAME}" --namespace default --tail-lines 200
```

## Example 3: Stateful Actor Counter

```bash
JOB_NAME="actor-counter-$(date +%s)"
datalayer ray jobs submit my-ray --namespace default --job-name "${JOB_NAME}" --py @ray/actor_counter.py
datalayer ray jobs monitor "${JOB_NAME}" --namespace default
datalayer ray jobs logs "${JOB_NAME}" --namespace default --tail-lines 200
```

## Cleanup

```bash
datalayer ray jobs ls --namespace default --cluster-name my-ray
datalayer ray clusters delete my-ray --namespace default
```
