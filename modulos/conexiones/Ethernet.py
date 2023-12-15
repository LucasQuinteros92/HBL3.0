import os,time

from  modulos.aplicaciones.Files import *
from configuracion.Settings import Networkcfg as N

def mascara_a_cidr(mascara):
    # Convierte la máscara de subred a una lista de bits
    bits = ''.join(format(int(x), '08b') for x in mascara.split('.'))
    
    # Cuenta el número de bits en la máscara de subred
    cidr = sum(bit == '1' for bit in bits)
    
    return f'/{cidr}'

def iniciarEth0():
    if N.Eth0.activado == 1:
        os.system("sudo dhcpcd -n eth0") ##Habilita el puerto ethernet
        #time.sleep(1)
        # si está habilitado el dhcp, escribe la configuracion pero la comenta para que no tenga efecto
        if N.Eth0.dhcp == 1:
            parametrosNet = [   'interface eth0']
                                
            append_multiple_lines('/etc/dhcpcd.conf', parametrosNet, "a+")

        else:
            parametrosNet = ['interface eth0']
            if str(N.Eth0.metric) != "":
                parametrosNet.append('metric ' + str(N.Eth0.metric))
            
            if str(N.Eth0.static_ip_address) != "":
                parametrosNet.append('static ip_address=' + str(N.Eth0.static_ip_address)+mascara_a_cidr(N.Eth0.netmask))

            if str(N.Eth0.DNS) != "":
                parametrosNet.append('static domain_name-servers=' + str(N.Eth0.DNS))
            
            if str(N.Eth0.gateway) != "":
                parametrosNet.append('static routers=' + str(N.Eth0.gateway))

            append_multiple_lines('/etc/dhcpcd.conf', parametrosNet, "a+")
         
    else:
        os.system("sudo dhcpcd -k eth0")## Deshabilita el puerto ethernet
        #time.sleep(1)
        
    
    
    