import pigpio
import os
import time

from enum import Enum

flag  = True


class Edges(Enum):    
        
        RISING_EDGE  = 0
        FALLING_EDGE = 1
        EITHER_EDGE  = 2
        def __repr__(self) -> str:
            return f"{self.name}"

class GpioModo(Enum):
    INPUT  = 0
    OUTPUT = 1
    ALT5   = 2  
    ALT4   = 3  
    ALT0   = 4  
    ALT1   = 5  
    ALT2   = 6  
    ALT3   = 7
    SERIAL = 8
    I2C    = 9
    def __repr__(self) -> str:
        return f"{self.name}"

class PUD(Enum):
    UP   = 0
    DOWN = 1
    OFF  = 2
    UNDEFINED = 3
    def __repr__(self) -> str:
        return f"{self.name}"    
              
    

class GPIOS():
    class _Pin():
        def __init__(self,gpioNumero, modo  = None, name = ""):
            self._gpioNumero : int = gpioNumero
            self._pinFisicoNumero : int= None
            self._inverted : bool = False 
            self._PUD : PUD = PUD(3)
            self._valor : int = None
            self._modo : GpioModo = modo
            self._name : str = name
            
        def checkMode(self, modo : GpioModo):        
            if self.getModeP() == modo:
                return True
            return False
        
            
        def setPUDP(self, valor : PUD):
            self._PUD = valor 

        def getPUDP(self):
            return self._PUD
        
        def setInvertedP(self, valor : bool):    
            self._inverted = valor
            
        def getInvertedP(self):
            return self._inverted
        
        def setValorP(self,valor):
            self._valor = valor
            
        def getValorP(self):
            return self._valor
        
        def setModeP(self,modo : GpioModo):
            self._modo = modo
        
        def getModeP(self): 
            return self._modo
        
        def setName(self,name : str):
            self._name = name
        
        def __repr__(self) -> str:

            return f"{self._name} pin:{self._gpioNumero}  ( modo:{self._modo.name} valor:{self._valor} PUD:{self._PUD.name} )\n" 
        

    def __init__(self,pines  = None,
                 modo = GpioModo.OUTPUT,
                 name = None, 
                 pi = None) -> None:
        
            
        if pi == None:
            self.pi = pigpio.pi()
            
        else:
            self.pi = pi
        self.pinesDisponibles : list [self._Pin]= []
        self.pinesOcupados = []
        if pines is not None:
            if isinstance(pines,type(Enum)):
                self.pins= [i.value for i in pines]
            elif isinstance(pines, int):
                self.pins = [pines]
            elif isinstance(pines, list):
                self.pins = pines
                
            self._initPines(self.pins,modo,name)
        

    def __repr__(self) -> str:
        #ret = "Pines Disponibles:\n"
        ret =""
        ret += self._mostrarPinesDisponibles()
        return ret
    def __contains__(self,item):
        for pin in self.pinesDisponibles:
            if pin._gpioNumero == item:
                return True
        return False
        
    def agregarPines(self, pines, modo,name = None):
        if isinstance(pines,type(Enum)):
            pines= [i.value for i in pines]
    
        elif isinstance(pines, int):
            pines = [pines]
        elif isinstance(pines, list):
            pines = pines
            
        return self._initPines(pines,modo,name)
        
    def eliminarPin(self,pin):
        aux = None
        for item in self.pinesDisponibles:
            if item._gpioNumero == pin: 
                aux = item
        if aux != None:
            self.pinesDisponibles.remove(aux)
            print("eliminado")
            
    def cantidad(self):
        return self.pinesDisponibles.__len__()
            
                
    def _initPines(self,pines :list,modo,name = None) -> [_Pin]:
        #self.listaEnJson = range(2,27)
        i = 1
        if len(self.pinesDisponibles):
            i = len(self.pinesDisponibles) + 1
        
        ret = [] 
        if name == None:
            name = modo.name   
        
        for pin in pines:
            p = self._Pin(pin,modo,f"{name}:{i}")
            if not (p in self.pinesDisponibles):
                self.pinesDisponibles.append(p)
                if modo != GpioModo.SERIAL:
                    self.setearModo(p._gpioNumero,p._modo)
                self._updatePin(p)
                
                i += 1
                ret.append(p)
                
            
        return ret
    
            
    def _updatePin(self, p : _Pin):
            p._modo = GpioModo(self.pi.get_mode(p._gpioNumero))
            p._valor = self.pi.read(p._gpioNumero)
            #self.setearModo(pin,_GpioModo.INPUT)
            #print(self.leerGpio(pin))
            
    def existeElPin(self,gpioNumero) -> bool:
        if self._buscarGpio(gpioNumero) is not None:
            return True
        return False
            
    def _buscarGpio(self,gpioNumero : int) -> _Pin:
        for pin in self.pinesDisponibles:
            if gpioNumero == pin._gpioNumero:
                return pin
        
        return None
    
    def set_watchdog(self, gpioNumero : int,ms):
        self.pi.set_watchdog(gpioNumero,ms)
    
    
    
    def setearModo(self,gpioNumero,modo: GpioModo):
        #modo HBLGpios.INPUT ... INPUT, OUTPUT, ALT0, ALT1, ALT2, ALT3, ALT4, ALT5.
        pin = self._buscarGpio(gpioNumero)
        if pin != None:
                self.pi.set_mode(pin._gpioNumero,modo.value)
                pin.setModeP(GpioModo(self.pi.get_mode(pin._gpioNumero)))
        else:
            print("no se pudo setear el modo")
            return None
        
    def setearPUD(self,gpioNumero,modo : PUD):
        ret = ""
        if modo.value != PUD.UNDEFINED.value:
            pin = self._buscarGpio(gpioNumero)
            if pin != None:
                if pin.getModeP() == GpioModo.INPUT:
                    self.pi.set_pull_up_down(pin._gpioNumero,modo.value)
                    pin.setPUDP(modo)
                    ret = None
                else:
                    ret += f"ERROR: el pin: {gpioNumero} no esta configurado como entrada\n"
            else:
                ret += f"ERROR: el pin: {gpioNumero} no existe\n"
        else:
            ret += f"ERROR: el PUD del pin: {gpioNumero} no puede setearse como UNDEFINED\n"
        
        return ret
        
    
    def unsetModo(self, gpioNumero):
        self.setearModo(gpioNumero,GpioModo.INPUT)
    
    def setCallback(self,gpioNumero, callback, edge: Edges = Edges.RISING_EDGE):
        ret = None
        if self.existeElPin(gpioNumero):
            if self.leerGpio(gpioNumero).getModeP() == GpioModo.INPUT:
                self.pi.callback(gpioNumero,edge.value,callback)
            else:
                ret = f"ERROR: el pin {gpioNumero} no esta configurado como entrada\n"
        else:
            ret = f"ERROR: El pin {gpioNumero} no existe\n"

        return ret
    def _mostrarPinesDisponibles(self):
        ret = ""
        for pin in self.pinesDisponibles:
            ret +=pin.__repr__() 
        return ret
    
    def setOutput(self,p : _Pin,valor):
        self.pi.write(p._gpioNumero, valor)
        p.setValorP(valor)
        
    def setON(self, gpioNumero, inverted = False):
        ret = ""
        p = self._buscarGpio(gpioNumero)
        if p is not None:
            if  p.checkMode(GpioModo.OUTPUT):
                if inverted: 
                    self.setOutput(p, 0)
                else:
                    self.setOutput(p, 1)
                ret = None
            else:
                ret = f"ERROR: el pin {gpioNumero} no esta configurado como salida\n"
        else:
            ret = f"ERROR: El pin {gpioNumero} no existe\n"
        return ret
    
    def setOFF(self,gpioNumero,inverted = False):
        ret = ""
        p = self._buscarGpio(gpioNumero)
        if p is not None:
            if p.checkMode( GpioModo.OUTPUT ):
                if inverted: 
                    self.setOutput(p, 1)
                else:
                    self.setOutput(p, 0)
                ret = None
            else:
                ret = f"ERROR: el pin {gpioNumero} no esta configurado como salida\n"
        else:
            ret = f"ERROR: El pin {gpioNumero} no existe\n"
            
        return ret
    def mostrarPinesOcupados(self):
        pass
    
    def leerGpio(self, gpioNumero)-> _Pin:
        p = self._buscarGpio(gpioNumero)
        self._updatePin(p)
        return p


