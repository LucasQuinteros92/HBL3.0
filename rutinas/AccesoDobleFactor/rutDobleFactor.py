
from modulos.HBLmodels                import *
from modulos.aplicaciones.Heartbeat   import Heartbeat
from modulos.aplicaciones.Websockets  import WebSocket
from modulos.aplicaciones.LPR         import LPR
from modulos.aplicaciones.Reloj       import relojSerial
from modulos.aplicaciones.Barrera     import Barrera
from configuracion.Settings           import Bbddcfg
from db.BBDD                          import BBDDJSON
from rutinas.AccesoDobleFactor.ObjAux import Persona,EventosWebsocket,DobleFactorLPR



global RUN

def rutinaDobleFactor():
    ID_ANY_PATENTE = "?"
    RUN =True
    
        
    
    
    hbl    = HBLViejo()
    led    = hbl.leds.buscarLed(hbl.leds.Leds.Led1)
    heart  = Heartbeat(led)

    websocket = WebSocket()
    reporte   = EventosWebsocket(websocket)
    database  = BBDDJSON(file=Bbddcfg.Path)
    lpr       = LPR(hbl.serial1)
    reloj     = relojSerial(hbl.serial2)
    
    barrera = Barrera(hbl.salidas.buscarSalida(HBLSalidas.Salidas.OUT2))
    
    df = DobleFactorLPR(barrera)
    
    
    df.logReport("DOBLEFACTOR STARTED")
    
    
    
    
    def buscarPersona(database : BBDDJSON,wiegand):
        
        for dni in database.keys():
            dataPersona = database.get(dni)
            if dataPersona != None and dataPersona["wiegand"] == wiegand:
                return Persona(dni = dni, dataPersona=dataPersona) 
            
        return Persona(wiegand = wiegand)
    
    def procesarEvento(evento : EventosWebsocket.Evento):
        if evento.nombre == "actualizacionConfig":
            df.activarFactorDoble(evento.valor)
        elif evento.nombre == "nuevaVisita":
            persona : Persona = evento.valor
            database.addRecordtoBBDD(persona.dni, persona.wiegand,persona.patentes)
        elif evento.nombre == "abrirBarrera":
            df.barrera.abrirBarrera()
        
    while RUN:
        
        if reporte.hayEventos():
            evento = reporte.leerEvento()
            procesarEvento(evento)
            
        if websocket.reconnected:
            
            websocket.reconnected = False
            reporte.reconectarEventos()
            reporte.enviarEventosPendientes()
            
        if lpr.seDetectoPatente():
                reporte.reportarDeteccion(lpr.leerPatente())
                # borrarPatenteDetectada()
            
        
            
        if reloj.seDetectoFichada():
            
            reporte.enviarEventosPendientes()
            
            patentesLPR = lpr.patentesLeidas()
            
            database.actualizaBBDDSiHayDataNueva()
            
            newWiegand = reloj.leerFichada()
            
            persona = buscarPersona(database, newWiegand)
            
            seDioAcceso = df.accesoSegunFactores( persona , patentesLPR )
            
            if seDioAcceso:
                reporte.reportarIngreso(persona,df.fDobleActivado)
        
        time.sleep(1)
    
    
    hbl.stop()
    exit()