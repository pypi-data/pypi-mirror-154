from argparse import ArgumentParser
import socket
from threading import Thread
import platform
from os import system


def main():
    global args, parser_join, parser_box
    parser = ArgumentParser()
    parser.set_defaults(func=parser.print_usage)
    subparsers = parser.add_subparsers()

    parser_serve = subparsers.add_parser('serve', help='serve a chatroom')
    parser_serve.set_defaults(func=serve)
    parser_serve.add_argument('-p', '--port', type=int, default=4362, metavar='bind_port', help='the port to bind')

    parser_join = subparsers.add_parser('join', help='join a chatroom')
    parser_join.set_defaults(func=join)
    parser_join.add_argument('nickname', help='your nickname')
    parser_join.add_argument('-d', '--destination', metavar='host[:port]', default='localhost:4362', help='the host running the chatroom (default localhost[:4362])')
    parser_join.add_argument('-b', '--box-port', type=int, default=2262, metavar='bind_port', help='the port to accept input from a chatroom box (default 2262)')

    parser_box = subparsers.add_parser('box', help='open a text box and connect it to a host')
    parser_box.set_defaults(func=box)
    parser_box.add_argument('-d', '--destination', metavar='host[:port]', default='localhost:2262', help='the host to connect the box to')

    args = parser.parse_args()
    args.func()


def cls():
    os = platform.system()
    if os == 'Darwin':
        system('clear')
    elif os == 'Windows':
        system('cls')


def parse_hostname(default_port, argparser):
    global HOST, PORT
    HOST = (DEST := args.destination.split(':'))[0]
    if len(DEST) == 1:
        PORT = default_port
    elif len(DEST) == 2:
        PORT = int(DEST[1])
    else:
        argparser.error('invalid hostname ' + args.destination)


def serve():
    HOST = ''
    book = {}
    id = 0

    def prompt(txt, style='public'):
        formatted = {
            'public': f'\033[1;36m{txt}\033[0m',
            'private': f'\033[1;35m{txt}\033[0m',
            'error': f'\033[1;31m{txt}\033[0m'
        }
        return formatted[style].encode('utf-8')

    def message(msg, nickname, id):
        return f'\033[32m{nickname}[\033[1m{id}\033[0;32m]\033[0m {msg}'.encode('utf-8')

    def broadcast(x):
        for conn in book:
            conn.send(x)

    def client_handler(conn, id):
        nickname = conn.recv(1024).decode('utf-8')
        if not (nickname.isalnum() and not nickname.isdigit()):
            conn.send(prompt('Invalid nickname.', 'error'))
            conn.close()
            return
        conn.send(prompt('You are now in the chat room.', 'private'))
        book[conn].append(nickname)
        broadcast(prompt(f'{nickname}[{id}] has joined the chat.'))
        while True:
            msg = conn.recv(1024).decode('utf-8')
            if not msg:
                del book[conn]
                conn.close()
                broadcast(prompt(f'{nickname}[{id}] has left the chat.'))
                break
            for char in '\a\b\f\n\r\t\v\0':
                msg = msg.replace(char, '')
            if msg.isspace():
                continue
            broadcast(message(msg, nickname, id))

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, args.port))
        s.listen()
        while True:
            conn, addr = s.accept()
            book[conn] = [addr, id]
            Thread(target=client_handler, args=(conn, id)).start()
            id += 1


def join():
    parse_hostname(4362, parser_join)
    HOST_BOX = ''

    def receive():
        while True:
            x = s.recv(1024).decode('utf-8')
            if not x:
                print('\033[1;31mConnection lost.\033[0m\033[?25h')
                global status
                status = False
                break
            print('\r\033[K' + x)

    def block_input():
        print('\033[?25l', end='')
        while status:
            input()
            print('\033[1A\033[K', end='')

    status = True
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.connect((HOST, PORT))
        except ConnectionRefusedError:
            print('\033[1;31mConnection refused.\033[0m\033[?25h')
            return
        cls()
        s.send(args.nickname.encode('utf-8'))
        Thread(target=receive).start()
        Thread(target=block_input).start()
        while status:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s_send:
                s_send.bind((HOST_BOX, args.box_port))
                s_send.listen(1)
                conn, addr = s_send.accept()
                with conn:
                    while status:
                        msg = conn.recv(1024)
                        if not msg: break
                        s.send(msg)


def box():
    parse_hostname(2262, parser_box)
    print('\033[?25h', end='')
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.connect((HOST, PORT))
            except ConnectionRefusedError:
                print('\033[1;31mConnection failed.\033[0m')
                return
            cls()
            while True:
                msg = input()
                print('\033[1A\033[K', end='')
                s.send(msg.encode('utf-8'))
    except (KeyboardInterrupt, EOFError):
        print()



if __name__ == '__main__':
    main()
