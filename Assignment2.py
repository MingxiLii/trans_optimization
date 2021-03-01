#%%
from gurobipy import *
import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
path = os.getcwd()
#%%
def LP_Model_Analysis(MODEL, precision=3):
    if MODEL.status == GRB.Status.OPTIMAL:
        pd.set_option('display.precision', precision)  # 设置精度
        print("\nGlobal optimal solution found.")
        print(f"Objective Sense: {'MINIMIZE' if MODEL.ModelSense == 1 else 'MAXIMIZE'}")
        print(f"Objective Value = {MODEL.ObjVal}")
        try:

            print(pd.DataFrame([[var.X, var.RC] for var in MODEL.getVars()],
                               index=[var.Varname for var in MODEL.getVars()],
                               columns=["Value", "Reduced Cost"]))
            print(pd.DataFrame([[Constr.Slack, Constr.pi] for Constr in MODEL.getConstrs()],
                               index=[Constr.constrName for Constr in MODEL.getConstrs()],
                               columns=["Slack or Surplus", "Dual Price"]))
            print("\nRanges in which the basis is unchanged: ")
            print(pd.DataFrame([[var.Obj, var.SAObjLow, var.SAObjUp] for var in MODEL.getVars()],
                               index=[var.Varname for var in MODEL.getVars()],
                               columns=["Cofficient", "Allowable Minimize", "Allowable Maximize"]))
            print("Righthand Side Ranges:")
            print(pd.DataFrame([[Constr.RHS, Constr.SARHSLow, Constr.SARHSUp] for Constr in MODEL.getConstrs()],
                               index=[Constr.constrName for Constr in MODEL.getConstrs()],
                               columns=["RHS", "Allowable Minimize", "Allowable Maximize"]))
        except:
            print(pd.DataFrame([var.X for var in MODEL.getVars()], index=[var.Varname for var in MODEL.getVars()],
                               columns=["Value"]))
            print(pd.DataFrame([Constr.Slack for Constr in MODEL.getConstrs()],
                               index=[Constr.constrName for Constr in MODEL.getConstrs()],
                               columns=["Slack or Surplus"]))
#%%
Nodes = ["1","2","3","4","5","6"]
Links = {("1","2"):4,
         ("2","1"):4,
         ("1","3"):3,
         ("3","1"):3,
         ("1","4"):6,
         ("4","1"):6,
         ("2","4"):3,
         ("4","2"):3,
         ("2","5"):1,
         ("5","2"):1,
         ("3","5"):3,
         ("5","3"):3,
         ("4","6"):2,
         ("6","4"):2,
         ("5","6"):2,
         ("6","5"):2,
         }

MODEL_Q1 = Model()

x={}
list_key ={}
for node in Nodes:
    for key in Links.keys():
        index = 'x_' + node +'-' + key[0] + ',' + key[1]
        key_ = (node,key[0],key[1])
        list_key[key_]=Links[key]
        x[key_] = MODEL_Q1.addVar(vtype=GRB.CONTINUOUS,name=index)
MODEL_Q1.update()

obj = LinExpr(0)
for key in list_key.keys():
    obj.addTerms( list_key[key],x[key])
MODEL_Q1.setObjective(obj,GRB.MINIMIZE)


for node in Nodes:
    lhs_= LinExpr(0)
    for key in list_key.keys():
        if(key[0] == node and key[1]==node):
            lhs_.addTerms(1, x[key])
        if(key[0]== node and key[2]==node):
            lhs_.addTerms(-1, x[key])
    MODEL_Q1.addConstr(lhs_==5)

for node in Nodes:
    for node_ in Nodes:
        if(node_ != node):
            lhs = LinExpr(0)
            for key in list_key.keys():
                if (key[0]==node and key[1] == node_):
                    lhs.addTerms(1, x[key])
                if (key[0]==node and key[2] == node_):
                    lhs.addTerms(-1, x[key])
            MODEL_Q1.addConstr(lhs == -1)


