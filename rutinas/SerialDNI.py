from modulos.HBLmodels import HBLViejo
from modulos.aplicaciones.Heartbeat import Heartbeat
from configuracion.Settings import Logscfg,Cacheocfg
from modulos.conexiones.Conectividad import iniciarConexionesHabilitadas
from modulos.aplicaciones.logs import LogReport as log
from modulos.aplicaciones.Cacheo import Cacheo
from modulos.perifericos.GPIOs import *
import signal,os,sys

global RUN

def serialDNI():
    def receiveSignal(signalNumber, frame):
        print("Signal received")
        
        global RUN
        RUN = False
        
    global RUN
    RUN = True
    hbl = HBLViejo()
    leddata = hbl.leds.buscarLed(hbl.leds.Leds.Led1)
    ledHeartbeat = hbl.leds.buscarLed(hbl.leds.Leds.Led2)
    
    heart = Heartbeat(ledHeartbeat)

    serial = hbl.serial1
    serial.iniciarSerial()
    in2  = hbl.entradas.getGpio(hbl.entradas.EntradasV0.IN2)
    
    
    wiegandOut = hbl.wiegand2
    signal.signal(signal.SIGINT, receiveSignal)
    signal.signal(signal.SIGTERM, receiveSignal)

    #print(hbl.salidas)
    #print(hbl.salidas.activarSalida(hbl.Salidas.OUT1))
    cacheo = Cacheo(hbl.salidas)
    
    iniciarConexionesHabilitadas()
    

    print("PID NUMBER",os.getpid())
    with open("pid.txt","w") as f:
        f.write(os.getpid().__str__())

    print("HBL SERIAL DNI STARTED")
    log.escribeLineaLog(Logscfg.SerialDNI,"HBL SERIAL DNI STARTED",log.Colors.GREEN,True)
    
    def procesarSerial() -> str:
        try:
            ret  = serial.leerSerial()
            log.escribeLineaLog(Logscfg.SerialDNI,f"Nuevo DNI leido:{ret}",log.Colors.GREEN,True)
            leddata.toggleLed()
        except Exception as e:
            log.escribeLineaLog(Logscfg.SerialDNI,f"hubo un error al leer el wiegand {e}",log.Colors.RED,True)
        return ret
    
    def enviarWiegand(data) -> bool:
        try:
            wiegandOut.enviarWiegand34(int(data))
            log.escribeLineaLog(Logscfg.SerialDNI,f"DNI enviado:{int(data)}",log.Colors.GREEN,True)
            leddata.toggleLed()
            ret = True
        except Exception as e:
            log.escribeLineaLog(Logscfg.SerialDNI,f"hubo un error al enviar el wiegand {e}",log.Colors.RED,True)
            ret = False
        return ret
    
    ##########---------------------------------
    
    while RUN:
        
        if serial.hayDatanueva():
            
            DNI = procesarSerial()
            
            wiegandEnviado = enviarWiegand(DNI)
            
            if Cacheocfg.activado and wiegandEnviado:
                cacheo.procesoCacheo()
            
    ##########---------------------------------           
            
    
    heart.stop()
    hbl.stop()
    print("HBL SERIAL DNI STOPPED")
    log.escribeLineaLog(Logscfg.SerialDNI,"HBL SERIAL DNI STOPPED",log.Colors.GREEN,True)
    sys.exit()

