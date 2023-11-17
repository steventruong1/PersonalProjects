from socket import *
import time
import ipaddress
import concurrent.futures
from threading import Lock

LOCK = Lock() #mutex

def doprint(msg):
    with LOCK: #Threads will grab mutex and print message.
        print(msg)

def scan(portNumber):
    s = socket(AF_INET, SOCK_STREAM)
    try:
        con = s.connect((address,portNumber)) #Attempt to connect via socket. If we can, that means it's open
        doprint(f"Port {portNumber} is open")
        return True
    except:
        return False
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
    return portNumber
    
address = ip_validator(gethostbyname(input('Enter address: '))) #grabs input and validates it is a valid address
portNumber = portNumber_validator(int(input('Enter Upper Range Port Number to Check?: '))) #iterates from 1 to number for open ports

start_time = time.time()
print("Starting Port Scanning ...")
futures=[]
with concurrent.futures.ThreadPoolExecutor(max_workers=portNumber) as executor: #Thread pools
     executor.map(scan,[*range(1,portNumber+1)])


print("Port Scanning Complete",time.time() - start_time,"seconds to run")
