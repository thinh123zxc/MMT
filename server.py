import socket
import os
import threading

ENCODING = 'utf-8'
PORT_SERVER = 5051
HOST_SERVER = socket.gethostbyname(socket.gethostname())
LENGTH = 64
BUFFER = 1024
ADDRESS_SERVER = (HOST_SERVER, PORT_SERVER)

#Init
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#Init server
def init_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(ADDRESS_SERVER)
    server_socket.listen(10)
    return server_socket

#Listening
def listening(server_socket):
    print(f'Server is lisening: HOST {HOST_SERVER}')
    while True:
        conn, adrr = server_socket.accept()
        print(f'{adrr} connected')
        mode = conn.recv(8).decode().strip()
        if mode == 'upload':
            client_thread = threading.Thread(target= respone_upload, args= (conn, ))
            client_thread.start()
        elif mode == 'download':
            client_thread = threading.Thread(target= respone_download, args= (conn, ))
            client_thread.start()
def response_download(connection):
    pass
def process_name_file(name_file):
    processed_name_file = name_file
    i = 1
    while os.path.exists(processed_name_file):
        name, extension = os.path.splitext(name_file) 
        processed_name_file = f"{name}({i}){extension}"
        i += 1
    return processed_name_file


def respone_upload(connection):
    #Nhan name file
    name_file = connection.recv(1024).decode().strip()
    print(name_file)
    #Xu li name file
    name_file = process_name_file(name_file)
    #Nhan size
    file_size = int(connection.recv(16).decode().strip())
    print(file_size)
    #Nhan content
    with open(name_file, 'ab') as f:
        received_data = 0
        while received_data < file_size:
            data = connection.recv(BUFFER)
            if not data:
                if received_data < file_size:
                    connection.send('NOTENOUGH'.encode(ENCODING))
                    os.remove(name_file)
                    # connection.close()
                print('Het data')
                break
            received_data += len(data)
            f.write(data)
    connection.send('ENOUGH   '.encode(ENCODING))
    connection.close()

def respone_download(connection):
    #Nhan name file
    name_file = connection.recv(1024).decode().strip()
    if os.path.exists(name_file):
        os.path.getsize(name_file)
        connection.send(name_file.ljust(1024).encode(ENCODING))
        while True:
            with open(name_file, 'rb') as f:
                data = f.read(BUFFER)
                if not data:
                    break
                connection.send(data)
    else:
        connection.send('ERRORNOTFOUND'.encode(ENCODING))
        
    mess_from_client = connection.recv(13).decode().strip()
    if mess_from_client == 'NOTENOUGH':
        respone_download(connection)

def main():
    server_socket = init_server()
    listening(server_socket)
    
if __name__ == '__main__':
    main()