#! /usr/bin/env python3
import socket
from datetime import datetime
import os
import time
import hashlib
import threading

host_ip = '127.0.0.1'
host_port = 5000
buffersize = 1024
thread_list = []

class ClientThread(threading.Thread):
    def __init__(self, message, client_addr, clientsocket, f):
        threading.Thread.__init__(self)
        self.file = f
        self.msg = message
        self.csocket = clientsocket
        self.addr = client_addr

    def run(self):        
        #Server starts protocol with client
        server_action(self.msg, self.addr, self.csocket, self.file)
        print ("Client at ", self.addr , " disconnected.")
        time.sleep(0.5)
        

def hash_file(filename):

    hash = hashlib.sha256()
    with open('./media/'+filename, 'rb') as f:
        chunk = 0
        while chunk != b'':
            chunk = f.read(buffersize)
            hash.update(chunk)

    return hash.hexdigest()

def server_action(recvdata, addr, s, filename):
    
    current_time = datetime.now().time()
    print( '{} <- Recvfrom: {}'.format(current_time, addr))
    print( 'Data: {}'.format(recvdata) )
    log = open("./server_logs/udp_log.txt", "a") #server log gets created here
    log.write('UDP Client {} Log - '.format(addr) + str(datetime.now())+'\n\n')
    log.write('File: {}\n'.format(filename))

    start = time.time()
    with open('./media/'+filename,'rb') as f:
        size = os.path.getsize('./media/'+filename)
        s.sendto((filename+':'+str(size)).encode(), addr)
        while size > 0:
            data = f.read(buffersize)
            s.sendto(data,addr)
            time.sleep(0.000001)
            size -= buffersize
    print('Sent successfully.')

    size = os.path.getsize('./media/'+filename)
    packages = int(size/buffersize)
    end = time.time()
    file_time = str(round(end-start,3))
    log.write('Packages sent: {} - Packages received: {} - Packages transmitted: {}\n'.format(packages+1,packages+1,packages+1))
    log.write('Bytes sent: {} - Bytes received: {}\n'.format(size,size))
    log.write('Transaction time for file \'{}\' with size {} bytes was: {} seg\n\n'.format(filename, size, file_time))
    log.write('-------------------------------------------------------\n')

    #Hash gets created and sended
    file_hashed = hash_file(filename)
    s.sendto(file_hashed.encode(), addr)
    time.sleep(0.15)
    resp = s.recv(buffersize).decode()
    if resp == 'correct':
        print('File and hash correct.')
    elif resp == 'error':
        print('Error in file and hash')
    thread_list.remove(addr)    
    print('Remove, now size is {}'.format(len(thread_list)))

def main():
    #File selection
    file = int(input('Select what file you want to transfer:\n1. Big file\n2. Small file\n'))
    filename= 'big.mp4' if file == 1 else 'small.mp4'
    print('UDP Server Started on {}:{}'.format(host_ip, host_port))

    #Server starts to connect the socket
    address = (host_ip, host_port) #Tuple with host ip and host port
    server = socket.socket( socket.AF_INET, socket.SOCK_DGRAM )
    server.bind(address)

    while len(thread_list)<25:
        recvdata, addr = server.recvfrom( buffersize )
        recvdata = recvdata.decode()
        newthread = ClientThread(recvdata, addr, server, filename)
        thread_list.append(addr)
        print('Size is {}'.format(len(thread_list)))
        newthread.start()

    server.close()
    
if __name__ == '__main__':
    main()
