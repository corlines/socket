import socket
from _thread import *
from os.path import exists
import sys

client_sockets = []


HOST = socket.gethostbyname(socket.gethostname())
PORT = 9999 



def threaded(client_socket, addr):
    print('>> Connected by :', addr[0], ':', addr[1])


    while True:
        try:

            data = client_socket.recv(1024)
            #byte
            
            recv_data = data.decode()



            
            # threaded 함수 내의 /sendfile 처리 부분 수정
            if data.startswith(b'/sendfile '):
                print('파일 받았다')
                filename = data[len(b'/sendfile '):].decode()
                receive_file(client_socket, filename)

            if not recv_data:
                print('>> Disconnected by ' + addr[0], ':', addr[1])
                print('a')

                print('>> Received from ' + addr[0], ':', addr[1], recv_data.encode())

            print('>> Received from ' + addr[0], ':', addr[1], recv_data.encode())

            for client in client_sockets:
                if client != client_socket:
                    client.send(recv_data)
        
        except ConnectionResetError as e:
            print('>> Disconnected by ' + addr[0], ':', addr[1])
    
    if client_socket in client_sockets:
        client_sockets.remove(client_socket)
        print('remove client list : ', len(client_sockets))

    client_socket.close()

def receive_file(client_socket, filename):
    try:
        with open(filename, 'wb') as file:
            while True:
                file_data = client_socket.recv(1024)
                if not file_data:
                    print('b')
                    break
                file.write(file_data)
                break
            print(f'Successfully received {filename}')
            # 클라이언트에게 파일 수신 완료 메시지를 전송
            client_socket.send(b'File received successfully.')
    except Exception as e:
        print(f'Error receiving file: {e}')
        # 클라이언트에게 오류 메시지를 전송
        client_socket.send(f'Error receiving file: {e}'.encode())
print('>> Server Start with ip :', HOST)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((HOST, PORT))
server_socket.listen(5)


try:
    while True:
        print('>> Wait')

        client_socket, addr = server_socket.accept()
        client_sockets.append(client_socket)
        start_new_thread(threaded, (client_socket, addr))
        print("참가자 수 : ", len(client_sockets))

except Exception as e:
    print('에러 : ', e)

finally:
    print("서버를 닫음")
    server_socket.close()