'''
from imutils.video import VideoStream
from flask import Response
from flask import Flask
from flask import render_template
from flask import send_from_directory
import threading
import time
import cv2

outputFrame = None
lock = threading.Lock()
app = Flask(__name__)
#vs = VideoStream(src=0).start()
time.sleep(2.0)
cap = cv2.VideoCapture('./media/small.mp4')

def play():

    global vs,cap,lock

    # Check if camera opened successfully
    if not cap.isOpened() == False:
        print("Error opening video  file")

    # Read until video is completed
    while cap.isOpened():

        # Capture frame-by-frame
        ret, frame = cap.read()
        if ret == True:

            # Display the resulting frame
            cv2.imshow('St1', frame)

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


@app.route("/")
def index():
    # return the rendered template
    return render_template("index.html")


def generate():
    # grab global references to the output frame and lock variables
    global outputFrame, lock
    # loop over frames from the output stream
    while True:
        # wait until the lock is acquired
        with lock:
            # check if the output frame is available, otherwise skip
            # the iteration of the loop
            if outputFrame is None:
                continue
            # encode the frame in JPEG format
            (flag, encodedImage) = cv2.imencode(".jpg", outputFrame)
            # ensure the frame was successfully encoded
            if not flag:
                continue
        # yield the output frame in the byte format
        yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + bytearray(encodedImage) + b'\r\n')


@app.route("/video_feed")
def video_feed():
    return Response(generate(), mimetype="multipart/x-mixed-replace; boundary=frame")

@app.route("/movies", methods=["GET"])
def get_movie():
    return send_from_directory('./media/',"small.mp4",conditional=True,)

if __name__ == '__main__':

    t = threading.Thread(target=play)
    t.daemon = True
    t.start()

    # start the flask app
    app.run(host="0.0.0.0", port=8000, debug=True, threaded=True, use_reloader=False)

# release the video stream pointer
#vs.stop()
cap.release()
'''
import socket
import numpy as np
import cv2 as cv

addr = ("224.1.1.1",3000)
#addr = ("127.0.0.1", 65534)
buf = 512
width = 640
height = 480
cap = cv.VideoCapture('./media/small.mp4')
code = 'start'
code = ('start' + (buf - len(code)) * 'a').encode('utf-8')


if __name__ == '__main__':
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.IPPROTO_IP,socket.IP_MULTICAST_TTL,1)
    #s.bind(addrG)
    while(cap.isOpened()):
        ret, frame = cap.read()
        if ret:
            s.sendto(code, addr)
            data = frame.tostring()
            for i in range(0, len(data), buf):
                s.sendto(data[i:i+buf], addr)
            # cv.imshow('send', frame)
            # if cv.waitKey(1) & 0xFF == ord('q'):
                # break
        else:
            break
    # s.close()
    # cap.release()
    # cv.destroyAllWindows()