import socket
from _thread import *
import socket
import sys
import typing


HOST = socket.gethostbyname(socket.gethostname()) #자신의 socket host를 저장(ip저장)
PORT = 9999 #호스트 내에서 실행되고 있는 프로세스를 구분하기 위한


client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT)) #HOST 와 PORT를 연결함


def recv_data(client_socket): #서버와의 연결이 연결되었거나 끊어지는걸 보여줌
    while True:
        data = client_socket.recv(1024) #소켓으로부터 들어오는 데이터를 수신한다
        if not data: #테이터가 수집이 안된다면
            print("서버와의 연결이 끊어졌습니다.")
            break #끝냄
        print("Received: " + data.decode()) #


start_new_thread(recv_data, (client_socket,)) #recv함수를 실행함
print('>> 서버에 연결되었습니다.')


def send_file(client_socket, filename): #파일보내는 함수
    try: #시도
        with open(filename, 'rb') as file:
            file_data = file.read()
            client_socket.sendall(b'/sendfile ' + filename.encode())  # 파일 이름을 서버로 전송
            client_socket.sendall(file_data)  # 파일 데이터를 서버로 전송
        print(f'{filename} 파일을 성공적으로 보냈습니다.')
    except FileNotFoundError: #파일을 찾을수 없다면
        print(f'파일을 찾을 수 없습니다: {filename}')
    except Exception as e: #에러 낫을때
        print(f'에러 발생: {e}')


while True:
    message = input("메시지를 입력하세요: ")


    if message == '/quit':
        client_socket.send(message.encode())
        break


    if message.startswith('/sendfile'):
        filename = message[len('/sendfile '):]
        send_file(client_socket, filename)
    else:
        client_socket.send(message.encode())


client_socket.close()

