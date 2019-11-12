import pyodbc 
import time
import datetime
import lipigas_prueba




# ingresar ip y id desde la BBDD 
	### guarda en una variable la altura entregandole como variable ip y puerto

alturaEstanque1 = lipigas_prueba.alturaCuatro('192.168.121.1',6060)
volumenEstanque1 = lipigas_prueba.volumenCuatro('192.168.121.1',6060)
print volumenEstanque1

alturaEstanque2 = lipigas_prueba.alturaTres('192.168.122.1',6060)
volumenEstanque2 = lipigas_prueba.volumenTres('192.168.122.1',6060)
print volumenEstanque2

alturaEstanque3 = lipigas_prueba.alturaCuatro('192.168.123.1',6060)
volumenEstanque3 = lipigas_prueba.volumenCuatro('192.168.123.1',6060)
print volumenEstanque3

#insertBBDD recibe 2 variable , altura y id del estanque y los inserta en la BBDD SQL SERVER.


# if alturaEstanque1>0 and alturaEstanque1<2000 and alturaEstanque1 is not None:
# 	insertBBDD=lipigas_prueba.insertBBDD(alturaEstanque1,1)
# 	updateBBDD= lipigas_prueba.updateBBDD(1)
# else:
# 	print "alturaEstanque1 is none o null o no se pude insertar en la BBDD"
# 	#time.sleep(2)
# if alturaEstanque1>0 and alturaEstanque2<2000 and alturaEstanque1 is not None:
# 	insertBBDD=lipigas_prueba.insertBBDD(alturaEstanque2,2)
# 	updateBBDD= lipigas_prueba.updateBBDD(2)
# else:
# 	print "alturaEstanque2 is none o null o no se pude insertar en la BBDD"
# 	#time.sleep(2)
# if alturaEstanque1>0 and alturaEstanque2<2000 and alturaEstanque1 is not None:
# 	insertBBDD=lipigas_prueba.insertBBDD(alturaEstanque3,3)
# 	updateBBDD= lipigas_prueba.updateBBDD(3)
# else:
# 	print "alturaEstanque2 is none o null o no se pude insertar en la BBDD"



# 		conn = pyodbc.connect('Driver={SQL Server};'
# 	                      	'Server=DESKTOP-SI75KO8\SQLEXPRESS;'
# 	                      	'Database=ESTANQUES;'
# 	                      	'Trusted_Connection=yes;')
# 		if conn:
# 			print "Connect Sucess.."
# 			cursor = conn.cursor()
# 	#hora = (CURRENT_TIMESTAMP) 
# 			print "insertando datos a la base de datos de lipigas"
# 			consulta = "INSERT INTO ESTANQUES.dbo.ESTANQUES(HORA,ALTURA,VOLUMEN) VALUES (CURRENT_TIMESTAMP,?,?);"
# 			cursor.execute(consulta, (altura,volumen))
# 			print "Datos insertos en la BBDD"
# 		else:
# 			print "Can't Connect to BBDD"
# 	except:
# 		print "Can't Connect"

	


# #cursor.execute('SELECT * FROM master.dbo.ESTANQUES')
# #cursor.execute("INSERT INTO master.dbo.ESTANQUES VALUES (,67.7,67)") # el primer campo es un cont y no se evalua
# 	conn.commit()
# 	cursor.close()
# 	conn.close()
# 	time.sleep(5)
