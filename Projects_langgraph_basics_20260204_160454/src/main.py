from collections import deque


NODES = {
    "start": lambda state: {**state, "steps": state["steps"] + ["start"]},
    "retrieve": lambda state: {**state, "steps": state["steps"] + ["retrieve"]},
    "generate": lambda state: {**state, "steps": state["steps"] + ["generate"]},
}

EDGES = {
    "start": ["retrieve"],
    "retrieve": ["generate"],
    "generate": [],
}



def run_graph(start_node):
    state = {"steps": []}
    queue = deque([start_node])
    while queue:
        node = queue.popleft()
        state = NODES[node](state)
        queue.extend(EDGES[node])
    return state


if __name__ == "__main__":
    result = run_graph("start")
    print(" -> ".join(result["steps"]))
