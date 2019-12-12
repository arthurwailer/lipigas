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
from datetime import datetime

from pymodbus.factory import ClientDecoder, ServerDecoder

import logging
logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.DEBUG)
import pyodbc 
class Basededatos():


    def updateBBDDVolumen(self,numero,volumen,porcentaje_volumen):

        try:
            conn = pyodbc.connect('Driver={SQL Server};'
                                'Server=DESKTOP-HPBR3L8\SQLEXPRESS;'
                                'Database=fuel-explorer;'
                                'Trusted_Connection=yes;')
            if conn:
                
                print "Connectado a la BBDD"
                cursor = conn.cursor()
                print "actualizando fecha en la tabla estanques"
                #cursor.execute('SELECT * FROM [fuel-explorer].dbo.estanques')
                cursor.execute('''UPDATE [fuel-explorer].dbo.estanques
                    set volumen_medido = {1},
                    porcentaje_medido = {2},
                    fecha_hora_lectura = CURRENT_TIMESTAMP,
                    updated_at = CURRENT_TIMESTAMP
                    where id = {0}'''.format(numero,volumen, porcentaje_volumen))
               
                
                print "datos actualizados volumen bddd"
            else:
                print "nose pudo actualizar la BBDD"
        except Exception as e:

            print ("Ocurrio un error al tratar de conectar a la BBDD update volumen",e)
        finally:
            conn.commit()
            cursor.close()
            conn.close()

    def updateBBDD(self,numero,volumen_acumulado,contador,tiempo_llenado):
        
        # try:
        conn = pyodbc.connect('Driver={SQL Server};'
                            'Server=DESKTOP-HPBR3L8\SQLEXPRESS;'
                            'Database=fuel-explorer;'
                            'Trusted_Connection=yes;')
        if conn:
            
            print "Connectado a la BBDD"
            cursor = conn.cursor()
            print "actualizando fecha en la tabla estanques"
            #cursor.execute('SELECT * FROM [fuel-explorer].dbo.estanques')
            cursor.execute('''UPDATE [fuel-explorer].dbo.estanques
            set volumen_acumulado = {1},
            contador = {2},
            hora_acumulada = '{3}'
            where id = {0}'''.format(numero,volumen_acumulado,contador,tiempo_llenado))     
            print "datos actualizados"
            conn.commit()
            cursor.close()
            conn.close()

        else:
            print "nose pudo actualizar la BBDD"
        # except Exception as e:
        #     print ("Ocurrio un error al tratar de conectar a la BBDD update",e)
        # finally:
        #     conn.commit()
        #     cursor.close()
        #     conn.close()



    def insertBBDD(self,altura_raw,estanque_id,volumen_normalizado,altura_normalizada,volumen_raw):

        try:
            conn = pyodbc.connect('Driver={SQL Server};'
                                'Server=DESKTOP-HPBR3L8\SQLEXPRESS;'
                                'Database=fuel-explorer;'
                                'Trusted_Connection=yes;')
            if conn:
                print "Connectado a la BBDD"
                cursor = conn.cursor()
                consulta ='''INSERT INTO [fuel-explorer].dbo.estanque_lecturas(
                    estanque_id,
                    altura_raw,
                    altura_normalizada,
                    volumen_normalizado,
                    fecha_hora_lectura_sensor,
                    fecha_hora_recepcion,
                    fecha_hora_procesado,
                    updated_at,
                    created_at,
                    volumen_raw)
                    VALUES (?,?,?,?,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,?);'''
                cursor.execute(consulta, (estanque_id, altura_raw,altura_normalizada,volumen_normalizado,volumen_raw))
                

                print "Datos insertos en la BBDD"
            else:
                print "Can't Connect to BBDD"
        except Exception as e:

            print ("Ocurrio un error al tratar de conectar a la BBDD insertos",e)
        finally:
            conn.commit()
            cursor.close()
            conn.close()


    #_______ actualizar tabla con el ultimo dato adquirido___________

    # UPDATE [fuel-explorer].db_owner.estanques
    # SET [fuel-explorer].db_owner.estanques.fecha_hora_lectura= [fuel-explorer].db_owner.estanque_lecturas.fecha_hora_lectura_sensor
    # FROM [fuel-explorer].db_owner.estanques, [fuel-explorer].db_owner.estanque_lecturas
    # WHERE [fuel-explorer].db_owner.estanques.id = [fuel-explorer].db_owner.estanque_lecturas.estanque_id
    def volumen_actual_medido(self,volumen_porcentaje,estanque_modelo_id):
        # la formula para volumen medido es: volumen_actual = ((volumen_porcentaje*volumen_estanque)/100)*10
        try:
            conn = pyodbc.connect('Driver={SQL Server};'
                                'Server=DESKTOP-HPBR3L8\SQLEXPRESS;'
                                'Database=fuel-explorer;'
                                'Trusted_Connection=yes;')
            if conn:
                print "Connectado a la BBDD"
                cursor = conn.cursor()
                print "obteniendo tupla"
                cursor.execute("SELECT * FROM [fuel-explorer].dbo.estanques")
             
                if volumen_porcentaje is not None:

                    cursor.execute('''
                    select volumen_estanque from [fuel-explorer].dbo.estanque_modelos
                    where id = {0}'''.format(estanque_modelo_id))
                    volumen_estanque = cursor.fetchone()[0] # volumen total del estanque
                    volumen_actual = ((volumen_porcentaje*volumen_estanque)/100) # volumen de combustible en m3
                    return volumen_actual
                else:
                    print "la altura es None"
              
                        
        except Exception as e:
            print e

    ## variacion porcentual entre dos mediciones
    def variacion_porcentual_medido(self,porcentaje2,porcentaje1):

        variacion_porcentual = porcentaje2-porcentaje1
        return variacion_porcentual


    # Esta funcion recibe como entrada un volumen en porcentaje de la st1, y lo compara con el volumen anterior
    # que se encuentra registrado en la base de datos en la tabla dbo.estanques
    # calcula la variacion porcentual
    # si la variacion porcentual es mayor a 1.5 ese lo acumula en la columna volumen_acumulado en la tabla dbo.estanques
    # la tabla estanques tiene una columna llamada acumulador si el acumulador es = 0 este guarda el ultimo valor obtenido en la tabla
    # y lo guarda en la tabla dbo.estanque_rellenos eso se hace por si existe una variacion menor a 1.5 durante la carga de combustible
    # 


    def tiempo_llenado(self,estanque_id):
        
        conn = pyodbc.connect('Driver={SQL Server};'
                        'Server=DESKTOP-HPBR3L8\SQLEXPRESS;'
                        'Database=fuel-explorer;'
                        'Trusted_Connection=yes;')
        if conn:
            print "Connectado a la BBDD"
            cursor = conn.cursor()
            cursor.execute('''
            select fecha_hora_lectura from [fuel-explorer].dbo.estanques
            where id = {0}'''.format(estanque_id))
            fecha_hora_lectura = cursor.fetchone()[0]
            print "fecha_hora_lectura: ", fecha_hora_lectura
            now = datetime.now()
            print "now: ", now
            ahora = now - fecha_hora_lectura # delta de tiempo 
            #ahora2 = ahora.time()
            print " ahora: ", type(ahora), ahora
            cursor.execute('''
            select hora_acumulada from [fuel-explorer].dbo.estanques
            where id = {0}'''.format(estanque_id)) 
            hora_acumulada = cursor.fetchone()[0]
            print "la hora adquirida en la base de datos es: ", type(hora_acumulada), hora_acumulada
            hora_acumulada = hora_acumulada + ahora
            print type(hora_acumulada), hora_acumulada

            hora_acumulada2 = hora_acumulada.strftime("%H:%M:%S")
            print "la hora acumulada es : ", type(hora_acumulada2), hora_acumulada2
            hora_acumulada3 = datetime.strptime(hora_acumulada2,"%H:%M:%S") 
            print type(hora_acumulada3), hora_acumulada3

            # print type(ahora), ahora
            # ahora2 = datetime.strptime(ahora,"%H:%M:%S")
            # print type(ahora2), ahora2
            # ahora3 = ahora2.time()
           


            return hora_acumulada3 # retorna el tiempo llenado en formato datetime
        else:
            print "no se pudo conectar"

    def suma(self,a,b):
        c= a + b
        return c

    def relleno_estanque(self,porcentaje2,porcentaje1,estanque_estado_id,estanque_id,estanque_modelo_id,variacion_porcentual_basedatos):
        # el valor del porcentaje1 es igual ultimo valor guardado en la tabla estanques
       
        
        conn = pyodbc.connect('Driver={SQL Server};'
                        'Server=DESKTOP-HPBR3L8\SQLEXPRESS;'
                        'Database=fuel-explorer;'
                        'Trusted_Connection=yes;')
        if conn:
            print "Connectado a la BBDD"
            cursor = conn.cursor()
            print "obteniendo tupla"
            tiempo_llenado_estanque = self.tiempo_llenado(estanque_id)# el tiempo que se demora en hacer una carga del estanque
            print "el tiempo de llenado es", tiempo_llenado_estanque, type(tiempo_llenado_estanque)
            if estanque_estado_id != 2:
                if porcentaje2 is not None:
                    print "porcentaje1 bbdd es : ", porcentaje1,"porcentaje2 actual es : ", porcentaje2
                    volumen_medido = self.volumen_actual_medido(porcentaje2,estanque_modelo_id)#volumen actual medido m3
                    variacion_porcentual = self.variacion_porcentual_medido(porcentaje2,porcentaje1) # variacion de % 
                    print "la variacion_porcentual es: ", variacion_porcentual
                    cursor.execute('''
                    select volumen_medido from [fuel-explorer].dbo.estanques
                    where id = {0}'''.format(estanque_id))
                    volumen_anterior = cursor.fetchone()[0] #volumen medido en la base de datos en la tabla estanques
                    cursor.execute('''
                    select volumen_acumulado from [fuel-explorer].dbo.estanques
                    where id = {0}'''.format(estanque_id)) 
                    volumen_acumulado = cursor.fetchone()[0] # volumen acumulado en la base de datos en la tabla estanques
                    cursor.execute('''
                    select hora_acumulada from [fuel-explorer].dbo.estanques
                    where id = {0}'''.format(estanque_id)) # pendiente

                    cursor.execute('''
                    select fecha_hora_lectura from [fuel-explorer].dbo.estanques
                    where id = {0}'''.format(estanque_id))
                    fecha_hora_lectura = cursor.fetchone()[0]
                    fecha_hora_lectura2 = fecha_hora_lectura.strftime("%Y-%m-%d %H:%M:%S")
                    print "fecha_hora_lectura : ", type(fecha_hora_lectura2), fecha_hora_lectura2
                    fecha_hora_lectura3 = datetime.strptime(fecha_hora_lectura2,"%Y-%m-%d %H:%M:%S") 
                    print "fecha_hora_lectura : ", type(fecha_hora_lectura3),fecha_hora_lectura3


                    # hora_acumulada = cursor.fetchone()[0] #hora acumulada en la base de datos en la tabla estanques
                    # print "hora acumulada en bbdd: ", type(hora_acumulada),hora_acumulada
                    # print "el tipo de dato es: ", type(hora_acumulada), hora_acumulada
                    # hora_acumulada = hora_acumulada + tiempo_llenado_estanque
                    # print "hora acumulada mas tiempo de llenado: ", hora_acumulada
                    # tranforma datetime a string con formato "%Y-%m-%d %H:%M:%S"

                
                    print "hora acumulada convertida de str a datetime: ", tiempo_llenado_estanque
                    print "volumen_acumulado: ", volumen_acumulado , type(volumen_acumulado)
                    if variacion_porcentual > variacion_porcentual_basedatos:
                        cursor.execute('''
                        select contador_espera from [fuel-explorer].dbo.estanques
                        where id = {0}'''.format(estanque_id))
                        contador_espera = cursor.fetchone()[0] #contador espera  = 5 en la base de datos
                        print "contador_espera: ", type(contador_espera), contador_espera

                        print "volumen medido de la st1 es:  :", volumen_medido
                        print "volumen acumulado es: ", volumen_acumulado
                        volumen_acumulado = volumen_acumulado + ( volumen_medido - volumen_anterior)
                        print "volumen_acumulado", volumen_acumulado
                        print "tiempo llenado estanque es; ", type(tiempo_llenado_estanque), tiempo_llenado_estanque
                        cursor.execute('''
                        select contador_primer_volumen from [fuel-explorer].dbo.estanques
                        where id = {0}'''.format(estanque_id))
                        contador_primer_volumen = cursor.fetchone()[0]
                        print "contador_primer_volumen: ", contador_primer_volumen
                    
                        if contador_primer_volumen == 1:
                            cursor.execute('''UPDATE [fuel-explorer].dbo.estanques
                            set volumen_inicial = {1}
                            where id = {0}'''.format(estanque_id,volumen_anterior))  
                            

                            contador_primer_volumen = contador_primer_volumen + 1
                            print "contador_primer_volumen: ", contador_primer_volumen
                            cursor.execute('''UPDATE [fuel-explorer].dbo.estanques
                            set contador_primer_volumen = {1}
                            where id = {0}'''.format(estanque_id,contador_primer_volumen))
                            print "volumen_acumulado: ", type(volumen_acumulado), volumen_acumulado
                            print "estanque_id: ", type(estanque_id), estanque_id
                            print "contador_espera: ", type(contador_espera), contador_espera
                            print "tiempo_llenado_estanque: ", type(tiempo_llenado_estanque), tiempo_llenado_estanque
                            print "fecha_hora_lectura: ", type(fecha_hora_lectura3), fecha_hora_lectura3

                            cursor = conn.cursor()
                            
                            print "actualizando fecha en la tabla estanques"
                            #cursor.execute('SELECT * FROM [fuel-explorer].dbo.estanques')
                            cursor.execute('''UPDATE [fuel-explorer].dbo.estanques
                            set volumen_acumulado = {1},
                            contador = {2},
                            hora_acumulada = '{3}',
                            fecha_inicial = '{4}'
                            where id = {0}'''.format(estanque_id,volumen_acumulado,contador_espera, tiempo_llenado_estanque,fecha_hora_lectura3))     
                            print "datos actualizados"
                            print "actualizado volumen_inicial"
                            conn.commit()
                            cursor.close()
                            conn.close()
                        else:   
                            update=self.updateBBDD(estanque_id,volumen_acumulado,contador_espera,tiempo_llenado_estanque)
                            print "contador contador_primer_volumenes diferente  de 1"

                            # conn.commit()
                            # cursor.close()
                            # conn.close()
                                   
                            print "dato guardado volumen_acumulado"
                    else:
                        cursor.execute('''
                        select contador from [fuel-explorer].dbo.estanques
                        where id = {0}'''.format(estanque_id))
                        contador = cursor.fetchone()[0] # contador de la base de datos
                        contador = contador - 1 
                        cursor.execute('''UPDATE [fuel-explorer].dbo.estanques
                        SET contador={1}
                        where id = {0}'''.format(estanque_id,contador))
                        conn.commit()
                        if contador == 0:
                            if volumen_acumulado > 0:
                                cursor.execute('''
                                select fecha_inicial from [fuel-explorer].dbo.estanques
                                where id = {0}'''.format(estanque_id))
                                fecha_inicial = cursor.fetchone()[0]

                                cursor.execute('''
                                select volumen_inicial from [fuel-explorer].dbo.estanques
                                where id = {0}'''.format(estanque_id))
                                volumen_inicial = cursor.fetchone()[0]
                                print "en esta linea se debe guardar el ultimo valor acumulado en la tabla estanque_rellenos"
                                consulta ='''INSERT INTO [fuel-explorer].dbo.estanque_rellenos(
                                    volumen_cargado,
                                    tiempo_de_relleno,
                                    fecha_hora_carga,
                                    estanque_id,
                                    created_at,
                                    updated_at,
                                    volumen_inicial)   
                                    VALUES (?,?,?,?,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,?);'''
                                cursor.execute(consulta,(volumen_acumulado,tiempo_llenado_estanque,fecha_inicial,estanque_id,volumen_inicial))
                            

                                print "insert en la tabla rellenos con el ultimo valor acumulado"
                                # actualizando tablas
                                print "en esta linea se actualiza el valor volumen_acumulado a 0 en la tabla estanques"
                                cursor.execute('''UPDATE [fuel-explorer].dbo.estanques
                                SET volumen_acumulado=0,
                                hora_acumulada = '00:00:00',
                                volumen_inicial = 0, 
                                contador_primer_volumen = 1,
                                fecha_inicial = '00:00:00'
                                where id = {0}'''.format(estanque_id))
                                conn.commit()
                                cursor.close()
                                conn.close()
                                print "el volumen acumulado volvio a 0 en tabla estanques"
                            else:
                                print "la variacion_porcentual es menor a 1.5 y volumen acumulado es 0 "
                        else:
                            print "contador es diferente de 0"
            else:
                print "el estanque es 2 por lo tanto esta desabilitado"
        else:
            print "nose pudo conectar a la base de datos."




