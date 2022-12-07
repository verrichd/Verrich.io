from queue import Queue
from common.task import Task
class Pipeline:
    """_summary_ Pipeline holds a list of tasks in a FIFO queue.
    A Pipeline can be reordered after instantiating, but it MUST
    be setup before executing. The executor should check the status
    of the Pipeline and if needed call the setup method before executing.
    """
    def __init__(self,taskNames:list[Task] = []):
        """_summary_

        Args:
            taskNames (list[Task]): _description_ 
            A list of tasks to add to the pipeline (default is empty)
        """
        self.queue = Queue()
        self.results = {} 
        self.tasks = taskNames
        self.status = 'Created, Requires Setup'
        
    def setup(self):
        """Must be called before executing the Pipeline. Any executor
        should check the status and only proceed if it is 'Setup', if not
        call this method then execute.
        
        Setup adds each element in tasks to the queue in the exact same order"""
        for x in self.tasks:
            self.queue.put(x)
            
        self.status = 'Setup'
        
    def reorder(self,orderedList:list[Task]):
        """_summary_ Reorder the Tasks in this Pipeline. Requires
        to run setup function to update queue with new Task order.
        Intended use: Topologically sorted list of Tasks from DAG.

        Args:
            orderedList (list[Task]): _description_ sorted list of Tasks
        """
        self.tasks = orderedList 
        self.status = 'Reordered, Requires Setup'
        
        
        
        
        