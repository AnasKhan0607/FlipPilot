from rq import Queue
from redis import from_url
from tasks import run_pipeline

q = Queue("deals", connection=from_url("redis://localhost:6379/0"))
job = q.enqueue(run_pipeline, {"item_id":"demo-1"})
print(job.id)
print(job.result)  # after it runs