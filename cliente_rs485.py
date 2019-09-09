import socket 
import time
#s_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ip = '192.168.101.1'
port = 5000
while True:
	try:
		client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # objeto client 
		print "socket creado con el nombre de client..."
		client.settimeout(10)
		client.connect(('192.168.101.1',5000))#conectadome al servidor RUT955 con su ip y puerto
		print "Conectado"
		print 'Enviando mje'
		client.send('030300070001')
		print 'mje enviado'
		respuesta = client.recv(1024)
		print str(respuesta)


		time.sleep(60)
	except Exception as e:

		print e
		print "Can't connect"
		client.close()
	
	

	


#verbose=True
# while True:
#     try:
#         if(verbose):
#             print "connecting...",
        
      
#         #self.socket.settimeout(None)
#         if(verbose):
#             print "success!"
#         #return
#     except:
#         if(verbose):
#             print "can't connect"
       
#         #return