
import datetime
import os
import shutil
import zipfile
import time  
from threading import Thread
from queue import Queue
from configuracion.Settings import Logscfg,Requestcfg
from enum import Enum
""" --------------------------------------------------------------------------------------------


   Escritura en el Log HBL


-------------------------------------------------------------------------------------------- """
   
def configuracionHBL(log):
 
    # escribe configuracion HBL  
    logFile = open(os.getcwd() + '/logs/' + log, "a") 
    logFile.write("\n")
    logFile.write("Configuracion HBL :")
    logFile.write("\n")

    # path del archivo
    __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

    # Leo los parametros de configuracion en el JSON y los escribe en el hbl.log
    with open(os.path.join(__location__ , "hbl.json"), "r") as f:  
        while True:
            linea = f.readline() 
            logFile.write(str(linea))
            if not linea:
                break
    
    

    logFile.close() 
   
def escribeCabecera(log, tipoEvento):
    logFile = open(log, "a") 
    logFile.write("***********************************************************************************") 
    logFile.write("\n")
    logFile.write("Configuracion HBL :")
    logFile.write("\n")
    logFile.write("Timeout request (seg): ")
    logFile.write(str(Requestcfg.timeoutRequest))
    logFile.write("\n")
    #logFile.write("Modo funcionamiento: ")
    #logFile.write(str(Requestcfg.fun))
    logFile.write("\n")
    logFile.write("UrlRequest 1 : ")
    logFile.write(Requestcfg.urlRequest1)
    logFile.write("\n")
    logFile.write("UrlRequest 2 : ")
    logFile.write(Requestcfg.urlRequest2)
    logFile.write("\n")
    logFile.write("UrlRequest 3 : ")
    logFile.write(Requestcfg.urlRequest3)
    logFile.write("\n")
    logFile.write("UrlRequest 4 : ")
    logFile.write(Requestcfg.urlRequest4)
    logFile.write("\n")
    logFile.write("UrlRequest 5 : ")
    logFile.write(Requestcfg.urlRequest5)
    logFile.write("\n")
    logFile.write("Url seleccionada : ")
    logFile.write(str(Requestcfg.seleccionURL))
    logFile.write("\n")
    logFile.write("Url error : ")
    logFile.write(Requestcfg.urlError)
    #logFile.write("\n")
    #logFile.write("Url mock : ")
    #logFile.write(Requestcfg.MOCK_url)
    logFile.write("\n")
    #logFile.write("Mock activado ? : ")
    #logFile.write(str(Requestcfg.MOCK_activado))
    #logFile.write("\n")
    logFile.write("Ubicacion archivos log : ")
    logFile.write("/usr/programas/hbl/logs/")
    logFile.write("\n")
    #logFile.write("Tiempo act/des salidas (seg) : ")
    #logFile.write(str(Requestcfg.DIG_out_tiempo))
    logFile.write("\n")
    logFile.write("----------------------------------------------------------------------------------") 
    logFile.write("\n")
    logFile.write("Tipo de evento : ")  
    logFile.write(str(tipoEvento))
    logFile.write("\n")
    logFile.write("----------------------------------------------------------------------------------")  
    logFile.write("\n")
    logFile.close() 

""" --------------------------------------------------------------------------------------------

    Escribe serparador + fecha actual
         
        * escribe una linea en el log seleccionado
        * realiza un zip al superar el tamaño seleccionado

-------------------------------------------------------------------------------------------- """

