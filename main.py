
from modulos.HBLmodels import *
from modulos.perifericos.HBLi2cDevice import *
import time

from rutinas.SerialDNI import serialDNI
from modulos.conexiones.Conectividad import iniciarConexionesHabilitadas

def hola(gpio,level,tick):
    print("hola")
    hbl.leds.encender(hbl.Leds.Led1)
    hbl.leds.encender(hbl.Leds.Led2)
    time.sleep(0.5)
    hbl.leds.apagar(hbl.Leds.Led1)
    hbl.leds.apagar(hbl.Leds.Led2)
    

    
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
    #hbl.displayLCD.d.w
    #hbl.displayLCD.writeLine(0,"str(line+i)")
    #lines = range(4)
    i = 0
    hbl.displayLCD.move_to(1,2)
    hbl.displayLCD.selectSpecialChar(7)   
    running = True
    while running:
        hbl.displayLCD.move_to(2,10)
        
        hbl.displayLCD.put_str(f"{i}" )
        hbl.displayLCD.move_to(2,2)
        
        hbl.displayLCD.put_str(f"{i}" )
        #time.sleep(1)
        #hbl.displayLCD.move_to(2,10)
        #hbl.displayLCD.put_line(2,f"       {i}" )
        #hbl.displayLCD.writeLine(2,f"       {i}")
        #hbl.displayLCD.backlight(False)
        if i == 10:
            running  = False
       
        i += 1
    #    #time.sleep(1)
    #    #hbl.wiegand2.enviarWiegand34(36739686)
    #    if hbl.wiegand2.wiegandDisponible():
    #    #    
    #       print(hbl.wiegand2.leerDatoWiegand())
    #hbl.enviarWiegand34(36739686)
    hbl.displayLCD.stop()
    hbl.serial1.stop()
    hbl.leds.stopBlink()
    hbl.displayLCD.stop()
    
if __name__ =="__main__":
    
    serialDNI()