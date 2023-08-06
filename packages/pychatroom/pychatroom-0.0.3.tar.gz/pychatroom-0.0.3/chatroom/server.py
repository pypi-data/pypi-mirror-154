import socket
from threading import Thread

HOST = ''
PORT = 4362
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


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        while True:
            conn, addr = s.accept()
            book[conn] = [addr, id]
            Thread(target=client_handler, args=(conn, id)).start()
            id += 1
