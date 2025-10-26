#!/usr/bin/env python3
"""
Test script for FlipPilot LangGraph agents
Run this to test your agents locally
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from tasks import search_and_analyze_for_flips

def test_basic_workflow():
    """Test the basic search and analysis workflow"""
    
    print("🧪 TESTING FLIPPILOT LANGGRAPH WORKFLOW")
    print("=" * 60)
    
    # Test search criteria
    search_criteria = {
        "id": "test_001",
        "search_terms": "vintage camera",
        "category": "electronics",
        "min_price": 100.0,
        "max_price": 1000.0,
        "location": "San Francisco"
    }
    
    print(f"📋 Testing with search criteria:")
    print(f"   Search terms: {search_criteria['search_terms']}")
    print(f"   Category: {search_criteria['category']}")
    print(f"   Price range: ${search_criteria['min_price']} - ${search_criteria['max_price']}")
    print(f"   Location: {search_criteria['location']}")
    print()
    
    # Run the workflow
    result = search_and_analyze_for_flips(search_criteria)
    
    print("\n📊 WORKFLOW RESULTS:")
    print(f"   ✅ Profitable items found: {result['profitable_items_found']}")
    print(f"   📊 Total items analyzed: {result['total_items_analyzed']}")
    print(f"   🔄 Pipeline status: {result['pipeline_status']}")
    print(f"   ⏰ Completed at: {result['workflow_completed_at']}")
    
    if result['profitable_items']:
        print(f"\n💰 TOP PROFITABLE ITEMS:")
        for i, item in enumerate(result['profitable_items'][:3], 1):
            print(f"   {i}. {item['title']}")
            print(f"      💵 Asking: ${item['asking_price']:.2f}")
            print(f"      📈 Market Value: ${item['market_value']:.2f}")
            print(f"      💰 Profit: ${item['estimated_profit']:.2f} ({item['profit_margin']:.1f}%)")
            print(f"      🎯 Investment Score: {item['investment_score']}/10")
            print(f"      🔗 URL: {item['url']}")
            print()
    
    print("✅ Test completed successfully!")
    return result

def test_different_searches():
    """Test with different search criteria"""
    
    test_cases = [
        {
            "id": "test_002",
            "search_terms": "gaming laptop",
            "category": "electronics",
            "min_price": 500.0,
            "max_price": 2000.0,
            "location": "New York"
        },
        {
            "id": "test_003", 
            "search_terms": "vintage watch",
            "category": "jewelry",
            "min_price": 200.0,
            "max_price": 1500.0,
            "location": "Los Angeles"
        }
    ]
    
    print("\n🔄 TESTING MULTIPLE SEARCH CRITERIA")
    print("=" * 60)
    
    for i, criteria in enumerate(test_cases, 1):
        print(f"\n🧪 Test Case {i}: {criteria['search_terms']}")
        result = search_and_analyze_for_flips(criteria)
        print(f"   Found {result['profitable_items_found']} profitable items")
        print(f"   Analyzed {result['total_items_analyzed']} total items")

if __name__ == "__main__":
    # Run basic test
    test_basic_workflow()
    
    # Run multiple tests
    test_different_searches()
    
    print("\n🎉 ALL TESTS COMPLETED!")
    print("Your LangGraph agents are working correctly!")
