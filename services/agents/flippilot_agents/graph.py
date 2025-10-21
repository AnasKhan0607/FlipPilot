from typing import Literal, TypedDict
from langgraph.graph import StateGraph, END

class State(TypedDict, total=False):
    item_id: str
    step: str
    result: str

def ingest_node(state: State) -> State:
    state["step"] = "ingest"; state["result"] = "ok"
    return state

def value_node(state: State) -> State:
    state["step"] = "value"; state["result"] = "fair_value=123"
    return state

def build_graph():
    g = StateGraph(State)
    g.add_node("ingest", ingest_node)
    g.add_node("value", value_node)
    g.set_entry_point("ingest")
    g.add_edge("ingest", "value")
    g.add_edge("value", END)
    return g.compile()