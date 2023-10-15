from Crypto.Cipher import DES
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import sympy
import math
from hashlib import sha512

public_key, private_key, n = 0, 0, 0

string ="oombu da bunda mavane"
key1 = "abcdefgh"
key2 = "0123456789abcdef"

def DES_encrypt(string,key):
    k = bytes(key, 'utf-8')
    cipher = DES.new(k,DES.MODE_ECB)
    enc_text = cipher.encrypt(pad(bytes(string, 'utf-8'), 8))
    return enc_text

def DES_decrypt(enc_text,key):
    k = bytes(key, 'utf-8')
    cipher = DES.new(k,DES.MODE_ECB)
    dec_text = cipher.decrypt(enc_text)
    return unpad(dec_text, 8)

print("DES ENCRYPTION\n")
des_encrypt = DES_encrypt(string,key1)
print(des_encrypt)
print(DES_decrypt(des_encrypt, key1))

def AES_encrypt(string,key):
    k = bytes(key, 'utf-8')
    cipher = AES.new(k,AES.MODE_ECB)
    enc_text = cipher.encrypt(pad(bytes(string, 'utf-8'), 16))
    return enc_text

def AES_decrypt(enc_text,key):
    k = bytes(key, 'utf-8')
    cipher = AES.new(k, AES.MODE_ECB)
    dec_text = cipher.decrypt(enc_text)
    return unpad(dec_text, 16)

print("\n\nAES ENCRYPTION\n")
aes_encrypt = AES_encrypt(string,key2)
print(aes_encrypt)
print(AES_decrypt(aes_encrypt, key2))

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

def encoder(message):
    encrypted = []
    for x in message:
        enc = 1
        e = public_key
        while e > 0:
            enc *= ord(x)
            enc %= n
            e -= 1
        encrypted.append(enc)
    return encrypted

def decoder(message):
    decrypted = []
    for x in message:
        dec = 1
        d = private_key
        while d > 0:
            dec *= x
            dec %= n
            d -= 1
        decrypted.append(dec)
    return decrypted


print("\n\nRSA ENCRYPTION")
set_keys()
encrypt_text = encoder(string)
print('Encrypted Message - ', encrypt_text)
decrypt_text = decoder(encrypt_text)
print("'Decrypted Message - '", ''.join([chr(x) for x in decrypt_text]))


# SHA-512 
def sha(string):
    hash = sha512(string.encode('utf-8'))
    print(string)
    return hash.hexdigest()

print("\n\nSHA ENCRYPTION")
print(sha(string))