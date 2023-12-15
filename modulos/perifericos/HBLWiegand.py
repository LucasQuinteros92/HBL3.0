from modulos.perifericos.GPIOs import *
from modulos.perifericos.IO import *
from configuracion.Settings import Wiegandcfg,Logscfg
from modulos.aplicaciones.logs import LogReport as log

class WiegandModo(Enum):
    WIEGANDIN  = 0
    WIEGANDOUT = 1 
    C1WD0      = 2
    C1WD1      = 3
    C2WD0      = 4
    C2WD1      = 5 
    WIEGAND    = 6

    def __repr__(self) -> str:
        return f"{self.name}"

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

class HBLWiegand():
    
    def  __init__(self):
        pass
          
    def iniciar(self,cfg : Wiegandcfg.W1,pines=None,gpios = None,name = None):
        if name == None:
            name = cfg.name
        
        if name == 'W1':
            pines = Wiegand.W1
        elif name == 'W2':
            pines = Wiegand.W2
                    
        if cfg.activado:
            if cfg.modo == "IN":
                self.w = HBLWiegandInput(pines,cfg,gpios,name)
            elif cfg.modo =="OUT":
                self.w = HBLWiegandOutput(pines,cfg,gpios,name)
            else:
                raise Exception(f"Error modo wiegand incorrecto: {cfg.modo}")
            
            self.setearNombres(pines)
            log.escribeLineaLog(Logscfg.hblWiegand,self.w.__repr__(),date=True)
            return self.w
        else:
            return None
    def setearNombres(self,pines):
        p = self.w._gpios._buscarGpio(pines.WD0)
        p.setName("D0")
        p = self.w._gpios._buscarGpio(pines.WD1)
        p.setName("D1")
class HBLWiegandOutput(HBLIO):
    def __init__(self,pines,cfg : Wiegandcfg.W1,gpios : GPIOS = None,name = None) -> None:
        super().__init__(pines,WiegandModo.WIEGANDOUT,gpios) 
        #self._gpios = HBLIO(pines,WiegandModo.WIEGANDOUT,gpio,"WD OUT")
        self.name = name
        self.cfg = cfg
        for pin in self._pins:
            self._gpios.setON(pin)
        
        
    def enviarWiegand34(self,valor :int ):
        i = 0 
        
        variable = self._codificarWiegand34(valor)
        
        #variable = "10000000001000010011110011"
        #36739686 = 1000000100011000010011010011001101

        while i < 34:
                       
            if int(variable.format(valor)[i],2)  == 0: 
                self._gpios.setOFF(self._pins[0])#pi.write(__gpio_0, 0) 

                time.sleep(self.cfg.delayPulso) # sleep delay fall (std : 0.00008)

                self._gpios.setON(self._pins[0])#pi.write(__gpio_0, 1) 
                time.sleep(self.cfg.delayIntervalo) # sleep delay rise (std : 0.00024) 
                #print("0")
            else: 
                
                self._gpios.setOFF(self._pins[1])#pi.write(__gpio_1, 0) 
                time.sleep(self.cfg.delayPulso) # sleep delay fall (std : 0.00008)
                
                self._gpios.setON(self._pins[1])#pi.write(__gpio_1, 1) 
                time.sleep(self.cfg.delayIntervalo) # sleep delay rise (std : 0.00024)   
                #print("1")
            
            i = i + 1     
        
        log.escribeLineaLog(Logscfg.hblWiegand,f"wiegand enviado:\nvalor: {valor}\nbin: {variable}",date=True)   
        
    def _codificarWiegand34(self,dni):
        
        dniBase = "1000000100011000010011010011001101"#en DEC : 36739686
        dniBase2 = "1000000100011000010011010011010000" #en DEC: 36739688
        dniBin = list(bin(dni)[2:].zfill(33))
        dniBin.append("0")
        #el bit 0 indica paridad PAR
        #si los primeros bits son impares corrijo con un 1 
        if self._paridad(dniBin[1:16],par = False):
            dniBin[0] = "1"
        #el ultimo bit es paridad impar
        #si los ultimos bits son pares corrijo agregando un 1
        if self._paridad(dniBin[17:-1]):
            dniBin[-1] = "1"

        dniBin = ''.join(dniBin)
        #log.escribeLineaLog(hbl.LOGS_hblPruebaHbl,f"dni {dni}") 
        #log.escribeLineaLog(hbl.LOGS_hblPruebaHbl,f"dniBase{dniBase2}") 
        #log.escribeLineaLog(hbl.LOGS_hblPruebaHbl,f"dniBin {dniBin}")
        return dniBin
    
    def _paridad(self,data,par = True):
        '''
            hay que pasarle un dato iterable con unos y ceros
            devuelve true si el dato posee la paridad de unos deseada
        '''
        count = 0
        ret = False
        for i in data:
            count += int(i)
        
        if par:
            if count % 2 == 0:
                ret = True
        else:
            if count % 2 != 0:
                ret = True
        
        return ret
    
    def __repr__(self) -> str:
        
        return f"{self.name}:\n{self._gpios}"

