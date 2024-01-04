import socket
import threading

class ChatClient:
    def __init__(self, host='127.0.0.1', port=8080):
        self.server_addr = (host, port)
        self.client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.is_connected = True

    def connect_to_server(self):
        try:
            self.client_sock.connect(self.server_addr)
            nickname = input("Enter your nickname: ")
            self.client_sock.send(nickname.encode('cp949')) 
            print(f'Connected to {self.server_addr[0]}:{self.server_addr[1]}')

            receive_thread = threading.Thread(target=self.receive_data)
            receive_thread.start()

            self.send_messages()
        except Exception as e:
            print("서버 연결 중 오류 발생:", e)

    def send_messages(self):
        try:
            while self.is_connected:  # 플래그를 확인하여 루프를 제어
                data = input('')
                if data == 'q':
                    self.client_sock.send('quit_sign'.encode('cp949'))
                    break
                if self.is_connected:  # 소켓이 연결되어 있을 때만 메시지 전송
                    self.client_sock.send(data.encode('cp949'))
        except Exception as e:
            print("메시지 송신 중 오류 발생:", e)

    def receive_data(self):
        try:
            while True:
                recv_data = self.client_sock.recv(1024)
                if not recv_data:
                    break
                message = recv_data.decode('cp949')
                print(message)
                if message == "Server: 서버가 종료되었습니다.":
                    print("서버로부터 연결이 종료되었습니다.")
                    self.is_connected = False  # 연결 상태를 False로 설정
                    break
        except Exception as e:
            print("메시지 수신 중 오류 발생:", e)
        finally:
            self.client_sock.close()
            self.is_connected = False

if __name__ == "__main__":
    chat_client = ChatClient()
    chat_client.connect_to_server()