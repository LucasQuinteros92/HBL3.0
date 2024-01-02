import json,os
from enum import Enum
from modulos.aplicaciones.Websockets  import WebSocket
from modulos.aplicaciones.logs        import LogReport as log
from configuracion.Settings           import Websocketcfg,Logscfg,Bbddcfg
from datetime                         import datetime
from db.BBDD                          import BBDD



class PersonaLPR():
    def __init__(self,persona : dict):

        self.id         = persona.get("id") 
        self.dni        = persona.get("Persona")
        self.wiegand    = persona.get("Wiegand")
        self.vehiculos  = persona.get("Vehiculo")

        
    def jsonFormat(self):
        return {
            
        }
class VehiculoLPR():
    def __init__(self,patente : dict) -> None:
            self.id         = patente.get("id")
            self.patente    = patente.get("patente")
            self.habilitado = patente.get("habilitado")
            self.desde      = patente.get("desde")
            self.hasta      = patente.get("hasta")
        
class Visita():
    def __init__(self,personaid, patenteid : list) -> None:
        
        self.personaid = personaid
        self.patentesid = patenteid

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


class DBLPR():

    
    def __init__(self):
        self.tVisitas   = BBDD(file=Bbddcfg.tablaVisitas)
        self.tPersonas  = BBDD(file=Bbddcfg.tablaPersonas)
        self.tVehiculos = BBDD(file=Bbddcfg.tablaPatentes)
        
    def addPersona(self,persona : PersonaLPR):
        p = self.buscarPersona(persona.dni)
        idvehiculos = self.buscarIdVehiculos(persona.vehiculos)
        if p == None:
            persona.id = str(self.tPersonas.dict.__len__() + 1)
        else:
            persona.id = p.id
            
        self.tPersonas.dict[persona.id] = {
                "id"      : persona.id,
                "Persona" : persona.dni,
                "Wiegand" : persona.wiegand,
                "Vehiculo": idvehiculos
            }
        self.tPersonas.save()
            
        
    def buscarIdVehiculos(self, vehiculos) -> list:
        lista = []       
        for patente in vehiculos:
                v = self.buscarVehiculo(patente)
                if v is not None:
                    lista.append(v.id)
        return lista
    
    def buscarPersona(self, dni) -> PersonaLPR:
        
        for key in self.tPersonas.dict.keys():
            if self.tPersonas.dict[key]["Persona"] == dni:
                return PersonaLPR(self.tPersonas.dict[key])
        return None
    
    def addVehiculo(self,vehiculo : VehiculoLPR):
        p = self.buscarVehiculo(vehiculo.patente)
        if p == None:
            vehiculo.id = str(self.tVehiculos.dict.__len__()+1)
        else:
            vehiculo.id = p.id
            
        self.tVehiculos.dict[vehiculo.id] = {
            "id"        : vehiculo.id,
            "patente"   : vehiculo.patente,
            "habilitado": vehiculo.habilitado,
            "desde"     : vehiculo.desde,
            "hasta"     : vehiculo.hasta
        }
        self.tVehiculos.save()
        
    def buscarVehiculo(self,patente) -> VehiculoLPR:
        for key in self.tVehiculos.dict.keys():
            if self.tVehiculos.dict[key]["patente"] == patente:
                return VehiculoLPR(self.tVehiculos.dict[key])
        return None
    def buscarVehiculos(self,patentes : list):
        lista = []
        for p in patentes:
            v = self.buscarVehiculo(p)
            if v != None:
                lista.append(v)
        return lista
    def addVisita(self,dni,patentes):
        
        if self.buscarVisita(dni) == None:
            pass
    
    def buscarVisita(self,dni):
        persona = self.buscarPersona(dni)
        if persona != None:
            visita = self.tVisitas.dict.get(persona.id)
            
            return Visita(visita["personaid"],visita["patenteid"])
        
        return None
        
    def __LogReport(self, mensaje):
        
        log.escribeLineaLog("DBLPR.log",mensaje,date=True)

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
    
class AccesoSegunFactoresLPR():
    class AccesoPor(Enum):
        PERSONA     = 0,
        VEHICULO    = 1,
        DOBLEFACTOR = 2
        def __get__(self,instance,owner):
            return self.value
        
    def __init__(self, criterio : AccesoPor) -> None:
        self.critero = criterio
    
    def cumpleFactores(self,persona,vehiculo):
        
        if self.critero == self.AccesoPor.PERSONA:
            return True
        elif self.critero == self.AccesoPor.VEHICULO:
            return True
        elif self.critero == self.AccesoPor.DOBLEFACTOR:
            return True
        
        return False
    
    def permitirAcesso(self,persona,vehiculos):
        
        if self.critero == self.AccesoPor.PERSONA:
            return self.accesoPersona()
        elif self.critero == self.AccesoPor.VEHICULO:
            return self.accesoVehicular(vehiculos)
        elif self.critero == self.AccesoPor.DOBLEFACTOR:
            return True
        
        return False
    def accesoPersona(self,persona : PersonaLPR):
        if persona is not None:
            return persona
        else:
            return None
    def accesoVehicular(self, vehiculos : list):
        if vehiculos.__len__() > 0:
            v : VehiculoLPR = vehiculos[0] 
            if v.habilitado:
                
                return v
        else:
            return None
        