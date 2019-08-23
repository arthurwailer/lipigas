import minimalmodbus

import serial

instrument = minimalmodbus.Instrument('COM9', 1) #conexion a USB COM9

instrument.serial.parity = serial.PARITY_EVEN
instrument.serial.timeout = 0.2
instrument.serial.baudrate = 9600
instrument.mode = minimalmodbus.MODE_RTU
print instrument
temperature = instrument.read_register(40002, 1)  # Registernumber, number of decimals
print(temperature)
try:
    print(instrument.read_register(40007))
except IOError:
    print("Failed to read from instrument")