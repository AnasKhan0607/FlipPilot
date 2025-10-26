"""
Watchlist management routes
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
import redis
from rq import Queue
import uuid

router = APIRouter()

# Redis connection
redis_conn = redis.from_url("redis://localhost:6379/0")
queue = Queue("deals", connection=redis_conn)

# Pydantic models
class WatchlistSearch(BaseModel):
    """User's search criteria for items they want to track"""
    user_id: str
    search_terms: str  # e.g., "vintage furniture", "real estate", "investment property"
    category: str  # e.g., "furniture", "real_estate", "electronics"
    max_price: Optional[float] = None
    min_price: Optional[float] = None
    location: Optional[str] = None  # e.g., "San Francisco", "Bay Area"
    notification_preferences: dict = {}

class WatchlistSearchResponse(BaseModel):
    """Response when user adds a search to watchlist"""
    id: str
    user_id: str
    search_terms: str
    category: str
    max_price: Optional[float] = None
    min_price: Optional[float] = None
    location: Optional[str] = None
    status: str
    created_at: str
    items_found: int = 0

class PotentialFlip(BaseModel):
    """Items analyzed by agents as profitable flip opportunities"""
    id: str
    watchlist_search_id: str
    platform: str  # "ebay", "craigslist", "facebook", etc.
    url: str
    title: str
    asking_price: float
    market_value: float
    estimated_profit: float
    profit_margin: float  # percentage
    location: str
    description: str
    images: List[str] = []
    posted_date: str
    analyzed_at: str
    investment_score: int  # 1-10 rating
    risk_level: str  # "low", "medium", "high"
    status: str = "active"  # "active", "sold", "expired"

class JobStatus(BaseModel):
    job_id: str
    status: str
    result: Optional[dict] = None

# In-memory storage (replace with database in production)
watchlist_searches_db = {}
potential_flips_db = {}

@router.post("/watchlist/add", response_model=WatchlistSearchResponse)
def add_to_watchlist(search: WatchlistSearch):
    """Add search criteria to user's watchlist"""
    
    # Generate unique ID
    search_id = str(uuid.uuid4())
    
    # Create watchlist search
    watchlist_search = {
        "id": search_id,
        "user_id": search.user_id,
        "search_terms": search.search_terms,
        "category": search.category,
        "max_price": search.max_price,
        "min_price": search.min_price,
        "location": search.location,
        "notification_preferences": search.notification_preferences,
        "status": "active",
        "created_at": datetime.now().isoformat(),
        "items_found": 0
    }
    
    # Store in memory (replace with database)
    watchlist_searches_db[search_id] = watchlist_search
    
    # Queue analysis job for agents to find profitable flips
    job = queue.enqueue(
        "flippilot_agents.tasks.search_and_analyze_for_flips",
        watchlist_search
    )
    
    return WatchlistSearchResponse(**watchlist_search)

@router.get("/watchlist/{user_id}", response_model=List[WatchlistSearchResponse])
def get_watchlist(user_id: str):
    """Get user's watchlist searches"""
    user_searches = [
        search for search in watchlist_searches_db.values() 
        if search["user_id"] == user_id and search["status"] == "active"
    ]
    return [WatchlistSearchResponse(**search) for search in user_searches]

@router.get("/watchlist/search/{search_id}", response_model=WatchlistSearchResponse)
def get_watchlist_search(search_id: str):
    """Get specific watchlist search"""
    if search_id not in watchlist_searches_db:
        raise HTTPException(status_code=404, detail="Search not found")
    
    return WatchlistSearchResponse(**watchlist_searches_db[search_id])

@router.get("/watchlist/search/{search_id}/flips", response_model=List[PotentialFlip])
def get_potential_flips(search_id: str):
    """Get potential flip opportunities found for a specific search"""
    if search_id not in watchlist_searches_db:
        raise HTTPException(status_code=404, detail="Search not found")
    
    potential_flips = [
        flip for flip in potential_flips_db.values()
        if flip["watchlist_search_id"] == search_id and flip["status"] == "active"
    ]
    return [PotentialFlip(**flip) for flip in potential_flips]

@router.get("/flips/{user_id}", response_model=List[PotentialFlip])
def get_user_potential_flips(user_id: str):
    """Get all potential flip opportunities for a user"""
    user_flips = [
        flip for flip in potential_flips_db.values()
        if flip["status"] == "active"
    ]
    return [PotentialFlip(**flip) for flip in user_flips]

@router.put("/watchlist/search/{search_id}")
def update_watchlist_search(search_id: str, updates: dict):
    """Update watchlist search criteria"""
    if search_id not in watchlist_searches_db:
        raise HTTPException(status_code=404, detail="Search not found")
    
    # Update search
    for key, value in updates.items():
        if key in watchlist_searches_db[search_id]:
            watchlist_searches_db[search_id][key] = value
    
    return {"status": "updated", "search_id": search_id}

@router.delete("/watchlist/search/{search_id}")
def remove_from_watchlist(search_id: str):
    """Remove search from watchlist"""
    if search_id not in watchlist_searches_db:
        raise HTTPException(status_code=404, detail="Search not found")
    
    # Mark as inactive instead of deleting
    watchlist_searches_db[search_id]["status"] = "inactive"
    
    return {"status": "removed", "search_id": search_id}

@router.get("/job-status/{job_id}", response_model=JobStatus)
def get_job_status(job_id: str):
    """Check job status"""
    job = queue.fetch_job(job_id)
    if job:
        return JobStatus(
            job_id=job_id,
            status=job.get_status(),
            result=job.result
        )
    return JobStatus(job_id=job_id, status="not_found")
