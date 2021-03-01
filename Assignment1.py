#%%
import os
from gurobipy import *
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
path = os.getcwd()
print(path)
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
MODEL_Q1 = Model()
x1 = MODEL_Q1.addVar(vtype=GRB.CONTINUOUS,name="A")
x2= MODEL_Q1.addVar(vtype=GRB.CONTINUOUS,name="B")
MODEL_Q1.update()

MODEL_Q1.setObjective(3*x1 + 2*x2, sense=GRB.MAXIMIZE)

MODEL_Q1.addConstr(x1 + x2 == 500, name = "total_constr")
MODEL_Q1.addConstr(x1<=400, name="A_lim")
MODEL_Q1.addConstr(x2<=300, name="B_lim")

MODEL_Q1.optimize()

LP_Model_Analysis(MODEL_Q1)

#%%
MODEL_Q1_d = Model()
x1 = MODEL_Q1_d.addVar(vtype=GRB.CONTINUOUS,name="A")
x2= MODEL_Q1_d.addVar(vtype=GRB.CONTINUOUS,name="B")
MODEL_Q1_d.update()

MODEL_Q1_d.setObjective(2*x1 + 2*x2, sense=GRB.MAXIMIZE)

MODEL_Q1_d.addConstr(x1 + x2 == 500, name = "total_constr")
MODEL_Q1_d.addConstr(x1<=400, name="A_lim")
MODEL_Q1_d.addConstr(x2<=300, name="B_lim")

MODEL_Q1_d.optimize()

LP_Model_Analysis(MODEL_Q1_d)
#%%
MODEL_Q1_e = Model()
x1 = MODEL_Q1_e.addVar(vtype=GRB.CONTINUOUS,name="A")
x2= MODEL_Q1_e.addVar(vtype=GRB.CONTINUOUS,name="B")
MODEL_Q1_e.update()

MODEL_Q1_e.setObjective(3*x1 + 3*x2, sense=GRB.MAXIMIZE)

MODEL_Q1_e.addConstr(x1 + x2 == 500, name = "total_constr")
MODEL_Q1_e.addConstr(x1<=400, name="A_lim")
MODEL_Q1_e.addConstr(x2<=300, name="B_lim")

MODEL_Q1_e.optimize()

LP_Model_Analysis(MODEL_Q1_e)
#%%
MODEL_Q1_f = Model()

x1 = MODEL_Q1_f.addVar(vtype=GRB.CONTINUOUS,name="A")
x2= MODEL_Q1_f.addVar(vtype=GRB.CONTINUOUS,name="B")
MODEL_Q1_f.update()

MODEL_Q1_f.setObjective(2*x1 + 3*x2, sense=GRB.MAXIMIZE)

MODEL_Q1_f.addConstr(x1 + x2 == 500, name = "total_constr")
MODEL_Q1_f.addConstr(x1<=400, name="A_lim")
MODEL_Q1_f.addConstr(x2<=300, name="B_lim")

MODEL_Q1_f.optimize()

LP_Model_Analysis(MODEL_Q1_f)
#%%
MODEL_Q2 = Model()
x1 = MODEL_Q2.addVar(vtype=GRB.CONTINUOUS,name="X1")
x2 = MODEL_Q2.addVar(vtype=GRB.CONTINUOUS,name="X2")
x3 = MODEL_Q2.addVar(vtype=GRB.CONTINUOUS,name="X3")
MODEL_Q2.update()

MODEL_Q2.setObjective(12*x1 + 9*x2 +7*x3, sense=GRB.MAXIMIZE)
MODEL_Q2.addConstr(3*x1 + 5*x2 + 4*x3 <= 150)
MODEL_Q2.addConstr(2*x1 + 1*x2 + 1*x3 <= 64)
MODEL_Q2.addConstr(1*x1 + 2*x2 + 1*x3 <= 80)
MODEL_Q2.addConstr(2*x1 + 4*x2 + 3*x3 >= 116)

MODEL_Q2.optimize()

LP_Model_Analysis(MODEL_Q2)

