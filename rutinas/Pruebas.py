
from modulos.HBLmodels import *
from modulos.aplicaciones.Heartbeat import Heartbeat
from  modulos.aplicaciones.logs import LogReport as log

def rutinaPrueba():
    hbl = HBLnuevo()
    #log = log("rutinaPrueba")
    
    print(hbl)
    led1 = hbl.leds.buscarLed(hbl.Leds.Led1)
    heart = Heartbeat(led1)
    #log.EscribirLinea(Logscfg.rutinaPrueba)
    
    salida1 = hbl.salidas.buscarSalida(hbl.Salidas.OUT1)
    salida1.activarSalida()
    hbl.salidas
    #led1.encender()
    
    log.escribeLineaLog(Logscfg.rutinaPrueba,"rutina de prueba iniciada",log.Colors.GREEN,True)
    time.sleep(5)
    heart.changeDelay(0.1)
    log.escribeLineaLog(Logscfg.rutinaPrueba,"rutina de prueba finalizada",log.Colors.RED,True)
    print(hbl)
    print(heart)
    
    hbl.stop()
    heart.stop()
    #log.stop()