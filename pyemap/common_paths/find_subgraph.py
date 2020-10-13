import pyemap
import networkx as nx
from matplotlib import pyplot as plt

#buried labels, other is 7
res_labels = {
2:"W",
3:"Y",
4:"H",
5:"F",
6:"FAD",
7:"NP",
8:"W",
9:"Y",
10:"H",
11:"F",
12:"FAD",
13:"NP"
}

res_labels_inv = {
"W": 2,
"Y": 3,
"H": 4,
"F": 5,
"FAD": 6,
"FMN:":6,
"W": 8,
"Y": 9,
"H": 10,
"F": 11,
"FAD":12,
"FMN":12
}


#buried labels, other is 7
res_labels_bur = { "W": 2,
    "Y": 3,
        "H": 4,
            "F": 5,
    "FAD": 6,
        "FMN:":6
}

#surface exposed labels, other is 13
res_labels_exp = { "W": 8,
    "Y": 9,
        "H": 10,
            "F": 11,
                "FAD":6,
"FMN":6
}

def get_numerical_label(G,u):
    res_name = strip_res_number(u)
    shape = G.nodes[u]['shape']
    if shape == "box":
        if res_name in res_labels_exp:
            return res_labels_exp[res_name]
        else:
            return 13
    else:
        if res_name in res_labels_bur:
            return res_labels_bur[res_name]
        else:
            return 7

def strip_res_number(u):
    digit_idx=-1
    for i in range(0,len(u)):
        if u[i].isdigit():
            return u[:i]

# defines edge labels in the graphs for gspan, based on distance
def get_edge_label(G,edge):
    #dist = G.edges[edge[0], edge[1]]['distance']
    dist = G.edges[edge]['distance']
    if dist <= 10.0:
        return 2
    elif dist <=15.0:
        return 3
    else:
        return 4

def get_numerical_label(G,u):
    res_name = strip_res_number(u)
    shape = G.nodes[u]['shape']
    if shape == "box":
        if res_name in res_labels_exp:
            return res_labels_exp[res_name]
        else:
            return 13
    else:
        if res_name in res_labels_bur:
            return res_labels_bur[res_name]
        else:
            return 7

def strip_res_number(u):
    digit_idx=-1
    for i in range(0,len(u)):
        if u[i].isdigit():
            return u[:i]


def generate_candidate_subgraph(graph):
    G = nx.Graph()
    for i,node in enumerate(graph.nodes):
        G.add_node(i)
        num_label = get_numerical_label(graph,node)
        if num_label > 6:
            G.nodes[i]['shape']= 'box'
        else:
            G.nodes[i]['shape']= 'oval'
        G.nodes[i]['label']= res_labels[num_label]
    for i,edge in enumerate(graph.edges):
        node1_idx = list(graph.nodes()).index(edge[0])
        node2_idx = list(graph.nodes()).index(edge[1])
        edge_label = graph.edges[edge]['label']
        G.add_edge(node1_idx,node2_idx,label=edge_label)
    return G

def read_in_subgraph(subgraph_number,output_file):
    f_in = open(output_file, "r")
    lines = f_in.readlines()
    line_idx = 0
    graph_idx = 0
    while line_idx < len(lines):
        line = lines[line_idx]
        if len(line.split())>1 and line.split()[0]=="t" and int(line.split()[2])==subgraph_number:
            break
        line_idx+=1
    G = nx.Graph()
    line = lines[line_idx]
    while "---" not in line:
        line = lines[line_idx]
        if len(line.split())>1 and line.split()[0]=="v":
            node_idx = int(line.split()[1])
            node_label = int(line.split()[2])
            G.add_node(node_idx)
            if node_label > 6:
                G.nodes[node_idx]['shape']= 'box'
            else:
                G.nodes[node_idx]['shape']= 'oval'
            G.nodes[node_idx]['label']= res_labels[node_label]
        if len(line.split())>1 and line.split()[0]=="e":
            idx1 = int(line.split()[1])
            idx2 = int(line.split()[2])
            edge_label = int(line.split()[3])
            G.add_edge(idx1,idx2,label=edge_label)
        line_idx+=1
    return G
    

def get_candidates(G,source):
# returns networkx node
    candidates = []
    for node in G.nodes:
        if get_numerical_label(G,node)==source:
            candidates.append(node)
    return candidates


