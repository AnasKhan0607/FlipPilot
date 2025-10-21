from graph import build_graph

def run_pipeline(payload: dict):
    graph = build_graph()
    return graph.invoke(payload)