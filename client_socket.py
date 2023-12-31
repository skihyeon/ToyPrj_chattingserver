from socket import *

client_sock = socket(AF_INET, SOCK_STREAM)

server_addr = ('127.0.0.1', 8080)
client_sock.connect(server_addr)
print('{},{} 연결 됐습니다.'.format(*server_addr))

try:
    while True:
        data = input('')
        if data == 'q':
            break
        data = data.encode('cp949')
        client_sock.send(data)
        print('메시지를 전송했습니다.')

        recv_data = client_sock.recv(1024)
        print(recv_data.decode('cp949'))

except Exception as e:
    print("오류 발생:", e)
finally:
    client_sock.close()