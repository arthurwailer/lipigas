import win32console
import win32gui
import pyodbc 
import time
import datetime
import lipigas_prueba

# try:
conn = pyodbc.connect('Driver={SQL Server};'
                    'Server=DESKTOP-HPBR3L8\SQLEXPRESS;'
                    'Database=fuel-explorer;'
                    'Trusted_Connection=yes;')
if conn:
    print "Connectado a la BBDD"
    cursor = conn.cursor()
    print "obteniendo tupla"
    cursor.execute("SELECT * FROM [fuel-explorer].dbo.estanques")

    tables = cursor.fetchall()
    for rows in tables:
        id = rows[0]
        estanque_ip = rows[2]
        estanque_estado_id= rows[4]
        estanque_modelo_id= rows[5]
        volumen_medido = rows[10]
        porcentaje_medido = rows[11]
        volumen_acumulado = rows[33]
        hora_acumulada = rows[36]
        contador = rows [34]
        print "estanque id : ", id
        print "estanque ip es: ", estanque_ip
        print "estanque modelo id : ", estanque_modelo_id
        print "volumen medido es : ", volumen_medido
        print "porcentaje medido es : ", porcentaje_medido
        print "volumen_acumulado es : ", volumen_acumulado
        print "hora_acumulada es: ", hora_acumulada, type(hora_acumulada)
        print "contador es ", contador
        
        if estanque_estado_id !=2: # si estanque estado es igual a 2 significa que esta desabilitado
			volumen_porcentaje = lipigas_prueba.volumenCuatro(estanque_ip,6060)# lectura st1 volumen en porcentaje
			altura = lipigas_prueba.alturaCuatro(estanque_ip,6060)# lectura st1 altura
			print "el volumen es ", volumen_porcentaje
			print "la altura es ", altura
			if altura is not None and volumen_porcentaje is not None:
				cursor.execute('''
				select volumen_estanque from [fuel-explorer].dbo.estanque_modelos
				where id = {0}'''.format(estanque_modelo_id))
				volumen_estanque = cursor.fetchone()[0] # volumen del estanque
				volumen_actual = ((volumen_porcentaje*volumen_estanque)/100) # volumen en % de llenado
				insertBBDD=lipigas_prueba.insertBBDD(altura,id,round(volumen_actual,1),altura,round(volumen_actual,1)) # se inserta en la tabla estanques lecturas
				print "el volumen_actual= ", volumen_actual
				print "el volumen del estanque es: ", volumen_estanque
				print "el volumen porcentaje st1 es: ", volumen_porcentaje

				lipigas_prueba.relleno_estanque(volumen_porcentaje,porcentaje_medido,estanque_estado_id,id,estanque_modelo_id) 
				lipigas_prueba.updateBBDDVolumen(id,round(volumen_actual,1),volumen_porcentaje)


			else:
				volumen_porcentaje = lipigas_prueba.volumenTres(estanque_ip,6060)
				altura = lipigas_prueba.alturaTres(estanque_ip,6060)
				if altura is not None and volumen_porcentaje is not None:
					print "el volumen es ", volumen_porcentaje
					print "la altura es ", altura
					cursor.execute('''
					select volumen_estanque from [fuel-explorer].dbo.estanque_modelos
					where id = {0}'''.format(estanque_modelo_id))
					volumen_estanque = cursor.fetchone()[0]
					volumen_actual = ((volumen_porcentaje*volumen_estanque)/100)
					insertBBDD=lipigas_prueba.insertBBDD(altura,id,round(volumen_actual,1),altura,round(volumen_actual,1))
					print "el porcentaje_volumen= ", volumen_actual
					print "el volumen del estanque es: ", volumen_estanque
					print "el volumen es: ", volumen_porcentaje
					estanque_relleno = lipigas_prueba.relleno_estanque(volumen_porcentaje,porcentaje_medido,estanque_estado_id,id)
					updateBBDD = lipigas_prueba.updateBBDDVolumen(id,round(volumen_actual,1),volumen_porcentaje)
					
				else:
					print "nose pudo insertar datos por que son nulos"

else:
    print "Can't Connect to BBDD"
# except Exception as e:

#     print ("Ocurrio un error al tratar de conectar a la BBDD insertos",e)
# finally:
#     conn.commit()
#     cursor.close()
#     conn.close()