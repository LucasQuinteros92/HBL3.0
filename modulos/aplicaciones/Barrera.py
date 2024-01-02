from modulos.perifericos.IO import HBLSalidas,HBLEntradas
from threading import Thread
import threading
from enum import Enum
from queue import Queue
import time

class BarreraConSensores():
    class Ordenes(Enum):
        ABRIR = 1
        CERRAR = 2
        def __get__(self,instance,owner):
            return self.value
    def __init__(self, barreraAbrir : HBLSalidas,sensor1 : HBLEntradas,sensor2 : HBLEntradas,ton : int = None) -> None:
        self._barreraAbrir  = barreraAbrir
        self._sensor1 = sensor1
        self._sensor2 = sensor2
        self.__running = False
        if ton == None:
            self.ton = 1
        else:
            self.ton = ton
        self.q = Queue()
        self.t = Thread(target=self.__run,daemon=False,name="BarreraDoblePulso")
        self.t.start()
    def abrirBarrera(self):
        self.q.put(self.Ordenes.ABRIR)
        
            
    def cerrarBarrera(self):
        self.q.put(self.Ordenes.CERRAR)
    
    def __rutinaAbrir(self):
        self._barreraAbrir.activarSalida()
        #time.sleep(self.ton)
        #self._barreraAbrir.desactivarSalida()
        
    def __rutinaCerrar(self):
        '''self._barreraCerrar.activarSalida()
        time.sleep(self.ton)
        self._barreraCerrar.desactivarSalida()'''
        self._barreraAbrir.desactivarSalida()
    
    def stop(self):
        self.__running = False
    def __run(self):
        
        while self.__running:
            try:
                orden = self.q.get(timeout=1)
                if orden == self.Ordenes.ABRIR:
                    self.__rutinaAbrir()
                elif orden == self.Ordenes.CERRAR():
                    self.__rutinaCerrar()
            except:
                pass
            print(f"Barrera: {threading.main_thread().is_alive()}")
            
class Barrera():
    class Ordenes(Enum):
        ABRIR = 1
        CERRAR = 2
        def __get__(self,instance,owner):
            return self.value
    def __init__(self, barrera : HBLSalidas,ton : int = None) -> None:
        self._barrera  = barrera
        self.__running = True
        if ton == None:
            self.ton = 1
        else:
            self.ton = ton
        self.q = Queue()
        self.t = Thread(target=self.__run,daemon=False,name="Barrera")
        self.t.start()
    def abrirBarrera(self):
        self.q.put(self.Ordenes.ABRIR)
        
            
    def cerrarBarrera(self):
        self.q.put(self.Ordenes.CERRAR)
    
    def __rutinaAbrir(self):
        self._barrera.activarSalida()
        time.sleep(self.ton)
        self._barrera.desactivarSalida()
        
    def __rutinaCerrar(self):
        self._barrera.activarSalida()
        time.sleep(self.ton)
        self._barrera.desactivarSalida()
    
    def stop(self):
        self.__running = False
        
    def __run(self):
        
        while self.__running:
            if not threading.main_thread().is_alive():
                self.__running = False
                
            try:
                orden = self.q.get(timeout=1)
                if orden == self.Ordenes.ABRIR:
                    self.__rutinaAbrir()
                elif orden == self.Ordenes.CERRAR():
                    self.__rutinaCerrar()
            except:
                pass
            