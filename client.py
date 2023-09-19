import socket
import select
import sys
import threading

def user_input_thread(server):
    while True:
        message = sys.stdin.readline().strip()
        if message:
            if message == "@sair":
                print("Desconectando do servidor...")
                server.send(message.encode("utf-8"))
                break  
            elif message == "@ultimas_mensagens":
                server.send(message.encode("utf-8"))
            else:
                server.send(f"::Mensagem {message}".encode("utf-8"))

def server_receive_thread(server):
    while True:
        message = server.recv(2048).decode("utf-8")
        if message:
            if message.startswith("::Mensagem"):
                print(message[11:])
            else:
                print(message)

if len(sys.argv) < 2:
    print("usage: client SERVER_IP [PORT]")
    sys.exit(1)

ip_address = sys.argv[1]
port = int(sys.argv[2]) if len(sys.argv) > 2 else 19000

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.connect((ip_address, port))

# Inicia threads para entrada do usuário e recepção de mensagens do servidor
user_input_thread = threading.Thread(target=user_input_thread, args=(server,))
server_receive_thread = threading.Thread(target=server_receive_thread, args=(server,))

user_input_thread.start()
server_receive_thread.start()

user_input_thread.join()
server_receive_thread.join()

server.close()
