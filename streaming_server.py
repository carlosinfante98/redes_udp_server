
import socket
import numpy as np
import cv2 as cv

addr = ("224.1.1.1",3000)
addr2 = ("224.1.1.2",3001)
#addr = ("127.0.0.1", 65534)
buf = 512
width = 640
height = 480
cap = cv.VideoCapture('./media/small.mp4')
cap2 = cv.VideoCapture('./media/big.mp4')
code = 'start'
code = ('start' + (buf - len(code)) * 'a').encode('utf-8')


if __name__ == '__main__':
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.IPPROTO_IP,socket.IP_MULTICAST_TTL,1)
    #s.bind(addrG)
    while(cap.isOpened()):
        ret, frame = cap.read()
        ret2, frame2 = cap2.read()
        if ret:
            s.sendto(code, addr)
            data = frame.tostring()
            for i in range(0, len(data), buf):
                s.sendto(data[i:i+buf], addr)
            # cv.imshow('send', frame)
            # if cv.waitKey(1) & 0xFF == ord('q'):
                # break
        if ret2:
            s.sendto(code, addr2)
            data2 = frame2.tostring()
            for i in range(0, len(data2), buf):
                s.sendto(data2[i:i + buf], addr2)
        else:
            break
    # s.close()
    # cap.release()
    # cv.destroyAllWindows()