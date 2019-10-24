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
import pyodbc 

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

def receiveCuatro(socket, cmd):
    crc = ('%02x' % computeLRC(a2b_hex(cmd))).encode()
    send = (':' + cmd + crc + '\r\n').upper()
    print "Sending data: " + send
    socket.send(send)

    print "Receiving data..."
    message = recv_timeout(socket)

    if (len(message) > 0):

        print 'Received: ' + message 

        hex_val = a2b_hex(message[7:len(message)-4])
        return int(hex_val.encode('hex'), 16)

    return None

def volumen(ip,port):
    #while True:

    tcpSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        tcpSocket.connect((ip, port))
        print "conectado"
        print "consiguiendo volumen"
        volume = receive(tcpSocket, '0303000B0001')
        #height = receive(tcpSocket, '030300070001')
        #status = receive(tcpSocket, '030300020000' )
        print "volumen obtenido"
        #print str(status)
        try:
            if volume is not None and volume>0 and volume < 1000:
                return volume/10.0
                #print str(height/10.0), "[cm]"
            else:
                print "volume is None or Zero"
                #print "height is None or Zero"
        except:
            print "Error, no Succes"

            # En las siguientes lineas escribir en la base de datos los datos obtenidos
    except:
        print "Can't connect..."
    finally: #finally se ejecutar sin importar si el bloque try genera un error o no.
        tcpSocket.close()

    time.sleep(5)

time.sleep(5)


def alturaCuatro(ip,port):
    #while True:

    tcpSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        tcpSocket.connect((ip, port))
        print "conectado al socket"
        print "consiguiendo altura"
        #volume = receive(tcpSocket, '0303000B0001')
        height = receiveCuatro(tcpSocket, '030300070001')
        #status = receive(tcpSocket, '030300020000' )
        print "altura obtenida"
        print height
        #print str(status)
        try:
            if height>=0 and height<2000 and height is not None:
                #print str(volume/10.0), "%"
                return height
            else:
                print "altura is None or Zero"
                #print "height is None or Zero"
        except:
            print "Error, no Succes"

            # En las siguientes lineas escribir en la base de datos los datos obtenidos
    except:
        print "Can't connect..."
    finally: #finally se ejecutar sin importar si el bloque try genera un error o no.
        tcpSocket.close()

    time.sleep(5)


def insertBBDD(altura_raw,estanque_id):
    try:
        conn = pyodbc.connect('Driver={SQL Server};'
                            'Server=DESKTOP-HPBR3L8\SQLEXPRESS;'
                            'Database=fuel-explorer;'
                            'Trusted_Connection=yes;')
        if conn:
            print "Connectado a la BBDD"
            cursor = conn.cursor()
            print "insertando datos a la base de datos de lipigas"
            consulta ='''INSERT INTO [fuel-explorer].db_owner.estanque_lecturas(
                estanque_id,
                altura_raw,
                fecha_hora_lectura_sensor,
                fecha_hora_recepcion,
                created_at)
                VALUES (?,?,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP);'''
            cursor.execute(consulta, (estanque_id, altura_raw))
            print "Datos insertos en la BBDD"
        else:
            print "Can't Connect to BBDD"
    except Exception as e:

        print ("Ocurrio un error al tratar de conectar a la BBDD",e)
    finally:
        conn.commit()
        cursor.close()
        conn.close()

def alturaTres(ip,port):
    #while True:

    tcpSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        tcpSocket.connect((ip, port))
        print "conectado al socket"
        print "consiguiendo altura"
        #volume = receive(tcpSocket, '0303000B0001')
        height = receiveTres(tcpSocket, '030300070001')
        #status = receive(tcpSocket, '030300020000' )
        print "altura obtenida"
        print height
        #print str(status)
        try:
            if height>0 and height<2000 and height is not None:
                #print str(volume/10.0), "%"
                return height
            else:
                print "altura is None or Zero"
                #print "height is None or Zero"
        except:
            print "Error, no Succes"

            # En las siguientes lineas escribir en la base de datos los datos obtenidos
    except:
        print "Can't connect..."
    finally: #finally se ejecutar sin importar si el bloque try genera un error o no.
        tcpSocket.close()

    time.sleep(5)

def receiveTres(socket, cmd):
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


#_______ actualizar tabla con el ultimo dato adquirido___________

# UPDATE [fuel-explorer].db_owner.estanques
# SET [fuel-explorer].db_owner.estanques.fecha_hora_lectura= [fuel-explorer].db_owner.estanque_lecturas.fecha_hora_lectura_sensor
# FROM [fuel-explorer].db_owner.estanques, [fuel-explorer].db_owner.estanque_lecturas
# WHERE [fuel-explorer].db_owner.estanques.id = [fuel-explorer].db_owner.estanque_lecturas.estanque_id

