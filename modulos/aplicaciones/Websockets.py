import websocket
import time,os
from datetime import datetime
import requests
import ssl
import json
from threading import Thread 
import threading

from configuracion.Settings import Websocketcfg,Logscfg
from modulos.aplicaciones.logs import LogReport as log

"""
    *Para usar la libreria de websocket, hay que instalar:
        pip3 install websocket-client
        pip3 install rel
    Si se comete el error de instalar el paquete de websocket, hacer lo siguiente:
        pip3 uninstall websocket
        pip3 uninstall websocket-client
        pip3 install websocket-client

    *Hay dos tipos de eventos:
        # IDENTIFY_SUCCESS_FINGERPRINT
        # VERIFY_SUCCESS_CARD
        
    ###########################################
    modificacion de la libreria para que se detenga el hilo cuando muera el 
    proceso padre
    
    class SSLDispatcher(DispatcherBase):
    if threading.main_thread().is_alive():
                self.app.keep_running = False
                
    ###########################################
"""  
class WebSocket(object):
    
    def __init__(self) :
        if Websocketcfg.activado:
            #websocket.enableTrace(True)
            self.connected = False
            self.reconnected = False
            self.reRun = True
            self.connect()
    def connect(self):
        try:
            self.ws = websocket.WebSocketApp(Websocketcfg.host,
                                                on_open=self.on_open,
                                                on_message=self.on_message,
                                                on_error=self.on_error,
                                                on_close=self.on_close,
                                                header = {Websocketcfg.header},
                                                cookie= '{"Token": "'+Websocketcfg.token+'","ClientId": "'+Websocketcfg.clientId+'"} ' )
            #self.ws.on_message = dbFactor.Validacion_Doble_Factor.nuevoEventoRecibido
            self.connected = False
            self.reRun = True
            self.t = Thread( target=self.__run, daemon=False,name ="Websocket")
            self.t.start()
        except Exception as e:
            print(str(e))
            self.__LogReport(Logscfg.hblWebSocket,"Conexion no establecida",log.Colors.GREEN)

    def __run(self):
        try:
            
            self.ws.run_forever(reconnect= 2, 
                                ping_interval= 5,
                                ping_timeout= 3,
                                sslopt={"cert_reqs": ssl.CERT_NONE})  
            # Set dispatcher to automatic reconnection,
            # 5 second reconnect delay if connection closed unexpectedly
            
            #sslopt={"cert_reqs": ssl.CERT_NONE}
        except Exception as e:
            print(e)
        
    def on_open(self,ws):
        self.connected = True
        self.reconnected = True
        self.__LogReport("Conexion establecida",log.Colors.GREEN)
        #self.send_message(self.SALUDO)
        
    def on_message(self, ws, message):
        self.__LogReport("Mensaje Entrante: "+ str(message),log.Colors.GREEN)
        #{"id" : "24997319-0" , "dominio" : ""}
    
    def on_error(self,ws, error):
        self.connected = False 
        self.__LogReport(f"OnError: {error}\nReiniciando conexion",log.Colors.RED)
        
        self.ws.ping_timeout = 3
        self.ws.ping_interval = 5
        #if str(error) == "ping/pong timed out" or str(error) == "[Errno 113] No route to host":
        time.sleep(2)
        
        self.ws.close()
        if self.reRun:
            self.connect()
            
        #log.escribeLineaLog(hbl.LOGS_hblBioStar2_WebSocket,"Error : " + str(error))
    
    

    def on_close(self,ws, close_status_code, close_msg):
        self.connected = False
        self.ws.close()
        self.__LogReport("Conexion Terminada\n"+"close msg: " + str(close_msg) + 
                        "\ncode: "+ str(close_status_code),log.Colors.GREEN)
        if self.reRun:
            self.connect()

    def stop(self):
        self.reRun = False
        self.ws.close()
        self.__LogReport("Websocket STOPED")

    def on_data(self,arg1,arg2,arg3):
        print("### New Data ###")
        
    def send_message(self, mensaje):
        res = False
        try:
            self.ws.send(mensaje)
            self.__LogReport("Mensaje Enviado: "+ str(mensaje),log.Colors.GREEN)
            res = True
        except Exception as e:
            self.__LogReport("Error al enviar mensaje: "+ str(mensaje)+"\n Error:"+str(e),log.Colors.RED)
            res = False
            
        return res

    def estaConectado(self):
        return self.connected 

    def __LogReport(self, mensaje,color):
        
        log.escribeLineaLog(Logscfg.hblWebSocket, mensaje,color,True)
        
        

        
