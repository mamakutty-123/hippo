import socket
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

def AES_encrypt(string,key):
    k = bytes(key, 'utf-8')
    cipher = AES.new(k,AES.MODE_ECB)
    enc_text = cipher.encrypt(pad(string, 16))
    return enc_text

def AES_decrypt(enc_text,key):
    k = bytes(key, 'utf-8')
    cipher = AES.new(k, AES.MODE_ECB)
    dec_text = cipher.decrypt(enc_text)
    return unpad(dec_text, 16)

HOST = "127.0.0.1"
PORT = 9090
buffsize = 1024
TCPSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
TCPSocket.bind((HOST, PORT))
TCPSocket.listen()
set_ip = ['127.0.0.1']
print("Server open for connection")
conn, addr = TCPSocket.accept()
if addr[0] not in set_ip:
    print("Address out of range")
    exit()
else:
    print("Client Address: ", addr)
    msg = conn.recv(1024)
    key2 = "0123456789abcdef"

    aes_encrypt = AES_encrypt(msg, key2)
    conn.send(aes_encrypt)
    enc_text=conn.recv(1024)
    msg=AES_decrypt(enc_text,key2)
    print(msg)
    conn.send(msg)
    conn.close()
    TCPSocket.close()