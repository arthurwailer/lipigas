import socket 

servidor = socket.socket()
servidor.bind(('127.0.0.1',5000))
servidor.listen(5)

while True:
	conexion, addr = servidor.accept()
	print "conexion establecida.."
	print addr
	conexion.send('Hola desde el servidor')
	respuesta = conexion.recv(1024)
	print respuesta
	conexion.close()
