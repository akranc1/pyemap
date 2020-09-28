import numpy as np
import networkx as nx
import matplotlib
from matplotlib import pyplot as plt
from networkx.drawing.nx_agraph import from_agraph, to_agraph

res_labels = { "2":"W",
    "3":"Y",
        "4":"H",
"5":"F",
"6":"FAD",
"7":"NP",
"8":"W",
    "9":"Y",
        "10":"H",
"11":"F",
"12":"FAD",
"13":"NP"
}

graphs = []
f_in = open("pruned_results.out", "r")
lines = f_in.readlines()
line_idx = 0
graph_idx = 0
while line_idx < len(lines):
    line = lines[line_idx]
    if len(line.split())>1 and line.split()[0]=="t" and line.split()[1]=="#":
        G = nx.Graph()
        graph_idx=int(line.split()[2])
        node_labels = {}
        start_idx = line_idx
        contains_source = False
        line_idx+=1
        line = lines[line_idx]
        edge_labels = {}
        buried_nodes = []
        se_nodes = []
        support = []
        while "---" not in line:
            line = lines[line_idx]
            if len(line.split())>1 and line.split()[0]=="v":
                G.add_node(line.split()[1])
                if int(line.split()[2]) > 6:
                    se_nodes.append(line.split()[1])
                else:
                    buried_nodes.append(line.split()[1])
                node_labels[line.split()[1]] = res_labels[line.split()[2]]
            if len(line.split())>1 and line.split()[0]=="e":
                G.add_edge(line.split()[1],line.split()[2])
                edge_labels[(line.split()[1],line.split()[2])] = line.split()[3]
            if "Support" in line:
                support = line.split()[1]
            line_idx+=1
        pos = nx.spring_layout(G)
        #nx.draw_networkx(G, pos)
        nx.draw_networkx_nodes(G, pos, nodelist=buried_nodes, node_shape='o')
        nx.draw_networkx_nodes(G, pos, nodelist=se_nodes, node_shape='s')
        nx.draw_networkx_labels(G, pos, node_labels)
        nx.draw_networkx_edges(G,pos)
        nx.draw_networkx_edge_labels(G,pos,edge_labels=edge_labels)
        plt.title("Frequency:" + support)
        plt.savefig('graphs/graph'+str(graph_idx)+'.png')
        plt.clf()
#plt.show()
    else:
        line_idx+=1



