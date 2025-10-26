from typing import Literal, TypedDict
from langgraph.graph import StateGraph, END
import time

class State(TypedDict, total=False):
    item_id: str
    step: str
    result: str
    ebay_url: str
    user_id: str

def ingest_node(state: State) -> State:
    print(f"🔍 DUMMY AGENT: Working on data ingestion for item {state.get('item_id', 'unknown')}")
    print(f"   📥 Scraping eBay URL: {state.get('ebay_url', 'N/A')}")
    time.sleep(10)  # Simulate 10 seconds of work
    
    state["step"] = "ingest"
    state["result"] = "Data scraped successfully"
    print(f"   ✅ Ingestion complete!")
    return state

def value_node(state: State) -> State:
    print(f"💰 DUMMY AGENT: Working on property valuation for item {state.get('item_id', 'unknown')}")
    print(f"   🏠 Analyzing property features and market data...")
    time.sleep(10)  # Simulate 10 seconds of work
    
    state["step"] = "value"
    state["result"] = "Property valued at $150,000"
    print(f"   ✅ Valuation complete!")
    return state

def market_analysis_node(state: State) -> State:
    print(f"📊 DUMMY AGENT: Working on market analysis for item {state.get('item_id', 'unknown')}")
    print(f"   📈 Analyzing market trends and comparable sales...")
    time.sleep(10)  # Simulate 10 seconds of work
    
    state["step"] = "market_analysis"
    state["result"] = "Market analysis: Strong growth potential"
    print(f"   ✅ Market analysis complete!")
    return state

def investment_advice_node(state: State) -> State:
    print(f"💡 DUMMY AGENT: Working on investment advice for item {state.get('item_id', 'unknown')}")
    print(f"   🎯 Generating personalized investment recommendations...")
    time.sleep(10)  # Simulate 10 seconds of work
    
    state["step"] = "investment_advice"
    state["result"] = "Investment advice: BUY - Strong potential for 15% ROI"
    print(f"   ✅ Investment advice complete!")
    return state

def build_graph():
    g = StateGraph(State)
    g.add_node("ingest", ingest_node)
    g.add_node("value", value_node)
    g.add_node("market_analysis", market_analysis_node)
    g.add_node("investment_advice", investment_advice_node)
    
    g.set_entry_point("ingest")
    g.add_edge("ingest", "value")
    g.add_edge("value", "market_analysis")
    g.add_edge("market_analysis", "investment_advice")
    g.add_edge("investment_advice", END)
    
    return g.compile()