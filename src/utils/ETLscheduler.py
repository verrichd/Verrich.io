from scheduler import DefaultScheduler
import os,time
from pickle import load

scheduler = DefaultScheduler()
scheduler.start()

def check_for_pipeline(directory:str):
    with os.scandir(directory) as pipes:
        for p in pipes:
            if(p.is_file()):
                pipe = load(p)
                scheduler.add_job(pipe)

                
def __main__():
    startTime = time.time()
    while time.time() < (startTime + 30):
        check_for_pipeline('.pipeline')
        scheduler.print_jobs()
        time.sleep(5)