from enum import Enum
from configuracion.Settings import I2ccfg
from modulos.perifericos.LCDs import *
from modulos.perifericos.RTC import *



class HBLi2cDevice():
    def __init__(self) -> None:
        self.name = ""
    def iniciar(self,cfg : I2ccfg.I2c,gpios : GPIOS,thread = True):
        self.d = None
        if cfg.activado:
            if cfg.name == "Lcd20x4":
                lines = [cfg.line0,cfg.line1,cfg.line2,cfg.line3]
                self.d = LCD20x4(cfg.bus,cfg.addr,gpios,lines)

            elif cfg.name == "Rtc":
                self.d  = RTC(cfg.bus,cfg.addr,gpios)
               
                
                
        return self.d
    def __repr__(self) -> str:
        if self.d != None:
            return f"{self.d.name}:\n{self.d._gpios}"
        else:
            return "None"
    
    #def start(self):
    #    self.d.__running = True
    
    
        
    
        
