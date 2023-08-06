from collections import deque
import heapq

import cpge
import matplotlib.animation
import matplotlib.pyplot as plt
import networkx as nx
from IPython.display import HTML

options = {"font_size": 25, "node_size": 1000, "edgecolors": "black"}
figsize = (16, 10)


def anim_traversal(G, traversal):
    for i, e in enumerate(G.edges):
        G.edges[e]['index'] = i
    t = traversal(G)
    colors, widths = t[0], t[1]
    fig, ax = plt.subplots(figsize=figsize)
    pos = cpge.graph.spring_pos(G)
    plt.close()

    def update(frame):
        ax.clear()
        nx.draw(G, pos, ax, width=widths[frame], node_color=colors[frame], **options)

    ani = matplotlib.animation.FuncAnimation(fig, update, frames=len(colors), interval=800, repeat=False)
    return HTML(ani.to_jshtml())


def dfs(G):
    colors, widths = ['black'] * len(G), [1] * len(G.edges)
    frame_colors, frame_widths = [], []

    def add_frame():
        frame_colors.append(colors.copy())
        frame_widths.append(widths.copy())

    def aux(u):
        colors[u] = 'red'
        add_frame()
        for v in G.neighbors(u):
            if colors[v] == 'black':
                colors[u] = 'orange'
                widths[G[u][v]['index']] = 5
                aux(v)
                colors[u] = 'red'
                add_frame()
        colors[u] = 'green'
        add_frame()

    aux(0)
    return frame_colors, frame_widths


def anim_dfs(G):
    G = cpge.graph.generate.to_nx(G)
    return anim_traversal(G, dfs)


def anim_bfs(G):
    G = cpge.graph.generate.to_nx(G)
    for i, e in enumerate(G.edges):
        G.edges[e]['index'] = i

    colors, width = ['black'] * len(G), [1] * len(G.edges)
    q_frames, width_frames, colors_frames = [], [], []
    q = deque([(0, -1)])

    def add_frame():
        width_frames.append(width.copy())
        colors_frames.append([c if c == "orange" else "white" for c in colors])
        if q:
            q_frames.append(' '.join(map(str, list(zip(*q))[0])))
        else:
            q_frames.append('')

    while q:
        u, p = q.pop()
        if p != -1:
            width[G[p][u]['index']] = 5
        colors[u] = 'orange'
        add_frame()
        for v in G.neighbors(u):
            if colors[v] == 'black':
                colors[v] = 'green'
                q.appendleft((v, u))
        add_frame()
        colors[u] = 'green'

    fig, ax = plt.subplots(figsize=figsize)
    pos = cpge.graph.spring_pos(G)
    plt.close()

    def update(frame):
        ax.clear()
        ax.text(-.1, 0, f"File : {q_frames[frame]}", fontsize=25, transform=ax.transAxes)
        nx.draw(G, pos, ax, width=width_frames[frame], node_color=colors_frames[frame], with_labels=True, **options)

    ani = matplotlib.animation.FuncAnimation(fig, update, frames=len(width_frames), interval=800, repeat=False)
    return HTML(ani.to_jshtml())


def anim_graph(G, widths, dist):
    fig, ax = plt.subplots(figsize=figsize)
    plt.close()
    pos = cpge.graph.spring_pos(G)
    labels = nx.get_edge_attributes(G, "weight")
    plt.close()

    def update(frame):
        ax.clear()
        nx.draw(G,
                pos=pos,
                ax=ax,
                node_color=["green"] + (len(G) - 1) * ["white"],
                width=widths[frame],
                with_labels=True,
                **options)
        nx.draw_networkx_edge_labels(G, ax=ax, pos=pos, edge_labels=labels, font_size=20)
        for v, (x, y) in pos.items():
            ax.text(x, y + .1, dist[frame][v], fontsize=20)

    ani = matplotlib.animation.FuncAnimation(fig, update, frames=len(widths), interval=800, repeat=False)
    return HTML(ani.to_jshtml())


def dijkstra(M, G, s):
    for i, e in enumerate(G.edges):
        G.edges[e]['index'] = i
    widths = [1] * len(G.edges)
    dist_estimated = {v: float("inf") for v in range(len(G))}
    frame_widths, frame_dist = [], []
    dist = [float("inf")] * len(G)
    q = []
    heapq.heappush(q, (0, s, s))
    while len(q) > 0:
        d, u, p = heapq.heappop(q)
        if dist[u] == float("inf"):
            if p != u:
                widths[G[p][u]['index']] = 6
                frame_widths.append(widths.copy())
            dist[u] = d
            for v in range(len(M)):
                if M[u][v] != float("inf"):
                    dv = dist[u] + M[u][v]
                    if dv < dist_estimated[v]:
                        dist_estimated[v] = dv
                        heapq.heappush(q, (dv, v, u))
                        dist_estimated[v] = dv
                        frame_dist.append(dist_estimated.copy())
    return frame_widths, frame_dist


def anim_dijkstra(M, start):
    G = cpge.graph.to_nx(M)
    return cpge.graph.anim_graph(G, *cpge.graph.dijkstra(M, G, start))
