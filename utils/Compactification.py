import networkx as nx


def compactify(graph, compactification_data=None):
    compact_graph = nx.Graph()
    # for node in graph.nodes():
    # compact_graph.add_node(graph.node[node][compactification_data])

    for node in graph.nodes():
        for edge in graph.edges(node):
            c_node_s = graph.node[edge[0]][compactification_data]
            c_node_e = graph.node[edge[1]][compactification_data]
            if compact_graph.has_edge(c_node_s, c_node_e):
                compact_graph[c_node_s][c_node_e]["weight"] += 1
            else:
                compact_graph.add_edge(c_node_s, c_node_e, weight=1)

    return compact_graph