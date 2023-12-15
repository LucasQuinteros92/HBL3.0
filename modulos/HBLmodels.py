import configuracion.Autoconfig
from enum import Enum
from modulos.perifericos.IO import *
from modulos.perifericos.HBLWiegand import *
from modulos.perifericos.HBLSerial import *
from modulos.perifericos.HBLi2cDevice import *
from configuracion.Settings import *

class HBLModel():
    
    
    
    

    class Entradas(Enum):
        pass
    
    def __init__(
                    self,
                    modelo,
                    logs    = None ) -> None:
        #genero instancia de pigpio
        
        self._gpios = GPIOS()
        #lleno la misma instancia si lo paso como parametro
        #sino genero nuevos hilos de pigpio
        self.entradas   = HBLEntradas(modelo,self._gpios)
        self.salidas    = HBLSalidas(gpios=self._gpios)
        self.leds       = HBLLeds(gpios=self._gpios)
        self.serial1    = HBLSerial(Serialcfg.Com1,gpios=self._gpios)
        self.wiegand1   = HBLWiegand().iniciar(Wiegandcfg.W1,gpios=self._gpios)
        self.wiegand2   = HBLWiegand().iniciar(Wiegandcfg.W2,gpios=self._gpios)
        self.displayLCD = HBLi2cDevice().iniciar(I2ccfg.Lcd20x4,gpios=self._gpios)
        self.rtc        = None#HBLi2cDevice().iniciar(I2ccfg.Rtc,gpios=self._gpios)
        
        log.escribeLineaLog(Logscfg.hblCore,self.__repr__(),date=True)

        

    def stop(self):
        if self.serial1 != None:
            self.serial1.stop()
        if self.displayLCD != None:
            self.displayLCD.stop()


    def __repr__(self):
        modulos = [self.entradas.__repr__() , 
               self.salidas.__repr__(),
               self.leds.__repr__(),
               self.wiegand1.__repr__(),
               self.wiegand2.__repr__(),
               self.serial1.__repr__(),
               self.displayLCD.__repr__(),
               self.rtc.__repr__()]
        ret = ""
        for mod in modulos:
            if mod != "None":
                ret += mod 
        return (ret)

    
class HBLViejo(HBLModel):
    
    def __init__(self):
        super().__init__(modelo=0)

class HBLnuevo(HBLModel):


    def __init__(self):
        super().__init__(modelo=1)

if __name__ == "__main__":
    
    hbl = HBLViejo()
    
    print(hbl)
    #print(hbl.leerEntradas(hbl.Entradas.IN2) ) 
    #print(hbl.leerSalidas(hbl.Salidas.OUT1) )