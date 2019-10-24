import pyodbc 
import time
import datetime
import lipigas_prueba

while True:

	### guarda en una variable la altura entregandole como variable ip y puerto

	alturaEstanque1 = lipigas_prueba.alturaCuatro('192.168.121.1',6060)
	alturaEstanque2 = lipigas_prueba.alturaTres('192.168.122.1',6060)
	alturaEstanque3 = lipigas_prueba.alturaCuatro('192.168.123.1',6060)

	#insertBBDD recibe 2 variable , altura y id del estanque y los inserta en la BBDD SQL SERVER.

	insertBBDD=lipigas_prueba.insertBBDD(alturaEstanque1,1)
	updateBBDD= lipigas_prueba.updateBBDD(1)
	#time.sleep(2)
	insertBBDD=lipigas_prueba.insertBBDD(alturaEstanque2,2)
	updateBBDD= lipigas_prueba.updateBBDD(2)
	#time.sleep(2)
	insertBBDD=lipigas_prueba.insertBBDD(alturaEstanque3,3)
	updateBBDD= lipigas_prueba.updateBBDD(3)



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
