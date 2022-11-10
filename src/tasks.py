from abc import ABCMeta,abstractclassmethod

class AbstractTask(metaclasss=ABCMeta):
    """This Abstract class provides the basic structure of any 
    BaseTask that performs an action in the workflow
    """
    
    @abstractclassmethod
    def run(self):
        raise NotImplementedError('The method called is abstract and must be implemented by BaseTask.')
    
class BaseTask(AbstractTask):
    """This is a concrete base class for an AbstractTask"""
    
    def run(self, *args, **kwargs) -> any:
        """Executes python callable
        
        Returns:
            Any:
        """
        return self.func(*args, **kwargs)