#https://stackoverflow.com/questions/603852/how-do-you-udp-multicast-in-python

import socket
import struct

import socket

MCAST_GRP = '239.1.1.234'
MCAST_PORT = 7234

MULTICAST_TTL = 2

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, MULTICAST_TTL)

sock.sendto(b"robot", (MCAST_GRP, MCAST_PORT))

'''
user = sock.recv(1024).decode().split(",")
allowed_users = [("sergio","123"),("carlos","123")]
sock.sendto(b"Authenticate in the following format:\nusername,password", (MCAST_GRP, MCAST_PORT))
username = user[0]
password = user[1]
if (username,password) in allowed_users:
    sock.sendto("authenticated, you can now upload videos".encode(),(MCAST_GRP1, MCAST_PORT_recieve))
else:
    sock.sendto("not a valid user".encode(), (MCAST_GRP1, MCAST_PORT_recieve))
        #terminar
'''
