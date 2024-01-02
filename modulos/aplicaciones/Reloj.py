

from modulos.perifericos.HBLSerial import HBLSerial
from modulos.perifericos.HBLWiegand import HBLWiegandInput


class relojSerial():
    def __init__(self, serial : HBLSerial) -> None:
        self._serial = serial
        self._serial.iniciarSerial()
        self._fichadasLeidas = [""] * 10

    def seDetectoFichada(self):
        if self._serial.hayDatanueva():
            f : str= self._serial.leerSerial()
            if f[0:3].isnumeric():
                self._fichadasLeidas.pop(0)
                self._fichadasLeidas.append(f)
            return True
        else:
            return False
    
    def fichadasLeidas(self):
        return self._fichadasLeidas
    
    def ultimaFichadaLeida(self):
        return self._fichadasLeidas[self._fichadasLeidas.__len__()-1]
    
    def leerFichada(self):
        
        return self.ultimaFichadaLeida()
         
    def stop(self):
        self._serial.stop()
        
class relojWiegand():
    
    def __init__(self, wiegand : HBLWiegandInput) -> None:
        self._wiegand = wiegand
        
        self._fichadasLeidas = [""] * 10

    def seDetectoFichada(self):
        return self._wiegand.wiegandDisponible()
    
    def fichadasLeidas(self):
        return self._fichadasLeidas
           
    def leerFichada(self):
        f = self._wiegand.leerDatoWiegand()
        self._fichadasLeidas.pop(0)
        self._fichadasLeidas.append(f)
        return f
        