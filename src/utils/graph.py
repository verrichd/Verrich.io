import networkx as nx
from common.task import Task
import matplotlib.pyplot as plt

class DirectedAcyclicGraph:
    
    def __init__(self):
        self.graph = nx.MultiDiGraph()
        self.labelDict = {}
        
    def addNode(self, task:Task):
        self.graph.add_node(task)
        self.labelDict[task] = task.name
        
    def addNodes(self,taskList:list[Task]):
        self.graph.add_nodes_from(taskList)
        for x in taskList:
            self.labelDict[x] = x.name
        
    def addEdge(self, task1:Task,task2:Task):
        self.graph.add_edge(task1,task2)
        
    def addEdges(self,edges_list:list[(Task,Task)]):
        self.graph.add_edges_from(edges_list)
        
    def sortTasks(self) -> list[Task]:
        return list(nx.topological_sort(self.graph))
    
    def print(self,file_location=None):
        #nx.draw(self.graph,with_labels = False,pos=nx.spring_layout(self.graph))
        #nx.draw_networkx_labels(self.graph,pos=nx.spring_layout(self.graph),labels=self.labelDict)
        # if(file_location is not None):
        #     plt.savefig(file_location)

        nodelist = []
        for n in self.graph.nodes:
        
            nodelist.append(n)

        # hierarchy here is arbitrarily defined based on the index of hte node in nodelist. 
        # {hierarchy_level : number_of_nodes_at_that_level}
        hierarchy = {
            0:3,
            1:7,
            2:8,
            3:7,
            4:5
        }

        coords = []
        for y, v in hierarchy.items():
            coords += [[x, y] for x in list(range(v))]

        # map node names to positions 
        # this is based on index of node in nodelist.
        # can and should be tailored to your actual hierarchy    
        positions = {}
        for n, c in zip(nodelist, coords):
            positions[n] = c

        fig = plt.figure(figsize=(15,5))
        nx.draw_networkx_nodes(self.graph, pos=positions, node_size=50)
        nx.draw_networkx_edges(self.graph, pos=positions, alpha=0.2)

        # generate y-offset for the labels, s.t. they don't lie on the nodes
        label_positions = {k:[v0, v1-.25] for k, (v0,v1) in positions.items()}
        nx.draw_networkx_labels(self.graph, pos=label_positions, font_size=8)
        if(file_location is not None):
            plt.savefig(file_location)
        plt.show()    
        
            
                
            
            


            
            