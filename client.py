import socket
from alive_progress import alive_bar
import time
import os
import math
import concurrent.futures
import sys

size = 16
port = 5051
server = socket.gethostbyname(socket.gethostname())
address =(server, port)
chunk_size = 1024

def add_padding(data, sum_byte):
    if len(data) == sum_byte:
        return data
    return data + ' ' * (sum_byte - len(data))

def init():
    client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    client.connect(address)
    return client

#xử lý lấy tổng dung lượng file và gửi dung lượng file
def send_header_to_server(client, name_file):
    file = open(name_file,"rb")
    file.seek(0,os.SEEK_END)
    file_size = file.tell()
    file.seek(0)
    file_size_string = str(file_size)
    file_size_string = add_padding(file_size_string,16)
    client.send(add_padding(name_file, 1024).encode())
    client.send(file_size_string.encode())
    return file_size

#nhận dữ liệu từ server
def client_receive_signal(client):
    return client.recv(9)

stop_signal = "NOTENOUGH"

def send_content_to_server(client, name_file, file_size):
    file = open(name_file,"rb")
    while True:
        #tạo thanh % t
        numberOfRepeat =math.ceil(file_size/ chunk_size)
        with alive_bar(numberOfRepeat, title="Downloading") as bar:
            for _ in range(numberOfRepeat):
                chunk = file.read(chunk_size)  
                if not chunk:
                    break  
                client.send(chunk)
                time.sleep(0.0000000005) 
                bar()
            break
    # tạo timeout
    # with concurrent.futures.ThreadPoolExecutor() as executor:
    #     future = executor.submit(client_receive_signal)
    # try:
    #     message = future.result(timeout=5) 
    #     if message == stop_signal:
    #         break
    # except concurrent.futures.TimeoutError:
    #     break
def main():
    client = init()
    #gửi mode
    mode = "upload  " # chưa có download

    name_file = input("Input name file to upload:")
    client.send(mode.encode())
    file_size = send_header_to_server(client, name_file)
    send_content_to_server(client,name_file,file_size)


    
if __name__ == '__main__':
    main()