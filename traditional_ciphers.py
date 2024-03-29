import pprint
from sympy import mod_inverse
from collections import defaultdict

alphabets = dict()
for i in range(0, 26):
  character = chr(i + 97)
  if character not in alphabets:
    alphabets[character] = i

pprint.pprint(alphabets)

"""#1
**Encrypt the message “ this an exercise” using the following ciphers. Ignore the blank space between words. Decrypt the message to get the original plain text.**

##a) Additive cipher with key=20
"""

def additive_encrypt(plain_text, key):
  cipher_text = ''
  for letter in plain_text:
     value = (alphabets[letter] + key) % 26
     cipher_text += (list(alphabets.keys())[list(alphabets.values()).index(value)])
  return cipher_text

def additive_decrypt(cipher_text, key):
  plain_text = ''
  for letter in cipher_text:
    value = (alphabets[letter] - key) % 26
    plain_text += (list(alphabets.keys())[list(alphabets.values()).index(value)])
  return plain_text

text, key = "thisanexercise", 20
cipher_text = additive_encrypt(text, key)
plain_text = additive_decrypt(cipher_text, key)
print(text, end = " -> ")
print(cipher_text, end = " -> ")
print(plain_text)

"""##b) Multiplicative cipher with key=*15*"""

def multiplicative_encrypt(plain_text, key):
  cipher_text = ''
  for letter in plain_text:
     value = (alphabets[letter] * key) % 26
     cipher_text += (list(alphabets.keys())[list(alphabets.values()).index(value)])
  return cipher_text

def multiplicative_decrypt(cipher_text, key):
  plain_text = ''
  for letter in cipher_text:
    value = (alphabets[letter] * mod_inverse(key, 26)) % 26
    plain_text += (list(alphabets.keys())[list(alphabets.values()).index(value)])
  return plain_text

text, key = "thisanexercise", 15
cipher_text = multiplicative_encrypt(text, key)
plain_text = multiplicative_decrypt(cipher_text, key)
print(text, end = " -> ")
print(cipher_text, end = " -> ")
print(plain_text)

"""##c) Affine cypher with key = (15,20)"""

def affine_encrypt(plain_text, key1, key2):
  cipher_text = ''
  for letter in plain_text:
    value = (alphabets[letter] * key1 + key2) % 26
    cipher_text += (list(alphabets.keys())[list(alphabets.values()).index(value)])
  return cipher_text

def affine_decrypt(cipher_text, key1, key2):
  plain_text = ''
  for letter in cipher_text:
    value = ((alphabets[letter] - key2) * mod_inverse(key1, 26)) % 26
    plain_text += (list(alphabets.keys())[list(alphabets.values()).index(value)])
  return plain_text

text, key1, key2 = 'thisanexercise', 15, 20
cipher_text = affine_encrypt(text, key1, key2)
plain_text = affine_decrypt(cipher_text, key1, key2)
print(text, end = " -> ")
print(cipher_text, end = " -> ")
print(plain_text)

"""##d) Auto key cipher with key = 7"""

def autokey_encrypt(plain_text, key1):
  keystream, cipher_text = [], ''
  keystream.append(key1)
  value1 = (alphabets[plain_text[0]] + key1) % 26
  cipher_text += (list(alphabets.keys())[list(alphabets.values()).index(value1)])
  for i in range(1, len(plain_text)):
    keystream.append(alphabets[plain_text[i-1]])
    value = (alphabets[plain_text[i]] + alphabets[plain_text[i-1]]) % 26
    cipher_text += (list(alphabets.keys())[list(alphabets.values()).index(value)])
  return cipher_text, keystream

def autokey_decrypt(cipher_text, keystream):
  plain_text = ''
  for i in range(len(cipher_text)):
    value = (alphabets[cipher_text[i]] - keystream[i]) % 26
    plain_text += (list(alphabets.keys())[list(alphabets.values()).index(value)])
  return plain_text

