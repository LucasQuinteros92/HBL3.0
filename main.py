
from modulos.HBLmodels import *

import time



def hola(gpio,level,tick):
    print("hola")
    hbl.leds.encender(hbl.Leds.Led1)
    hbl.leds.encender(hbl.Leds.Led2)
    time.sleep(0.5)
    hbl.leds.apagar(hbl.Leds.Led1)
    hbl.leds.apagar(hbl.Leds.Led2)
    
if __name__ =="__main__":
    
    hbl = HBLnuevo()
    print(hbl)
    gpio = hbl.leerEntrada(hbl.Entradas.IN4)
    hbl.activarSalida(hbl.Salidas.OUT1)
    #hbl.setInterrupcionPin(hbl.Entradas.IN2,hola,Edges.FALLING_EDGE)
    #print(hbl)
    #hbl.leds.apagar(hbl.Leds.Led1)
    #hbl.leds.encender(hbl.Leds.Led2)
    #time.sleep(1)
    #hbl.leds.apagar(hbl.Leds.Led2)
    #time.sleep(1)
    #print(hbl)
    #while True:
        #pass
        #time.sleep(1)
        #hbl.wiegand2.enviarWiegand34(36739686)
        #if hbl.wiegand1.wiegandDisponible():
        #    
        #   print(hbl.wiegand1.leerDatoWiegand())
    #hbl.enviarWiegand34(36739686)
    