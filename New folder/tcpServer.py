from socket import *
import configparser
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from base64 import b64encode

serverSocket = socket(AF_INET,SOCK_STREAM)
config = configparser.ConfigParser()
config.read('config.ini') # Reads config file to get hostname, post number and output file name
serverSocket.bind(((config['DEFAULT']['address'],int(config['DEFAULT']['portNumber']))))
serverSocket.listen(1)
print('The server is ready to receive')
connectionSocket, addr = serverSocket.accept()
open(config['DEFAULT']['outputName'], 'w').close()  #Clear Output Text File
with open(config['DEFAULT']['outputName'], "a") as my_file:
    while True:
        data = connectionSocket.recv(4096).decode() #Read from input stream and writes to file
        #print(data)
        if not data:
           break
        my_file.write(data)
        #with open("key.txt", "rb") as my_file:
         #   key = my_file.readline()
        #with open("nonce.txt","rb") as nonce:
           # nonce = nonce.read()
        #cipher = AES.new(key, AES.MODE_OCB, nonce=nonce)
       # plaintext = cipher.decrypt(data)
        #print(plaintext)
connectionSocket.close()
