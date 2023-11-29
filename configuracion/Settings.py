#ADVERTENCIA:
#ESTE ARCHIVO SE GENERA DINAMICAMENTE
#NO MODIFICAR

#######HBL######
class Hblcfg():
	idHBL = '3'

#######WIEGAND######
class Wiegandcfg():
	class W1cfg():
		activado = 1
		modo = 'IN'
		esperaSenial = 0
		bitsSalida = 0
		delayPulso = 5e-05
		delayIntervalo = 0.002
		primerBit = 1

	class W2cfg():
		activado = 1
		modo = 'OUT'
		esperaSenial = 0
		bitsSalida = 0
		delayPulso = 0.0005
		delayIntervalo = 0.001
		primerBit = 9


#######SERIAL######
class Serialcfg():
	class Com1cfg():
		activado = 1
		port = '/dev/serial0'
		baudrate = 9600
		bytesize = 8
		parity = 'N'
		stopbits = 1

	class Com2cfg():
		activado = 0
		port = '/dev/ttyAMA2'
		baudrate = 9600
		bytesize = 8
		parity = 'N'
		stopbits = 1


#######DISPLAY######
class Displaycfg():
	activado = 0
	line0 = 'OCUPACION'
	line1 = '0'
	line2 = ''
	line3 = 'PWC  Acceso Castelli'

