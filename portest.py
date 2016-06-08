import socket
import sys
import time

now=time.time()
def usage():
        print 'Usage:\n\tportest.py ip:port \n\tportest.py domainname:port'
        sys.exit(1)

        
try:
    if not sys.argv[1]:
        usage()
except IndexError:
    usage()


try:
    ip=sys.argv[1].split(':')[0]
    port=sys.argv[1].split(':')[1]
    if port=="":
        port="80"
except IndexError:
    port="80"

sock = socket.socket()
# sock =  socket.socket(socket.AF_INET,socket.SOCK_DGRAM) 
sock.settimeout(5)
try:
    int(ip.split('.')[0].split()[0])
except ValueError:
    ip=socket.getaddrinfo(ip.split(':')[0],None)[-1][-1][0]
    print ip
try:
    # print ip,':',port
    sock.connect((ip, int(port)))
    
    sock.sendto('test', (ip, int(port)))
    print 'ok'
    sock.close()
except :
    print 'failed'


