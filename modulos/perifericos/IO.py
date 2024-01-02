



from threading import Thread
from configuracion.Settings import Logscfg,Wiegandcfg
from modulos.perifericos.GPIOs import GPIOS,GpioModo,Edges
from modulos.aplicaciones.logs import LogReport as log
from enum import Enum
import time

class enumprueba(Enum):
        IN1 = 21
        IN2 = 20
class HBLIO():
    def __init__(self,pines,modo : GpioModo = GpioModo.OUTPUT,gpios = None,name = None) -> None:
        
        self._gpios = None
        self._pins = None
        self.it = 0
        if isinstance(pines,type(Enum)):
            self._pins= [i.value for i in pines]
    
        elif isinstance(pines, int):
            self._pins = [pines]
        elif isinstance(pines, list):
            self._pins = pines
        
            
        if gpios is None:
            
            self._gpios = GPIOS(self._pins, modo,name=name)
        else:
            self._gpios = GPIOS(self._pins, modo,pi=gpios.pi,name=name)
        
    def getGpio(self,gpio :int = None) :
        return self._gpios.leerGpio(gpio)
    
    
    def __contains__(self,item):
        return item in self._gpios

class HBLSalidas(HBLIO):
    class Salidas(Enum):
        OUT1 = 5
        OUT2 = 6
        OUT3 = 26
        OUT4 = 16
        if not Wiegandcfg.W1.activado:
            OUT5 = 23
            OUT6 = 24
        if not Wiegandcfg.W2.activado:
            OUT7 = 17
            OUT8 = 27
        def __repr__(self) -> str:
            return f"{self.name}"
        def __get__(self,instance,owner):
            return self.value
        
    def __init__(self,pines = Salidas,gpios : GPIOS = None,name = None) -> None:

        super().__init__(pines,gpios=gpios,name=name)
        
    ''' def __iter__(self):
        return self
    
    def __next__(self):
        if self._gpios.pinesDisponibles.__len__() > self.it:
            ret = self._gpios.pinesDisponibles[self.it]
            self.it += 1
            
        else:
            self.it = 0
            raise StopIteration
        return ret'''
        
    
    def activarSalida(self,gpio = None,inverted =False):
        if gpio == None:
            if self._gpios.cantidad() == 1:
                gpio = self._gpios.pinesDisponibles[0]._gpioNumero
                self._gpios.setON(gpio,inverted)
            else:
                raise Exception("debe especificarse una salida para activar")
        else:
            self._gpios.setON(gpio,inverted)
        
    def desactivarSalida(self,gpio = None,inverted = False):
        if gpio == None:
            if self._gpios.cantidad() == 1:
                gpio = self._gpios.pinesDisponibles[0]._gpioNumero
                self._gpios.setOFF(gpio,inverted)
            else:
                raise Exception("debe especificarse una salida para desactivar")
        else:
            self._gpios.setOFF(gpio,inverted)
            
        
    def buscarSalida(self, out : int):
        if out in self._pins:
            return HBLSalidas(out,self._gpios)
        else: 
            raise Exception("La salida no existe o no esta configurada")
    
    def __repr__(self) -> str:       
        return f"Salidas:\n{self._gpios}"

class HBLLeds(HBLSalidas):
    
    class Leds(Enum):
        Led1 = 13
        Led2 = 19
        
        def __repr__(self) -> str:
            return f"{self.name}"
        def __get__(self,instance,owner):
            return self.value
    
    def __init__(self, pines = Leds, gpios: GPIOS = None) -> None:
        super().__init__(pines, gpios,name="LED")
        self.t = Thread(target=self.blink,name = "blink")
        self.__running = True
        
    def encender(self,led = None):
        
        self.activarSalida(led)
        
    def apagar(self,led = None):
        
        self.desactivarSalida(led)
        
    def __repr__(self) -> str:       
        return f"Leds:\n{self._gpios}"

    def startBlink(self,led : int):
        self.ledBlink = led
        self.t.start()
    
    def stopBlink(self):
        self.__running = False
    
    def buscarLed(self, led : int):
        if led in self._pins:
            return HBLLeds(led,self._gpios)
        else: 
            raise Exception("El led no existe o no esta configurado")
        
    def toggleLed(self,led : int = None,ton :int = None):
        if ton == None:
            ton = 0.2
        self.encender(led)
        time.sleep(ton)
        self.apagar(led)
        time.sleep(ton)
        
    def blink(self):
        while self.__running:
            self.activarSalida(self.ledBlink)
            time.sleep(0.5)
            self.desactivarSalida(self.ledBlink)
            time.sleep(0.5)
    
class HBLEntradas(HBLIO):
    
    class EntradasV0(Enum):
        IN1 = 21
        IN2 = 20
        def __get__(self,instance,owner):
            return self.value
    class EntradasV1(Enum):
        IN1 = 21
        IN2 = 20
        IN3 = 25
        IN4 = 22
        
        def __get__(self,instance,owner):
            return self.value
    def __init__(self,modelo,gpios : GPIOS = None) -> None:
       

        if modelo == 0:
            super().__init__(self.EntradasV0,GpioModo.INPUT,gpios=gpios)
        elif modelo == 1:
            super().__init__(self.EntradasV1,GpioModo.INPUT,gpios=gpios)
        else:
            raise Exception("Modelo de HBL incorrecto")
        
        log.escribeLineaLog(Logscfg.hblEntradas, self.__repr__(),log.Colors.GREEN,date=True)
        
    
    def __repr__(self) -> str: 
        
        return f"Entradas:\n{self._gpios}"

    def buscarEntrada(self, input : int):
        if input in self._pins:
            return HBLIO(input,modo=GpioModo.INPUT,gpios=self._gpios)
        else: 
            raise Exception("La entrada no existe o no esta configurada")
    
    def setCallback(self, gpio: int, callback, edge: Edges):
        return self._gpios.setCallback(gpio, callback, edge)
    
    def set_watchdog(self,gpioNumero:int,ms):
        return self._gpios.set_watchdog(gpioNumero,ms)

if __name__ == "__main__":
    pass
    #print(HBLViejo())
    inputs = HBLEntradas(enumprueba)
    print(inputs)
    inputs = HBLEntradas(2)
    print(inputs)
    inputs = HBLEntradas([2])
    print(inputs)
    
       