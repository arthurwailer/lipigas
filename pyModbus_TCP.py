from pymodbus.client.sync import ModbusSerialClient as ModbusClient

import logging
logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.DEBUG)

client = ModbusClient(method = "ascii", port="COM10", stopbits = 1, bytesize = 8, parity = 'N', baudrate = 9600)
connection = client.connect()
print (connection)

request = client.read_holding_registers(40007, 1, unit=3)
print(request)
print (request.registers)


client.close()