from modulos.HBLmodels                      import *
from modulos.aplicaciones.Heartbeat         import Heartbeat
from modulos.aplicaciones.Websockets        import WebSocket
from modulos.aplicaciones.LPR               import LPR
from modulos.aplicaciones.Reloj             import relojSerial
from modulos.aplicaciones.Barrera           import BarreraConSensores
from modulos.conexiones.Conectividad        import iniciarConexionesHabilitadas
from configuracion.Settings                 import Bbddcfg
from rutinas.AccesoLPR.ObjAux               import EventosWebsocket,DBLPR,PersonaLPR,VehiculoLPR,AccesoSegunFactoresLPR




def rutinaAccesoLPR():
    iniciarConexionesHabilitadas( )
    
    hbl    = HBLViejo()
    led    = hbl.leds.buscarLed(hbl.leds.Leds.Led1)
    heart  = Heartbeat(led)

    websocket = WebSocket()
    reporte   = EventosWebsocket(websocket)
    database  = DBLPR()
    lpr       = LPR(hbl.serial1)
    reloj     = relojSerial(hbl.serial2)
    
    barrera = BarreraConSensores(barreraAbrir=hbl.salidas.buscarSalida(HBLSalidas.Salidas.OUT2),
                                 sensor1=hbl.entradas.buscarEntrada(HBLEntradas.EntradasV0.IN1),
                                 sensor2=hbl.entradas.buscarEntrada(HBLEntradas.EntradasV0.IN2))
    
    df = AccesoSegunFactoresLPR(AccesoSegunFactoresLPR.AccesoPor.VEHICULO)
    
    def procesarEvento(evento : EventosWebsocket.Evento):

        if evento.nombre == "nuevaVisita":
            procesarVisita( evento.valor )
        if evento.nombre == "nuevoVehiculo":
            procesarVehiculo ( evento.valor )
        elif evento.nombre == "abrirBarrera":
            barrera.abrirBarrera()
            
    def procesarVehiculo(vehiculo : dict):
        
        database.addVehiculo( VehiculoLPR(vehiculo))
        
    def procesarVisita( visita : dict):
        
        database.addPersona(PersonaLPR(visita))
           
    
    visita = {"Persona":"367396865",
              "Wiegand":"367396866",
              "Vehiculo":["CCC123"]}
    vehiculo = {
            "patente": "EEE123",
            "habilitado" : False,
            "desde" : "1:00",
            "hasta" : "22:00"
    }
    #procesarVisita(visita)
    #procesarVehiculo(vehiculo)
    while True:
        
        if lpr.seDetectoPatente():
            lpr.leerPatente()
            nuevaPatente = True
            
        if reloj.seDetectoFichada():
            fichada = reloj.leerFichada()
            nuevaFichada = True
            
        if df.cumpleFactores(nuevaFichada,nuevaPatente):
            persona = database.buscarPersona(fichada)
            vehiculos = database.buscarVehiculos(lpr.patentesLeidas())
            df.permitirAcesso(persona,vehiculos)
            
        if lpr.seDetectoPatente():
            patente = lpr.leerPatente()
            vehiculo : VehiculoLPR= database.buscarVehiculo(patente)
            if vehiculo != None:
                if vehiculo.habilitado:
                    barrera.abrirBarrera()
                    reporte.reportarIngreso(vehiculo)
                else:
                    log.escribeLineaLog("rutAccesoLPR.log",f"La patente no esta habilitada",date = True)
            else:
                log.escribeLineaLog("rutAccesoLPR.log",f"La patente {vehiculo.patente} no esta registrada",date = True)
                
            