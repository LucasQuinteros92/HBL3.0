
from modulos.perifericos.HBLSerial import HBLSerial



class LPR():
    def __init__(self, serial : HBLSerial) -> None:
        self._serial = serial
        self._serial.iniciarSerial()
        self._patentesLeidas  = ["XX114"] * 10
        #print(f"patentes: {self._patentesLeidas}, len {self._patentesLeidas.__len__()}")
        
    def seDetectoPatente(self):
        return self._serial.hayDatanueva()
            
    def patentesLeidas(self):
        return self._patentesLeidas
    
    def ultimaPatenteLeida(self):
        return self._patentesLeidas[self._patentesLeidas.__len__()-1]
    
    def leerPatente(self):
        p = self._serial.leerSerial()
        self._patentesLeidas.pop()
        self._patentesLeidas.insert(0,p)
        return p
         
    def stop(self):
        self._serial.stop()