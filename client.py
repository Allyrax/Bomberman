import socket

TCP_IP = '127.0.0.1'
TCP_PORT = 2000
BUFFER_SIZE = 1024
MESSAGE = "Hello, World!"
bytesMessage = MESSAGE.encode('utf-8')

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
s.send(bytesMessage)
data = s.recv(BUFFER_SIZE)
dataDecoded = data.decode('utf-8')

s.close()

print ("received data:", dataDecoded)