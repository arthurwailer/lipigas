import pyodbc 
import time
import datetime
import lipigas_prueba




try:
    conn = pyodbc.connect('Driver={SQL Server};'
                        'Server=DESKTOP-HPBR3L8\SQLEXPRESS;'
                        'Database=fuel-explorer;'
                        'Trusted_Connection=yes;')
    if conn:
        print "Connectado a la BBDD"
        cursor = conn.cursor()
        print "obteniendo tupla"
        cursor.execute("SELECT * FROM [fuel-explorer].db_owner.estanques")

        tables = cursor.fetchall()
        for rows in tables:
            id = rows[0]
            estanque_ip = rows[2]
            volumen = lipigas_prueba.volumenCuatro(estanque_ip,6060)
            altura = lipigas_prueba.alturaCuatro(estanque_ip,6060)
            print "el volumen 4 es: ", volumen
            print "la altura 4 es: ", altura
            if altura is not None and volumen is not None:
				print altura
				insertBBDD=lipigas_prueba.insertBBDD(altura,id,volumen)
				updateBBDD= lipigas_prueba.updateBBDD(id)

            else:
                volumen = lipigas_prueba.volumenTres(estanque_ip,6060)
                altura = lipigas_prueba.alturaTres(estanque_ip,6060)
                print "la altura 3 es: ", altura 
                print "el volumen 3 es: ", volumen
                insertBBDD=lipigas_prueba.insertBBDD(altura,id,volumen)
                updateBBDD= lipigas_prueba.updateBBDD(id)

       
        print "tupla obtenida"

    else:
        print "Can't Connect to BBDD"
except Exception as e:

    print ("Ocurrio un error al tratar de conectar a la BBDD insertos",e)
finally:
    conn.commit()
    cursor.close()
    conn.close()