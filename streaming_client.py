'''
import socket
import time
import struct
import cv2

def client_action(buffersize,sock,group_tuple):
    print('UDP Client Started ')
    name_size = sock.recv(buffersize).decode()
    name_size = name_size.split(':')
    filename = name_size[0]
    size = int(name_size[1])
    print('Received File:', filename)

    with open('./media_client/' + filename, 'wb') as f:
        while size > 0:
            data = sock.recv(buffersize)
            f.write(data)
            size -= buffersize

def play(filename):
    # Create a VideoCapture object and read from input file
    cap = cv2.VideoCapture('./media/{}'.format(filename))

    # Check if camera opened successfully
    if not cap.isOpened() == False:
        print("Error opening video file")

    # Read until video is completed
    while cap.isOpened():

        # Capture frame-by-frame
        ret, frame = cap.read()
        if ret == True:

            # Display the resulting frame
            cv2.imshow('Frame', frame)

            # Press Q on keyboard to  exit
            if cv2.waitKey(25) & 0xFF == ord('q'):
                #debería borrar el archivo?
                break

        # Break the loop
        else:
            break

    # When everything done, release
    # the video capture object
    cap.release()

    # Closes all the frames
    cv2.destroyAllWindows()

def main():
    buffersize = 1024
    MCAST_GRP = '224.1.1.2'
    MCAST_PORT = 5008
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((MCAST_GRP, MCAST_PORT))
    mreq = struct.pack("4sl", socket.inet_aton(MCAST_GRP), socket.INADDR_ANY)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
    client_action(buffersize,sock,(MCAST_GRP,MCAST_PORT))


if __name__ == '__main__':
    main()
    '''
import socket
import numpy as np
import cv2 as cv


addr = ("127.0.0.1", 65534)
buf = 512
width = int(640*1.5)
height = int(480*1.5)
code = b'start'
num_of_chunks = width * height * 3 / buf

if __name__ == '__main__':
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(addr)
    while True:
        chunks = []
        start = False
        while len(chunks) < num_of_chunks:
            chunk, _ = s.recvfrom(buf)
            if start:
                chunks.append(chunk)
            elif chunk.startswith(code):
                start = True

        byte_frame = b''.join(chunks)

        frame = np.frombuffer(byte_frame, dtype=np.uint8).reshape(height, width, 3)

        cv.imshow('recv', frame)
        if cv.waitKey(1) & 0xFF == ord('q'):
            break

    s.close()
    cv.destroyAllWindows()