MODEL_Q1.optimize()
print(MODEL_Q1.ObjVal)
counts_var=0
for var in MODEL_Q1.getVars():
    counts_var+=1
    print(var.varName,'\t', var.x)
print (MODEL_Q1.display())
LP_Model_Analysis(MODEL_Q1,precision=1)

#%%
G = nx.MultiDiGraph()
G.add_nodes_from(Nodes)
def new_add_edge(G, a, b,value):
    if (a, b) in G.edges:
        max_rad = max(x[2]['rad'] for x in G.edges(data=True) if sorted(x[:2]) == sorted([a,b]))
    else:
        max_rad = 0
    G.add_edge(a, b, distance = value, rad=max_rad+0.1)
for key,value in Links.items():
    new_add_edge(G,key[0],key[1],value)

# G = nx.erdos_renyi_graph(8,0.4)
# p = nx.shortest_path(G,0,3)
# # Set all edge color attribute to black
# for e in G.edges():
#     G[e[0]][e[1]]['color'] = 'black'
# # Set color of edges of the shortest path to green
# for i in xrange(len(p)-1):
#     G[p[i]][p[i+1]]['color'] = 'blue'
# # Store in a list to use for drawing
# edge_color_list = [ G[e[0]][e[1]]['color'] for e in G.edges() ]
# nx.draw(G,edge_color = edge_color_list, with_labels = True)
# plt.show()
# pos = nx.spring_layout(G)
# distance = nx.get_edge_attributes(G, 'distance')
# fig = nx.draw_networkx_nodes(G, pos,node_size=600)
# fig = nx.draw_networkx_edges(G, pos)
# fig = nx.draw_networkx_labels(G, pos, font_size= 12)
# fig = nx.draw_networkx_edge_labels(G,pos,distance,label_pos=0.5, font_size= 12)
# plt.show()



pos = nx.circular_layout(G)
for edge in G.edges(data=True):
nx.draw_networkx_edges(G, pos, edgelist=[(edge[0], edge[1])],
                               connectionstyle=f'arc3, rad = {edge[2]["rad"]}',label=True)
plt.show()
# path_list = []
# for node in Nodes:
#     shortest_path = nx.single_source_shortest_path(G,node)
#     path_list.append(shortest_path)
# for one_to_all in path_list:
#     skim_tree = nx.DiGraph()
#     for single_path in one_to_all.values():
#         for i in range(len(single_path)-1):
#             skim_tree.add_edge(single_path[i],single_path[i+1])
#     nx.draw(skim_tree,  with_labels=True,pos=pos)
#     plt.show()
    # one_to_all = nx.MultiDiGraph()
    # for e in G.edges():
    #     G[e[0]][e[1]][0]['color'] = 'black'
    # for single_path in shortest_path:
    #     for i in range(len(single_path) - 1):
    #         G[single_path[i]][single_path[i + 1]][0]['color'] = 'red'
    #
    # edge_color_list = [G[e[0]][e[1]][0]['color'] for e in G.edges()]
    # nx.draw_networkx_nodes(G, pos, node_color= "blue")
    # nx.draw_networkx_labels(G, pos)
    #
    # for edge in G.edges(data=True):
    #     nx.draw_networkx_edges(G, pos, edge_color=G[edge[0]][edge[1]][0]['color'],edgelist=[(edge[0], edge[1])],
    #                                     connectionstyle=f'arc3, rad = {edge[2]["rad"]}')

            #nx.draw(G, pos=pos,edge_color=edge_color_list, with_labels=True)
#     plt.show()
#     path_list.append(shortest_path)
# print(path_list)
#
# path_lengths = nx.floyd_warshall(G,weight='distance')
# Y = {a:dict(b) for a,b in path_lengths.items()}
# print(Y)

