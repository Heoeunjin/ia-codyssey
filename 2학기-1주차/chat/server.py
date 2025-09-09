import socket
import threading

HOST = '0.0.0.0'
PORT = 12345

clients = {}  # conn -> name

def broadcast(message, exclude_conn=None):
    for conn in clients:
        if conn != exclude_conn:
            try:
                conn.sendall(message.encode())
            except:
                pass

def send_private(sender, target_name, message):
    for conn, name in clients.items():
        if name == target_name:
            try:
                conn.sendall(f'(귓속말) {sender}> {message}'.encode())
            except:
                pass
            return
    sender_conn = get_conn_by_name(sender)
    if sender_conn:
        sender_conn.sendall(f'[서버] 대상 사용자 "{target_name}" 없음.'.encode())

def get_conn_by_name(name):
    for conn, uname in clients.items():
        if uname == name:
            return conn
    return None

def handle_client(conn):
    try:
        conn.sendall('이름을 입력하세요: '.encode())
        name = conn.recv(1024).decode().strip()
        clients[conn] = name
        broadcast(f'[서버] {name}님이 입장하셨습니다.')

        while True:
            data = conn.recv(1024).decode()
            if not data or data.strip() == '/종료':
                break

            if data.startswith('/to '):
                try:
                    _, target, msg = data.split(' ', 2)
                    send_private(name, target, msg)
                except ValueError:
                    conn.sendall('[서버] 사용법: /to 사용자이름 메시지'.encode())
            else:
                broadcast(f'{name}> {data}', exclude_conn=conn)
    except:
        pass
    finally:
        if conn in clients:
            broadcast(f'[서버] {clients[conn]}님이 퇴장하셨습니다.')
            del clients[conn]
        conn.close()

def start_server():
    print('[서버] 시작됨...')
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        while True:
            conn, addr = s.accept()
            threading.Thread(target=handle_client, args=(conn,), daemon=True).start()

if __name__ == '__main__':
    start_server()
