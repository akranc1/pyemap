import numpy as np
import networkx as nx

cryptochrome_ids= ["3ZXS","1u3d","1u3c","6PU0","4I6G","2J4D","6LZ3","4GU5",
                   "6PTZ","6FN2","1np7","5zm0","6FN3","6lz3"]
photolyase_ids = [ "1IQR","4U63","6KII","3FY4","1DNP","1QNF","1IQU"]
flavoprotein_ids=["6RKF","1o96","1efp","1o97","1efp"]
protein_ids = cryptochrome_ids + photolyase_ids + flavoprotein_ids

res_labels = { "2":"W",
    "3":"Y",
        "4":"H",
"5":"F",
"6":"NP"
}


f_out = open("pruned_results.out", "w")
f_in = open("gspan_results.out", "r")

count = 0
lines = f_in.readlines()
line_idx = 0
while line_idx < len(lines):
    line = lines[line_idx]
    if len(line.split())==3 and line.split()[0]=="t" and line.split()[1]=="#":
        start_idx = line_idx
        contains_FAD = False
        other_res = False
        num_Ws = 0
        num_FADs = 0
        line_idx+=1
        line = lines[line_idx]
        while "---" not in line:
            if len(line.split())==3 and line.split()[0]=="v" and (line.split()[2]=="6" or line.split()[2]=="12"):
                contains_FAD = True
                num_FADs+=1
            elif len(line.split())==3 and line.split()[0]=="v" and (line.split()[2]=="2" or line.split()[2]=="8"):
                num_Ws+=1
            elif len(line.split())==3 and line.split()[0]=="v":
                other_res = True
            line_idx+=1
            line = lines[line_idx]
        if contains_FAD and num_Ws>=3 and num_FADs==2 and not other_res and (num_Ws+num_FADs)<=6:
            count+=1
            for i in range(start_idx,line_idx+1):
                f_out.write(lines[i])
                if "where" in lines[i]:
                    l1 = lines[i][7:-2].strip('][').split(', ')
                    l2 = list(np.array(l1,dtype=int))
                    pdbs = []
                    for idx in l2:
                        pdbs.append(protein_ids[idx])
                    f_out.write("PDBS: "+ str(pdbs)+"\n")

    line_idx+=1

f_out.write("Count:" + str(count))




