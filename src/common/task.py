
import samples.functions as f

class Task:

    def __init__(self, functionName:str, func:callable, dependencies:dict, kwargs:dict ):
        self.name = functionName
        self.func = func
        self.result = None
        self.status = "Not Started"
        self.dependencies = dependencies
        self.kwargs = kwargs
        
    def run(self,*inputs:tuple):
        self.status = "In Progress"
        self.result = self.func(*inputs,**self.kwargs)
        self.status = "Complete"
        
    def getStatus(self):
        return self.status
    
    def updateStatus(self,newStatus):
        self.status = newStatus
        
    def __str__(self):
        return self.name
    
    def manage_dependencies(self,taskName_to_result:dict):
        
        for x in self.dependencies:
            self.kwargs[self.dependencies[x]] = taskName_to_result[x]

        
    
        

