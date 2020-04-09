
import socket
import numpy as np
import cv2 as cv
import struct

group = "224.1.1.1"
port = 3000
addr = (group,port)

#addr = ("127.0.0.1", 65534)
buf = 512
width = int(640*2)
height = int(480*1.5)
code = b'start'
num_of_chunks = width * height * 3 / buf

if __name__ == '__main__':
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(('', port))
    #s.bind(addr)
    mreq = struct.pack("4sl", socket.inet_aton(group), socket.INADDR_ANY)
    s.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
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