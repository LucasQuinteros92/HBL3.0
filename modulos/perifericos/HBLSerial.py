
from modulos.perifericos.GPIOs import GPIOS,GpioModo
from modulos.perifericos.IO import HBLIO
from configuracion.Settings import Serialcfg,Logscfg
from modulos.aplicaciones.logs import LogReport as log
from threading import Thread
import serial,threading
'''
    recordar habilitar las uart en /boot/config.txt
'''
class COM():
        def __init__(self, nombre ,Rx,Tx,cfg = None):
            self.nombre = nombre
            self.Rx = Rx
            self.Tx = Tx
            self.gpiomodo = None
        def __eq__(self,__value: object) -> bool:
            if (self.nombre == __value.nombre):
                return True
            else:
                return False
class ttyS0(COM):
    def __init__(self) -> None:
        super().__init__("/dev/serial0",15,14)
        self.pines = [15,14]
        self.gpioModo = GpioModo.ALT5
        
class ttyAMA2(COM):
    def __init__(self) -> None:
        super().__init__("/dev/ttyAMA2",5,4)
        self.pines = [5,4]
        self.gpioModo = GpioModo.ALT4 
class HBLSerial(HBLIO):
    
    def __init__(self,cfg :Serialcfg.Com1= None,gpios :GPIOS = None ) -> None:
        self._cfg = cfg
        self._data = ""
        if cfg.activado:
            
            self._com = self.__obtenerSerial(self._cfg.port)
            super().__init__(self._com.pines,GpioModo.SERIAL,gpios,self._com.nombre)
            self.name = self._com.nombre
            self.__setearPinSerial(self._com.Rx,self._com.gpioModo,"Rx")
            self.__setearPinSerial(self._com.Tx,self._com.gpioModo,"Tx")
            
            
            self.__running = True
            
            
            self.t = Thread(target=self.__run,name= self.name)
            
            log.escribeLineaLog(Logscfg.hblSerial,
                                                f"Serial {self.name} configurado",date=True)
            
        else:
            return None
    def __setearPinSerial(self,pin,modo : GpioModo,name):
        
        p = self.getGpio(pin)
        self._gpios.setearModo(pin,modo)
        p.setName(name)
    
    def __obtenerSerial(self,name):
        if name == ttyS0().nombre:
            return ttyS0()
        elif name == ttyAMA2().nombre:
            return ttyAMA2()
    
    def iniciarSerial(self):
        if self._cfg.activado:
            self.ser = serial.Serial(port =  self._cfg.port,
                                baudrate= self._cfg.baudrate,
                                bytesize= self._cfg.bytesize,
                                parity =  self._cfg.parity,
                                stopbits= self._cfg.stopbits,
                                timeout=  self._cfg.timeout)
            
            log.escribeLineaLog(Logscfg.hblSerial,
                                                    f"Serial {self.name} iniciado",date=True)
            self._data = ""
            self.t.start()
            self.ser.flushInput()
            
    def stop(self):
        self.__running = False
    def __run(self):
        
        while self.__running:
                if not threading.main_thread().is_alive():
                    self.__running = False
                try:
                        
                        data  = self.ser.readline()
                        
                        if data.__len__() > 0:
                            #print(data.decode(errors='ignore'))
                            data = data.decode(encoding='utf-8',errors='ignore').strip().replace("\x00", "")
                            if data.__len__() > 0:
                                self._data = data
                                log.escribeLineaLog(Logscfg.hblSerial,
                                                    f"Datos recibidos:{self._data}",date=True)
                            
                except Exception as e:
                    print(e)
                    log.escribeLineaLog(Logscfg.hblSerial,
                                                "Hubo un error al decodificar el serial",date=True)
        
        #print("serial stopped")
                
    def hayDatanueva(self) -> bool:
        return  self._data != ""
    
    def leerSerial(self) -> str:
        data = self._data
        self._data = ""
        return data
    
    def __repr__(self) -> str:
        try:
            return f"{self.name}:\n{self._gpios}"
        except:
            return ""