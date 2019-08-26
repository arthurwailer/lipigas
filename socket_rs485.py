import socket

mi_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
mi_socket.bind(("127.0.0.2", 5000))
mi_socket.listen(5)
sc, addr = mi_socket.accept()
recibido = sc.recv(1024)
nuestra_respuesta = "Hola cliente, yo soy el servidor. Unete a underc0de!"
sc.send(nuestra_respuesta.encode('utf-8'))
sc.close()
mi_socket.close()
