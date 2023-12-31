from socket import *

server_sock = socket(AF_INET, SOCK_STREAM)

server_addr = ('localhost', 8080)
print('Start up on {} port {}'.format(*server_addr))

server_sock.bind(server_addr)
server_sock.listen()

while True:
    print('accept wait')
    client_sock, client_addr = server_sock.accept()
    print(str(client_addr),'에서 접속이 확인되었습니다.')

    while True:
        data = client_sock.recv(1024)
        if not data:
            print('클라이언트 연결 종료')
            break
        data = data.decode('cp949')
        print('받은 데이터 : ', data)
        client_sock.send(f'{data} has received.'.encode('cp949'))

    client_sock.close()
    break

server_sock.close()
print("서버 종료")