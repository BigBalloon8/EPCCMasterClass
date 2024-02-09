import socket
from multiprocessing import Queue
from message_handler import ...

def setup_client(send_queue: Queue, recv_queue:Queue):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = '127.0.0.1'
    port = 12345
    client_socket.connect((host, port))
    try:
        while True:
            if not send_queue.empty():
                message = send_queue.get()
                client_socket.sendall(message)
                data = client_socket.recv(1024)
                response = data.decode('utf-8')
                recv_queue.put(response)
    except Exception as e:
        client_socket.close()
        raise e

if __name__ == "__main__":
    setup_client()