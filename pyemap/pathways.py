import itertools
import os
import string
import sys
import networkx as nx
import numpy as np
import pygraphviz as pg
from networkx.drawing.nx_agraph import from_agraph, to_agraph
from .dijkstras import yens_shortest_paths, dijkstras_shortest_paths


def finish_graph(G, original_shape_start, source):
    """Draws the graph with the shortest pathways highlighted.

    Parameters
    ----------
    G: NetworkX graph object
        Residue graph
    source: str
        name of source node
    original_shape_start: str
        shape of source node

    """
    G.node[source]['fillcolor'] = '#FFD700FF'
    G.node[source]['penwidth'] = 6.0
    G.node[source]['shape'] = original_shape_start
    # if not is not involved in pathways, make it less opaque on the graph.
    # change font color to slate gray, and change transparency of edges
    for name_node in G.nodes():
        if len(G.node[name_node]['fillcolor']) != 9:
            G.node[name_node]['fillcolor'] += '40'
            G.node[name_node]['fontcolor'] = '#708090'
    for edge in G.edges():
        name_node1, name_node2 = edge[0], edge[1]
        if G[name_node1][name_node2]['style'] == 'dashed':
            G[name_node1][name_node2]['color'] = '#7788994F'
    # draw graph


def find_pathways(emap, source, target=None,graph_dest="",max_paths=10):
    """Function which calculates pathways from source to target or surface exposed residues.

    Performs shortest path analysis on source and (optionally) target residues. After analysis is completed, the pathways
    graph is drawn and saved to the passed emap object.

    Parameters
    ---------
    emap: emap object
        Object for storing state of emap analysis.
    source: str
        source node for analysis
    target: str, optional
        target node for analysis
    max_paths: int, optional
        maximum number of paths to search for in yen's algorithm
    """
    # read in graph from file
    emap.reset_paths()
    G = emap.init_graph.copy()
    for u, v, d in G.edges(data=True):
        d['weight'] = np.float64(d['weight'])
    # process source and target
    source = source.strip()
    original_shape_start = G.node[source]['shape']
    G.node[source]['shape'] = 'oval'
    if target:
        target = target.strip()
        branches = yens_shortest_paths(G, source, target,max_paths=max_paths)
        # color target node blue
        G.node[target]['fillcolor'] = '#40e0d0FF'
        G.node[target]['penwidth'] = 6.0
    else:
        goals = []
        for n, d in G.nodes(data=True):
            if d['shape'] == "box":
                goals.append(n)
        branches = dijkstras_shortest_paths(G, source, goals)
    finish_graph(G, original_shape_start, source)
    emap.store_paths_graph(G)
    shortest_paths=[]
    for br in branches:
        shortest_paths+=br.paths
    if graph_dest:
        emap.store_paths(shortest_paths)
        emap.save_paths_graph(dest=graph_dest+".svg")
        emap.save_paths_graph(dest=graph_dest+".png")
    emap.store_paths(shortest_paths)
    return branches
