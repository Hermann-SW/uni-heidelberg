""" learned from Gemini about this related to pythogarean triples, and got code """
import networkx as nx
import matplotlib.pyplot as plt

# Gaussian Primes:
# p1 = 3 + 4i  (c=5)
# p2 = 5 + 12i (c=13)
# p3 = 8 + 15i (c=17)

# Level 2 Products:
# p1 * p2 = -33 + 56i    (c=65)
# p1 * p3 = -36 + 77i    (c=85)
# p2 * p3 = -140 + 171i  (c=221)

# Level 3 Product:
# p1 * p2 * p3 = -1104 - 47i (c=1105)

# Layout mapping arranged in clear levels by prime count
pos = {
    # Level 0: Root
    "1": (0, 0),

    # Level 1: 1 Prime factor
    "3+4i\n(c=5)": (-3, 1),
    "5+12i\n(c=13)": (0, 1),
    "8+15i\n(c=17)": (3, 1),

    # Level 2: 2 Prime factors
    "-33+56i\n(c=65)": (-3, 2),
    "-36+77i\n(c=85)": (0, 2),
    "-140+171i\n(c=221)": (3, 2),

    # Level 3: 3 Prime factors
    "-1104-47i\n(c=1105)": (0, 3)
}

# Directed edges forming the complete Boolean lattice for 3 prime generators
edges = [
    # Level 0 -> Level 1
    ("1", "3+4i\n(c=5)"),
    ("1", "5+12i\n(c=13)"),
    ("1", "8+15i\n(c=17)"),

    # Level 1 -> Level 2
    ("3+4i\n(c=5)", "-33+56i\n(c=65)"),
    ("5+12i\n(c=13)", "-33+56i\n(c=65)"),

    ("3+4i\n(c=5)", "-36+77i\n(c=85)"),
    ("8+15i\n(c=17)", "-36+77i\n(c=85)"),

    ("5+12i\n(c=13)", "-140+171i\n(c=221)"),
    ("8+15i\n(c=17)", "-140+171i\n(c=221)"),

    # Level 2 -> Level 3
    ("-33+56i\n(c=65)", "-1104-47i\n(c=1105)"),
    ("-36+77i\n(c=85)", "-1104-47i\n(c=1105)"),
    ("-140+171i\n(c=221)", "-1104-47i\n(c=1105)")
]

G = nx.DiGraph()
G.add_edges_from(edges)

plt.figure(figsize=(13, 9))

# Draw graph components
nx.draw_networkx_nodes(G, pos, node_size=22000, node_color='lightblue', edgecolors='black')
nx.draw_networkx_edges(G, pos, arrowstyle='->', arrowsize=20, edge_color='gray', width=2)
nx.draw_networkx_labels(G, pos, font_size=24, font_weight='bold')

plt.title(r"Divisibility DAG of Gaussian Integers $\mathbb{Z}[i]$ (PPT Generators)",
          fontsize=24, fontweight='bold', pad=20)
plt.axis('off')
plt.tight_layout()
plt.show()
