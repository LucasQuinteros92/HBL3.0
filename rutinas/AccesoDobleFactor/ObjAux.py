import json,os
from modulos.aplicaciones.Websockets  import WebSocket
from modulos.aplicaciones.Barrera     import Barrera
from modulos.aplicaciones.logs        import LogReport as log
from configuracion.Settings           import Websocketcfg,Logscfg
from datetime                         import datetime
FACTOR_DOBLE  = 2
FACTOR_SIMPLE = 1
  

class Persona():
    def __init__(self,wiegand = None,dni = None,patente = None,dataPersona : dict = None):
        if dataPersona == None:
            self.dni      = dni
            self.patentes = patente
            self.wiegand  = wiegand 
        else:
            self.dni      : str  = dni
            self.wiegand  : str  = dataPersona["wiegand"]
            self.patentes : list = dataPersona["patentes"]
            
        self.patenteIngreso = ""
        self.patentesLeidasLPR = ""


class DobleFactorLPR():
    
    def __init__(self,barrera : Barrera) -> None:
        self.fDobleActivado = False
        self.barrera        = barrera
        
    def activarFactorDoble(self,valor : bool):
        
        self.fDobleActivado = valor
        res = "FACTOR_ACTUALIZADO"
        return res 
        
    def factorDobleActivado(self) -> bool:
        
        return self.fDobleActivado
    
    def accesoSegunFactores(self,persona : Persona , patentesLeidas):
        ret = False
        if self.factorDobleActivado():
            if self.cumpleFactorDoble(persona,patentesLeidas):
                self.PermitirAcceso()
                persona.patentesLeidasLPR = patentesLeidas
                persona.patenteIngreso = self.encontrarPatenteIngreso(persona.patentes,patentesLeidas)
                self.logReport(persona,FACTOR_DOBLE)
                
                ret = persona
            else:
                
                if  persona.dni == None:
                    self.logReport(f"NO CUMPLE FACTOR DOBLE\nDNI NO ENCONTRADO: {persona.dni}\nWD LEIDO: {persona.wiegand}")
                else:
                    self.logReport(f"NO CUMPLE FACTOR DOBLE\nDNI ENCONTRADO: {persona.dni} \nPATENTES NO ENCONTRADAS:  {persona.patentes}")
                
                ret = False
        else:
            self.PermitirAcceso()
            self.logReport(persona,FACTOR_SIMPLE)
            ret = persona
            #reportarAccesoSegunFactores(dni)
        return ret
    def PermitirAcceso(self):
        self.barrera.abrirBarrera()    

    def cumpleFactorSimple():
        
        #if dniValido():
        #    cumple = True
        #else:
        #    cumple = False
        #el factor simple lo realiza biostar
        cumple = True
        return cumple
        
    def cumpleFactorDoble(self, persona : Persona,patentesLeidas)-> bool:
        '''
            verifica que el dni, y la patentes son validas
            buscandolas en la base de datos
        '''
        if persona.dni != None:
            for p in persona.patentes:
                if p in patentesLeidas:
                    return True

        return False
    
    def encontrarPatenteIngreso(self,patentesPersona,patenteLeidas):
        for p in patentesPersona:
            if p in patenteLeidas:
                return p
            
        return ""

                
    
    def logReport(self,data ,factor = None):
        
        if factor == FACTOR_DOBLE:
            data : Persona 
            log.escribeLineaLog(Logscfg.rutinaDobleFactor, "ACCESO",date=True,color=log.Colors.GREEN)
            log.escribeLineaLog(Logscfg.rutinaDobleFactor, "FACTOR DOBLE")
            log.escribeLineaLog(Logscfg.rutinaDobleFactor, "DNI :                " + str(data.dni.__repr__()))
            log.escribeLineaLog(Logscfg.rutinaDobleFactor, "WD LEIDO:            " + data.wiegand.__repr__())
            log.escribeLineaLog(Logscfg.rutinaDobleFactor, "Patentes esperadas : " + str(data.patentes.__repr__()))
            log.escribeLineaLog(Logscfg.rutinaDobleFactor, "Patentes Leidas :    " + str(data.patentesLeidasLPR))
            log.escribeLineaLog(Logscfg.rutinaDobleFactor, "Patente " + str(data.patenteIngreso.__repr__()) + " validada")
        elif factor == FACTOR_SIMPLE:
            data : Persona
            log.escribeLineaLog(Logscfg.rutinaDobleFactor, "ACCESO",date=True,color=log.Colors.GREEN)
            log.escribeLineaLog(Logscfg.rutinaDobleFactor, "FACTOR SIMPLE")
            log.escribeLineaLog(Logscfg.rutinaDobleFactor, "DNI VALIDADO: " + data.dni.__repr__())
            log.escribeLineaLog(Logscfg.rutinaDobleFactor, "WD LEIDO: " + data.wiegand.__repr__())
        else:
            
            log.escribeLineaLog(Logscfg.rutinaDobleFactor, str(data),date=True)



