import os
from rq import Queue, Worker
import redis

# RQ worker bootstrap
redis_url = os.getenv("REDIS_URL", "redis://localhost:6379/0")
conn = redis.from_url(redis_url)
queues = [Queue("deals", connection=conn)]

if __name__ == "__main__":
    Worker(queues, connection=conn).work(with_scheduler=True)