import socket
import threading

class ChatClient:
    def __init__(self, host='127.0.0.1', port=8080):
        self.server_addr = (host, port)
        self.client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect_to_server(self):
        try:
            self.client_sock.connect(self.server_addr)
            print(f'Connected to {self.server_addr[0]}:{self.server_addr[1]}')

            receive_thread = threading.Thread(target=self.receive_data)
            receive_thread.start()

            self.send_messages()
        except Exception as e:
            print("서버 연결 중 오류 발생:", e)

    def send_messages(self):
        try:
            while True:
                data = input('')
                if data == 'q':
                    self.client_sock.send('quit_sign'.encode('cp949'))  # 서버에게 종료 신호를 보냄
                    break
                self.client_sock.send(data.encode('cp949'))
        except Exception as e:
            print("메시지 송신 중 오류 발생:", e)

    def receive_data(self):
        try:
            while True:
                recv_data = self.client_sock.recv(1024)
                if not recv_data:
                    break
                print(recv_data.decode('cp949'))
        except Exception as e:
            print("메시지 수신 중 오류 발생:", e)

if __name__ == "__main__":
    chat_client = ChatClient()
    chat_client.connect_to_server()