import os,random,sys
from modulos.perifericos.IO import HBLSalidas
from configuracion.Settings import Cacheocfg,Logscfg
from modulos.aplicaciones.logs import LogReport as log

import time

class Cacheo(object):
    """ ******************************************************************************************

        PINOUT 

            luzVerde = Pin_Salida1
            sirena  = Pin_Salida2
            luzRoja = Pin_Salida3
            barrera = Pin_Salida4

    ****************************************************************************************** """  
    
    def __init__(self,salidas : HBLSalidas) -> None:
        self.salidas : HBLSalidas = salidas
        self.ubicacionCacheo = 0
        self.listaAleatoria = []
        self.valorEncontrado = 0
        self.CACHEO_cacheosPositivos   = Cacheocfg.cacheosPositivos
        self.CACHEO_cantidadCacheos    = Cacheocfg.cantidadCacheos 
        self.CACHEO_repRelePositivo    = Cacheocfg.repRelePositivo 
        self.CACHEO_repReleNegativo    = Cacheocfg.repReleNegativo
        self.CACHEO_tiempoReleNegativo = Cacheocfg.tiempoReleNegativo
        self.CACHEO_tiempoRelePositivo = Cacheocfg.tiempoRelePositivo
        
        
        ### logica inversa ###
        # modulo de 4 relay
        # 1 a la salida apaga el relay
        # 0 a la salida enciende el relay
        self.salidas.activarSalida(HBLSalidas.Salidas.OUT1)
        self.salidas.activarSalida(HBLSalidas.Salidas.OUT2)
        self.salidas.activarSalida(HBLSalidas.Salidas.OUT3)
        self.salidas.activarSalida(HBLSalidas.Salidas.OUT4)
        
        
        
    def aleatorioValor(self,cacheosPositivos, cantidadCacheos):
    
        try:

            random.seed()
            listaNumeros = random.sample(range(0, cantidadCacheos), cacheosPositivos) 
            listaNumeros.sort()

            return listaNumeros
        
        except Exception as e:  

            exc_type, exc_obj, exc_tb = sys.exc_info() 
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1] 
            errorExcepcion = "ERROR - archivo : " + str(fname) + " - linea : " + str(sys.exc_info()[-1].tb_lineno) + " - mensaje : " + str(exc_obj) 

            #log.escribeSeparador(hbl.LOGS_hblCacheo)
            #log.escribeLineaLog(hbl.LOGS_hblCacheo, "Error : " + str(errorExcepcion))

    """ ******************************************************************************************

        



    ****************************************************************************************** """ 

    def ApagaReles(self):
        
        try:
            
            self.salidas.activarSalida(HBLSalidas.Salidas.OUT1)
            self.salidas.activarSalida(HBLSalidas.Salidas.OUT2)
            self.salidas.activarSalida(HBLSalidas.Salidas.OUT3)
            self.salidas.activarSalida(HBLSalidas.Salidas.OUT4)

        except Exception as e:  

            exc_type, exc_obj, exc_tb = sys.exc_info() 
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1] 
            errorExcepcion = "ERROR - archivo : " + str(fname) + " - linea : " + str(sys.exc_info()[-1].tb_lineno) + " - mensaje : " + str(exc_obj) 

            #log.escribeSeparador(hbl.LOGS_hblCacheo)
            #log.escribeLineaLog(hbl.LOGS_hblCacheo, "Error : " + str(errorExcepcion))

    """ ******************************************************************************************

        

        

    ****************************************************************************************** """ 

    def AbreBarrera(self):
        
    
        try:
            self.salidas.desactivarSalida(HBLSalidas.Salidas.OUT4)
        
        except Exception as e:  

            exc_type, exc_obj, exc_tb = sys.exc_info() 
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1] 
            errorExcepcion = "ERROR - archivo : " + str(fname) + " - linea : " + str(sys.exc_info()[-1].tb_lineno) + " - mensaje : " + str(exc_obj) 

            #log.escribeSeparador(hbl.LOGS_hblCacheo)
            #log.escribeLineaLog(hbl.LOGS_hblCacheo, "Error : " + str(errorExcepcion))  

    """ ******************************************************************************************

        

        

    ****************************************************************************************** """ 

    def CierraBarrera(self):
        #auxiliar.EscribirFuncion("CierraBarrera")

        try:
            self.salidas.activarSalida(HBLSalidas.Salidas.OUT4)
            

        except Exception as e:  

            exc_type, exc_obj, exc_tb = sys.exc_info() 
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1] 
            errorExcepcion = "ERROR - archivo : " + str(fname) + " - linea : " + str(sys.exc_info()[-1].tb_lineno) + " - mensaje : " + str(exc_obj) 

            #log.escribeSeparador(hbl.LOGS_hblCacheo)
            #log.escribeLineaLog(hbl.LOGS_hblCacheo, "Error : " + str(errorExcepcion))  
    
    """ ******************************************************************************************

        

        

    ****************************************************************************************** """ 

    def NoPasa(self):
        #auxiliar.EscribirFuncion("NoPasa")

        try: 

            contador = 0

            while contador < self.CACHEO_repRelePositivo:
                self.salidas.desactivarSalida(HBLSalidas.Salidas.OUT2)
                self.salidas.desactivarSalida(HBLSalidas.Salidas.OUT3)

                time.sleep(int(self.CACHEO_tiempoRelePositivo))
                self.salidas.activarSalida(HBLSalidas.Salidas.OUT2)
                self.salidas.activarSalida(HBLSalidas.Salidas.OUT3)

                time.sleep(int(self.CACHEO_tiempoRelePositivo))
                contador = contador + 1
            
            # abre la barrera
            self.AbreBarrera()
            #time.sleep(int(hbl.CACHEO_tiempoRelePositivo))    
            # cierra la barrera
            self.CierraBarrera()  

        except Exception as e:  

            exc_type, exc_obj, exc_tb = sys.exc_info() 
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1] 
            errorExcepcion = "ERROR - archivo : " + str(fname) + " - linea : " + str(sys.exc_info()[-1].tb_lineno) + " - mensaje : " + str(exc_obj) 

            #log.escribeSeparador(hbl.LOGS_hblCacheo)
            #log.escribeLineaLog(hbl.LOGS_hblCacheo, "Error : " + str(errorExcepcion))

    """ ******************************************************************************************

        

        

    ****************************************************************************************** """ 

    def Pasa(self):
        #auxiliar.EscribirFuncion("Pasa")

        try:

            contador = 0

            # abre la barrera
            self.AbreBarrera()
            time.sleep(int(self.CACHEO_tiempoReleNegativo))  
            # cierra la barrera
            self.CierraBarrera()  

            while contador < self.CACHEO_repReleNegativo:
                self.salidas.desactivarSalida(HBLSalidas.Salidas.OUT1)
                time.sleep(int(self.CACHEO_tiempoReleNegativo))
                self.salidas.activarSalida(HBLSalidas.Salidas.OUT1)
                time.sleep(int(self.CACHEO_tiempoReleNegativo))
                contador = contador + 1
        
        except Exception as e:  

            exc_type, exc_obj, exc_tb = sys.exc_info() 
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1] 
            errorExcepcion = "ERROR - archivo : " + str(fname) + " - linea : " + str(sys.exc_info()[-1].tb_lineno) + " - mensaje : " + str(exc_obj) 

            #log.escribeSeparador(hbl.LOGS_hblCacheo)
            #log.escribeLineaLog(hbl.LOGS_hblCacheo, "Error : " + str(errorExcepcion))

    """ ******************************************************************************************

        

        

    ****************************************************************************************** """ 

    def botonPanico(self):
        #auxiliar.EscribirFuncion("botonPanico")

        try:
    
            #log.escribeLineaLog(hbl.LOGS_hblCacheo, "NoPasa (Boton Panico Activado)")
            self.NoPasa() 
        
        except Exception as e:  

            exc_type, exc_obj, exc_tb = sys.exc_info() 
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1] 
            errorExcepcion = "ERROR - archivo : " + str(fname) + " - linea : " + str(sys.exc_info()[-1].tb_lineno) + " - mensaje : " + str(exc_obj) 

            #log.escribeSeparador(hbl.LOGS_hblCacheo)
            #log.escribeLineaLog(hbl.LOGS_hblCacheo, "Error : " + str(errorExcepcion)) 

    """ ******************************************************************************************

        

        

    ****************************************************************************************** """ 


    """El proceso de Cacheo consiste en hacer una listaAleatoria con hbl.CACHEO_cacheosPositivos elementos donde cada elemento son numeros del 0 a hbl.CACHEO_cantidadCacheos.
    Los numeros que contiene la listaAleatoria son los numeros que van a tener que hacer Cacheo. Es decir, supongamos que hbl.CACHEO_cacheosPositivos = 2 y hbl.CACHEO_cantidadCacheos = 10
    entonces tengo listaAleatoria = [2,6] entonces con la variable n yo voy a recorrer la lista y comparar con ubicacionCacheo con cada valor de ubicacionCacheo desde el 0 hasta
    10. Es decir que 10 veces voy a chequear si el 2 o el 6 son iguales al valor de ubicacionCacheo, osea que van a ser iguales cuando ubicacionCacheo sea igual a 2 y a 6 y en
    esos dos casos tendre cacheos positivos. Una vez recorrido la listaAleatoria 10 veces genero una nueva lista y empiezo de vuelta"""
    def procesoCacheo(self):
        #auxiliar.EscribirFuncion("procesoCacheo")

        try:
            flag = 0
            
            if self.ubicacionCacheo >= self.CACHEO_cantidadCacheos: # Una vez que recorrida la lista la cantidad de veces necesaria (CantidadCacheos), genero una lista nueva
                self.ubicacionCacheo = 0

            # si el valor de ubicacionCacheo es 0, significa que recien empieza el cacheo entonces
            # calcula las n posiciones a cachear por positivo
            if self.ubicacionCacheo == 0:           

                self.listaAleatoria = self.aleatorioValor(self.CACHEO_cacheosPositivos, self.CACHEO_cantidadCacheos)       

                #log.escribeSeparador(hbl.LOGS_hblCacheo)       
                #log.escribeLineaLog(hbl.LOGS_hblCacheo, "Calculo de valores de posicion de cacheo : " + str(variablesGlobales.listaAleatoria)) 
                #log.escribeLineaLog(hbl.LOGS_hblCacheo, "Cantidad de cacheos : " + str(hbl.CACHEO_cantidadCacheos)) 
                #log.escribeLineaLog(hbl.LOGS_hblCacheo, "Cantidad de cacheos positivos: " + str(hbl.CACHEO_cacheosPositivos)) 
    
            #Recorro la lista con la variable n la cual determinara las posiciones en las cuales voy a tener cacheo positivo
            for n in self.listaAleatoria:
                # Me fijo si en esta ubicacionCacheo tengo un cacheo positivo
                if self.ubicacionCacheo == n:   
                    self.valorEncontrado = 1

            if self.valorEncontrado == 1:
                self.NoPasa()
                log.escribeLineaLog(Logscfg.hblCacheo, "NoPasa :" + str(self.ubicacionCacheo)) 
                flag = 1
            else:
                self.Pasa()
                log.escribeLineaLog(Logscfg.hblCacheo, "Pasa :" + str(self.ubicacionCacheo))            
                flag = 0
            
            # incrementa la variable en 1
            self.ubicacionCacheo = self.ubicacionCacheo + 1
            # reinicia la variable 
            self.valorEncontrado = 0 
            return flag
        
        except Exception as e:  

            exc_type, exc_obj, exc_tb = sys.exc_info() 
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1] 
            errorExcepcion = "ERROR - archivo : " + str(fname) + " - linea : " + str(sys.exc_info()[-1].tb_lineno) + " - mensaje : " + str(exc_obj) 

            #log.escribeSeparador(Logscfg.hblCacheo)
            log.escribeLineaLog(Logscfg.hblCacheo, "Error : " + str(errorExcepcion),log.Colors.RED,True)  

            return 99