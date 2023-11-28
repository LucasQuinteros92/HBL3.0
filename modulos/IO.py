

from modulos.GPIOs import *
from enum import Enum

from modulos.GPIOs import GPIOS
class enumprueba(Enum):
        IN1 = 21
        IN2 = 20
class HBLIO():
    def __init__(self,pines,modo : GpioModo = GpioModo.OUTPUT,gpios = None,name = None) -> None:
        
        self._gpios = None
        
        
        
        if isinstance(pines,type(Enum)):
            self.pins= [i.value for i in pines]
    
        elif isinstance(pines, int):
            self.pins = [pines]
        elif isinstance(pines, list):
            self.pins = pines
            
        if gpios is None:
            
            self._gpios = GPIOS(self.pins, modo,name=name)
        else:
            self._gpios = GPIOS(self.pins, modo,pi=gpios.pi,name=name)

    def setCallback(self, gpio : int ,callback ,edge : Edges):
        self._gpios.setCallback(gpio,callback,edge)
        
    def getGpio(self,gpio :int = None) :
        return self._gpios.leerGpio(gpio)
    
    def __contains__(self,item):
        return item in self._gpios

class HBLSalidas(HBLIO):
    def __init__(self,pines,gpios : GPIOS = None,name = None) -> None:

        super().__init__(pines,gpios=gpios,name=name)
        
    
    def activarSalida(self,gpio):
        self._gpios.setON(gpio)
    
    def desactivarSalida(self,gpio):
        self._gpios.setOFF(gpio)
    
    def __repr__(self) -> str:       
        return f"Salidas:\n{self._gpios}"

class HBLLeds(HBLSalidas):
    def __init__(self, pines, gpios: GPIOS = None) -> None:
        super().__init__(pines, gpios,name="LED")

    def encender(self,led):
        self.activarSalida(led)
        
    def apagar(self,led):
        self.desactivarSalida(led)
        
    def __repr__(self) -> str:       
        return f"Leds:\n{self._gpios}"
    
class HBLEntradas(HBLIO):
    def __init__(self,pines = None,gpios : GPIOS = None) -> None:

        super().__init__(pines,GpioModo.INPUT,gpios=gpios)

        
        
    
    def __repr__(self) -> str: 
        
        return f"Entradas:\n{self._gpios}"



if __name__ == "__main__":
    pass
    #print(HBLViejo())
    inputs = HBLEntradas(enumprueba)
    print(inputs)
    inputs = HBLEntradas(2)
    print(inputs)
    inputs = HBLEntradas([2])
    print(inputs)
    
       