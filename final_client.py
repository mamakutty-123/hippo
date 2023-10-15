import socket
HOST = "127.0.0.1"
string = "oombu da bunda mavane"
PORT = 9090
buffsize = 102
TCPSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
TCPSocket.connect((HOST,PORT))
TCPSocket.send(bytes(string, 'utf-8'))
encrypt_str = TCPSocket.recv(1024)
print(encrypt_str)
TCPSocket.send(encrypt_str)
text = TCPSocket.recv(1024)
print(text)
TCPSocket.close()