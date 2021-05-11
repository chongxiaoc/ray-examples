from horovod.ray import RayExecutor
import ray

# Start the Ray cluster or attach to an existing Ray cluster
ray.init()

num_hosts = 4
num_slots = 1

# Start num_hosts * num_slots actors on the cluster
settings = RayExecutor.create_settings(timeout_s=30)
executor = RayExecutor(settings, num_hosts=num_hosts, num_slots=num_slots, use_gpu=True)

# Launch the Ray actors on each machine
# This will launch `num_slots` actors on each machine
executor.start()

# Using the stateless `run` method, a function can take in any args or kwargs
def simple_fn():
    hvd.init()
    print("hvd rank", hvd.rank())
    return hvd.rank()

# Execute the function on all workers at once
result = executor.run(simple_fn)
# Check that the rank of all workers is unique
assert len(set(result)) == hosts * num_slots

executor.shutdown()
