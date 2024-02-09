from multiprocessing import Queue

class SingletonMetaClass(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(SingletonMetaClass, cls).__call__(*args, **kwargs)
        return cls._instances[cls]
    
class GlobalContext(object, metaclass=SingletonMetaClass):
    """Used to store Queues used by multiple operation"""
    def __init__(self, send_queue:Queue, recv_queue:Queue) -> None:
        self.send_queue, self.recv_queue = send_queue, recv_queue

