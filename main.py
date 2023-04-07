import math
import heapq
import networkx as nx
import matplotlib.pyplot as plt
from collections import defaultdict
import random
import time


def dijkstra(graph, start, end):
    dist = defaultdict(lambda: math.inf)
    dist[start] = 0
    visited = set()
    heap = [(0, start)]
    predecessors = {}

    while heap:
        min_dist, min_node = heapq.heappop(heap)

        if min_node == end:
            break

        if min_node in visited:
            continue

        for neighbor in graph.neighbors(min_node):
            if neighbor not in visited:
                new_dist = dist[min_node] + graph[min_node][neighbor]['weight']
                if new_dist < dist[neighbor]:
                    dist[neighbor] = new_dist
                    predecessors[neighbor] = min_node
                    heapq.heappush(heap, (new_dist, neighbor))

        visited.add(min_node)

    path = []
    node = end
    while node != start:
        path.append(node)
        node = predecessors[node]
    path.append(start)
    path.reverse()

    return path


def draw_path_edges(G, pos, path):
    # Draw the path edges and nodes
    edge_list = [(path[i], path[i+1]) for i in range(len(path)-1)]
    path_nodes = path
    edge_color = 'green'
    node_color = 'green'

    # Draw edges
    nx.draw_networkx_edges(G, pos, edgelist=edge_list, edge_color=edge_color, width=1)

    # Draw nodes
    nx.draw_networkx_nodes(G, pos, nodelist=path_nodes, node_color=node_color, node_size=200)

    # Draw edge labels on top of green line
    nx.draw_networkx_edge_labels(G, pos, edge_labels={(u, v): d['weight'] for u, v, d in G.edges(data=True)}, font_size=8)

    plt.draw()

def on_click(event):
    global selected_nodes, path_edges, path_nodes
    
    if event.button == 1: # left click
        if len(selected_nodes) < 2:
            node = None
            for n in G.nodes():
                if (pos[n][0]-event.xdata)**2 + (pos[n][1]-event.ydata)**2 < 0.01:
                    node = n
                    break
            if node is not None:
                selected_nodes.append(node)
                nx.draw_networkx_nodes(G, pos, nodelist=[node], node_color="green", node_size=200)
                plt.draw()
        
            if len(selected_nodes) == 2:
                path = dijkstra(G, selected_nodes[0], selected_nodes[1])
                print(path)
                for i in range(len(path)-1):
                    edge = (path[i], path[i+1])
                    if edge not in path_edges and (edge[1], edge[0]) not in path_edges:
                        path_edges.add(edge)
                        nx.draw_networkx_edges(G, pos, edgelist=[edge], edge_color="green", width=1)
                        plt.draw()
                        time.sleep(0.5)
                draw_path_edges(G, pos, path)

    elif event.button == 3: # right click
        nx.draw_networkx_nodes(G, pos, node_size=200, node_color="#FFAE42", linewidths=0.5)
        nx.draw_networkx_edges(G, pos, edge_color = "#000000", width = 1)
        nx.draw_networkx_labels(G, pos, font_size=10)
        nx.draw_networkx_edge_labels(G, pos, edge_labels={(u, v): d['weight'] for u, v, d in G.edges(data=True)}, font_size=8)

        path_edges.clear()
        selected_nodes.clear()
        path_nodes.clear()
        plt.draw()

# Prompt the user for the graph parameters
n = 12
p = .25

G = nx.erdos_renyi_graph(n, p, seed=42)
for u, v, d in G.edges(data=True):
    d['weight'] = float(random.randint(1, 10))

# Draw the graph
pos = nx.spring_layout(G, k=.4*n)
nx.draw_networkx_nodes(G, pos, node_size=200, node_color="#FFAE42", linewidths=0.5)
nx.draw_networkx_edges(G, pos, edge_color = "#000000", width = 1)
nx.draw_networkx_labels(G, pos, font_size=10)
nx.draw_networkx_edge_labels(G, pos, edge_labels={(u, v): d['weight'] for u, v, d in G.edges(data=True)}, font_size=8)

selected_nodes = list()
path_nodes = list()
path_edges = set()

cid = plt.gcf().canvas.mpl_connect("button_press_event", on_click)
plt.show()