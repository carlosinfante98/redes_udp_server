import socket
import hashlib
import time

# server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

def hash_file(filename):

    hash = hashlib.sha256()
    with open('./mediaClient/'+filename, 'rb') as f:

        chunk = 0
        while chunk != b'':
            chunk = f.read(BUFFER_SIZE)
            hash.update(chunk)

    return hash.hexdigest()

port = 6789
host = socket.gethostname()
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect((host,port))
BUFFER_SIZE = 2048

msg = s.recv(BUFFER_SIZE).decode()
while msg != 'exit' :
    print("Connection established with TCP server")
    s.send('ok'.encode())
    name_size = s.recv(BUFFER_SIZE).decode()
    name_size = name_size.split(':')
    filename = name_size[0]
    size = int(name_size[1])
    while True:
        start = time.time()
        with open('./mediaClient/'+filename, 'wb') as f:
            print('File', filename, 'has been created...')
            # print('Receiving data...')
            while size > 0:
                data = s.recv(BUFFER_SIZE)
                f.write(data)
                size -= BUFFER_SIZE
        end = time.time()
        #Receives hash
        hash_rec = s.recv(BUFFER_SIZE).decode()
        hash_cal = hash_file(filename)
        if hash_rec == hash_cal:
            s.send('received'.encode())
        time.sleep(0.1)
        file_time = str(end-start)
        s.send(file_time.encode())
        print('File saved correctly.')
        name_size = s.recv(BUFFER_SIZE).decode()
        if name_size == 'no_files':
            break
        name_size = name_size.split(':')
        filename = name_size[0]
        size = int(name_size[1])
    s.send('exit'.encode())
    break
    
print('Connection terminated.')
s.close()