text, key1 = 'thisanexercise', 7
cipher_text, keystream = autokey_encrypt(text, key1)
plain_text = autokey_decrypt(cipher_text, keystream)
print(text, end = " -> ")
print(cipher_text, end = " -> ")
print(plain_text)

"""#2
**Use a brute-force attack to decipher the following message enciphered by Alice using an additive cipher. Suppose that Alice always uses a key that is close to her birthday which is on the 13th of the month.**
"""

def additive_decrypt(cipher_text, key):
  plain_text = ''
  for letter in cipher_text:
    value = (alphabets[letter] - key) % 26
    plain_text += (list(alphabets.keys())[list(alphabets.values()).index(value)])
  return plain_text

for key in range(9, 15):
  cipher_text = "NCJAEZRCLASJLYODEPRLYZRCLASJLCPEHZDTOPDZQLNZTY".lower()
  plain_text = additive_decrypt(cipher_text, key)
  print(key, end = " -> ")
  print(plain_text)

"""#3
**Use a Kasiski test and single-frequency attack to break the following ciphertext. You know that it has been created with a Vigenere cipher**
"""



"""#4
**The encryption key in a transposition cipher is (3,2,6,1,5,4). Find the decryption key.**
"""

def find_decryptkey(key_stream):
  key_dict = defaultdict(int)
  for i in range(len(key_stream)):
    key_dict[key_stream[i]] = i+1

  keys = list(key_dict.keys())
  keys.sort()
  key_dict = {i: key_dict[i] for i in keys}
  return key_dict.values()

key_stream = [3, 2, 6, 1, 5, 4]
find_decryptkey(key_stream)

"""#5
**Encrypt the plain text “enemyattackstonight” using Double transposition Cipher.**
"""

def transpose(matrix):
  temp_Matrix = [['']*len(matrix) for j in range(len(matrix[0]))]
  for i in range(len(matrix)):
    for j in range(len(matrix[0])):
      temp_Matrix[j][i] = matrix[i][j]
  return temp_Matrix

def double_transpose_encrypt(plain_text, key_stream, block_size):
  res, cipher_text = [], ''
  plain_text = plain_text.replace(' ', '')
  for i in range(0, len(plain_text), block_size):
    blocked_text = plain_text[i:i+block_size]
    if len(blocked_text) != block_size:
      blocked_text += 'z'*(block_size - len(blocked_text))
    res1 = list(blocked_text)
    res.append(res1)

  key_encrypted = []
  for i in range(len(res)):
    temp = []
    for j in key_stream.keys():
        temp.append(res[i][j-1])
    key_encrypted.append(temp)
  for res in transpose(key_encrypted):
    cipher_text += ''.join(res)

  return cipher_text

def find_decryptkey(key_stream):
  keys = list(key_stream.keys())
  keys.sort()
  key_dict = {i: key_stream[i] for i in keys}
  return key_dict

def double_transpose_decrypt(cipher_text, key_stream, block_size):
  plain_text = ''
  row_size = len(cipher_text) // block_size
  col_mat = [['']*block_size for i in range(row_size)]
  k = 0
  for i in range(block_size):
    for j in range(row_size):
      col_mat[j][i] = cipher_text[k]
      k += 1

  plain_mat = [['']*block_size for i in range(row_size)]
  key_decrypted = find_decryptkey(key_stream)
  keys = list(key_decrypted.values())
  for i in range(row_size):
    for j in range(block_size):
      plain_mat[i][j] = col_mat[i][keys[j]-1]
      plain_text += col_mat[i][keys[j]-1]

  return plain_text

key_stream = {3:1, 1:2, 4:3, 5:4, 2:5}
text = 'enemy attacks tonight'
block_size = 5
cipher_text = double_transpose_encrypt(text, key_stream, block_size)
plain_text = double_transpose_decrypt(cipher_text, key_stream, block_size)
print(text, end = " -> ")
print(cipher_text, end = " -> ")
print(plain_text)

"""#6)
**Modify the double transposition cipher by adding three more rounds and encrypt the above plain text.**
"""

