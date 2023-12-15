from modulos.perifericos.I2c import *

#quizas no corresponda ya que el rtc lo utiliza la misma rpi desde el SO
class RTC(I2c):

    def __init__(self,bus,addr,gpios : GPIOS):
            super().__init__(bus,addr,pi=gpios.pi)
            self.name = "RTC"

    def __repr__(self) -> str:
        
        return f"{self.name}:\n{self._gpios}"
    
    def iniciar(self):
        self.openI2c() 