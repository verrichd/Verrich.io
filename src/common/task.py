
class Task:
    """ Basic building block in a data processing pipeline. 
    Task is a container that holds a callable function along 
    with dependencies and keyword arguments that are needed to
    call the function. 
    """

    def __init__(self, functionName:str, func:callable, dependencies:dict, kwargs:dict ):
        """ Create a Task object with a name, function, dependencies and keyword arguments

        Args:
            functionName (str): _description_ user generated name for this Task object
            func (callable): _description_  callable function this Task executes
            dependencies (dict): _description_ dictionary with other Task names as keys and 
            keyword argument names as values where the key Tasks's result corresponds to 
            the value keyword argument of this Task's function
            kwargs (dict): _description_ dictionary of keyword arguments for the function
        """
        self.name = functionName
        self.func = func
        self.result = None
        self.status = "Not Started"
        self.dependencies = dependencies
        self.kwargs = kwargs
     
    def run(self):
        """_summary_ calls function passing kwargs as parameters
        """
        self.status = "In Progress"
        self.result = self.func(**self.kwargs)
        self.status = "Complete"
    
    def manage_dependencies(self,taskName_to_result:dict):
        """_summary_ Takes a dictionary of task names as keys that correspond
        to the result after that task was run. Then traverses each key in self
        dependencies dictionary to assign the corresponding result value to the
        correct keyword argument. This method must be run during execution if 
        the pipeline contains interdependent Tasks.

        Args:
            taskName_to_result (dict): _description_ 
            {task name (corresponding to a key in dependencies) : task result}
        """
        for x in self.dependencies:
            self.kwargs[self.dependencies[x]] = taskName_to_result[x]        
        
    def getStatus(self):
        return self.status
    
    def updateStatus(self,newStatus):
        self.status = newStatus
        
    def __str__(self):
        return self.name
    
    

        
    
        

