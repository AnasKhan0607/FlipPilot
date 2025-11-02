"""
One-shot script to register scheduled jobs with rq-scheduler
Run this once to set up all recurring jobs
"""
import os
import sys

# Add parent directory to Python path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from datetime import datetime, timedelta
from rq_scheduler import Scheduler
from redis import from_url

from flippilot_agents.tasks import monitor_watchlist

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
SCHEDULE_ID = "watchlist-monitor-01"

def main():
    conn = from_url(REDIS_URL)
    scheduler = Scheduler(connection=conn)

    # Idempotent: skip if already present
    existing_jobs = [j for j in scheduler.get_jobs() if hasattr(j, 'id') and j.id == SCHEDULE_ID]
    if existing_jobs:
        print(f"[scheduler] Job '{SCHEDULE_ID}' already exists; skipping")
        return

    scheduler.schedule(
        scheduled_time=datetime.utcnow() + timedelta(minutes=1),
        func=monitor_watchlist,
        interval=10,              # 10 seconds for testing. Use 900 for 15 minutes.
        repeat=None,
        queue_name="deals",
        id=SCHEDULE_ID,
    )
    print(f"[scheduler] Scheduled '{SCHEDULE_ID}' (interval=10s)")

if __name__ == "__main__":
    main()

