from apscheduler.schedulers.background import BackgroundScheduler

class DefaultScheduler(BackgroundScheduler):
    """_summary_ Singleton subclass of Background scheduler from APScheduler library
    """
    def __new__(self):
        if(self._instance is None):
            return super(DefaultScheduler, self).__new__(self)
        else:
            return self
        
    