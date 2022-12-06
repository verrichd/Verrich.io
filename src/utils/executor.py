from common.workflows import Pipeline
import time
   
def execute(pipe:Pipeline):
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
    print("Pipeline Executed in " + (time.time() - startTime).__str__() + ' seconds')           