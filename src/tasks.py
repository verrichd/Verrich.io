
class Task:

    def __init__(self, func:callable, kwargs:dict):
        self.func = func
        self.kwargs = kwargs
        self.result = None
        
    def run(self, *args):
        self.result = self.func(*args, **self.kwargs)
    