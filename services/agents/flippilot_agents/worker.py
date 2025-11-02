import os
import sys

# Add parent directory to Python path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from rq import Queue, Worker
import redis

# RQ worker bootstrap
redis_url = os.getenv("REDIS_URL", "redis://localhost:6379/0")
conn = redis.from_url(redis_url)
queues = [Queue("deals", connection=conn)]

if __name__ == "__main__":
    import logging
    
    # Set up logging for RQ
    logging.basicConfig(level=logging.INFO)
    
    print("Starting worker...")
    
    # Start worker - scheduler runs separately as a different service
    Worker(queues, connection=conn).work()