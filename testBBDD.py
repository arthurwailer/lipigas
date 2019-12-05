
import datetime
import time
import pyodbc
from datetime import datetime
from time import gmtime, strftime



hola = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
hola2= datetime.strptime(hola,"%Y-%m-%d %H:%M:%S")
print type(hola2), hola




# datetime object containing current date and time
#now = datetime.now().strptime("%Y-%m-%d %H:%M:%S")
#print type(now),now

def tiempo_llenado(estanque_id):
    
    conn = pyodbc.connect('Driver={SQL Server};'
                    'Server=DESKTOP-HPBR3L8\SQLEXPRESS;'
                    'Database=fuel-explorer;'
                    'Trusted_Connection=yes;')
    if conn:
		cursor = conn.cursor()
		cursor.execute('''
		select fecha_hora_lectura from [fuel-explorer].dbo.estanques
		where id = {0}'''.format(estanque_id))
		fecha_hora_lectura = cursor.fetchone()[0]
		fecha_hora_lectura2 = fecha_hora_lectura.strftime("%Y-%m-%d %H:%M:%S")
		print "fecha_hora_lectura1 : ", type(fecha_hora_lectura2), fecha_hora_lectura2
		fecha_hora_lectura3 = datetime.strptime(fecha_hora_lectura2,"%Y-%m-%d %H:%M:%S") 
		print "fecha_hora_lectura2 : ", type(fecha_hora_lectura3),fecha_hora_lectura3
		# print "Connectado a la BBDD"
		# cursor = conn.cursor()
		# cursor.execute('''
		# select fecha_hora_lectura from [fuel-explorer].dbo.estanques
		# where id = {0}'''.format(estanque_id))
		# fecha_hora_lectura = cursor.fetchone()[0]
		# now = datetime.now()
		# print type(now),now
		# print type(fecha_hora_lectura), fecha_hora_lectura

		# ahora = now - fecha_hora_lectura
		# print type(ahora), ahora
		# # ahora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
		# # ahora2 = datetime.strptime(ahora,"%Y-%m-%d %H:%M:%S")
		# cursor.execute('''
		# select hora_acumulada from [fuel-explorer].dbo.estanques
		# where id = {0}'''.format(estanque_id)) 
		# hora_acumulada = cursor.fetchone()[0]
		# print type(hora_acumulada), hora_acumulada
		# hora_acumulada = hora_acumulada + ahora
		# print type(hora_acumulada), hora_acumulada
		# hora_acumulada2 = hora_acumulada.strftime("%Y-%m-%d %H:%M:%S")
		# print type(hora_acumulada2), hora_acumulada2
		# fecha_hora_lectura3 = datetime.strptime(hora_acumulada2,"%Y-%m-%d %H:%M:%S") 
		# print "fecha_hora_lectura : ", type(fecha_hora_lectura3),fecha_hora_lectura3

		
		#return type(hora_acumulada2), "la hora acumulada es",hora_acumulada2

    else:
        print "no se pudo conectar"
llenado = tiempo_llenado(10079)




#print llenado , type(llenado)

 	