def escribeSeparador(log,color = None):
    logFile = open(os.getcwd() + '/logs/' + log, "a")
    csi    = '\x1B['
    if color is not None:
        if color == 'red':
            seleccion    = csi +  '31;1m'
        elif color == 'yellow':
            seleccion = csi + '33;1m'
    else:
        seleccion = csi + '97;1m'
    end    = csi + '0m'

    
    logFile.write("%s***********************************************************************************%s"%(seleccion,end))
    logFile.write("\n")
    fecha = seleccion + "Fecha / Hora : " + str(datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')) + end
    logFile.write( fecha )
    logFile.write("\n")
    logFile.close() 
  


        
""" --------------------------------------------------------------------------------------------

    Escribe lineas logs
         
        *Escribe mensajes en el log seleccionado
        *Si llegan mensajes mientras esta escribiendo se meten en una lista
        *
-------------------------------------------------------------------------------------------- """

class LogReport(object):
    class Colors(Enum):
        RED = 'r'
        YELLOW = 'y'
        GREEN = 'g'
        def __get__(self,instance,owner):
                return self.value
    def __init__(self, name,file = None):
        self.__running = True
        
        if file == None:
            self.file = name +".log"
        name = name + "_log"
        self.texto = []
        self.q = Queue()
        self.t = Thread(target=self.__run, name=name,daemon=False)
        self.t.start()
        
        self.csi    = '\x1B['
        self.red    = self.csi + '31;1m'
        self.yellow = self.csi + '33;1m'
        self.green  = self.csi + '92;1m'
        self.white  = self.csi + '97;1m'
        self.end    = self.csi + '0m'

        
    
    def EscribirLinea(self,logname,texto :str = '', color = None,fecha :bool = False):
        self.q.put([logname,texto,color,fecha])
        
        
    def stop(self):
        self.__running = False

    def __run(self):
        while self.__running:
                try:
                    log,texto,color,fecha = self.q.get(timeout=0.1)

                    if fecha:
                        escribeSeparador(self.file)    
                    
                    
                    self.escribeLineaLog(self.file,texto,color)
                   
                except :
                    pass
                
    """ --------------------------------------------------------------------------------------------

    Escribe lineas logs
         
        * escribe una linea en el log seleccionado
        * realiza un zip al superar el tamaño seleccionado

    -------------------------------------------------------------------------------------------- """

    def escribeLineaLog(log, texto,color = None,date =False):

        try:

            ruta = os.getcwd() + '/logs/' + log 

            #print(os.getcwd() + hbl.LOGS_pathBackup + log)

            # escribo la linea en el log seleccionado
            csi    = '\x1B['
            if color is not None:
                if color == 'r':
                    seleccion    = csi +  '31;1m'
                elif color == 'y':
                    seleccion = csi + '33;1m'
                elif color == 'g':
                    seleccion = csi + '92;1m'
            else:
                seleccion = csi + '97;1m'
            end    = csi + '0m'
            logFile = open(ruta, "a")
            if date:
                logFile.write("%s***********************************************************************************%s"%(csi + '97;1m',end))
                logFile.write("\n")
                fecha = csi + '97;1m' + "Fecha / Hora : " + str(datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')) + end
                logFile.write( fecha )
                logFile.write("\n")
            texto = seleccion + texto + end
            logFile.write(texto)
            logFile.write("\n")
            logFile.close()   
        
            # leo el tamaño del archivo
            tamanioArchivo = os.path.getsize(ruta) 

            # si el tamaño del archivo supera lo indicaado, prosigue a la compresion y
            # borra el nuevo archivo para que continue grabando
            if tamanioArchivo >= Logscfg.tamañoArchivos:
                
                # lee la fecha y hora actual
                fechaHora = str(datetime.datetime.now().strftime('%Y-%m-%d-%H:%M:%S'))  

                # genera la ruta para grabar el zip
                archivo = ruta + ' ' + fechaHora + '.zip' 

                # genera el .zip
                with zipfile.ZipFile(archivo, mode='w') as zf: 
                    zf.write(ruta, compress_type=zipfile.ZIP_DEFLATED)

                    # mueve el archivo recien zipeado a la carpeta backup
                    origen = archivo
                    destino = os.getcwd() + Logscfg.pathBackup  
                    
                    # vacia el archivo de log base
                    logFile = open(ruta, "w")   
                    logFile.close()  
                    
                    # realiza el movimiento del archivo
                    if os.path.exists(origen) and os.path.exists(destino):  
                        shutil.move(origen, destino) 
                        
                    #se debe agregar las carpetas logs y backuplogs si no existen

                           
    
        except Exception as inst: 

            escribeSeparador(Logscfg.hblCore) 
            #log.escribeLineaLog(hbl.LOGS_hblCore, "Error : " + str(inst))
            

