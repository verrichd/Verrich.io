from queue import Queue
from task import Task

class Pipeline:

    def __init__(self,taskNames:list[Task]):
        self.task_list = taskNames
        self.queue = Queue()
        self.results = {}
        self.tasks = taskNames
        self.status = 'Empty'
        
    def setup(self):
        for x in self.tasks:
            self.queue.put(x)
            
        self.status = 'Setup'
        
    def reorder(self,orderedList:list[Task]):
        self.task_list = orderedList 
        