from scheduler import DefaultScheduler
import os,time
from pickle import load

scheduler = DefaultScheduler()
scheduler.start()

def check_for_pipeline(directory:str):
    """_summary_ Scans given directory for Pipeline
    objects saved using pickle library. Then adds any 
    Pipelines found to the jobs in the Scheduler. Requires a 
    method for Pipeline to save itself to a directory.
    This feature is not yet fully implemented.

    Args:
        directory (str): _description_ expected location of Pipeline objects
    """
    with os.scandir(directory) as pipes:
        for p in pipes:
            if(p.is_file()):
                pipe = load(p)
                scheduler.add_job(pipe)

                
def __main__():
    """_summary_ Creates a background scheduler that prints jobs
    as it checks the directory every 5 seconds. Programmed to stop after
    30 seconds from start time.
    """
    startTime = time.time()
    while time.time() < (startTime + 30):
        check_for_pipeline('.pipeline')
        scheduler.print_jobs()
        time.sleep(5)