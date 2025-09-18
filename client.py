
import socket

HEADER = 64
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)
    
    # Wait for and print server response
    response = client.recv(2048).decode(FORMAT)
    print(f"[SERVER] {response}")

# Get input and send it
while True:
    msg = input("Enter message (or 'quit' to exit): ")
    send(msg)
    if msg.lower() == 'quit':
        send(DISCONNECT_MESSAGE)
        break

client.close()