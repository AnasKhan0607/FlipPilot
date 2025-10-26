import os
from rq import Queue, Worker
from rq_scheduler import Scheduler
import redis

# RQ worker bootstrap
redis_url = os.getenv("REDIS_URL", "redis://localhost:6379/0")
conn = redis.from_url(redis_url)
queues = [Queue("deals", connection=conn)]

def setup_scheduled_jobs():
    """Set up scheduled jobs for watchlist monitoring"""
    scheduler = Scheduler(connection=conn)
    
    # Schedule watchlist monitoring every 15 minutes
    scheduler.schedule(
        scheduled_time=None,  # Start immediately
        func="flippilot_agents.tasks.monitor_watchlist",
        interval=900,  # 15 minutes in seconds
        repeat=None,   # Repeat indefinitely
        queue_name="deals"
    )
    
    print("Scheduled watchlist monitoring every 15 minutes")

if __name__ == "__main__":
    # Set up scheduled jobs
    setup_scheduled_jobs()
    
    # Start worker with scheduler
    Worker(queues, connection=conn).work(with_scheduler=True)