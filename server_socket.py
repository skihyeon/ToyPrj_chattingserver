import socket
import threading

class ChatServer:
    def __init__(self, host='localhost', port=8080):
        self.server_addr = (host, port)
        self.server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_count = 0
        self.lock = threading.Lock()
        self.is_server_running = True
        self.clients = []
        self.client_nicknames = {}

    def start_server(self):
        print(f'Starting server on {self.server_addr[0]} port {self.server_addr[1]}')
        self.server_sock.bind(self.server_addr)
        self.server_sock.listen()
        self.accept_clients()

    def accept_clients(self):
        try:
            while self.is_server_running:
                try:
                    client_sock, client_addr = self.server_sock.accept()
                    if not self.is_server_running:
                        break
                    client_thread = threading.Thread(target=self.handle_client, args=(client_sock, client_addr))
                    client_thread.start()
                except OSError:
                    break
        except Exception as e:
            print(f"서버 오류:{e}", )
        finally:
            self.server_sock.close()
            print("서버 종료")

    def handle_client(self, client_sock, client_addr):
        nickname = client_sock.recv(1024).decode('cp949')
        welcome_message = f"{nickname}님이 입장하셨습니다."
        self.broadcast_message(welcome_message, None)

        with self.lock:
            self.client_nicknames[client_sock] = nickname
            self.client_count += 1
            self.clients.append(client_sock)

        print(f'{client_addr}에서 닉네임 {nickname}으로 접속이 확인됐습니다.')
        try:
            while True:
                data = client_sock.recv(1024)
                if not data or data.decode('cp949') == 'quit_sign':
                    leave_message = f"{nickname}님이 퇴장하셨습니다."
                    self.broadcast_message(leave_message, None)
                    print(f'클라이언트 연결 종료:{client_addr}, {nickname}')
                    break
                data = data.decode('cp949')
                print(f'({client_addr}, {nickname}) 받은 데이터: {data}')
                self.broadcast_message(data, client_sock)
        except Exception as e:
            print(f'오류 발생: {e}')
        finally:
            client_sock.close()
            with self.lock:
                self.client_count -= 1
                self.clients.remove(client_sock)
                del self.client_nicknames[client_sock]
                if self.client_count == 0:
                    print("모든 클라이언트 연결 종료, 서버 종료;")
                    self.is_server_running = False
                    self.server_sock.close()

    def broadcast_message(self, message, sender_sock, is_leave=False):
        if sender_sock is None:
            message_w_nickname = f"Server: {message}"  # 서버에서 보낸 메시지 처리
        else:
            nickname = self.client_nicknames.get(sender_sock, "Unknown")
            message_w_nickname = f"{nickname}: {message}"  # 클라이언트에서 보낸 메시지 처리

        for client in self.clients:
            if client != sender_sock or is_leave:
                try:
                    client.send(message_w_nickname.encode('cp949'))
                except Exception as e:
                    print(f'메시지 전송 중 오류: {e}')


if __name__ == "__main__":
    chat_server = ChatServer()
    chat_server.start_server()
