import socket
from threading import Thread
from os import system

nickname = 'heqi'
HOST = 'home.data.onl'
PORT = 4362
HOST_SEND = ''
PORT_SEND = 2262


def cli():
    ...


def receive():
    while True:
        x = s.recv(1024).decode('utf-8')
        if not x:
            print('\033[1;31mConnection lost.\033[0m')
            global status
            status = False
            break
        print('\r\033[K' + x)


def block_input():
    print('\033[?25l', end='')
    while True:
        input()
        print('\033[1A\033[K', end='')


system('clear')
if __name__ == '__main__':
    status = True
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.connect((HOST, PORT))
        except ConnectionRefusedError:
            print('\033[1;31mConnection refused.\033[0m')
            exit()
        s.send(nickname.encode('utf-8'))
        Thread(target=receive).start()
        Thread(target=block_input).start()
        while status:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s_send:
                s_send.bind((HOST_SEND, PORT_SEND))
                s_send.listen(1)
                conn, addr = s_send.accept()
                with conn:
                    while status:
                        msg = conn.recv(1024)
                        if not msg: break
                        s.send(msg)
