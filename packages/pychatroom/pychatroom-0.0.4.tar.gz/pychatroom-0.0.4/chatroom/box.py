import socket
from . import client
import readline


def main():
    print('\033[?25h', end='')
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.connect((client.HOST_SEND, client.PORT_SEND))
            except ConnectionRefusedError:
                print('\033[1;31mText box connection failed.\033[0m')
                exit()
            while True:
                msg = input()
                print('\033[1A\033[K', end='')
                s.send(msg.encode('utf-8'))
    except (KeyboardInterrupt, EOFError):
        print()
