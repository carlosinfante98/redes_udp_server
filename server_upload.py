#! /usr/bin/env python3
import socket
from datetime import datetime
import time
import hashlib

host_ip = '127.0.0.1'
host_port = 5000
serv_ip = '127.0.0.1'
serv_port = 0
buffersize = 1024

def hash_file(filename):

    hash = hashlib.sha256()
    with open('./media/'+filename, 'rb') as f:
        chunk = 0
        while chunk != b'':
            chunk = f.read(buffersize)
            hash.update(chunk)

    return hash.hexdigest()

def server_action():
    client = (host_ip, host_port) # client tuple
    serv = (serv_ip, serv_port) # serv tuple

    #Socket creation
    s = socket.socket( socket.AF_INET, socket.SOCK_DGRAM )
    s.bind( serv )

    print('UDP client Started on {}:{}'.format(serv_ip, serv_port))

    #Connection starts here
    message = 'Hello, ready.'
    print('Sending data to client: {}'.format(message))
    time.sleep(0.1)
    s.sendto(message.encode(), client)

    name_size = s.recv(buffersize).decode()
    name_size = name_size.split(':')
    filename = name_size[0]
    size = int(name_size[1])
    packages = int(size/buffersize)


    #File gets received
    print('Received File:',filename)
    start = time.time()

    with open('./media/' + filename,'wb') as f:
        while size > 0:
            data = s.recv(buffersize)
            f.write(data)
            size -= buffersize

    end = time.time()
    size = int(name_size[1])
    file_time = str(round(end-start,3))
    
    #Receives hash
    hash_rec = s.recv(buffersize).decode()
    hash_cal = hash_file(filename)
    if hash_rec == hash_cal:
        s.sendto('correct'.encode(), client)
        print('Hash is correct.')
    else:
        s.sendto('error'.encode(), client)
        print('Wrong hash.')

    #Close socket communication
    s.close()

def main():
    server_action()

if __name__ == '__main__':
    main()
