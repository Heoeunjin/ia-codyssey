import socket
import threading
import sys

HOST = '127.0.0.1'
PORT = 12345

def receive_messages(sock):
    while True:
        try:
            data = sock.recv(1024).decode()
            if not data:
                break
            print(data)
        except:
            break

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((HOST, PORT))

        threading.Thread(target=receive_messages, args=(sock,), daemon=True).start()

        while True:
            msg = input()
            if msg.strip() == '/종료':
                sock.sendall(msg.encode())
                break
            sock.sendall(msg.encode())

if __name__ == '__main__':
    main()
