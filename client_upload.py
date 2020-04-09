#! /usr/bin/env python3
import socket
from datetime import datetime
import os
import time
import hashlib
import threading

client_ip = '127.0.0.1'
client_port = 5000
buffersize = 1024
thread_list = []

class Server(threading.Thread):
    def __init__(self, message, client_addr, clientsocket, f):
        threading.Thread.__init__(self)
        self.file = f
        self.msg = message
        self.csocket = clientsocket
        self.addr = client_addr

    def run(self):        
        #Client starts protocol with server
        client_action(self.msg, self.addr, self.csocket, self.file)
        print ("Server at ", self.addr , " disconnected.")
        time.sleep(0.5)
        

def hash_file(filename):

    hash = hashlib.sha256()
    with open('./media/'+filename, 'rb') as f:
        chunk = 0
        while chunk != b'':
            chunk = f.read(buffersize)
            hash.update(chunk)

    return hash.hexdigest()

def client_action(recvdata, addr, s, filename):
    
    current_time = datetime.now().time()
    print( '{} <- Recvfrom: {}'.format(current_time, addr))
    print( 'Data: {}'.format(recvdata) )

    start = time.time()
    with open('./media_client/'+filename,'rb') as f:
        size = os.path.getsize('./media_client/'+filename)
        s.sendto((filename+':'+str(size)).encode(), addr)
        while size > 0:
            data = f.read(buffersize)
            s.sendto(data,addr)
            time.sleep(0.000001)
            size -= buffersize
    print('Sent successfully.')

    size = os.path.getsize('./media_client/'+filename)
    packages = int(size/buffersize)
    end = time.time()
    file_time = str(round(end-start,3))

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

    users = {'carlos':'123','sergio':'123'}
    ans = input('Do you want to transfer a file? Type yes/no\n').lower()
    if ans == 'yes':
        user = input('Type your username: ')
        pswd = input('Type your password: ')
        if user in users and users[user] == pswd:
            filename= 'guitar.mp4'
            print('UDP Client Started on {}:{}'.format(client_ip, client_port))

            #Server starts to connect the socket
            address = (client_ip, client_port) #Tuple with host ip and host port
            client = socket.socket( socket.AF_INET, socket.SOCK_DGRAM )
            client.bind(address)

            while len(thread_list)<25:
                recvdata, addr = client.recvfrom( buffersize )
                recvdata = recvdata.decode()
                newthread = Server(recvdata, addr, client, filename)
                thread_list.append(addr)
                newthread.start()
        else:
            print('Wrong user. Goodbye')
    else:
        print('Goodbye')

    client.close()
    
if __name__ == '__main__':
    main()
