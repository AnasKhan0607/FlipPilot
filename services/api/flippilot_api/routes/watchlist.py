"""
Simple Watchlist API using Redis as database
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
import redis
import json
import uuid
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

# Redis connection for all data
import os
redis_url = os.getenv("REDIS_URL", "redis://localhost:6379/0")
redis_conn = redis.from_url(redis_url)

# Pydantic models
class CreateUserRequest(BaseModel):
    email: str
    name: str
    location: Optional[str] = None

class UserResponse(BaseModel):
    id: str
    email: str
    name: str
    location: Optional[str] = None
    created_at: str

class CreateWatchlistRequest(BaseModel):
    user_id: str
    name: str  # e.g., "vintage camera"
    location: Optional[str] = None

class WatchlistResponse(BaseModel):
    id: str
    user_id: str
    name: str
    location: Optional[str] = None
    created_at: str

class AddToWatchlistRequest(BaseModel):
    watchlist_id: str
    item_name: str  # What they're looking for
    location: Optional[str] = None

class RemoveFromWatchlistRequest(BaseModel):
    watchlist_id: str
    item_id: str

# Helper functions
def get_user(user_id: str) -> Optional[dict]:
    """Get user from Redis"""
    data = redis_conn.get(f"user:{user_id}")
    return json.loads(data) if data else None

def get_watchlist(watchlist_id: str) -> Optional[dict]:
    """Get watchlist from Redis"""
    data = redis_conn.get(f"watchlist:{watchlist_id}")
    return json.loads(data) if data else None

# API Endpoints

@router.post("/users", response_model=UserResponse)
def create_user(request: CreateUserRequest):
    """Create a new user"""
    logger.info(f"Creating user: {request.email}")
    user_id = str(uuid.uuid4())
    user = {
        "id": user_id,
        "email": request.email,
        "name": request.name,
        "location": request.location,
        "created_at": datetime.now().isoformat()
    }
    
    # Store in Redis
    redis_conn.set(f"user:{user_id}", json.dumps(user))
    
    # Add to users list
    redis_conn.sadd("users", user_id)
    
    logger.info(f"User created successfully: {user_id}")
    return UserResponse(**user)

@router.post("/watchlists", response_model=WatchlistResponse)
def create_watchlist(request: CreateWatchlistRequest):
    """Create a new watchlist"""
    logger.info(f"Creating watchlist '{request.name}' for user: {request.user_id}")
    # Check if user exists
    if not get_user(request.user_id):
        raise HTTPException(status_code=404, detail="User not found")
    
    watchlist_id = str(uuid.uuid4())
    watchlist = {
        "id": watchlist_id,
        "user_id": request.user_id,
        "name": request.name,
        "location": request.location,
        "items": [],
        "created_at": datetime.now().isoformat()
    }
    
    # Store in Redis
    redis_conn.set(f"watchlist:{watchlist_id}", json.dumps(watchlist))
    
    # Add to user's watchlists list
    redis_conn.sadd(f"user:{request.user_id}:watchlists", watchlist_id)
    
    logger.info(f"Watchlist created successfully: {watchlist_id}")
    return WatchlistResponse(**{k: v for k, v in watchlist.items() if k != 'items'})

@router.post("/watchlists/add")
def add_to_watchlist(request: AddToWatchlistRequest):
    """Add an item to a watchlist"""
    logger.info(f"Adding item '{request.item_name}' to watchlist: {request.watchlist_id}")
    watchlist = get_watchlist(request.watchlist_id)
    if not watchlist:
        raise HTTPException(status_code=404, detail="Watchlist not found")
    
    # Add item to watchlist
    item = {
        "id": str(uuid.uuid4()),
        "name": request.item_name,
        "location": request.location,
        "added_at": datetime.now().isoformat()
    }
    
    watchlist["items"].append(item)
    
    # Update in Redis
    redis_conn.set(f"watchlist:{request.watchlist_id}", json.dumps(watchlist))
    
    logger.info(f"Item added successfully: {item['id']}")
    return {"status": "success", "item": item}

@router.delete("/watchlists/{watchlist_id}")
def delete_watchlist(watchlist_id: str):
    """Delete a watchlist"""
    logger.info(f"Deleting watchlist: {watchlist_id}")
    watchlist = get_watchlist(watchlist_id)
    if not watchlist:
        raise HTTPException(status_code=404, detail="Watchlist not found")
    
    # Remove from Redis
    redis_conn.delete(f"watchlist:{watchlist_id}")
    
    # Remove from user's watchlists list
    redis_conn.srem(f"user:{watchlist['user_id']}:watchlists", watchlist_id)
    
    logger.info(f"Watchlist deleted successfully: {watchlist_id}")
    return {"status": "deleted", "watchlist_id": watchlist_id}

@router.delete("/watchlists/{watchlist_id}/items/{item_id}")
def remove_from_watchlist(watchlist_id: str, item_id: str):
    """Remove an item from a watchlist"""
    logger.info(f"Removing item {item_id} from watchlist: {watchlist_id}")
    watchlist = get_watchlist(watchlist_id)
    if not watchlist:
        raise HTTPException(status_code=404, detail="Watchlist not found")
    
    # Remove item
    watchlist["items"] = [item for item in watchlist["items"] if item["id"] != item_id]
    
    # Update in Redis
    redis_conn.set(f"watchlist:{watchlist_id}", json.dumps(watchlist))
    
    logger.info(f"Item removed successfully: {item_id}")
    return {"status": "removed", "item_id": item_id}

# Additional helper endpoints

@router.get("/users/{user_id}/watchlists")
def get_user_watchlists(user_id: str):
    """Get all watchlists for a user"""
    if not get_user(user_id):
        raise HTTPException(status_code=404, detail="User not found")
    
    watchlist_ids = redis_conn.smembers(f"user:{user_id}:watchlists")
    watchlists = []
    
    for watchlist_id in watchlist_ids:
        data = redis_conn.get(f"watchlist:{watchlist_id.decode()}")
        if data:
            watchlist = json.loads(data)
            # Return without items
            watchlists.append({k: v for k, v in watchlist.items() if k != 'items'})
    
    return watchlists

@router.get("/watchlists/{watchlist_id}")
def get_watchlist_items(watchlist_id: str):
    """Get all items in a watchlist"""
    watchlist = get_watchlist(watchlist_id)
    if not watchlist:
        raise HTTPException(status_code=404, detail="Watchlist not found")
    
    return {"watchlist_id": watchlist_id, "items": watchlist.get("items", [])}