import socket

class ChatClient:
    def __init__(self, host='127.0.0.1', port=8080):
        self.server_addr = (host, port)
        self.client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect_to_server(self):
        try:
            self.client_sock.connect(self.server_addr)
            print(f'Connected to {self.server_addr[0]}:{self.server_addr[1]}')
            self.handle_communication()
        except Exception as e:
            print("서버 연결 중 오류 발생:", e)
        finally:
            self.client_sock.close()
            print("클라이언트 종료")

    def handle_communication(self):
        try:
            while True:
                data = input('메시지 입력: ')
                if data == 'q':
                    break
                self.send_data(data)
                self.receive_data()
        except Exception as e:
            print("데이터 송수신 중 오류 발생:", e)

    def send_data(self, data):
        try:
            self.client_sock.send(data.encode('cp949'))
            print('메시지 전송됨.')
        except Exception as e:
            print("메시지 전송 중 오류 발생:", e)

    def receive_data(self):
        try:
            recv_data = self.client_sock.recv(1024)
            if not recv_data:
                print("서버로부터 연결이 종료되었습니다.")
                return
            print(recv_data.decode('cp949'))
        except Exception as e:
            print("메시지 수신 중 오류 발생:", e)

if __name__ == "__main__":
    chat_client = ChatClient()
    chat_client.connect_to_server()