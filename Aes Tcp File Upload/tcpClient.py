from socket import *
import ipaddress
import time
import configparser
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from base64 import b64encode
import time

def ip_validator(ip):
    try:
        ip_obj = ipaddress.ip_address(ip) 
        print(f"{ip} is a valid IP address")
        return ip
    except:
        print(f"ERROR: {ip} is not a valid IP address!")
        exit()
def portNumber_validator(portNumber):
    match portNumber:
        case 0:
            print("Port Number 0 is reserved")
            exit()
        case _ if portNumber <0:
            print("Port Number can not be negative")
            exit()
        case _ if portNumber > 65535:
            print("Port Number can not be greater than 65535")
            exit()
    return portNumber
def connect():
    address = ip_validator(gethostbyname(config['DEFAULT']['address'])) #grabs input and validates it is a valid address
    portNumber = portNumber_validator(int(config['DEFAULT']['portNumber'])) #iterates from 1 to number for open ports
    try:
        clientSocket.connect((address,portNumber))
        return True
    except:
        print("Invalid Address and Port Number Combination")
        exit()
        return False
#def encrypt(key,line):
  #  message = line.encode()
   # cipher = AES.new(key, AES.MODE_OCB, nonce=nonce)
    #ciphertext, mac = cipher.encrypt_and_digest(message)
    #return ciphertext,mac

clientSocket = socket(AF_INET, SOCK_STREAM)
config = configparser.ConfigParser() # Reads config file to determine hostname, portnumber and source text file
config.read('config.ini')
connect()

try:
    filename = config['DEFAULT']['sourceName']
except:
    print("Invalid File Name")
    exit()

print("Sending File ...")
start_time = time.time()

#with open("key.txt","wb") as fh:
   # key = get_random_bytes(16) # Generates key for AES
   # fh.write(key)


#with open("nonce.txt","wb") as fh:
   # nonce = get_random_bytes(15)
   # fh.write(nonce)

try:
    with open(filename) as fh: #Opens file, reads 1024 bytes at a time and sends it
        while True:
                data = fh.read(1024)
                #print(data)
               # result = encrypt(key,data) #Read file and encrypts
                clientSocket.send(data.encode())
                if not data:
                    break
except Exception as e:
    print(e)
    exit()
clientSocket.close()
print("File Transmission Complete", time.time() - start_time, "seconds taken")
exit()
            
