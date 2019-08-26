import socket 
import time
#s_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

while True:
	try:
		client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # objeto client 
		client.settimeout(10)
		client.connect(('127.0.0.1',5000))#conectadome al servidor RUT955 con su ip y puerto
		print "Conectado"
		print 'Enviando mje'
		client.send('hola desde el cliente')
		print 'mje enviado'
		respuesta = client.recv(1024)
		print (respuesta)
		time.sleep(60)
	except Exception as e:

		print e
		print "Can't connect"
		time.sleep(2)
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