#%%
G = nx.DiGraph()
G.add_node('W1', demand = -200)
G.add_node('W2', demand = -400)
G.add_node('W3', demand = -300)
G.add_node('P1', demand = 300)
G.add_node('P2', demand = 500)
G.add_node('P3', demand = 100)

G.add_edge('P1', 'W1', capacity = 20)
G.add_edge('P1', 'W2', capacity = 16)
G.add_edge('P1', 'W3',  capacity = 24)
G.add_edge('P2', 'W1', capacity = 10)
G.add_edge('P2', 'W2', capacity = 10)
G.add_edge('P2', 'W3',  capacity = 8)
G.add_edge('P3', 'W1', capacity = 12)
G.add_edge('P3', 'W2', capacity = 18)
G.add_edge('P3', 'W3',  capacity = 10)
X = ['P3','P2','P1']
Y = ['W3','W2','W1']
pos = dict()
pos.update( (n, (1, i)) for i, n in enumerate(X) )
pos.update( (n, (2, i)) for i, n in enumerate(Y) )
capacity = nx.get_edge_attributes(G, 'capacity')
nx.draw_networkx_nodes(G, pos)
nx.draw_networkx_edges(G, pos)
nx.draw_networkx_labels(G, pos)
nx.draw_networkx_edge_labels(G,pos,capacity,label_pos=0.75)
plt.show()
#%%
MODEL_Q3 = Model()

x=MODEL_Q3.addVars(9,vtype=GRB.CONTINUOUS,name="product/unit")

c=[20,16,24,10,10,8,12,18,10]
rhs=[[300,500,100],[200,400,300]]

MODEL_Q3.update()

MODEL_Q3.setObjective(x.prod(c),GRB.MINIMIZE)

MODEL_Q3.addConstr(x[0]+x[1]+x[2]==rhs[0][0])
MODEL_Q3.addConstr(x[3]+x[4]+x[5]==rhs[0][1])
MODEL_Q3.addConstr(x[6]+x[7]+x[8]==rhs[0][2])
MODEL_Q3.addConstr(x[0]+x[3]+x[6]==rhs[1][0])
MODEL_Q3.addConstr(x[1]+x[4]+x[7]==rhs[1][1])
MODEL_Q3.addConstr(x[2]+x[5]+x[8]==rhs[1][2])
for i in range(9):
    MODEL_Q3.addConstr(x[i] >= 0)
MODEL_Q3.optimize()

LP_Model_Analysis(MODEL_Q3)

#%%
MODEL_Q3_ = Model()

x=MODEL_Q3_.addVars(9,vtype=GRB.CONTINUOUS,name="product/unit")

c=[20,16,24,10,10,8,12,18,10]
rhs=[[300,500,100],[200,400,300]]

MODEL_Q3_.update()

MODEL_Q3_.setObjective(x.prod(c),GRB.MAXIMIZE)

MODEL_Q3_.addConstr(x[0]+x[1]+x[2]==rhs[0][0])
MODEL_Q3_.addConstr(x[3]+x[4]+x[5]==rhs[0][1])
MODEL_Q3_.addConstr(x[6]+x[7]+x[8]==rhs[0][2])
MODEL_Q3_.addConstr(x[0]+x[3]+x[6]==rhs[1][0])
MODEL_Q3_.addConstr(x[1]+x[4]+x[7]==rhs[1][1])
MODEL_Q3_.addConstr(x[2]+x[5]+x[8]==rhs[1][2])
for i in range(9):
    MODEL_Q3_.addConstr(x[i] >= 0)
MODEL_Q3_.optimize()

LP_Model_Analysis(MODEL_Q3_)

#%%
MODEL_Q4 = Model()

