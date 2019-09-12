import pyodbc 
import time
import datetime
import lipigas_prueba

while True:
	altura= lipigas_prueba.altura('192.168.101.1',5050)
	print altura
	insertBBDD=lipigas_prueba.insertBBDD(altura)
	time.sleep(2)

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
