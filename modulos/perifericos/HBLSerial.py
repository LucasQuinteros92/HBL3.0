
from modulos.perifericos.GPIOs import GPIOS,GpioModo
from modulos.perifericos.IO import HBLIO
from configuracion.Settings import Serialcfg,Logscfg
from modulos.aplicaciones.logs import LogReport as log
from threading import Thread
import serial
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
        
class HBLSerial(HBLIO):
    
    def __init__(self,cfg :Serialcfg.Com1= None,gpios :GPIOS = None ) -> None:
        
        
        
        if cfg.activado:
            self.cfg = cfg
            self.com = self.__obtenerSerial(cfg.port)
            super().__init__(self.com.pines,GpioModo.SERIAL,gpios,self.com.nombre)
            self.name = self.com.nombre
            self.__setearPinSerial(self.com.Rx,self.com.gpioModo,"Rx")
            self.__setearPinSerial(self.com.Tx,self.com.gpioModo,"Tx")
            self.data = ""
            
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
    
    def iniciarSerial(self):
        if self.cfg.activado:
            self.ser = serial.Serial(port =  self.cfg.port,
                                baudrate= self.cfg.baudrate,
                                bytesize= self.cfg.bytesize,
                                parity =  self.cfg.parity,
                                stopbits= self.cfg.stopbits,
                                timeout=  self.cfg.timeout)
            
            log.escribeLineaLog(Logscfg.hblSerial,
                                                    f"Serial {self.name} iniciado",date=True)
            self.t.start()
            self.ser.flushInput()
    def stop(self):
        self.__running = False
    def __run(self):
        
        while self.__running:
            
                try:
                        
                        data  = self.ser.readline()
                        
                        if data.__len__() > 0:
                            #print(data.decode(errors='ignore'))
                            data = data.decode(encoding='utf-8',errors='ignore').strip().replace("\x00", "")
                            if data.__len__() > 0:
                                self.data = data
                                log.escribeLineaLog(Logscfg.hblSerial,
                                                    f"Datos recibidos:{self.data}",date=True)
                            
                except Exception as e:
                    print(e)
                    log.escribeLineaLog(Logscfg.hblSerial,
                                                "Hubo un error al decodificar el serial",date=True)
        
        #print("serial stopped")
                
    def hayDatanueva(self) -> bool:
        return  self.data != ""
    
    def leerSerial(self) -> str:
        data = self.data
        self.data = ""
        return data
    
    def __repr__(self) -> str:
        try:
            return f"{self.name}:\n{self._gpios}"
        except:
            return ""