#%%
def showGraph(linkList):
    for vert in linkList:
        for n in vert.getNeighbor():
            print("%s---adjacent---%s--weight: %s"%(vert.getValue(),n,vert.getWightTo(n)))
class vertix:
    def __init__(self,v):
        self.value=v
        self.neighbor={}
        self.D=float("inf")
    def getValue(self):
        return  self.value
    def getNeighbor(self):
        return self.neighbor.keys()
    def addNeighbor(self,v,w):
        self.neighbor[v]=w
    def getWightTo(self,v):
        return self.neighbor[v]
    def getD(self):
        return self.D
    def setD(self,newD):
        self.D=newD
#%%
import heapq
#%%
class dijkstra:
    def __init__(self,gragh):
        self.gragh=gragh
    def getMinPath(self,start):
        for i,node in enumerate(self.gragh):
            node.setD(2**32+i)
        self.gragh[start].setD(0)
        #Create a binary heap
        mydata=[[node.getD(),node.getValue()] for node in self.gragh]
        heapq.heapify(mydata)
        #Priority queue uses D as the key to establish priority
        while mydata:
            key,thisIndex=heapq.heappop(mydata)
            thisNode=self.gragh[thisIndex]
            for neibor in self.gragh[thisIndex].getNeighbor():
                self.gragh[neibor].setD(min(self.gragh[neibor].getD(),thisNode.getD()+thisNode.getWightTo(neibor)))
            tempData=[]
            for node in mydata:
                tempVer=self.gragh[node[1]]
                heapq.heappush(tempData,[tempVer.getD(),tempVer.getValue()])
            mydata=tempData
        res=[]
        for ver in self.gragh:
            res.append(ver.getD())
        return res

#%%
Links_assi2 = {
        ("0", "1"): 2, ("0", "2"): 1, ("0", "3"): 2,
        ("1", "0"): 2, ("1", "2"): 2, ("1", "4"): 1,
        ("2", "0"): 1, ("2", "1"): 2, ("2", "3"): 2,("2", "5"): 1,
        ("3", "0"): 2, ("3", "2"): 2, ("3", "6"): 2,
        ("4", "1"): 1, ("4", "5"): 1, ("4", "7"): 1,
        ("5", "2"): 1, ("5", "4"): 1, ("5", "6"): 1, ("5", "8"): 1,
        ("6", "3"): 2, ("6", "5"): 1, ("6", "9"): 2,
        ("7", "4"): 1, ("7", "8"): 1, ("7", "12"): 3,
        ("8", "5"): 1, ("8", "7"): 1, ("8", "9"): 1, ("8", "10"): 1,
        ("9", "6"): 2, ("9", "8"): 1, ("9", "14"): 4,
        ("10", "8"): 1, ("10", "11"): 1, ("10", "22"): 1,
        ("11", "10"): 1, ("11", "13"): 1, ("11", "22"): 1,
        ("12", "7"): 3, ("12", "13"): 2, ("12", "17"): 2,
        ("13", "11"): 1, ("13", "12"): 2, ("13", "14"): 2, ("13", "15"): 1,
        ("14", "9"): 4, ("14", "13"): 2, ("14", "16"): 2,
        ("15", "13"): 1, ("15", "16"): 1, ("15", "17"): 1,
        ("16", "14"): 2, ("16", "15"): 1, ("16", "18"): 1,
        ("17", "12"): 2, ("17", "15"): 1, ("17", "18"): 2, ("17", "19"): 2,
        ("18", "16"): 1, ("18", "17"): 2, ("18", "20"): 1,
        ("19", "17"): 2, ("19", "20"): 2, ("19", "21"): 3,
        ("20", "18"): 1, ("20", "19"): 2, ("20", "21"): 2,
        ("21", "19"): 3, ("21", "20"): 2,
        ("22", "10"): 1, ("22", "11"): 1
    }
# Convert the raw data into suitable data format
input_data_list = []
nodes_list = [str(i) for i in range(0, 23)]
for node in nodes_list:
    temp_list = []
    for key, value in Links_assi2.items():
        if (node == key[0]):
            temp_list.append((int(key[1]), value))
    input_data_list.append(temp_list)

# Construct adjacency list
linkList=[]
for i in range(len(input_data_list)):
    thisVerix=vertix(i)
    for v,w in input_data_list[i]:
        thisVerix.addNeighbor(v,w)
    linkList.append(thisVerix)
# Compute results
showGraph(linkList)
myDijstrs=dijkstra(linkList)
print("Final result------->")
print(myDijstrs.getMinPath(0))
print(myDijstrs.getMinPath(1))
print(myDijstrs.getMinPath(2))
print(myDijstrs.getMinPath(3))
print(myDijstrs.getMinPath(4))
print(myDijstrs.getMinPath(6))
print(myDijstrs.getMinPath(7))
print(myDijstrs.getMinPath(8))
print(myDijstrs.getMinPath(9))
print(myDijstrs.getMinPath(10))
print(myDijstrs.getMinPath(11))
print(myDijstrs.getMinPath(12))
print(myDijstrs.getMinPath(13))
print(myDijstrs.getMinPath(14))
print(myDijstrs.getMinPath(15))
print(myDijstrs.getMinPath(16))
print(myDijstrs.getMinPath(17))
print(myDijstrs.getMinPath(18))
print(myDijstrs.getMinPath(19))
print(myDijstrs.getMinPath(20))
print(myDijstrs.getMinPath(21))
print(myDijstrs.getMinPath(22))
result=[]
for i in range(0,23):
    result.append(myDijstrs.getMinPath(i))
import os
path = os.getcwd()
print(path)
df_result=pd.DataFrame(result)
df_result.to_excel('df_result.xlsx')