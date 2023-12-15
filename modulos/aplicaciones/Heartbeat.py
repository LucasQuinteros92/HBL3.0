from threading import Thread
from modulos.perifericos.IO import HBLLeds
import time


class Heartbeat(object):
    def __init__(self, led : HBLLeds):
        self.__running = True
        self.led = led
        self.delay = 0.5
        self.t = Thread(target=self.heartBeat,name = "heartbeat")
        self.t.start()
        
    def __repr__(self) -> str:
        return f"led: { self.led.__repr__()}delay: {self.delay} "
    
    def heartBeat(self):

        while self.__running:
            self.led.encender()
            time.sleep(self.delay)
            
            self.led.apagar()
            time.sleep(self.delay)
            
            
    def changeDelay(self,delay : float):
        if delay > 0:
            self.delay = delay
    
    def stop(self):
        self.__running = False