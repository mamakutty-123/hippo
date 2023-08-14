# -*- coding: utf-8 -*-
"""
Created on Tue Aug  8 11:02:42 2023

@author: 19pd06
"""



# Import socket module
import socket	
from Crypto.Cipher import DES		

DES_KEY = b'K Ashish'
cipher = DES.new(DES_KEY, DES.MODE_ECB)

# Create a socket object
s = socket.socket()		

# Define the port on which you want to connect
port = 12345			

# connect to the server on local computer
s.connect(('127.0.0.1', port))

print("Succesfully connected")

# receive data from the server and decoding to get the string.
received_mesage = s.recv(1024)
decrypted_data = cipher.decrypt(received_mesage)

# Remove the padding
unpadded_data = decrypted_data[:-decrypted_data[-1]]
print("Decrypted Message: ",unpadded_data)
# close the connection
s.close()	
	
