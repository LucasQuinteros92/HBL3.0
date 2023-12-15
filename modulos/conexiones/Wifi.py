
import os,time,apt,subprocess,datetime
import threading
from modulos.aplicaciones.Files import *
from configuracion.Settings import Networkcfg as N


def mascara_a_cidr(mascara):
    # Convierte la máscara de subred a una lista de bits
    bits = ''.join(format(int(x), '08b') for x in mascara.split('.'))
    
    # Cuenta el número de bits en la máscara de subred
    cidr = sum(bit == '1' for bit in bits)
    
    return f'/{cidr}'

def iniciarWlan0():
    if N.Wlan0.activado == 1:
        #tambien se puede utilizar rfkill esto permite que se pueda activar el wifi
        #desde el logo azul
        os.system("sudo dhcpcd -k wlan0")
        os.system("sudo dhcpcd -n wlan0")## Habilita el WIFI
        #de esta manera no se puede habilitar desde el escritorio
        #time.sleep(1)
        # si está habilitado el dhcp, escribe la configuracion pero la comenta para que no tenga efecto
        if (N.Wlan0.Hotspotcfg.activado == 1):
            hotspotThread = threading.Thread(target=WifiHostpot,name = "AP",daemon = False)
            hotspotThread.start()
        else:
            subprocess.run(["sudo","killall", "hostapd"],
                       stdout=subprocess.DEVNULL,
                       stderr=subprocess.STDOUT)
            
            subprocess.run(["sudo","killall", "dnsmasq"],
                       stdout=subprocess.DEVNULL,
                       stderr=subprocess.STDOUT)
            
            subprocess.run(["sudo","rfkill","unblock", "wifi"],
                       stdout=subprocess.DEVNULL,
                       stderr=subprocess.STDOUT)
            
            subprocess.run(["sudo","dnsmasq"],
                       stdout=subprocess.DEVNULL,
                       stderr=subprocess.STDOUT)
            
            if N.Wlan0.dhcp == 1:
                parametrosNet = [' ' , 
                                 'interface wlan0'] 
                
                append_multiple_lines('/etc/dhcpcd.conf', parametrosNet, "a+")
                
            else:
                # se agregan los parametros de IP estatica al archivo dhcpcf.conf
                parametrosNet = [' ' , 'interface wlan0']
                if str(N.Wlan0.metric) != "":
                    parametrosNet.append('metric ' + str(N.Wlan0.metric))
                
                if str(N.Wlan0.static_ip_address) != "":
                    parametrosNet.append('static ip_address=' + str(N.Wlan0.static_ip_address)+mascara_a_cidr(N.Wlan0.netmask))
                    
                if str(N.Wlan0.DNS) != "":
                    parametrosNet.append('static domain_name-servers=' + str(N.Wlan0.DNS))
                
                if str(N.Wlan0.gateway) != "":
                    parametrosNet.append('static routers=' + str(N.Wlan0.gateway))

                append_multiple_lines('/etc/dhcpcd.conf', parametrosNet, "a+")

            # archivo wpa_supplicant.conf
            # agrega la cabecera de inicializacion

            # ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
            # update_config=1
            # country=AR

        
                    
            parametrosNet = [' ' , 'network={', '    ssid="' + str(N.Wlan0.ssid) + '"', '    psk="' + str(N.Wlan0.password) + '"', '}']
            append_multiple_lines('/etc/wpa_supplicant/wpa_supplicant.conf', parametrosNet, "a+")

            subprocess.run(["sudo","systemctl","restart", "dhcpcd"],
                       stdout=subprocess.DEVNULL,
                       stderr=subprocess.STDOUT)
    else:
        
        os.system("sudo dhcpcd -k wlan0")## Deshabilita el WIFI
        #time.sleep(1)
        