class EventosWebsocket():
    class Evento():
        def __init__(self, nombre,valor) -> None:
            self.nombre = nombre
            self.valor = valor
    def __init__(self,websocket : WebSocket) -> None:
        self._websocket = websocket
        self._websocket.ws.on_message = self.nuevoEventoRecibido
        self._eventoRecibido = False
        self._evento = ""
        self.ultimoDniReportado = ""
        
    def reconectarEventos(self):
        self._websocket.ws.on_message = self.nuevoEventoRecibido
        
    def nuevoEventoRecibido(self,ws, message):
        mensajeDict : dict = json.loads(message)
        keys               = list(mensajeDict.keys())
        data        : dict = json.loads(mensajeDict.get(keys[1]) )
        evento      : str  = data.get("evento")
        msgId       : str  = data.get("msgId")
        datos       : dict = data.get("datos")
        res = ""
        
        self._websocket.on_message(None,message)
        
        if evento == "nuevaVisita":
            #add : dict = evento.get("nuevaVisita")
            #agregar_Y_(add.get("id"),add.get("plate"))
            #res = database.addRecordtoBBDD(datos.get("Persona"),datos.get("Wiegand"),datos.get("Vehiculo"))
            self.generarEvento(evento,
                               Persona(
                                   wiegand=datos.get("Wiegand"),
                                   dni=datos.get("Persona"),
                                   patente=datos.get("Vehiculo")
                                   )
                               )
            
        elif evento ==  "remove":
            #remove :dict = datos.get("remove")
            #res = database.remove_Y_InFile(datos.get("Persona"),datos.get("Vehiculo"))
            self.generarEvento(evento,"")
            
        
        elif evento == "actualizacionConfig":
            #config : dict = evento.get("actualizacionConfig")
            if datos.get("nombre") == "DOBLE_FACTOR_VALIDACION":
                self.generarEvento(evento,datos.get('valor'))
                #res = estado.activarFactorDoble(datos.get('valor'))
            else:
                res= "ConfiguracionDesconocida"
                
        elif evento== "abrirBarrera":
            
            self.generarEvento(evento,"")
        
        eventoRes = self.generarEventoRespuesta(data,msgId)
        
        self.reportar(eventoRes)
        
    def generarEvento(self,nombre,data):
        self._evento = self.Evento(nombre,data)
        self._eventoRecibido =True
        
    def hayEventos(self)-> bool:
        return self._eventoRecibido
    
    def leerEvento(self):
        self._eventoRecibido = False
        ret = self._evento
        self._evento = self.Evento("","")
        return ret
    
    def reportarDeteccion(self,patente):
        
        eventoNuevaDeteccion = self.generarEventoReporte("nuevaPatente",patente=patente)
        self.reportar(eventoNuevaDeteccion)

    def reportarIngreso(self,persona,factorDoble : bool):
        '''
            Reporta en log y al server a quien se le otorgo el acceso
        '''
        if persona.dni != self.ultimoDniReportado:
            if factorDoble:
                e = self.generarEventoReporte("nuevoIngreso", DNI = persona.dni, patente=persona.patenteIngreso)
            else:
                e = self.generarEventoReporte("nuevoIngreso", DNI = persona.dni)
            self.reportar(e)
            self.ultimoDniReportado = persona.dni


    def reportar(self,evento):

        if self._websocket.estaConectado():
            res = self._websocket.send_message(evento)
            #self.guardarEvento(evento)
            #
            #
        else:
            self.guardarEvento(evento)
            #
            #
            res = False
            
        return res
    def guardarEvento(self, evento):
            try:
                if os.path.isfile(Websocketcfg.eventosGuardadosPath):
                    
                    with open(Websocketcfg.eventosGuardadosPath,"r") as jsonFile:
                        obj :dict = json.load(jsonFile)
                    i = int(list(obj.keys())[-1])
                    obj[i+1] = json.loads(evento)
                    with open(Websocketcfg.eventosGuardadosPath,"w") as jsonFile:
                        jsonFile.write(json.dumps(obj,indent=4))
                    
                    
                else:
                    jsonFile = open(Websocketcfg.eventosGuardadosPath,"w")
                    
                    aux = dict()
                    aux["1"] = json.loads(evento)
                    jsonFile.write(json.dumps(aux,indent=4))
                    jsonFile.close()
                
            except Exception as e:
                print(e)

    def enviarEventosPendientes(self):
        try:
            if os.path.isfile(Websocketcfg.eventosGuardadosPath):
                
                with open(Websocketcfg.eventosGuardadosPath,"r") as jsonFile:
                    obj :dict = json.load(jsonFile)
                
                for evento in obj.keys():    
                    self.reportar(json.dumps(obj[evento]))
                    
                os.remove(Websocketcfg.eventosGuardadosPath)
                    
                
            
        except Exception as e:
            print(e)


    def generarEventoRespuesta( self,data : dict ,msgId):
            
            evento = json.dumps({
                "evento": "",
                "datos" : {
                    "clientId" : Websocketcfg.clientId,
                    "msgId": msgId,
                    "data": data,
                    "status": 1
                    },
                "msgId" : msgId
            })
            
            return evento

    def generarEventoReporte( self,evento,DNI="",patente = ""):
        now = datetime.now()
        date = datetime.timestamp(now)
        evento = json.dumps({
            "evento" : evento,
            "datos" : {
                "Persona": DNI,
                "Vehiculo" : patente,
                "fechaHora": date,
                "clientId": Websocketcfg.clientId,
                "clientName" : Websocketcfg.clientName
            },
            "msgId" : date
        })

        return evento
    
    