#%%
Nodes_assi2 = [str(i) for i in range(0,22)]
Links_assi2 ={
         ("0","1"):2,
         ("0","2"):1,
         ("0","3"):2,
         ("1","0"):2,
         ("1","2"):2,
         ("1","4"):1,
         ("2","0"):1,
         ("2","1"):2,
         ("2","3"):2,
         ("2","5"):1,
         ("3","0"):2,
         ("3","2"):2,
         ("3","6"):2,
         ("4","1"):1,
         ("4","5"):1,
         ("4","7"):1,
         ("5","2"):1,
         ("5","4"):1,
         ("5","6"):1,
         ("5","8"):1,
         ("6","3"):2,
         ("6","5"):1,
         ("6","9"):2,
         ("7","4"):1,
         ("7","8"):1,
         ("7","12"):3,
         ("8","5"):1,
         ("8","7"):1,
         ("8","9"):1,
         ("8","10"):1,
         ("9","6"):2,
         ("9","8"):1,
         ("9","14"):4,
("10","8"):1,
("10","11"):1,
("10","22"):1,
("11","10"):1,
("11","13"):1,
("11","22"):1,
("12","7"):3,
("12","13"):2,
("12","17"):2,
("13","11"):1,
("13","12"):2,
("13","14"):2,
("13","15"):1,
("14","9"):4,
("14","13"):2,
("14","16"):2,
("15","13"):1,
("15","16"):1,
("15","17"):1,
("16","14"):2,
("16","15"):1,
("16","18"):1,
("17","12"):2,
("17","15"):1,
("17","18"):2,
("17","19"):2,
("18","16"):1,
("18","17"):2,
("18","20"):1,
("19","17"):2,
("19","20"):2,
("19","21"):3,
("20","18"):1,
("20","19"):2,
("20","21"):2,
("21","19"):3,
("21","20"):2,
("22","10"):1,
("22","11"):1
         }
source_list=[]
target_list=[]
time_list=[]
for key,value in Links_assi2.items():
    source_list.append(key[0])
    target_list.append(key[1])
    time_list.append(value)
print(source_list)
print(target_list)
print(time_list)
excel_list = pd.DataFrame(
    {'From': source_list,
     'To': target_list,
     'Time': time_list
    })
print(excel_list)
Nodes_list = pd.DataFrame({'Nodes':int_Nodes })
Nodes_list.to_excel("nodes_task1.xlsx")
excel_list.to_excel("shortest_path_task1.xlsx")
#%%
MODEL_Q2_task1 = Model()
x={}
for key in Links_assi2.keys():
    index = 'x_' + key[0] + ',' + key[1]
    x[key] = MODEL_Q2_task1.addVar(vtype=GRB.CONTINUOUS,name=index)
MODEL_Q2_task1.update()

obj = LinExpr(0)
for key in Links_assi2.keys():
    obj.addTerms( Links_assi2[key],x[key])
MODEL_Q2_task1.setObjective(obj,GRB.MINIMIZE)



for node in Nodes_assi2:
    lhs = LinExpr(0)
    if (node != '0' and node != '21'):
        for key in Links_assi2.keys():
            if (key[1] == node):
                lhs.addTerms(1, x[key])
            elif (key[0] == node):
                lhs.addTerms(-1, x[key])
        MODEL_Q2_task1.addConstr(lhs == 0, name='flow conservation')
lhs = LinExpr(0)
for key in Links_assi2.keys():
    if (key[0] == "0"):
        lhs.addTerms(1, x[key])
    elif (key[1] == "0"):
        lhs.addTerms(-1, x[key])
MODEL_Q2_task1.addConstr(lhs == 1, name='start flow')

lhs = LinExpr(0)
for key in Links_assi2.keys():
    if (key[0] == "21"):
        lhs.addTerms(1, x[key])
    elif (key[1] == "21"):
        lhs.addTerms(-1, x[key])
MODEL_Q2_task1.addConstr(lhs == -1, name='end flow')



MODEL_Q2_task1.optimize()
print(MODEL_Q2_task1.ObjVal)
print (MODEL_Q2_task1.display())
LP_Model_Analysis(MODEL_Q2_task1)

#%%
input_data_list=[]
nodes_list = [str(i) for i in range(0,23)]
for node in nodes_list:
    temp_list = []
    for key,value in Links_assi2.items():
        if(node==key[0]):
            temp_list.append((key[1],value))
    input_data_list.append(temp_list)
