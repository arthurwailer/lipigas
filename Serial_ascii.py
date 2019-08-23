from pymodbus.client.sync import ModbusSerialClient as ModbusClient

import logging
logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.DEBUG)

client = ModbusClient(method = "ascii", port="COM10", stopbits = 1, bytesize = 8, parity = 'N', baudrate = 9600)
connection = client.connect()
print (connection)

cont = 0
registro = 40000
while registro<=40012:
	while cont<=8:
		client.inter_char_timeout = 0.05


		request = client.read_holding_registers(registro, 1, unit=3)
		print(request)

		print 'intento de conexion'+' '+ str(cont) 
		cont = cont+1 
		print 'registro num'+' '+ str(registro)+'\n'
		print (request.registers)
	registro+=1
	cont = 0

	

client.close()