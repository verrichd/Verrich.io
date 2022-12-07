from common.workflows import Pipeline
import time
   
def execute(pipe:Pipeline):
    """_summary_ Executes a Pipeline object while keeping track
    of time and the result of each Task execution. Prior to each
    Task execution, the manage_dependencies method is called passing
    through the most up to date results dictionary in the Pipeline.

    Args:
        pipe (Pipeline): _description_
    """
    startTime = time.time()
    if(not pipe.status.__eq__('Setup')):
        pipe.setup()
    while(not pipe.queue.empty()):
        currentTask = pipe.queue.get()
        print("Running Task: " + currentTask.name)
        currentTask.manage_dependencies(pipe.results)
        currentTask.run()
        pipe.results[currentTask.name] = currentTask.result
    pipe.status = 'Executed'
    print("Pipeline Executed in " +
          (time.time() - startTime).__str__() + ' seconds')           
    
    
    
    