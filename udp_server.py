#! /usr/bin/env python3
import socket
import datetime
import os
import time
import hashlib

host_ip = '127.0.0.1'
host_port = 5000
buffersize = 1024

def hash_file(filename):

    hash = hashlib.sha256()
    with open('./media/'+filename, 'rb') as f:
        chunk = 0
        while chunk != b'':
            chunk = f.read(buffersize)
            hash.update(chunk)

    return hash.hexdigest()

def main():
    #Tuple with host ip and host port
    server = (host_ip, host_port)
   
    s = socket.socket( socket.AF_INET, socket.SOCK_DGRAM )
    s.bind(server)
    
    print('UDP Server Started on {}:{}'.format(host_ip, host_port))
    while True:
        recvdata, addr = s.recvfrom( buffersize )
        recvdata = recvdata.decode()
        current_time = datetime.datetime.now().time()
        print( '{} <- Recvfrom: {}'.format(current_time, addr))
        print( 'data: {}'.format(recvdata) )
        
        filename= 'big.mp4'

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
    
    s.close()
    
if __name__ == '__main__':
    main()
