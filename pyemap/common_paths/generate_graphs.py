import pyemap
import numpy as np
import networkx as nx
import time
cryptochrome_ids= ["1u3d","1u3c","6PU0","4I6G","2J4D","6LZ3","4GU5","6FN2","6FN3","1np7","3ZXS"]
flavoprotein_ids=["6RKF","1o96","1efp","1o97","1x0p","2z6c","1g28","4eer","2iyg","4xnb"]
photolyase_ids = [ "1IQR","4U63","6KII","3FY4","1DNP","1QNF","1IQU","2wb2","1tez"]
protein_ids = cryptochrome_ids + photolyase_ids + flavoprotein_ids

#notes:
#6RKF   no incident edges to tryptophan from fad
#6kx7:  no fad, one of the buggy cases
#2wb2:  buggy case
# 6fn0: buggy case
# 1tez: buggy case
# 2ijg: buggy case
# 3ZXS,5zm0

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
    dist = G.edges[edge[0], edge[1]]['distance']
    if dist <= 10.0:
        return 2
    elif dist <=15.0:
        return 3
    else:
        return 4

emaps = []
for i in range(0,len(protein_ids)):
    emap_obj = pyemap.fetch_and_parse(protein_ids[i])
    pyemap.process(emap_obj,dist_def=1,sdef=0)
    emaps.append(emap_obj)

f = open("graphdata.txt", "w")
for i in range(0,len(emaps)):
    G = emaps[i].init_graph
    #emaps[i].init_graph_to_Image().show()
    f.write("t # "+str(i)+"\n")
    for i,node in enumerate(G.nodes):
        f.write("v "+str(i) + " " + str(get_numerical_label(G,node))+"\n")
    for i,edge in enumerate(G.edges):
        f.write("e " + str(list(G.nodes()).index(edge[0]))+ " " + str(list(G.nodes()).index(edge[1]))+ " " + str(get_edge_label(G,edge))+ "\n")
f.write("t # -1")




