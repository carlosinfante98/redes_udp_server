#! /usr/bin/env python3
import socket
from datetime import datetime
import time
import hashlib

host_ip = '127.0.0.1'
host_port = 5000
client_ip = '127.0.0.1'
client_port = 0
buffersize = 1024

def hash_file(filename):

    hash = hashlib.sha256()
    with open('./media_client/'+filename, 'rb') as f:
        chunk = 0
        while chunk != b'':
            chunk = f.read(buffersize)
            hash.update(chunk)

    return hash.hexdigest()

def client_action():
    server = (host_ip, host_port) # Server tuple
    client = (client_ip, client_port) # Client tuple
    
    #Socket creation
    s = socket.socket( socket.AF_INET, socket.SOCK_DGRAM )
    s.bind( client )
    # s.connect(server)
    
    print('UDP Client Started on {}:{}'.format(client_ip, client_port))

    #Connection starts here
    log = open("./client_logs/udp_log ({}, {}).txt".format(client_ip, client_port), "w") #client log gets created here
    log.write('UDP Client Log - ' + str(datetime.now())+'\n\n')
    message = 'Hello, ready.'
    print('Sending data to server: {}'.format(message))
    time.sleep(0.1)
    s.sendto(message.encode(), server)

    name_size = s.recv(buffersize).decode()
    name_size = name_size.split(':')
    filename = name_size[0]
    size = int(name_size[1])
    packages = int(size/buffersize)


    #File gets received
    print('Received File:',filename)
    start = time.time()

    with open('./media_client/' + filename,'wb') as f:
        while size > 0:
            data = s.recv(buffersize)
            f.write(data)
            size -= buffersize

    end = time.time()
    size = int(name_size[1])
    file_time = str(round(end-start,3))
    log.write('File: {}\n'.format(filename))
    log.write('Packages sent: {} - Packages received: {} - Packages transmitted: {}\n'.format(packages+1,packages+1,packages+1))
    log.write('Bytes sent: {} - Bytes received: {}\n'.format(size,size))
    log.write('Transaction time for file \'{}\' with size {} bytes was: {} seg\n\n'.format(filename, size, file_time))

    #Receives hash
    hash_rec = s.recv(buffersize).decode()
    hash_cal = hash_file(filename)
    if hash_rec == hash_cal:
        s.sendto('correct'.encode(), server)
        print('Hash is correct.')
    else:
        s.sendto('error'.encode(), server)
        print('Wrong hash.')
    
    #Close log and socket communication
    log.close()
    s.close()

def main():
    client_action()
    
if __name__ == '__main__':
    main()
