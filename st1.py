from pymodbus.client.sync import ModbusTcpClient
import socket


try:
	client = ModbusTcpClient('192.168.100.187',5000)
except:
	print "problemas con el host y port"
client.write_coil(1, True)
result = client.read_coils(1,1)
print(result.bits[8])
client.close()