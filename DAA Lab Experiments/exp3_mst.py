import heapq
import math
import matplotlib.pyplot as plt

# --- Union-Find for Kruskal ---
class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank   = [0] * n

    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])  # Path compression
        return self.parent[x]

    def union(self, x, y):
        rx, ry = self.find(x), self.find(y)
        if rx == ry: return False
        if self.rank[rx] < self.rank[ry]: rx, ry = ry, rx
        self.parent[ry] = rx
        if self.rank[rx] == self.rank[ry]: self.rank[rx] += 1
        return True

def kruskal(n, edges):
    """edges: list of (weight, u, v)"""
    edges.sort()  # O(E log E)
    uf   = UnionFind(n)
    mst  = []
    cost = 0
    for w, u, v in edges:
        if uf.union(u, v):
            mst.append((u, v, w))
            cost += w
            if len(mst) == n - 1:
                break
    return mst, cost

def prim(n, adj, start=0):
    """adj: adjacency list {u: [(v, w), ...]}"""
    INF     = float('inf')
    key     = [INF] * n
    parent  = [-1]  * n
    inMST   = [False] * n
    key[start] = 0
    pq = [(0, start)]
    mst = []
    cost = 0
    while pq:
        w, u = heapq.heappop(pq)
        if inMST[u]: continue
        inMST[u] = True
        if parent[u] != -1:
            mst.append((parent[u], u, w))
            cost += w
        for v, wt in adj.get(u, []):
            if not inMST[v] and wt < key[v]:
                key[v] = wt
                parent[v] = u
                heapq.heappush(pq, (wt, v))
    return mst, cost

# --- Graph Definition ---
n = 7
edges = [
    (7, 0, 1), (5, 0, 3), (8, 1, 2), (9, 1, 3),
    (7, 1, 4), (5, 2, 4), (15, 3, 4), (6, 3, 5),
    (8, 4, 5), (9, 4, 6), (11, 5, 6)
]
adj = {}
for w, u, v in edges:
    adj.setdefault(u, []).append((v, w))
    adj.setdefault(v, []).append((u, w))

k_mst, k_cost = kruskal(n, edges[:])
p_mst, p_cost = prim(n, adj)

print('=== Kruskal\'s MST ===')
for u, v, w in k_mst:
    print(f'  Edge ({u} - {v})  Weight: {w}')
print(f'  Total MST Cost: {k_cost}')

print('\n=== Prim\'s MST ===')
for u, v, w in p_mst:
    print(f'  Edge ({u} - {v})  Weight: {w}')
print(f'  Total MST Cost: {p_cost}')

# --- Graphical Representation (Matplotlib) ---
# Circular layout for the 7 vertices
positions = {}
for i in range(n):
    angle = 2 * math.pi * i / n
    positions[i] = (math.cos(angle), math.sin(angle))

def draw_graph(ax, title, mst_edges):
    mst_set = set()
    for u, v, w in mst_edges:
        mst_set.add((u, v)); mst_set.add((v, u))

    # Draw all original edges (light gray)
    for w, u, v in edges:
        x1, y1 = positions[u]
        x2, y2 = positions[v]
        is_mst = (u, v) in mst_set
        ax.plot([x1, x2], [y1, y2],
                color='tab:blue' if is_mst else 'lightgray',
                linewidth=2.5 if is_mst else 1,
                zorder=1 if is_mst else 0)
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        ax.text(mx, my, str(w), fontsize=8, color='black',
                bbox=dict(boxstyle='round,pad=0.1', fc='white', ec='none', alpha=0.7))

    # Draw nodes
    for node, (x, y) in positions.items():
        ax.scatter(x, y, s=600, color='tab:orange', zorder=2, edgecolors='black')
        ax.text(x, y, str(node), fontsize=11, ha='center', va='center', zorder=3, fontweight='bold')

    ax.set_title(title)
    ax.set_xlim(-1.4, 1.4)
    ax.set_ylim(-1.4, 1.4)
    ax.set_aspect('equal')
    ax.axis('off')

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 6))
draw_graph(ax1, f"Kruskal's MST (Total Cost: {k_cost})", k_mst)
draw_graph(ax2, f"Prim's MST (Total Cost: {p_cost})", p_mst)

plt.tight_layout()
plt.savefig('exp3_mst.png', dpi=150)
plt.show()
