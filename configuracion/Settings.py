#ADVERTENCIA:
#ESTE ARCHIVO SE GENERA DINAMICAMENTE
#NO MODIFICAR

#######HBL######
class Hblcfg():
	idHBL = '3'
	name = 'Desarollo'
	model = 0

#######WIEGAND######
class Wiegandcfg():
	class W1():
		name = 'W1'
		activado = 1
		modo = 'IN'
		delayPulso = 5e-05
		delayIntervalo = 0.002
		primerBit = 1

	class W2():
		name = 'W2'
		activado = 1
		modo = 'OUT'
		delayPulso = 0.0005
		delayIntervalo = 0.001
		primerBit = 1


#######NETWORK######
class Networkcfg():
	activado = 1
	class Eth0():
		name = 'Eth0'
		activado = 1
		dhcp = 1
		static_ip_address = '172.30.2.58'
		gateway = '172.30.2.1'
		DNS = '8.8.8.8 1.1.1.1'
		metric = 0
		netmask = '255.255.254.0'

	class Wlan0():
		name = 'Wlan0'
		activado = 1
		class Hotspotcfg():
			activado = 1
			ssid = 'RPIHOTSPOT'
			wpa_passphrase = 'Jphlions135'

		dhcp = 1
		static_ip_address = '172.30.7.22'
		gateway = '172.30.7.1'
		DNS = '8.8.8.8 1.1.1.1'
		netmask = '255.255.254.0'
		ssid = 'JPH_SUB'
		password = 'Tecnica_labo'
		metric = 201

	class Ppp0():
		name = 'Ppp0'
		activado = 0
		vendor_ID = ''
		product_ID = ''
		dialcommand = 'ATDT'
		init1 = 'ATZ'
		init2 = ''
		init3 = ''
		init4 = 'AT+CGDCONT=1,IP,igprs.claro.com.ar'
		stupidmode = 1
		ISDN = 0
		modemType = 'Analog Modem'
		askPassword = 0
		phone = '*99#'
		username = 'clarogprs'
		password = 'clarogprs999'
		baud = 9600
		newPPPD = 1
		carrierCheck = 0
		autoReconnect = 0
		dialAttempts = 1
		metric = 0

	class Eth1():
		name = 'Eth1'
		activado = 0
		dhcp = 1
		static_ip_address = '192.168.1.1/24'
		static_routers = '192.168.1.1'
		gateway = '172.16.0.1'
		DNS = '172.19.201.17 172.19.201.18'
		netmask = '255.255.255.0'
		network = '192.168.1.0'
		broadcast = '192.168.1.255'
		metric = 200
		vendor_ID = '0x2357'
		product_ID = '0x0600'
		timeDelay = 5

	class Testconexion():
		name = 'Testconexion'
		activado = 1
		url = 'http://8.8.8.8'
		timeoutUrl = 8
		timeDelay = 5
		timeRepeat = 5
		intentosConexion = 25
		resetActivado = 0


#######SERIAL######
class Serialcfg():
	class Com1():
		name = 'Com1'
		activado = 1
		port = '/dev/serial0'
		baudrate = 9600
		bytesize = 8
		parity = 'N'
		stopbits = 1
		timeout = 1

	class Com2():
		name = 'Com2'
		activado = 0
		port = '/dev/ttyAMA2'
		baudrate = 9600
		bytesize = 8
		parity = 'N'
		stopbits = 1
		timeout = 0.5


#######I2C######
class I2ccfg():
	class I2c():
		name = 'I2c'
		activado = 0
		bus = 1
		addr = ''

	class Lcd20x4():
		name = 'Lcd20x4'
		activado = 0
		addr = '0x27'
		bus = '3'
		line0 = '     OCUPACION'
		line1 = '         0'
		line2 = ''
		line3 = '  PWC  Acceso Castelli'

	class Rtc():
		name = 'Rtc'
		activado = 0
		addr = '0x28'
		bus = '1'


#######CACHEO######
class Cacheocfg():
	activado = 1
	cantidadCacheos = 10
	cacheosPositivos = 2
	tiempoRelePositivo = 1
	repRelePositivo = 2
	tiempoReleNegativo = 1
	repReleNegativo = 1

#######REQUEST######
class Requestcfg():
	activado = 0
	seleccionURL = 3
	urlRequest1 = 'http://localhost/jphaccess/trp/alcoholemia.php?tarjeta='
	urlRequest2 = 'http://localhost/jphaccess/trp/validar.php?tarjeta='
	urlRequest3 = 'http://172.16.23.27/workpass/login.hk.php'
	urlRequest4 = ''
	urlRequest5 = ''
	urlError = 'http://localhost/jphaccess/error.php'
	timerActivado = 0
	timeoutRequest = 10

#######LOGS######
class Logscfg():
	pathBackup = '/backupLog/'
	tamañoArchivos = 1024768
	hblCore = 'hblCore.log'
	hblConexiones = 'hblConexiones.log'
	hblWiegand = 'hblWiegand.log'
	hblTcp = 'hblTcp.log'
	hblEntradas = 'hblEntradas.log'
	hblHTTP = 'hblHTTP.log'
	hblReporte = 'hblReporte.log'
	hblhidDevice = 'hblhidDevice.log'
	hbli2c = 'hbli2c.log'
	hblFTP = 'hblFTP.log'
	hblSerial = 'hblSerial.log'
	hblCacheo = 'hblCacheo.log'
	hblKiosco = 'hblKiosco.log'
	hblTareas = 'hblTareas.log'
	hblEsclusa = 'hblEsclusa.log'
	hblMQTT = 'hblMQTT.log'
	hblTimer = 'hblTimer.log'
	hblPuerta = 'hblPuerta.log'
	hblBioStar2_WebSocket = 'hblBioStar2_WebSocket.log'
	hblMail = 'hblMail.log'
	hblPruebaHBL = 'hblPruebaHBL.log'
	rutinaPrueba = 'rutinaPrueba.log'
	SerialDNI = 'SerialDNI.log'

#######LPR######
class Lprcfg():
	serial = 'pepe'

