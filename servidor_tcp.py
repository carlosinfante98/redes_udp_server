import socket
from _thread import *
import threading
from threading import Thread
import hashlib
import time
import os
from socketserver import ThreadingMixIn 
import datetime

# Multithreaded Python server : TCP Server Socket Thread Pool
class ClientThread(Thread): 
 
    def __init__(self,ip,port): 
        Thread.__init__(self) 
        self.ip = ip 
        self.port = port 
        print("[+] New server socket thread started for " + ip + ":" + str(port) )
 
    def run(self): 
        while True : 
            c_socket.send('prepared'.encode())
            msg = c_socket.recv(BUFFER_SIZE).decode()
            
            if msg == 'ok':
                print('Sending files to client ', self.ip)
                for filename in os.listdir(os.getcwd() + "/media"):
                    with open('./media/'+filename, "rb") as f:
                        l = f.read()
                        size = len(l)
                        packages = int(size/BUFFER_SIZE)
                        c_socket.send((filename+':'+str(size)).encode())
                        time.sleep(0.2)
                        #Send all the file
                        c_socket.sendall(l)
                        time.sleep(0.2)
                        #Hash gets created and sended
                        file_hashed = hash_file(filename)
                        print(file_hashed)
                        c_socket.send(file_hashed.encode())
                    resp = c_socket.recv(BUFFER_SIZE).decode()
                    if resp == 'received':
                        print("File received by client.")
                        log.write('File sent succesfully.\n')
                        log.write('Packages sent: {} - Packages received: {} - Packages transmitted: {}\n'.format(packages+1,packages+1,packages+1))
                        log.write('Bytes sent: {} - Bytes received: {}'.format(size,size))
                    else:
                        print('Hash doesn\'t match file.')
                    time.sleep(0.2)
                    file_time = round(float(c_socket.recv(BUFFER_SIZE).decode()),4)
                    time.sleep(0.25)
                    log.write("\nTransaction time for file {} with size {} bytes was: {} seg\n".format(filename, size, file_time))
                    time.sleep(0.2)
                c_socket.send('no_files'.encode())
                print('All files sent.')
                print('Connection terminated with client', self.ip)
                msg = c_socket.recv(BUFFER_SIZE).decode()
                log.close()

                if msg == 'exit':
                    break
        # print_lock.release()
        c_socket.close()

def hash_file(filename):

    hash = hashlib.sha256()
    with open('./media/'+filename, 'rb') as f:

        chunk = 0
        while chunk != b'':
            chunk = f.read(BUFFER_SIZE)
            hash.update(chunk)

    return hash.hexdigest()

if __name__ == '__main__':
    #Parametros de la conexion
    # print_lock=threading.Lock()
    port = 6789
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    host = socket.gethostname()
    s.bind((host,port))
    BUFFER_SIZE = 2048
    threads = []

    #Maximo 25 errores/usuarios antes de apagarse
    s.listen(25)

    print('Listening on port {} ...'.format(port))
    i = 1
    while True:
        # print_lock=threading.Lock()
        c_socket, (addr,c_port) = s.accept()
        print('Connected to client ', addr, ':', c_port) 
        # print_lock.acquire()#coge un thread
        new_thread = ClientThread(addr, c_port)
        log = open("TCPlog{}.txt".format(i), "w")
        log.write('Test {}\n'.format(i))
        log.write(str(datetime.datetime.now())+'\n')
        log.write('TCP connection with client {}:{}\n'.format(addr,c_port))
        i+=1
        new_thread.start()
        threads.append(new_thread)
        # start_new_thread(thread,(c_socket,(log,)))
    for t in threads:
        t.join()