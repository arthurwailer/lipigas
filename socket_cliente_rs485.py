import socket 
import time
#s_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

while True:
	try:
		client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # objeto client ipv4 y protocolo TCP/IP
		client.settimeout(2)
		client.connect(("127.0.0.1",5000))#Conecta al servidor RUT955 con su ip y puerto
		print "Conectado"
		print 'Enviando mje'
		client.send("hola desde el cliente")# Envia mje al servidor
		# qry = bytearray()
		# qry.append(0x03)
		# qry.append(0x09)
		# qry.append(0x00)
		# qry.append(0x08)
		# #qry.append(0x00)
		# # qry.append(0x01)
		# crc_high = 1
		# crc_low = 2
		# #calcualte with crcmod
		# qry.append(crc_high)
		# qry.append(crc_low) 

		respuesta = client.recv(1024)# guarda la respuesta que entrega el servidor en bytes
		
		print respuesta
		time.sleep(60)

	except:
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