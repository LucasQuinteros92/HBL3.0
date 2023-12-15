from modulos.perifericos.GPIOs import *
from smbus import SMBus
from re import findall, match
from time import sleep
from subprocess import check_output
from os.path import exists




class I2c():
    class Bus:
        class Bus1(Enum):
            SDA = 2
            SCL = 3
            def __get__(self,instance,owner):
                    return self.value
        class Bus4(Enum):
            SDA = 8
            SCL = 7
            def __get__(self,instance,owner):
                    return self.value
    def __init__(self,bus,addr,name = None,pi = None):
        #RTC gpio 2,3 data,clock alt0 bus 1
        #displayLcd gpio 7,8 clock,data alt5 bus 4

        self._gpios = None
        self.bus = int(bus)
        self.addr = int(addr,16)
        if self.bus == 1:
            self._gpios = GPIOS(self.Bus.Bus1,GpioModo.ALT0,name,pi)
            self.setearNombres(self.Bus.Bus1)
        if self.bus == 3:
            self._gpios = GPIOS(self.Bus.Bus4,GpioModo.ALT5,name,pi)
            self.setearNombres(self.Bus.Bus4)
        self.pi = self._gpios.pi
        
    def setearNombres(self,pines ):
        p = self._gpios._buscarGpio(pines.SDA)
        p.setName("SDA")
        p = self._gpios._buscarGpio(pines.SCL)
        p.setName("SCL")
        
    
    def openI2c(self):
        self.h = self.pi.i2c_open(self.bus,self.addr)
        
    def writeI2c(self,data):
        self.pi.i2c_write_byte(self.h,data)
        
    def closeI2c(self):
        self.pi.i2c_close(self.h)
    
    # write a single command
    def write_cmd(self, cmd):
        
        self.pi.i2c_write_byte(self.h,cmd)
        sleep(0.0001)

    # write a command and argument
    def write_cmd_arg(self, cmd, data):
        self.pi.i2c_write_byte_data(self.h, cmd, data)
        sleep(0.0001)
    
    def write_device(self,device,data):
        self.pi.i2c_write_device(device,data)

    # write a block of data
    def write_block_data(self, cmd, data):
        self.pi.i2c_write_block_data(self.h, cmd, data)
        sleep(0.0001)

    # read a single byte
    def read(self):
        return self.pi.i2c_read_byte(self.h)

    # read
    def read_data(self, cmd):
        return self.pi.i2c_read_byte_data(self.h, cmd)

    # read a block of data
    def read_block_data(self, cmd):
        return self.pi.i2c_read_block_data(self.h, cmd)
        