class HBLWiegandInput(HBLIO):
    
    def __init__(self,pines,cfg : Wiegandcfg.W1 ,gpios : GPIOS = None,name = None,callback = None) -> None:
            super().__init__(pines,WiegandModo.WIEGANDIN,gpios,name="WD IN") 
            #for pin in self.pins:
            #    self._gpios.setOFF(pin)
            self.cfg = cfg
            self.name = name
            self.__gpio_0 = self._pins[0]
            self.__gpio_1 = self._pins[1]

            self.callback = callback

            self.__config = True

            self.__datoWiegand = None
            self.__formato = None
            
            self._gpios.setearModo(self.__gpio_0, GpioModo.INPUT)
            self._gpios.setearModo(self.__gpio_1, GpioModo.INPUT)

            self._gpios.setearModo(self.__gpio_0, PUD.UP)
            self._gpios.setearModo(self.__gpio_1, PUD.UP)

            self._gpios.setCallback(self.__gpio_0, self._cb,Edges.FALLING_EDGE)
            self._gpios.setCallback(self.__gpio_1, self._cb,Edges.FALLING_EDGE)
            
            
    
    def _cb(self, gpio, level, tick):
      

        """
        Acumula bits 0 y 1
        """
        #print(gpio,self.__gpio_0)
        if level < pigpio.TIMEOUT:
            #cuando se vence el timeout del watchdog, se llama a este callback con 
            #level = 2 o pigpio.TIMEOUT
            if self.__config == True:
                #setea los parametros de inicio
                #cantidad de bits y watchdog
                #no vuelve a entrar hasta que finalice la comunicacion
                self.bits = 1
                self.num = 0

                self.__config = False
                
                self._gpios.set_watchdog(self.__gpio_0, 100)
                self._gpios.set_watchdog(self.__gpio_1, 100)
            else:
                #acumula la cantidad de interrupciones como bits
                #desplaza el bit anterior a la izq MSB
                self.bits += 1
                self.num = self.num << 1

            #si es D0 solo borra el timeout
            #si es D1 agrega un 1 en esa posicion de self.num
            if gpio == self.__gpio_1:
                self.num = self.num | 1

        else:
            #para que no entre dos veces al terminar
            if not self.__config:
                
                self._gpios.set_watchdog(self.__gpio_0, 0)
                self._gpios.set_watchdog(self.__gpio_1, 0)
                self.__config = True

                # recarga los parametros de hbl.json por actualizacion
                

                # decodifica el valor wiegand 
                # auto deteccion de cantidad de bits y formateo
                cantidadBits = self.bits
                numero = self.num 
                #habria que detectar la cantidad de bits
                #y llamar una funcion acorde para decodificar el dato
                try:
                        
                        numeroBinario = bin(numero)[2:].zfill(cantidadBits)   
                        
                        id = int(numeroBinario.format(numero)[self.cfg.primerBit:int(cantidadBits-1)],2) 
                        self.__datoWiegand = id
                        self.__formato = cantidadBits
                        log.escribeLineaLog(Logscfg.hblWiegand,
                                            f"wiegand recibido:\nvalor: {self.__datoWiegand}\nbin: {numeroBinario}\nbits:{self.__formato}",
                                            date=True) 
                except: 

                    print("ERROR 100 : Wiegand IN")
                    # hardcode de valor de error
                    self.__datoWiegand = 99999
                       


    def wiegandDisponible(self):
        return self.__datoWiegand != None 
    
    def leerDatoWiegand(self):
        dato = self.__datoWiegand
        self.__datoWiegand = None
        return dato,self.__formato
    
    def __repr__(self) -> str:
        
        return f"{self.name}:\n{self._gpios}"
    
    
'''def pinesW1libres(self):
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
        return False'''