from pymodbus.client.sync import ModbusTcpClient
import time
import logging
import serial.rs485
import struct 

# Conexion a traves de WZ ST1, la WZ debe estar solo ejecutando este Script para tenga un buen funcionamiento
import logging
logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.DEBUG)



try:
	client = ModbusTcpClient('192.168.101.1',5000,timeout=10)
except:
	print "problemas con el host y port"

tesConnect=client.connect()
print tesConnect

request = client.read_holding_registers(40007, 1,unit=3) 
#response = client.execute(request)

print request
tesConnect=client.connect()
print tesConnect

request = client.read_holding_registers(40007, 1,unit=3) 
#response = client.execute(request)

print request


client.close()