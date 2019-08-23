from pymodbus.client.sync import ModbusTcpClient
import time
import logging
import serial.rs485
import struct 

# Conexion a traves de WZ ST1, la WZ debe estar solo ejecutando este Script para tenga un buen funcionamiento



try:
	client = ModbusTcpClient('192.168.101.1',5000,timeout=10)
except:
	print "problemas con el host y port"

tesConnect=client.connect()
print tesConnect

# logging.basicConfig()
# log = logging.getLogger()
# log.setLevel(logging.DEBUG)
# logging.warning("Cuidado!!!")

cont = 0
registro = 40000
while registro<=40012:
	while cont<=8:
		client.inter_char_timeout = 0.05


		request = client.read_holding_registers(registro, 1, unit=cont)
		print(request)

		print 'intento de conexion'+' '+ str(cont) 
		cont = cont+1 
		print 'registro num'+' '+ str(registro)+'\n'
	registro+=1
	cont = 0
	

		







#coil=client.read_holding_registers(40002,0x11)# address, count, 
#slave address
#print(coil)

client.close()







# Si conecta entrga un True si no False.
#result = client.read_coils(1,1)

# logging.basicConfig()
# log = logging.getLogger()
# log.setLevel(logging.DEBUG)

# log.debug("Reading Coils\n")
# print('First Try: ')
# res = client.read_holding_registers(40022, 4011, unit=21)
# print('isError = {}'.format(res.isError()))

# print('Second Try: ')


# res = client.read_holding_registers(4002, 40011, unit=21)
# print (res.registers[4002])
# print (res.registers[4007])
# print (res.registers[40010])
# print (res.registers[40011])
# rc= read_coils(0,1)
# print rc.bits[0]
# print('isError = {}'.format(res.isError()))