class fuelexplorer(Basededatos):

    def __init__(self,TCP_IP='192.168.1.1',TCP_PORT=5000):

        self.TCP_IP=TCP_IP
        self.TCP_PORT=TCP_PORT

    def recv_end(self,the_socket):
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

    def recv_timeout(self,the_socket,timeout=10):
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


    def volumenTres(self,ip,port):
        #while True:

        tcpSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            tcpSocket.connect((ip, port))
            print "conectado"
            print "consiguiendo volumen"
            volume = self.receiveTres(tcpSocket, '0303000B0001')
            #height = receive(tcpSocket, '030300070001')
            #status = receive(tcpSocket, '030300020000' )
            print "volumen obtenido"
            #print str(status)
            try:
                if volume is not None and volume>0 and volume < 1000:
                    return volume/10
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



    def volumenCuatro(self,ip,port):
        #while True:

        tcpSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            tcpSocket.connect((ip, port))
            print "conectado"
            print "consiguiendo volumen"
            volume = self.receiveCuatro(tcpSocket, '0303000B0001')
            #height = receive(tcpSocket, '030300070001')
            #status = receive(tcpSocket, '030300020000' )
            print "volumen obtenido"
            #print str(status)
            try:
                if volume is not None and volume>0 and volume < 1000:
                    return volume/10
                    #print str(height/10.0), "[cm]"
                else:
                    print "volume is None or Zero"
                    #print "height is None or Zero"
            except:
                print "Error, no Succes"

                # En las siguientes lineas escribir en la base de datos los datos obtenidos
        except Exception as e:
            print "Can't connect...", e
        finally: #finally se ejecutar sin importar si el bloque try genera un error o no.
            tcpSocket.close()

        time.sleep(5)



    def alturaTres(self,ip,port):
        #while True:

        tcpSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            tcpSocket.connect((ip, port))
            print "conectado al socket"
            print "consiguiendo altura"
            #volume = receive(tcpSocket, '0303000B0001')
            height = self.receiveTres(tcpSocket, '030300070001')
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


    def alturaCuatro(self,ip,port):
        #while True:

        tcpSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            tcpSocket.connect((ip, port))
            print "conectado al socket"
            print "consiguiendo altura"
            #volume = receive(tcpSocket, '0303000B0001')
            height = self.receiveCuatro(tcpSocket, '030300070001')
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
    def receiveTres(self,socket, cmd):
        crc = ('%02x' % computeLRC(a2b_hex(cmd))).encode()
        send = (':' + cmd + crc + '\r\n').upper()
        print "Sending data: " + send
        socket.send(send)

        print "Receiving data..."
        message = self.recv_timeout(socket)

        if (len(message) > 0):

            print 'Received: ' + message 

            hex_val = a2b_hex(message[7:len(message)-3])
            return int(hex_val.encode('hex'), 16)

        return None

    def receiveCuatro(self,socket, cmd):
        crc = ('%02x' % computeLRC(a2b_hex(cmd))).encode()
        send = (':' + cmd + crc + '\r\n').upper()
        print "Sending data: " + send
        socket.send(send)

        print "Receiving data..."
        message = self.recv_timeout(socket)

        if (len(message) > 0):

            print 'Received: ' + message 

            hex_val = a2b_hex(message[7:len(message)-4])
            return int(hex_val.encode('hex'), 16)

        return None




#tiempo_llenado(10079)
#update=updateBBDD(10079,1000,5,'1900-01-01 00:01:00.000')