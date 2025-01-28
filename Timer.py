import time

class EventTimer:
    def __init__(self):
        self.active_time = 0
        self._start_time = None
        
    def start_timer(self):
        if self._start_time is None:
            self._start_time = time.time()
            
    def stop(self):
        if self._start_time is not None:
            self.active_time += time.time() - self._start_time
            self._start_time = None
    
    def reset(self):
        self.active_time = 0
        self._start_time = None
        
    def get_active_time(self):
        if self._start_time is not None:
            return self.active_time + (time.time()- self._start_time) 
        return self.active_time