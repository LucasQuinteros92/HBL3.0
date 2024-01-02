
from modulos.HBLmodels import *
from modulos.aplicaciones.Heartbeat import Heartbeat
from  modulos.aplicaciones.logs import LogReport as log

def rutinaPrueba():
    hbl = HBLViejo()
    #log = log("rutinaPrueba")
    
    print(hbl)
    led1 = hbl.leds.buscarLed(hbl.leds.Leds.Led1)
    heart = Heartbeat(led1)

    w  = hbl.wiegand1
    w2 = hbl.wiegand2
    
    log.escribeLineaLog(Logscfg.rutinaPrueba,"rutina de prueba iniciada",log.Colors.GREEN,True)
    time.sleep(5)
    heart.changeDelay(0.1)
    
    log.escribeLineaLog(Logscfg.rutinaPrueba,"rutina de prueba finalizada",log.Colors.RED,True)
    print(hbl)
    print(heart)
    
    while True:
        if w.wiegandDisponible():
            
            print(f"canal1: {w.leerDatoWiegand()}")
        
        if w2.wiegandDisponible():
             print(f"canal2: {w2.leerDatoWiegand()}")
    
    hbl.stop()
    heart.stop()
    #log.stop()