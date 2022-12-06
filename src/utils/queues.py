from queue import Queue as Queue
from asyncio import Queue as AsyncQueue
from multiprocessing import Queue as Multiqueue
from typing import Union
class QueueFactory: 
    """Factory that returns various type of queues"""
    def factory(type: str = 'default') -> Union(Queue, AsyncQueue, Multiqueue) :
        """Depending on type parameter, will return selected Queue"""
        
        if (type == 'default') : 
            return Queue()
        if (type == 'async') : 
            return AsyncQueue()
        if (type == 'multiprocessing') :
            return Multiqueue()