def prueba(gpio, level, tick):
    
    if not level:
        global flag
        flag = False
        print("OK")
        
if __name__ == "__main__":
    os.system("sudo pigpiod")
    
    gpios = GPIOS(range(2,26))
    
    print(gpios)

    #gpios.setearModo(25,_GpioModo.OUTPUT)
    #print(gpios.leerGpio(25))
    ##    

    #gpios.unsetModo(25)
    ##
    #print(gpios)
        
    #for g in range(0,40):
    #    gpios.setearModo(g,_GpioModo.OUTPUT)
    #
    #gpios.setearModo(20,GpioModo.OUTPUT)
    #print(gpios.setearPUD(20,PUD.UP))
    #gpios.setON(19)
    #print(gpios)
    #time.sleep(1)
    #gpios.setOFF(19)
    #
    #print(gpios.leerGpio(19))
    pin = 19
    print(gpios.setearModo(pin,GpioModo.INPUT))
    print(gpios.setON(pin))
    time.sleep(1)
    print(gpios.setOFF(pin) )
    #gpios.setearPUD(pin,PUD.UP)
    #print(gpios.setCallback(pin,prueba))
    
    #print(gpios.leerGpio(pin))
    
    #gpios.setearModo(pin,GpioModo.OUTPUT)
    #print(gpios._buscarGpio(pin))
    #while flag:
    #    time.sleep(1)
        
        
    