x61= MODEL_Q4.addVar(vtype=GRB.CONTINUOUS)
x12= MODEL_Q4.addVar(vtype=GRB.CONTINUOUS)
x14= MODEL_Q4.addVar(vtype=GRB.CONTINUOUS)
x13= MODEL_Q4.addVar(vtype=GRB.CONTINUOUS)
x24= MODEL_Q4.addVar(vtype=GRB.CONTINUOUS)
x25= MODEL_Q4.addVar(vtype=GRB.CONTINUOUS)
x34= MODEL_Q4.addVar(vtype=GRB.CONTINUOUS)
x36= MODEL_Q4.addVar(vtype=GRB.CONTINUOUS)
x42= MODEL_Q4.addVar(vtype=GRB.CONTINUOUS)
x43= MODEL_Q4.addVar(vtype=GRB.CONTINUOUS)
x45= MODEL_Q4.addVar(vtype=GRB.CONTINUOUS)
x46= MODEL_Q4.addVar(vtype=GRB.CONTINUOUS)
x54= MODEL_Q4.addVar(vtype=GRB.CONTINUOUS)
x56= MODEL_Q4.addVar(vtype=GRB.CONTINUOUS)

MODEL_Q4.update()

MODEL_Q4.setObjective(x61,GRB.MAXIMIZE)

MODEL_Q4.addConstr(x61-x12-x14-x13 == 0)
MODEL_Q4.addConstr(x12+x42-x24-x25 == 0)
MODEL_Q4.addConstr(x13+x43-x34-x36 == 0)
MODEL_Q4.addConstr(x14+x24+x34+x54-x42-x43-x45-x46 == 0)
MODEL_Q4.addConstr(x25+x45-x56-x54 == 0)
MODEL_Q4.addConstr(x56+x46+x36-x61 == 0)
MODEL_Q4.addConstr(x12 <= 2000)
MODEL_Q4.addConstr(x14 <= 3000)
MODEL_Q4.addConstr(x13 <= 6000)
MODEL_Q4.addConstr(x24 <= 1000)
MODEL_Q4.addConstr(x25 <= 4000)
MODEL_Q4.addConstr(x34 <= 3000)
MODEL_Q4.addConstr(x36 <= 2000)
MODEL_Q4.addConstr(x42 <= 1000)
MODEL_Q4.addConstr(x43 <= 3000)
MODEL_Q4.addConstr(x45 <= 1000)
MODEL_Q4.addConstr(x46 <= 3000)
MODEL_Q4.addConstr(x54 <= 1000)
MODEL_Q4.addConstr(x56 <= 6000)
for var in MODEL_Q4.getVars():
    MODEL_Q4.addConstr(var >= 0)


MODEL_Q4.optimize()
LP_Model_Analysis(MODEL_Q4)

#%%
MODEL_Q5 = Model()

MODEL_Q5.addVars(range(1,6),vtype=GRB.BINARY)

MODEL_Q5.update()

MODEL_Q5.addConstr(x[1]+x[3]+x[5]+x[6] >2)

MODEL_Q5.addConstr(x[3]==x[5])

MODEL_Q5.addConstr(x[1]+x[4]==1)

MODEL_Q5.addConstr(x[1]*x[3]-x[4]>=0)

MODEL_Q5.addConstr(x[4]-x[1]*x[3]>=0)

#%%
G = nx.DiGraph()
G.add_nodes_from(Nodes)
for key,value in links.items():
    G.add_edge(key[0],key[1],capacity=value)
A = ["start_state"]
B = ["1_2","1_3","1_4","2_3","2_4","3_4"]
C = ["1","2","3","4"]
D = ["1_2_3","1_2_4","1_3_4","2_3_4"]
E = ["1_2_","1_3_","1_4_","2_3_","2_4_","3_4_"]
F = ["1_2_3_4"]
pos = dict()
pos.update( (n, (2.5, 12)) for i, n in enumerate(A) )
pos.update( (n, (i, 10)) for i, n in enumerate(B) )
pos.update( (n, (i+1, 8)) for i, n in enumerate(C) )
pos.update( (n, (i+1, 6)) for i, n in enumerate(D) )
pos.update( (n, (i, 4)) for i, n in enumerate(E) )
pos.update( (n, (2.5, 2)) for i, n in enumerate(F) )
capacity = nx.get_edge_attributes(G, 'capacity')

