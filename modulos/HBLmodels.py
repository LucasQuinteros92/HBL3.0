from enum import Enum
from modulos.IO import *
from modulos.Wiegand import *

class HBLModel():
    class Leds(Enum):
        Led1 = 13
        Led2 = 19
        
        def __repr__(self) -> str:
            return f"{self.name}"
        def __get__(self,instance,owner):
            return self.value
    class Salidas(Enum):
        OUT1 = 5
        OUT2 = 6
        OUT3 = 26
        OUT4 = 16

        def __repr__(self) -> str:
            return f"{self.name}"
        def __get__(self,instance,owner):
            return self.value

    class Entradas(Enum):
        pass
    class Wiegand():
        class W1(Enum):
            WD0 = 23
            WD1 = 24
            def __get__(self,instance,owner):
                return self.value
        class W2(Enum):
            WD0 = 17
            WD1 = 27
            def __get__(self,instance,owner):
                return self.value
            
    def __init__(self,entradas,
                 salidas = Salidas,
                 leds    = Leds,
                 wiegand1 = Wiegand.W1,
                 wiegand2 = Wiegand.W2) -> None:
        #genero instancia de pigpio
        self._gpios = GPIOS()
        #lleno la misma instancia si lo paso como parametro
        #sino genero nuevos hilos de pigpio
        self.entradas = HBLEntradas(entradas,self._gpios)
        self.salidas  = HBLSalidas(salidas,self._gpios)
        self.leds     = HBLLeds(leds,self._gpios)
        self.wiegand1 = None
        self.wiegand2 = None
        if self.pinesW1libres():
            self.wiegand1 = HBLWiegandInput(wiegand1,self._gpios) 
        if self.pinesW2libres():
            self.wiegand2 = HBLWiegandOutput(wiegand2,self._gpios)
            
        self._serial1 =  None
    
    def enviarWiegand34(self,numero : int):
        self.wiegand2.enviarWiegand34(numero)
    
    def pinesW1libres(self):
        if not (
            self.Wiegand.W1.WD0 in self.entradas or
            self.Wiegand.W1.WD1 in self.entradas or
            self.Wiegand.W1.WD0 in self.salidas  or
            self.Wiegand.W1.WD1 in self.salidas  ):
            return True
        return False
    def pinesW2libres(self):
        if not (
            self.Wiegand.W2.WD0 in self.entradas or
            self.Wiegand.W2.WD1 in self.entradas or 
            self.Wiegand.W2.WD0 in self.salidas  or
            self.Wiegand.W2.WD1 in self.salidas    ):
            return True
        return False
        
    def leerEntrada(self, gpio : Entradas = None):
        if gpio  != None:            
            if gpio  in self.entradas:
                return self.entradas.getGpio(gpio )
            else:
                return "No se encontro la entrada"
        else:
            return self.entradas
    
    def leerSalida(self,gpio : Salidas  = None):
        if gpio != None:
            if gpio in self.salidas:
                return self.salidas.getGpio(gpio)
            else:
                return "No se encontro la salida"
        else:
            return self.salidas
    
    def activarSalida(self,gpio : Salidas):
        if gpio != None:
            if gpio in self.salidas:
                self.salidas.activarSalida(gpio)
            else:
                return "No se encontro la salida"
    def desactivarSalida(self,gpio : Salidas):
        if gpio != None:
            if gpio in self.salidas:
                self.salidas.desactivarSalida(gpio)
            else:
                return "No se encontro la salida"
        
    def setInterrupcionPin(self, gpio : Entradas,callback ,edge : Edges):
        
        self.entradas.setCallback(gpio,callback ,edge )
    
    def __repr__(self):
        
        return (self.entradas.__repr__() + 
               self.salidas.__repr__()+
               self.leds.__repr__()+
               self.wiegand1.__repr__()+
               self.wiegand2.__repr__())

    
class HBLViejo(HBLModel):
    class Entradas(Enum):
        IN1 = 21
        IN2 = 20
        def __get__(self,instance,owner):
            return self.value

    def __init__(self):
        super().__init__(self.Entradas)

class HBLnuevo(HBLModel):
    class Entradas(Enum):
        IN1 = 21
        IN2 = 20
        IN3 = 25
        IN4 = 22
        
        def __get__(self,instance,owner):
            return self.value

    def __init__(self):
        super().__init__(self.Entradas)

if __name__ == "__main__":
    
    hbl = HBLViejo()
    
    print(hbl)
    #print(hbl.leerEntradas(hbl.Entradas.IN2) ) 
    #print(hbl.leerSalidas(hbl.Salidas.OUT1) )