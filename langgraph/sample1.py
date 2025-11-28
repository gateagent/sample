import os
from gateagent import init ## Change1: import gateagent package

os.environ["GATEAGENT_API_KEY"] = "your_key"                    ## Change2: set your API key
os.environ["GATEAGENT_ENDPOINT"] = "https://api.gateagent.dev"  ## Change2:
os.environ["GATEAGENT_PROJECT"] = "test-graph"                  ## Change2:

# enable tracing
init() ## Change3: initialize gateagent package

# ---- LangGraph stuff ----
from langgraph.graph import StateGraph, END

def node1(state):
    return {"x": state["x"] + 1}

def node2(state):
    return {"x": state["x"] * 2}

g = StateGraph(dict)
g.add_node("n1", node1)
g.add_node("n2", node2)
g.set_entry_point("n1")
g.add_edge("n1", "n2")
g.add_edge("n2", END)

app = g.compile()
print(app.invoke({"x": 10}))
