# first of all import the socket library
import socket			
from Crypto.Cipher import DES
from Crypto.Random import get_random_bytes

# next create a socket object
s = socket.socket()		
print ("Socket successfully created")

DES_KEY = b'Chandler Bing'
# reserve a port on your computer in our
# case it is 12345 but it can be anything
port = 12345			

# Next bind to the port
# we have not typed any ip in the ip field
# instead we have inputted an empty string
# this makes the server listen to requests
# coming from other computers on the network
s.bind(('', port))		
print ("socket binded to %s" %(port))

# put the socket into listening mode
s.listen(5)	
print ("socket is listening")		

cipher = DES.new(DES_KEY, DES.MODE_ECB)
data = b'This is a secret message.'

# Padding the data to be a multiple of 8 bytes
block_size = 8
padding_length = block_size - len(data) % block_size
padded_data = data + bytes([padding_length]) * padding_length

# Encrypt the data
encrypted_data = cipher.encrypt(padded_data)

# a forever loop until we interrupt it or
# an error occurs
while True:
    # Establish connection with client.
    c, addr = s.accept()	
    print ('Got connection from', addr )
    
    # send a thank you message to the client. encoding to send byte type.
    c.send(encrypted_data)
    
    # Close the connection with the client
    c.close()
    
    # Breaking once connection closed
    break
