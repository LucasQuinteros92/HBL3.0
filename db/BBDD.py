from threading import Thread,Lock
import json
import os
from modulos.aplicaciones.logs import LogReport as log
from configuracion.Settings import Logscfg


class BBDD():
    def __init__(self, file):
        self.file = file
        self.mutexBBDD_DNI_Patente = Lock()
        self.newDataBBDD = False
        self.dict : dict = self.read()
        
    def hayNuevaData(self):
        return self.newDataBBDD
    
    def read(self):
        '''
            Devuelve Diccionario equivalente al JSON dentro del archivo
            en la ruta self.file
        '''
        self.mutexBBDD_DNI_Patente.acquire()
        
        with open(self.file) as f:
            JSON = json.load(f)
            #print("JSON" + str(JSON))
        self.mutexBBDD_DNI_Patente.release()
        return JSON
    
    def save(self):
        '''
            Escribe data en formato JSON dentro de un archivo
            con ruta self.file
        '''
        self.mutexBBDD_DNI_Patente.acquire()
        
        with open(self.file, 'w') as convert_file:
            convert_file.write(json.dumps(self.dict,indent=6))
            
        self.mutexBBDD_DNI_Patente.release()

class BBDDJSON(object):
    
    
    def __init__(self, file):
        self.file = file
        self.mutexBBDD_DNI_Patente = Lock()
        self.newDataBBDD = False
        self.BBDD : dict = self.getBBDDfromJSON()
        
    def hayDataNuevaData(self):
        return self.newDataBBDD
    
    def getBBDDfromJSON(self):
        '''
            Devuelve Diccionario equivalente al JSON dentro del archivo
            en la ruta self.file
        '''
        self.mutexBBDD_DNI_Patente.acquire()
        
        with open(self.file) as f:
            JSON = json.load(f)
            #print("JSON" + str(JSON))
        self.mutexBBDD_DNI_Patente.release()
        return JSON
    
    def writeBBDDtoJSON(self,newData):
        '''
            Escribe data en formato JSON dentro de un archivo
            con ruta self.file
        '''
        self.mutexBBDD_DNI_Patente.acquire()
        
        with open(self.file, 'w') as convert_file:
            convert_file.write(json.dumps(newData,indent=6))
        self.mutexBBDD_DNI_Patente.release()
    
    def get(self, key):
        '''
           devuelve las patentes asociadas al dni en la base de datos
        '''    
        return self.BBDD.get(key)
    
    
        
    def __LogReport(self, mensaje):
        
        log.escribeLineaLog(Logscfg.BBDDJSON,mensaje,date=True)
        
            
    def addRecordtoBBDD(self,id,wiegand,plate = ""):
        '''
            Agrega una patente al id, en formato json.
            Devuelve diccionario actualizado con los cambios realizados.
            Sino Devuelve que salio mal
        '''
        try:
            #if str(plate) == "":
            #    errorStr = "ERROR: Patente VACIA"
            #    self.__LogReport(errorStr)
            #    return errorStr
            if str(id) == "":
                errorStr = "ERROR: DNI VACIO"
                self.__LogReport( errorStr )
                return errorStr
            
            JSON :dict = self.getBBDDfromJSON()
            personaLocal : dict = JSON.get(str(id))
            
            if personaLocal is None:
                self.__LogReport( "Nuevo ID")
                JSON[str(id)] = {}
                JSON[str(id)]["wiegand"] = str(wiegand)
                JSON[str(id)]["patentes"] = []
                if plate.strip() != "":
                    JSON[str(id)]["patentes"] = [plate]
                
                    
            else:
                self.__LogReport( "ID ya existe")
                """Check si la patente no esta ya"""
                patentesPersonaLocal = personaLocal.get("patentes")
                if str(plate) in patentesPersonaLocal:
                    errorStr = "ERROR: Patente ya existe"
                    self.__LogReport( errorStr )
                    return errorStr
                else:
                    if str(plate).strip() != "":
                        JSON[str(id)]["patentes"].append(str(plate))
                
            #print("newData" + str(JSON))
            self.writeBBDDtoJSON(JSON)
            self.newDataBBDD = True
            self.__LogReport( "BBDD actualizada")
            return "OK"
        
        except Exception as e:
            self.__LogReport( "Error al agregar data: " + str(e))
            return str(e)
    
    
    def getDNIfromWD(self,wiegand) :
        dni = "NULL"
        JSON :dict = self.getBBDDfromJSON()
        personas = JSON.keys()
        for p in personas:
            #print(wiegand)
            if JSON[p]["wiegand"] == str(wiegand):
                dni = p
                
        return str(dni)
    
    def remove_Y_InFile(self,id,plate):
        try:
            JSON : dict = self.getBBDDfromJSON()
            
            if JSON.get(str(id)) is None:
                errorStr = "El ID no existe"
                self.__LogReport( errorStr)
                return errorStr
            
            else:
                print("JSON" + str(JSON))
                if plate == "": # si no se especifica la patente, se borran todas
                    JSON.pop(str(id))
                else:
                    if str(plate) in JSON.get(str(id)): #Me fijo si la patente existe
                        JSON[str(id)].remove(str(plate)) #Borro la patente      
                    else:
                        errorStr = "La patente no existe"
                        self.__LogReport( errorStr)
                        return errorStr
                                     
                print("newData" + str(JSON))
                self.writeBBDDtoJSON(JSON)
                self.newDataBBDD = True
                self.__LogReport( "BBDD actualizada")
            
            return JSON
        except Exception as e:
            self.__LogReport( "Error al agregar data: " + str(e))
            return str(e)
        
        
    def actualizaBBDDSiHayDataNueva(self):
        '''
            actualiza la base de datos local(archivo json)
            si hay un dato nuevo en la misma 
            sino no hace nada
        '''
        try:
            if self.newDataBBDD:
                self.mutexBBDD_DNI_Patente.acquire()
                with open(self.file) as f:
                    self.BBDD = json.load(f)
                    #print(data)
                self.mutexBBDD_DNI_Patente.release()
                self.newDataBBDD = False
                
        except Exception as e:
            print(str(e))
            lista = []
            return lista #Checkear esto
        
    def dniValido(self,dni):
        '''
            indica si el dni existe en la base de dato
            retorna booleano
        '''
        
        for p in self.BBDD.keys():
            if dni == p:
                return True
        
        return False
    
    def keys(self):
        return self.BBDD.keys()
    
    def esUnaPatenteValida(self,dni,patentes):
        '''
            verifica que la patente es valida
            el dni debe existir en la base de datos
        '''
        if self.validar_patente(dni,patentes) != 'NO MATCH':
            
            return True
        else:
            
            return False
    
    def validar_patente(self,dni,patentes):
        '''
            Devuelve la primer patente esperada asociada al dni
            si la encuentra en las ultimas 10 patentes captadas por la camara
            sino devuelve NO_MATCH
        '''
        try:
            self.patentes_esperadas = self.get_patentes_asociadas_from_BBDD(dni)
            self.patentes_LPR = patentes#self.get_patentes_from_LPR()
            
            if "?" in self.patentes_esperadas:
                return "?"
            
            for p in self.patentes_esperadas:
                if p in self.patentes_LPR:
                    return p
            
            
            return "NO MATCH"
        except Exception as e:
            return "NO MATCH"
        
    def get(self, key):
        '''
           devuelve las patentes asociadas al dni en la base de datos
        '''    
        return self.BBDD.get(key)
    
    
        
    def __LogReport(self, mensaje):
        
        log.escribeLineaLog(Logscfg.BBDDJSON,mensaje,date=True)
        
