import networkx as nx
from common.task import Task
import matplotlib.pyplot as plt

class DirectedAcyclicGraph:
    """_summary_ Directed Graph container with a label dictionary as well as
    sorting and printing functionality.
    """
    def __init__(self):
        """Constructs an empty MultiDiGraph 
        """
        self.graph = nx.MultiDiGraph()
        self.labelDict = {}
        
    def addNode(self, task:Task):
        """Adds Task Node and updates label dictionary"""
        self.graph.add_node(task)
        self.labelDict[task] = task.name
        
    def addNodes(self,taskList:list[Task]):
        """_summary_ Add nodes to the graph from a list
        of Task objects.

        Args:
            taskList (list[Task]): _description_ list of Tasks
        """
        self.graph.add_nodes_from(taskList)
        for x in taskList:
            self.labelDict[x] = x.name
        
    def addEdge(self, task1:Task,task2:Task):
        """Add one edge to the graph between task1 node and 
        task2 node with respect to direction (Task1 --> Task2)

        Args:
            task1 (Task): _description_ from
            task2 (Task): _description_ to
        """
        self.graph.add_edge(task1,task2)
        
    def addEdges(self,edges_list:list[(Task,Task)]):
        """Add a list of edges to the graph. Every element in 
        the list must be a tuple of two Task objects with respect
        to the direction (Task1 --> Task2)

        Args:
            edges_list (list[): _description_ List of Task tuples 
        """
        self.graph.add_edges_from(edges_list)
        
    def sortTasks(self) -> list[Task]:
        """_summary_ Returns a topologically sorted list of tasks
        in this graph.

        Returns:
            list[Task]: _description_ list of sorted Task objects
        """
        return list(nx.topological_sort(self.graph))
    
    def print(self,hierarchyDict:dict,file_location=None):
        """Prints graph with a nicely spaced nodes in a hierarchy 
        where the number of nodes on each level of the hierarchy are
        determined by the items in hierarchyDict
        Example: {0:1,1:2,2:5} would indicate one node on level 0, 
        2 nodes on level 1, and 5 nodes on level 2. 
        Note: the sum of all values in hierarchydict must equal the 
        number of nodes in self.graph to ensure proper function."""
        nodelist = []
        for n in self.graph.nodes:
            nodelist.append(n)
 
        # {hierarchy_level : number_of_nodes_at_that_level}
        hierarchy = hierarchyDict

        #create coordinates for positioning of nodes and edges based on hierarchy
        coords = []
        for y, v in hierarchy.items():
            coords += [[x, y] for x in list(range(v))]

        # map node names to positions    
        positions = {}
        for n, c in zip(nodelist, coords):
            positions[n] = c

        # Overall size of figure
        fig = plt.figure(figsize=(10,5))
        
        # Drawing nodes and edges based on positions dictionary 
        nx.draw_networkx_nodes(self.graph, pos=positions, node_size=50)
        nx.draw_networkx_edges(self.graph, pos=positions, alpha=0.2)

        # generate y-offset for the labels so they are below the node
        label_positions = {k:[v0, v1-.25] for k, (v0,v1) in positions.items()}
        nx.draw_networkx_labels(self.graph, pos=label_positions, font_size=8)
        
        # Save plot to file if path is provided
        if(file_location is not None):
            plt.savefig(file_location)
        
        #show printed graph
        plt.show()  
        
        
            
                
            
            


            
            