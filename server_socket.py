from socket import *
import threading

client_count = 0
lock = threading.Lock()
is_server_running = True

def multi_client(client_sock, client_addr, client_count_lock):
    global client_count, is_server_running

    with client_count_lock:
        client_count += 1

    print(str(client_addr), '에서 접속이 확인됐습니다.')
    while True:
        data = client_sock.recv(1024)
        if not data:
            print('클라이언트 연결 종료: ',client_addr)
            break
        data = data.decode('cp949')
        print(f'({client_addr}) 받은 데이터: ',data)
        client_sock.send(f'{data} has received.'.encode('cp949'))
    client_sock.close()

    with client_count_lock:
        client_count -= 1
        if client_count == 0:
            print("모든 클라이언트 연결 종료, 서버 종료;")
            is_server_running = False
            server_sock.close()

server_sock = socket(AF_INET, SOCK_STREAM)
server_addr = ('localhost', 8080)
print('Start up on {} port {}'.format(*server_addr))

server_sock.bind(server_addr)
server_sock.listen()

try:
    while is_server_running:
        try:
            client_sock, client_addr = server_sock.accept()
            if not is_server_running:
                break
            client_thread = threading.Thread(target=multi_client, args=(client_sock, client_addr, lock))
            client_thread.start()
        except OSError:
            break
except Exception as e:
    print("서버 오류:", e)
finally:
    server_sock.close()
    print("서버 종료")