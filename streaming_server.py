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
    def __init__(self,clientsocket, f,group_tuple):
        threading.Thread.__init__(self)
        self.file = f
        self.csocket = clientsocket
        self.group_tuple = group_tuple

        # print ("New connection added: ", client_addr)

    def run(self):
        # print ("Connection from : ", self.addr)

        # Server starts protocol with client
        server_action(self.csocket, self.file,self.group_tuple)
        #print("Client at ", self.addr, " disconnected.")





def server_action(sock, filename,group_tuple):
    # Tuple with host ip and host port

    while True:

        with open('./media/' + filename, 'rb') as f:
            size = os.path.getsize('./media/' + filename)
            sock.sendto((filename + ':' + str(size)).encode(),group_tuple)
            while size > 0:
                data = f.read(buffersize)
                sock.sendto(data, group_tuple)
                time.sleep(0.000001)
                size -= buffersize
        print('Enviado')



def main():
    # File selection
    MCAST_GRP = '224.1.1.1'
    MCAST_PORT = 5007
    MULTICAST_TTL = 2
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, MULTICAST_TTL)
    file = int(input('Select which file you wish to transfer:\n1. Big file\n2. Small file\n'))
    filename = 'big.mp4' if file == 1 else 'small.mp4'


    while True:
        newthread = ClientThread( sock, filename,(MCAST_GRP,MCAST_PORT))
        time.sleep(0.2)
        newthread.start()


if __name__ == '__main__':
    main()