def node_match(node1,node2):
    return node1['label'] == node2['label'] and node1['shape'] == node2['shape']

def edge_match(edge1,edge2):
    return edge1['label'] == edge2['label']

# recursive version
def dfs(full_graph,target_subgraph,G,prev_node,cur_node):
    target_num_nodes = len(list(target_subgraph.nodes))
    target_num_edges = len(list(target_subgraph.edges))
    cur_G = G.copy()
    # first iteration
    if not prev_node:
        for neighbor in full_graph.neighbors(cur_node):
            dfs(full_graph,target_subgraph,G,cur_node,neighbor)
    else:
        edge = (prev_node,cur_node)
        edge_label = get_edge_label(full_graph,edge)
        cur_G.add_node(cur_node,shape=full_graph.nodes[cur_node]['shape'])
        cur_G.add_edge(prev_node,cur_node,label=edge_label,distance=full_graph.edges[edge]['distance'])
        cur_num_nodes = len(list(cur_G.nodes))
        cur_num_edges = len(list(cur_G.edges))
        if target_num_nodes == cur_num_nodes and target_num_edges == cur_num_edges:
            test_graph = generate_candidate_subgraph(cur_G)
            if nx.is_isomorphic(test_graph,target_subgraph,edge_match=edge_match,node_match=node_match):
                found_subgraphs.append(cur_G)
        elif target_num_nodes > cur_num_nodes:
            for neighbor in full_graph.neighbors(cur_node):
                if not neighbor == prev_node:
                    dfs(full_graph,target_subgraph,cur_G,cur_node,neighbor)

#non-recursive
def dfs_nr(full_graph,target_subgraph,src):
    target_num_nodes = len(list(target_subgraph.nodes))
    target_num_edges = len(list(target_subgraph.edges))
    G = nx.Graph()
    G.add_node(src,shape=full_graph.nodes[src]['shape'])
    graph_stack = []
    stack = []
    stack.append(src)
    graph_stack.append(G)
    while(len(stack)):
        prev_node = stack.pop()
        G = graph_stack.pop()
        for cur_node in full_graph.neighbors(prev_node):
            if not G.has_edge(prev_node,cur_node):
                cur_G = G.copy()
                edge = (prev_node,cur_node)
                edge_label = get_edge_label(full_graph,edge)
                cur_G.add_node(cur_node,shape=full_graph.nodes[cur_node]['shape'])
                cur_G.add_edge(prev_node,cur_node,label=edge_label,distance=full_graph.edges[edge]['distance'])
                cur_num_nodes = len(list(cur_G.nodes))
                cur_num_edges = len(list(cur_G.edges))
                if target_num_nodes == cur_num_nodes and target_num_edges == cur_num_edges:
                    test_graph = generate_candidate_subgraph(cur_G)
                    if nx.is_isomorphic(test_graph,target_subgraph,edge_match=edge_match,node_match=node_match):
                        found_subgraphs.append(cur_G)
                elif target_num_nodes > cur_num_nodes:
                    stack.append(cur_node)
                    graph_stack.append(cur_G)

def find_subgraph(graph,subgraph,source):
# graph is a networkx object generated by emap
# subgraph is networkx object with node labels in the same format as our gspan stuff
# source is a numerical label of the starting node
# residue_map is a dict mapping node labels to residue types
    source_candidates = get_candidates(graph,source)
    source_candidates = source_candidates
    for src in source_candidates:
        #dfs(graph,subgraph,G,None,src)
        dfs_nr(graph,subgraph,src)



my_emap = pyemap.fetch_and_parse("4U63")
pyemap.process(my_emap,dist_def=1,sdef=1)
G = my_emap.init_graph

found_subgraphs = []
#visited_edges = []
subgraph = read_in_subgraph(104,"asa_pruned_results.out")
find_subgraph(G,subgraph,6)

print(len(found_subgraphs))
for found_sg in found_subgraphs:
    relabeled_sg = found_sg.copy()
    for edge in found_sg.edges:
        dist = '{0:.2f}'.format(found_sg.edges[edge]['distance'])
        relabeled_sg.edges[edge]['length'] = dist
        relabeled_sg.edges[edge]['label'] = dist
    my_emap._graph_to_Image(relabeled_sg).show()





