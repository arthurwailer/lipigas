from pymodbus.server.sync import StartTcpServer
from pymodbus.server.sync import StartUdpServer
from pymodbus.server.sync import ModbusTcpServer

from pymodbus.device import ModbusDeviceIdentification
from pymodbus.datastore import ModbusSequentialDataBlock
from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext

from pymodbus.transaction import ModbusAsciiFramer

from pymodbus.interfaces import IModbusSlaveContext

from pymodbus.client.sync import ModbusTcpClient, BaseModbusClient, ModbusSocketFramer, ClientDecoder

from pymodbus.constants import Defaults

import sys
import struct
import socket
from binascii import b2a_hex, a2b_hex

from pymodbus.interfaces import IModbusFramer
from pymodbus.utilities  import checkCRC, computeCRC
from pymodbus.utilities  import checkLRC, computeLRC
import time, datetime
#import psycopg2

from pymodbus.factory import ClientDecoder, ServerDecoder

import logging
logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.DEBUG)

#mport requests

End='\n'
def recv_end(the_socket):
    total_data=[];data=''
    while True:
            data=the_socket.recv(8192)
            print data
            if End in data:
                total_data.append(data[:data.find(End)])
                break
            total_data.append(data)
            if len(total_data)>1:
                #check if end_of_data was split
                last_pair=total_data[-2]+total_data[-1]
                if End in last_pair:
                    total_data[-2]=last_pair[:last_pair.find(End)]
                    total_data.pop()
                    break
    return ''.join(total_data)

def recv_timeout(the_socket,timeout=10):
    the_socket.setblocking(0)
    total_data=[];data='';begin=time.time()
    while 1:
        #if you got some data, then break after wait sec
        if total_data and time.time()-begin>timeout:
            break
        #if you got no data at all, wait a little longer
        elif time.time()-begin>timeout*2:
            break
        try:
            data=the_socket.recv(8192)
            if data:
                total_data.append(data)
                begin=time.time()
            else:
                time.sleep(0.1)
        except:
            pass
    return ''.join(total_data)

def receive(socket, cmd):
    crc = ('%02x' % computeLRC(a2b_hex(cmd))).encode()
    send = (':' + cmd + crc + '\r\n').upper()
    print "Sending data: " + send
    socket.send(send)

    print "Receiving data..."
    message = recv_timeout(socket)

    if (len(message) > 0):

        print 'Received: ' + message

        hex_val = a2b_hex(message[7:len(message)-3])
        return int(hex_val.encode('hex'), 16)

    return None

def insertDb(date, level, heigth):
    conn = psycopg2.connect("host='aikologic.cc1kwqrigrxi.us-east-1.rds.amazonaws.com' dbname='abastible' user='aikologic' password='aiko2011'")
    cur = conn.cursor()
    cur.execute("insert into data (equipment_id, date, level, height) values (1, %s, %s, %s)", (date, level, heigth))
    conn.commit()
    cur.close()
    conn.close()

def sendRest(level, height):
    url = "http://lipigas.aikologic.com/Api/Value?equipmentID=1&level=" + str(level) + "&height=" + str(height) + "&key=AIKOLOGIC"
    print url
    response = requests.get(url)

while True:
    tcpSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:

        #tcpSocket.connect(("10.89.64.51", 5050))
        tcpSocket.connect(("lipigas-cmpc-talca.enlazza.net", 4605))
        volume = receive(tcpSocket, '0303000B0001')
        height = receive(tcpSocket, '030300070001')
        #status = receive(tcpSocket, '030300020001')

        if (volume is not None and height is not None and volume > 0):

            print 'Volume: ' + str(volume) + ' - Height: ' + str(height) #+ '-Status: '+ str(status)

            with open("log.txt", "a") as myfile:
                myfile.write(datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S") + ',' + str(volume) + ',' + str(height) + '\n')

            #insertDb(datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"), volume/10.0, height)
            sendRest(volume/1.0 if volume < 100 else volume/10.0, height)
            print 'Volumen: ' + str(volume)
        else:
            print 'Volume or height is None or zero'
            with open("log.txt", "a") as myfile:
                myfile.write(datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S") + ' - Error: ' + str(volume) + ',' + str(height) + '\n')

    except:
        print "Unexpected error:", sys.exc_info()[0]
        try:
            with open("log.txt", "a") as myfile:
                myfile.write(datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S") + ' - Exception: ' + str(sys.exc_info()[0]) + '\n')
        except:
            print "Error logging error"

    finally:
        tcpSocket.close()

    time.sleep(60)
