import socket 

servidor = socket.socket()
servidor.bind(('192.168.101.1',5000))
servidor.listen(5)
