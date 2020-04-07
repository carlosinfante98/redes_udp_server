#! /usr/bin/env python3
import socket
import datetime
import os
import time
import hashlib
import threading

host_ip = '127.0.0.1'
host_port = 5000
buffersize = 1024

class ClientThread(threading.Thread):
    def __init__(self, message, client_addr, clientsocket, f):
        threading.Thread.__init__(self)
        self.file = f
        self.msg = message
        self.csocket = clientsocket
        self.addr = client_addr
        # print ("New connection added: ", client_addr)

    def run(self):
        # print ("Connection from : ", self.addr)
        
        #Server starts protocol with client
        server_action(self.msg, self.addr, self.csocket, self.file)
        print ("Client at ", self.addr , " disconnected.")

def hash_file(filename):

    hash = hashlib.sha256()
    with open('./media/'+filename, 'rb') as f:
        chunk = 0
        while chunk != b'':
            chunk = f.read(buffersize)
            hash.update(chunk)

    return hash.hexdigest()

def server_action(recvdata, addr, s, filename):
    #Tuple with host ip and host port
    
    while True:
        # recvdata, addr = s.recvfrom( buffersize )
        # recvdata = recvdata.decode()
        current_time = datetime.datetime.now().time()
        print( '{} <- Recvfrom: {}'.format(current_time, addr))
        print( 'Data: {}'.format(recvdata) )

        with open('./media/'+filename,'rb') as f:
            size = os.path.getsize('./media/'+filename)
            s.sendto((filename+':'+str(size)).encode(), addr)
            while size > 0:
                data = f.read(buffersize)
                s.sendto(data,addr)
                time.sleep(0.000001)
                size -= buffersize
        print('Sent successfully.')

        #Hash gets created and sended
        file_hashed = hash_file(filename)
        s.sendto(file_hashed.encode(), addr)
        time.sleep(0.1)
        resp = s.recv(buffersize).decode()
        if resp == 'correct':
            print('File and hash correct.')
        elif resp == 'error':
            print('Error in file and hash')

def main():
    #File selection
    file = int(input('Select what file you want to transfer:\n1. Big file\n2. Small file\n'))
    filename= 'big.mp4' if file == 1 else 'small.mp4'
    print('UDP Server Started on {}:{}'.format(host_ip, host_port))

    #Server starts to connect the socket
    address = (host_ip, host_port)
    server = socket.socket( socket.AF_INET, socket.SOCK_DGRAM )
    server.bind(address)

    while True:
        # c_socket, addr = server.accept()
        recvdata, addr = server.recvfrom( buffersize )
        recvdata = recvdata.decode()
        newthread = ClientThread(recvdata, addr, server, filename)
        time.sleep(0.2)
        newthread.start()
    
if __name__ == '__main__':
    main()
