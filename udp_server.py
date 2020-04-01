#! /usr/bin/env python3
import socket
import datetime

host_ip = '127.0.0.1'
host_port = 5000
buffersize = 1024


def main():
    #Tuple with host ip and host port
    server = (host_ip, host_port)
   
    s = socket.socket( socket.AF_INET, socket.SOCK_DGRAM )
    s.bind(server)
    
    print('UDP Server Started on {}:{}'.format(host_ip, host_port))
    while True:
        recvdata, addr = s.recvfrom( buffersize )
        current_time = datetime.datetime.now().time()
        
        print( '{} <- Recvfrom: {}'.format(current_time, addr))
        print( 'data: {}'.format(recvdata) )
        
        current_time = datetime.datetime.now().time()
        send_data = 'OK'
        print( '{} -> senddata: {}'.format(current_time, send_data))
        s.sendto(send_data.encode('utf-8'), addr)
        
        if recvdata == b'kill':
            print( 'Requested Server Shutdown' )
            break
    
    s.close()
    
if __name__ == '__main__':
    main()