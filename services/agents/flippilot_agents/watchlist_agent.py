"""
Watchlist monitoring agent for FlipPilot
Handles scheduled monitoring of user watchlists
"""

from rq_scheduler import Scheduler
import redis
from datetime import datetime, timedelta
import requests
from bs4 import BeautifulSoup
import json

def setup_watchlist_monitoring():
    """Set up scheduled monitoring of watchlist items"""
    
    redis_conn = redis.from_url("redis://localhost:6379/0")
    scheduler = Scheduler(connection=redis_conn)
    
    # Schedule watchlist monitoring every 15 minutes
    scheduler.schedule(
        scheduled_time=None,  # Start immediately
        func="flippilot_agents.tasks.monitor_watchlist",
        interval=900,  # 15 minutes in seconds
        repeat=None,   # Repeat indefinitely
        queue_name="deals"
    )
    
    print("Watchlist monitoring scheduled every 15 minutes")

def scrape_ebay_item(ebay_url):
    """Scrape eBay item data"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        response = requests.get(ebay_url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extract item data
        item_data = {
            "url": ebay_url,
            "title": extract_title(soup),
            "price": extract_price(soup),
            "availability": extract_availability(soup),
            "description": extract_description(soup),
            "images": extract_images(soup),
            "seller": extract_seller(soup),
            "scraped_at": datetime.now().isoformat()
        }
        
        return item_data
        
    except Exception as e:
        print(f"Error scraping eBay item {ebay_url}: {e}")
        return None

def extract_title(soup):
    """Extract item title"""
    title_elem = soup.find('h1', {'id': 'x-title-label-lbl'})
    if title_elem:
        return title_elem.get_text().strip()
    return "Title not found"

def extract_price(soup):
    """Extract item price"""
    price_elem = soup.find('span', {'id': 'prcIsum'})
    if price_elem:
        price_text = price_elem.get_text().strip()
        # Extract numeric price
        import re
        price_match = re.search(r'[\d,]+\.?\d*', price_text.replace(',', ''))
        if price_match:
            return float(price_match.group())
    return 0.0

def extract_availability(soup):
    """Extract item availability"""
    # Check for "Buy It Now" button
    buy_now = soup.find('a', {'id': 'binBtn_btn'})
    if buy_now:
        return True
    
    # Check for auction status
    auction = soup.find('span', {'id': 'mm-saleDscPrc'})
    if auction:
        return True
    
    return False

def extract_description(soup):
    """Extract item description"""
    desc_elem = soup.find('div', {'id': 'desc_div'})
    if desc_elem:
        return desc_elem.get_text().strip()[:500]  # Limit to 500 chars
    return "Description not found"

def extract_images(soup):
    """Extract item images"""
    images = []
    img_elements = soup.find_all('img', {'id': 'icImg'})
    for img in img_elements:
        src = img.get('src')
        if src:
            images.append(src)
    return images

def extract_seller(soup):
    """Extract seller information"""
    seller_elem = soup.find('span', {'class': 'mbg-nw'})
    if seller_elem:
        return seller_elem.get_text().strip()
    return "Seller not found"

def detect_changes(old_data, new_data):
    """Detect changes in item data"""
    
    if not old_data or not new_data:
        return {"error": "Missing data for comparison"}
    
    changes = {}
    
    # Price changes
    old_price = old_data.get("price", 0)
    new_price = new_data.get("price", 0)
    
    if old_price != new_price and old_price > 0:
        change_percent = ((new_price - old_price) / old_price) * 100
        changes["price"] = {
            "old": old_price,
            "new": new_price,
            "change_percent": round(change_percent, 2),
            "change_amount": round(new_price - old_price, 2)
        }
    
    # Availability changes
    old_available = old_data.get("availability", False)
    new_available = new_data.get("availability", False)
    
    if old_available != new_available:
        changes["availability"] = {
            "old": old_available,
            "new": new_available,
            "status": "became_available" if new_available else "became_unavailable"
        }
    
    # Title changes
    old_title = old_data.get("title", "")
    new_title = new_data.get("title", "")
    
    if old_title != new_title:
        changes["title"] = {
            "old": old_title,
            "new": new_title
        }
    
    # Description changes
    old_desc = old_data.get("description", "")
    new_desc = new_data.get("description", "")
    
    if old_desc != new_desc:
        changes["description"] = "updated"
    
    return changes

def should_notify_user(item, changes):
    """Determine if user should be notified"""
    
    if not changes or "error" in changes:
        return False
    
    # Price dropped below target
    if changes.get("price"):
        new_price = changes["price"]["new"]
        target_price = item.get("target_price", 0)
        
        if new_price <= target_price:
            return True
        
        # Significant price drop (>20%)
        if changes["price"]["change_percent"] < -20:
            return True
    
    # Item became available
    if changes.get("availability") and changes["availability"]["new"]:
        return True
    
    return False

def generate_notification(item, changes):
    """Generate notification message for user"""
    
    notifications = []
    
    # Price alerts
    if changes.get("price"):
        price_change = changes["price"]
        new_price = price_change["new"]
        target_price = item.get("target_price", 0)
        
        if new_price <= target_price:
            notifications.append({
                "type": "target_reached",
                "message": f"🎯 Target reached! {item['item_name']} is now ${new_price} (target: ${target_price})",
                "priority": "high"
            })
        
        elif price_change["change_percent"] < -20:
            notifications.append({
                "type": "major_drop",
                "message": f"📉 Major price drop! {item['item_name']} dropped {abs(price_change['change_percent'])}% to ${new_price}",
                "priority": "medium"
            })
    
    # Availability alerts
    if changes.get("availability") and changes["availability"]["new"]:
        notifications.append({
            "type": "available",
            "message": f"✅ {item['item_name']} is now available!",
            "priority": "medium"
        })
    
    return notifications