def WifiHostpot():
        package = 'hostapd' # insert your package name here
        cache = apt.Cache()
        package_installed = False

        if package in cache:
            package_installed = cache[package].is_installed
        else:
            raise Exception("ERROR : hostapd no esta instalado")
        
        subprocess.run(["sudo","rfkill","block", "wifi"],
                       stdout=subprocess.DEVNULL,
                       stderr=subprocess.STDOUT)
        
        subprocess.run(["sudo","systemctl","restart", "dhcpcd"],
                       stdout=subprocess.DEVNULL,
                       stderr=subprocess.STDOUT)
            
        subprocess.run(["sudo","killall", "hostapd"],
                       stdout=subprocess.DEVNULL,
                       stderr=subprocess.STDOUT)
        
        subprocess.run(["sudo","systemctl","unmask", "hostapd"],
                       stdout=subprocess.DEVNULL,
                       stderr=subprocess.STDOUT)
        
        
        
         
        borrarArchivo('/etc/hostapd/hostapd.conf')
        
        
        
        parametrosNet = [ 
                            'interface=wlan0',
                            
                            f'ssid={N.Wlan0.Hotspotcfg.ssid}',
                            'hw_mode=g',
                            'channel=6',
                            'auth_algs=1',
                            'wmm_enabled=1',
                            'macaddr_acl=0',
                            'ignore_broadcast_ssid=0',
                            'wpa=2',
                            f'wpa_passphrase={N.Wlan0.Hotspotcfg.wpa_passphrase}',
                            'wpa_key_mgmt=WPA-PSK',
                            'rsn_pairwise=CCMP'] 
        
        append_multiple_lines('/etc/hostapd/hostapd.conf', parametrosNet, "a+")
        
            
        parametrosNet = [' ' , 
                        'interface wlan0',
                        'nohook wpa_supplicant',  
                        'static ip_address=192.168.0.1',
                        'static domain_name_servers=8.8.8.8'
                        ]
        
        append_multiple_lines('/etc/dhcpcd.conf', parametrosNet, "a+")
        
        borrarArchivo('/etc/dnsmasq.conf')
        
        parametrosNet = [
                        'interface=wlan0',
                        'bind-dynamic',
                        'domain-needed',
                        'bogus-priv',
                        'dhcp-range=192.168.0.3,192.168.0.100,255.255.255.0,12h']

        append_multiple_lines('/etc/dnsmasq.conf', parametrosNet, "a+")
        
        
        borrarArchivo('/etc/iptables-hs')
        
        parametrosNet = ['#!/bin/bash',
                         'sudo iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE',
                         'sudo iptables -A FORWARD -i eth0 -o wlan0 -m state --state RELATED,ESTABLISHED -j ACCEPT',
                         'sudo iptables -A FORWARD -i wlan0 -o eth0 -j ACCEPT']
        
        append_multiple_lines('/etc/iptables-hs', parametrosNet, "a+")
        
        subprocess.run(["sudo", "sh", "/etc/iptables-hs"],
                       stdout=subprocess.DEVNULL,stderr=subprocess.STDOUT)
        
        subprocess.run(["sudo", "dnsmasq"],
                       stdout=subprocess.DEVNULL,stderr=subprocess.STDOUT)
        subprocess.run(["sudo", "dhcp"],
                       stdout=subprocess.DEVNULL,stderr=subprocess.STDOUT)
        
        subprocess.run(["sudo","rfkill","unblock", "wifi"],
                       stdout=subprocess.DEVNULL,
                       stderr=subprocess.STDOUT)
        subprocess.run(["sudo","systemctl","restart", "dhcpcd"],
                       stdout=subprocess.DEVNULL,
                       stderr=subprocess.STDOUT)
        res = startHostapd()
        while res:
           res = startHostapd()
           time.sleep(2)
           
def startHostapd():
        process = subprocess.Popen("sudo hostapd /etc/hostapd/hostapd.conf", 
                                   shell=True, 
                                   stdout=subprocess.PIPE, 
                                   stderr=subprocess.PIPE, 
                                   text=True)

        while process.poll() is None:
            line = process.stdout.readline()
            if hayMensajesDeInteres(line.strip()):
                
                print(f"{datetime.datetime.now().strftime('%Y-%m-%d-%H:%M')} {line}", end='')

        # Capture any remaining output after the process completes
        for line in process.stdout.readlines():
            
            print(f"{datetime.datetime.now().strftime('%Y-%m-%d-%H:%M')} {line}", end='')

        # Check the return code to determine if the process was successful
        return process.returncode 
    
def hayMensajesDeInteres(texto):
    
    mensajes = [
                'wlan0: AP-ENABLED',
                'associated',
                'disassociated'
            ]
    for m in mensajes:
        if m in texto:
            return True
    
    return False
    
    