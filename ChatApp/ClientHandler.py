import socket
import sys
import select
import errno

IP = socket.gethostname()
PORT = 2017
ADDRESS = (IP, PORT)

HEADER_SIZE = 10


class ClientHandler:
    def __init__(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect(ADDRESS)
        self.client_socket.setblocking(False)

        # self.my_username = input('Username: ')
        # self.my_username = myusername
        # username = self.my_username.encode('utf-8')
        # username_header = f'{len(username):<{HEADER_SIZE}}'.encode('utf-8')
        # self.client_socket.send(username_header + username)

    def set_username(self, username):
        self.my_username = username
        username = self.my_username.encode('utf-8')
        username_header = f'{len(username):<{HEADER_SIZE}}'.encode('utf-8')
        self.client_socket.send(username_header + username)

    def send_message(self, message):
        if message:
            message = message.encode('utf-8')
            message_header = f'{len(message):<{HEADER_SIZE}}'.encode('utf-8')

            self.client_socket.send(message_header + message)


    def receive_message(self):
        try:
            # receive username
            username_header = self.client_socket.recv(HEADER_SIZE)
            if not len(username_header):
                print('[CONNECTION CLOSED BY THE SERVER]')
                sys.exit()

            username_length = int(username_header.decode('utf-8'))
            username = self.client_socket.recv(username_length).decode('utf-8')

            # receive message
            message_header = self.client_socket.recv(HEADER_SIZE)
            message_length = int(message_header.decode('utf-8'))
            message = self.client_socket.recv(message_length).decode('utf-8')

            print(f'{username} > {message}')

            return username, message

        except IOError as e:
            if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
                print('Reading Error', str(e))
                sys.exit()
            # continue

        except Exception as e:
            print('General Error', str(e))
            sys.exit()


    def loop(self):
        while True:
            message = input(f'{self.my_username} > ')

            self.send_message(message)

            self.receive_message()


if __name__ == "__main__":
    client_handler = ClientHandler()
    client_handler.loop()