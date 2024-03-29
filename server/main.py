import socket
from multiprocessing import Queue, Process
import threading
from message_handler import message_handler

def handle_client(client_socket, address, queue):
    while True:
        data = client_socket.recv(1024)
        message = data.decode('utf-8')
        if not message:
            break
        queue.put((client_socket, address, message))




def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = '127.0.0.1'
    port = 12345
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"Server listening at {host}:{port}")
    try:
        message_queue =  Queue()
        p = Process(target=message_handler, args=(message_queue,))
        p.start()

        while True:
            client_socket, client_address = server_socket.accept()
            print(f"Accepted connection from {client_address}")
            client_handler = threading.Thread(target=handle_client, args=(client_socket, client_address, message_queue))
            client_handler.start()
    except Exception as e:
        server_socket.close()
        raise e

if __name__ == "__main__":
    main()