#https://www.geeksforgeeks.org/python-play-a-video-using-opencv/
import cv2
import socket
import struct


MCAST_GRP = '224.3.0.0'
MCAST_PORT = 7234

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)

sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

sock.bind((MCAST_GRP, MCAST_PORT))
mreq = struct.pack("4sl", socket.inet_aton(MCAST_GRP), socket.INADDR_ANY)

sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

while True:
  data = sock.recv(16)
  print (data)



'''
MULTICAST_TTL = 2
sockS = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sockS.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, MULTICAST_TTL)


def play():

    # Create a VideoCapture object and read from input file
    cap = cv2.VideoCapture('./media/small.mp4')

    # Check if camera opened successfully
    if not cap.isOpened() == False:
        print("Error opening video  file")

    # Read until video is completed
    while cap.isOpened():

        # Capture frame-by-frame
        ret, frame = cap.read()
        if ret == True:

            # Display the resulting frame
            cv2.imshow('Frame', frame)

            # Press Q on keyboard to  exit
            if cv2.waitKey(25) & 0xFF == ord('q'):
                break

        # Break the loop
        else:
            break

    # When everything done, release
    # the video capture object
    cap.release()

    # Closes all the frames
    cv2.destroyAllWindows()

while True:
    buffersize = 1024
    #authentication message
    print("hola")
    print(sockR.recv(buffersize))
    print("hola2")
    #send username and password
    username = input()
    #sockS.sendto(username.encode(),(MCAST_GRP,MCAST_PORT))
    #print(sockR.recv(buffersize).decode())
'''