fig = nx.draw_networkx_nodes(G, pos,node_size=600)
fig = nx.draw_networkx_edges(G, pos)
fig = nx.draw_networkx_labels(G, pos, font_size= 7)
fig = nx.draw_networkx_edge_labels(G,pos,capacity,label_pos=0.5, font_size= 7)
plt.figure(figsize=[16, 16])
plt.savefig("new.png", dpi=1000, format="png", bbox_inches="tight")
plt.show()

#%%
Nodes =["start_state",
        "1_2","1_3","1_4","2_3","2_4","3_4",
        "1","2","3","4",
        "1_2_3","1_2_4","1_3_4","2_3_4",
        "1_2_","1_3_","1_4_","2_3_","2_4_","3_4_",
        "1_2_3_4"]
links = {("start_state","1_2"):10,
         ("start_state","1_3"):20,
         ("start_state","1_4"):25,
         ("start_state","2_3"):20,
         ("start_state","2_4"):25,
         ("start_state","3_4"):25,
         ("1_2","1"):10,
         ("1_2","2"):5,
         ("1_3","1"):20,
         ("1_3","3"):5,
         ("1_4","1"):25,
         ("1_4","4"):5,
         ("2_3","2"):20,
         ("2_3","3"):10,
         ("2_4","2"):25,
         ("2_4","4"):10,
         ("3_4","3"):25,
         ("3_4","4"):20,
         ("1","1_2_3"):20,
         ("1","1_2_4"):25,
         ("1","1_3_4"):25,
         ("2","1_2_3"):20,
         ("2","1_2_4"):25,
         ("2","2_3_4"):25,
         ("3","1_2_3"):10,
         ("3","1_3_4"):25,
         ("3","2_3_4"):25,
         ("4","1_2_4"):10,
         ("4","2_3_4"):20,
         ("4","1_3_4"):20,
         ("1_2_3","1_2_"):20,
         ("1_2_3","1_3_"):10,
         ("1_2_3","2_3_"):5,
         ("1_2_4","1_2_"):25,
         ("1_2_4","1_4_"):10,
         ("1_2_4","2_4_"):5,
         ("1_3_4","1_3_"):25,
         ("1_3_4","1_4_"):20,
         ("1_3_4","3_4_"):5,
         ("2_3_4","2_3_"):25,
         ("2_3_4","2_4_"):20,
         ("2_3_4","3_4_"):10,
         ("1_2_","1_2_3_4"):25,
         ("1_3_","1_2_3_4"):25,
         ("1_4_","1_2_3_4"):20,
         ("2_3_","1_2_3_4"):25,
         ("2_4_","1_2_3_4"):20,
         ("3_4_","1_2_3_4"):10,
         }

MODEL_Q6 = Model('dual problem')

x={}
for key in links.keys():
    index = "x_" + key[0] + ',' + key[1]
    x[key] = MODEL_Q6.addVar(vtype=GRB.BINARY,name= index)

MODEL_Q6.update()

obj = LinExpr(0)
for key in links.keys():
    obj.addTerms(links[key],x[key])

MODEL_Q6.setObjective(obj,GRB.MINIMIZE)

lhs_1 = LinExpr(0)
lhs_2 = LinExpr(0)
for key in links.keys():
    if(key[0]=="start_state"):
        lhs_1.addTerms(1,x[key])
    elif(key[1]=="1_2_3_4"):
        lhs_2.addTerms(1,x[key])
MODEL_Q6.addConstr(lhs_1==1, name="start flow")
MODEL_Q6.addConstr(lhs_2==1, name="end flow")

for node in Nodes:
    lhs = LinExpr(0)
    if(node != "start_state" and node != "1_2_3_4"):
        for key in links.keys():
            if(key[1] == node):
                lhs.addTerms(1,x[key])
            elif(key[0]==node):
                lhs.addTerms(-1,x[key])
    MODEL_Q6.addConstr(lhs == 0, name="travel")

MODEL_Q6.write('model_spp.lp')
MODEL_Q6.optimize()

print(MODEL_Q6.objVal)
for var in MODEL_Q6.getVars():
    if(var.x >0):
        print(var.varName,'\t',var.x)

