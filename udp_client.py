#! /usr/bin/env python3
import socket
import datetime
import hashlib

host_ip = '127.0.0.1'
host_port = 5000
client_ip = '127.0.0.1'
client_port = 5001
buffersize = 1024

def hash_file(filename):

    hash = hashlib.sha256()
    with open('./mediaClient/'+filename, 'rb') as f:
        chunk = 0
        while chunk != b'':
            chunk = f.read(buffersize)
            hash.update(chunk)

    return hash.hexdigest()

def main():
    server = (host_ip, host_port) # Server tuple
    client = (client_ip, client_port) # Client tuple
    
    #Socket creation
    s = socket.socket( socket.AF_INET, socket.SOCK_DGRAM )
    s.bind( client )
    
    print('UDP Client Started on {}:{}'.format(client_ip, client_port))

    #Connection starts here
    message = 'Hello, ready.'
    print('Sending data to server: {}'.format(message))
    s.sendto(message.encode(), server)

    name_size = s.recv(buffersize).decode()
    name_size = name_size.split(':')
    filename = name_size[0]
    size = int(name_size[1])

    # filename, addr = s.recvfrom(buffersize)
    # filename = filename.decode().strip()
    print('Received File:',filename)
    with open('./mediaClient/' + filename,'wb') as f:
        while size > 0:
            data = s.recv(buffersize)
            f.write(data)
            size -= buffersize

    #Receives hash
    hash_rec = s.recv(buffersize).decode()
    hash_cal = hash_file(filename)
    if hash_rec == hash_cal:
        s.sendto('hash_correct'.encode(), server)
        print('Hash is correct.')
    
    print('Created successfully.')
    s.close()
    
if __name__ == '__main__':
    main()