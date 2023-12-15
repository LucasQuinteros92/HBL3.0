
import os,time
from modulos.aplicaciones.Files import *
from modulos.conexiones.Ethernet import iniciarEth0
from modulos.conexiones.Wifi import iniciarWlan0 

def mascara_a_cidr(mascara):
    # Convierte la máscara de subred a una lista de bits
    bits = ''.join(format(int(x), '08b') for x in mascara.split('.'))
    
    # Cuenta el número de bits en la máscara de subred
    cidr = sum(bit == '1' for bit in bits)
    
    return f'/{cidr}'

def iniciarConexionesHabilitadas():
    
    #
    # ATENCION: NO MODIFICAR /etc/network/interfaces, modificar solamente dhcpcd.conf 
    # los tutoriales que se refieren a interfaces
    # son de versiones de RPI OS viejas y ya no se usan.
    #
    
    # agrega la cabecera de inicializacion HBL
    parametrosNet = [' ', '#Configuracion HBL', ' ']
    

    # escribe los parametros por defecto en el archivo dhcpcd.conf

    # hostname
    # clientid
    # persistent
    # option rapid_commit   
    # option domain_name_servers, domain_name, domain_search, host_name
    # option classless_static_routes
    # option ntp_servers
    # option interface_mtu
    # require dhcp_server_identifier
    # slaac private
 
    parametrosNet = ['hostname', 'clientid', 'persistent', 'option rapid_commit', 'option domain_name_servers, domain_name, domain_search, host_name', 'option classless_static_routes','option ntp_servers', 'option interface_mtu', 'require dhcp_server_identifier', 'slaac private', ' ']
    append_multiple_lines('/etc/dhcpcd.conf', parametrosNet, "w+") 
 
    parametrosNet = ['ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev' , 
                             'update_config=1', 'country=AR', ' ' , ' ']
        
    append_multiple_lines('/etc/wpa_supplicant/wpa_supplicant.conf', parametrosNet, "w+")
    
    # ************************************************************************************************************************************************
    # eth0
    
        
    iniciarEth0()
    
    iniciarWlan0()


    
    #os.system("sudo systemctl restart dhcpcd")