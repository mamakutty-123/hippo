# -*- coding: utf-8 -*-
"""DPS Final.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1WuEnoyF2PbNWrp_xqImODPIWI9vHHdkI
"""

!pip3 install pycryptodome

"""# Encryption and Decryption"""

import string
from sympy import mod_inverse
import math
import numpy as np

"""Addition cipher"""

letters = string.ascii_letters
letters_map = {}
number_map = {}
for letter,z in zip(letters,range(len(letters))):
  letters_map[letter] = z
  number_map[z]=letter
plain_text = "hello world"
letters_map[" "] = " "
number_map[" "]=" "
cipher_text = ""
key = 20
for letter in plain_text:
  if(letter == " "):
    cipher_text+=" "
  else:
    cipher_text +=letters[(letters_map[letter]+key)%26]
print(cipher_text)

decrypted_text = ""
for letter in cipher_text:
  if(letter==" "):
    decrypted_text+=" "
  else:
    number = (letters_map[letter]-key)%26
    decrypted_text+= number_map[number]

"""Multiplicative cipher"""

cipher_text = ""
for letter in plain_text:
  if(letter == " "):
    cipher_text+=" "
  else:
    cipher_text +=letters[(letters_map[letter]*19)%26]
print(cipher_text)

decrypted_text = ""
for letter in cipher_text:
  if(letter==" "):
    decrypted_text+=" "
  else:
    number = (letters_map[letter]*mod_inverse(19,26))%26
    decrypted_text+= number_map[number]

"""Transposition cipher

"""

plain_text = "enemyattackstonight"
key_size = 5
encryption_key = np.array([2,0,3,4,1])

map = {}
for i in range(len(encryption_key)):
  map[i] = encryption_key[i]
swap = {}
for i,j in map.items():
  swap[j] = i
keys = list(swap.keys())
keys.sort()
sorted_map = {i: swap[i] for i in keys}
decryption_key = np.array(list(sorted_map.values()))

def permute_columns(text):
  split_text  = []
  for i in range(int((len(text)/key_size))+1):
    val = text[i*key_size:(i+1)*key_size]
    while(len(val)<key_size):
      val+='z'
    split_text.append(val)
  return split_text

col_permute = permute_columns(plain_text)
rep = np.empty([int(len(plain_text)/key_size)+1,key_size],dtype=str)

for i in range(len(col_permute)):
  for j in range(len(col_permute[i])):
    rep[i][j] = col_permute[i][j]

encrypt = np.empty([int(len(plain_text)/key_size)+1,key_size],dtype=str)

for i in range(len(encryption_key)):
  encrypt[:,i] = rep[:,encryption_key[i]]

decrypt = np.empty([int(len(plain_text)/key_size)+1,key_size],dtype=str)
for i in range(len(decryption_key)):
  decrypt[:,i] = encrypt[:,decryption_key[i]]

def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

def mod_inverse(a, m):
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    return None

def affine_encrypt(plain_text, key_a, key_b):
    encrypted_text = ""
    for char in plain_text:
        if char.isalpha():
            if char.isupper():
                encrypted_char = chr((key_a * (ord(char) - ord('A')) + key_b) % 26 + ord('A'))
            else:
                encrypted_char = chr((key_a * (ord(char) - ord('a')) + key_b) % 26 + ord('a'))
            encrypted_text += encrypted_char
        else:
            encrypted_text += char
    return encrypted_text

def affine_decrypt(encrypted_text, key_a, key_b):
    decrypted_text = ""
    a_inverse = mod_inverse(key_a, 26)
    if a_inverse is None:
        return "Invalid key 'a', no modular inverse exists."

    for char in encrypted_text:
        if char.isalpha():
            if char.isupper():
                decrypted_char = chr((a_inverse * (ord(char) - ord('A') - key_b)) % 26 + ord('A'))
            else:
                decrypted_char = chr((a_inverse * (ord(char) - ord('a') - key_b)) % 26 + ord('a'))
            decrypted_text += decrypted_char
        else:
            decrypted_text += char
    return decrypted_text

# Encryption key (a must be coprime with 26)
key_a = 5
key_b = 21

# Plain text to encrypt
plain_text = "Hello World"

# Encrypt using Affine Cipher
encrypted_text = affine_encrypt(plain_text, key_a, key_b)
print("Encrypted Text:", encrypted_text)

# Decrypt using Affine Cipher
decrypted_text = affine_decrypt(encrypted_text, key_a, key_b)
print("Decrypted Text:", decrypted_text)

"""# RSA and SHA"""

# RSA
import sympy
import math

public_key, private_key, n = 0, 0, 0

def set_keys():
    global public_key, private_key, n
    p = sympy.randprime(1000, 2000)
    q = sympy.randprime(1000, 2000)
    print('Prime Numbers  - ', p, q)
    n = p * q
    fi = (p - 1) * (q - 1)
    e = 2
    while True:
        if math.gcd(e, fi) == 1:
            break
        e += 1
    public_key = e
    d = 2
    while True:
        if (d * e) % fi == 1:
            break
        d += 1
    private_key = d

message = "Hello There!"
message_ord = [ord(x) for x in message]
message_ord

set_keys()

def encoder(message):
  encoded = []
  for i in message:
    encoded.append((i**public_key)%n)
  return encoded

def decoder(message):
  decoded = []
  for i in message:
    decoded.append((i**private_key)%n)
  return decoded

encryption = encoder(message_ord)

decryption = decoder(encryption)

#SHA
from hashlib import sha512
text = 'Hello There!'
hash = sha512(text.encode('utf-8'))
print(text)
print(hash.hexdigest())

"""# DES"""

from Crypto.Cipher import DES
data = '123456ABCD132536'
print(data)
key = 'AABB09182736CCDD'.encode('utf-8')
cipher = DES.new(key[:8], DES.MODE_ECB)
ct = cipher.encrypt(data.encode('UTF-8'))
print(ct)
pt = cipher.decrypt(ct)
print(pt)

"""# AES"""

from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

data = b'secret data'

#Encyption
key = get_random_bytes(16)
cipher = AES.new(key, AES.MODE_EAX)
ciphertext, tag = cipher.encrypt_and_digest(data)
nonce = cipher.nonce

#Decryption
cipher = AES.new(key, AES.MODE_EAX, nonce)
data = cipher.decrypt_and_verify(ciphertext, tag)

"""# Firewall

send
"""

import socket
HOST = "127.0.0.1"
PORT = 65432
buffsize = 102
TCPSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
TCPSocket.connect((HOST,PORT))
TCPSocket.close()

"""recieve"""

import socket
HOST = "127.0.0.1"
PORT = 65432
buffsize = 1024
TCPSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
TCPSocket.bind((HOST, PORT))
TCPSocket.listen()
set_ip = ['127.0.0.1']
print("Server open for connection")
conn, addr = TCPSocket.accept()
if addr[0] not in set_ip:
    print("Address out of range")
else:
    print("Client Address: ", addr)
conn.close()
TCPSocket.close()

"""# Password Authentication"""

!pip3 install bcrypt

import bcrypt

password_map = {"pragathi":b'Prags@123'}

hashed = {}
salt = bcrypt.gensalt()
for i,j in password_map.items():
  hashed[i]=bcrypt.hashpw(j,salt)

username = input("Enter your username: ")
password = input("Enter your password: ")
hashed_password = bcrypt.hashpw(password.encode(),salt)
print(hashed_password == hashed[username])