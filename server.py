import socket
import threading

HEADER = 64
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected")
    connected = True
    messages_received = 0
    u = None
    v = None
    
    while connected and messages_received < 2:
        try:
            msg_length = conn.recv(HEADER).decode(FORMAT)
            if msg_length:
                msg_length = int(msg_length)
                msg = conn.recv(msg_length).decode(FORMAT)
                
                if msg == DISCONNECT_MESSAGE:
                    connected = False
                    print(f"[{addr}] Client disconnected")
                else:
                    messages_received += 1
                    if messages_received == 1:
                        u = msg
                        print(f"[{addr}] Received u: {u}")
                    elif messages_received == 2:
                        v = msg
                        print(f"[{addr}] Received v: {v}")
                        print(f"[{addr}] Stored messages - u: {u}, v: {v}")
                    
                    response = f"Server received message {messages_received}"
                    conn.send(response.encode(FORMAT))
        except ConnectionResetError:
            print(f"[{addr}] Connection lost")
            connected = False
    
    print(f"[{addr}] Closing connection")
    conn.close()

def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")

print("[STARTING] Server is starting...")
start()