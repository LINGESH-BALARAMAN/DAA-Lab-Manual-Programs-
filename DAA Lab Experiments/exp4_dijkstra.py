import heapq
import math
import matplotlib.pyplot as plt

def dijkstra(graph, source):
    """
    Dijkstra's Algorithm using Min-Heap
    Time: O((V + E) log V), Space: O(V)
    graph: dict {u: [(v, weight), ...]}, 0-indexed
    """
    n = len(graph)
    dist = [float('inf')] * n
    prev = [None] * n
    dist[source] = 0
    pq = [(0, source)]  # (distance, vertex)
    visited = set()

    while pq:
        d, u = heapq.heappop(pq)
        if u in visited:
            continue
        visited.add(u)
        for v, w in graph[u]:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                prev[v] = u
                heapq.heappush(pq, (dist[v], v))

    return dist, prev

def reconstruct_path(prev, source, target):
    path = []
    node = target
    while node is not None:
        path.append(node)
        node = prev[node]
    path.reverse()
    if path[0] == source:
        return path
    return []

# --- Graph Definition (Adjacency List) ---
graph = {
    0: [(1, 4), (2, 1)],
    1: [(3, 1)],
    2: [(1, 2), (3, 5)],
    3: [(4, 3)],
    4: [(5, 2)],
    5: []
}

source = 0
dist, prev = dijkstra(graph, source)

print(f'Shortest paths from vertex {source}:')
print(f'{"Vertex":>8} {"Distance":>10} {"Path":>30}')
print('-' * 55)
for v in range(len(graph)):
    path = reconstruct_path(prev, source, v)
    path_str = ' -> '.join(map(str, path)) if path else 'No path'
    d = dist[v] if dist[v] != float('inf') else 'INF'
    print(f'{v:>8} {str(d):>10} {path_str:>30}')

# --- Graphical Representation (Matplotlib) ---
n = len(graph)

# Plot 1: Bar chart of shortest distances from source
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 6))

vertices = list(range(n))
distances = [dist[v] for v in vertices]
colors = ['tab:orange' if v == source else 'tab:blue' for v in vertices]

ax1.bar(vertices, distances, color=colors)
for v, d in zip(vertices, distances):
    ax1.text(v, d + 0.1, str(d), ha='center', fontsize=10)
ax1.set_xlabel('Vertex')
ax1.set_ylabel('Shortest Distance')
ax1.set_title(f'Shortest Distances from Source Vertex {source}')
ax1.set_xticks(vertices)
ax1.grid(True, axis='y', alpha=0.3)

# Plot 2: Graph with shortest-path tree highlighted
positions = {}
for i in range(n):
    angle = 2 * math.pi * i / n
    positions[i] = (math.cos(angle), math.sin(angle))

# Collect shortest-path tree edges from prev[]
tree_edges = set()
for v in range(n):
    if prev[v] is not None:
        tree_edges.add((prev[v], v))

# Draw all original directed edges (light gray)
for u in graph:
    for v, w in graph[u]:
        x1, y1 = positions[u]
        x2, y2 = positions[v]
        is_tree = (u, v) in tree_edges
        ax2.annotate('', xy=(x2, y2), xytext=(x1, y1),
                     arrowprops=dict(arrowstyle='-|>',
                                      color='tab:blue' if is_tree else 'lightgray',
                                      lw=2.5 if is_tree else 1,
                                      shrinkA=15, shrinkB=15))
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        ax2.text(mx, my, str(w), fontsize=8, color='black',
                  bbox=dict(boxstyle='round,pad=0.1', fc='white', ec='none', alpha=0.7))

for node, (x, y) in positions.items():
    color = 'tab:orange' if node == source else 'tab:green'
    ax2.scatter(x, y, s=600, color=color, zorder=2, edgecolors='black')
    ax2.text(x, y, str(node), fontsize=11, ha='center', va='center', zorder=3, fontweight='bold')

ax2.set_title('Shortest Path Tree (highlighted) from Source')
ax2.set_xlim(-1.4, 1.4)
ax2.set_ylim(-1.4, 1.4)
ax2.set_aspect('equal')
ax2.axis('off')

plt.tight_layout()
plt.savefig('exp4_dijkstra.png', dpi=150)
plt.show()
