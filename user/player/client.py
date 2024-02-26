import socket
from multiprocessing import Queue

def setup_client(send_queue: Queue, recv_queue:Queue, port=54321):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.bind(('0.0.0.0', port))
    host = '127.0.0.1'
    port = 12345
    client_socket.connect((host, port))
    try:
        while True:
            message = send_queue.get()
            client_socket.sendall(message.encode())
            data = client_socket.recv(1024)
            response = data.decode('utf-8')
            recv_queue.put(response)
    except Exception as e:
        client_socket.close()
        raise e

if __name__ == "__main__":
    setup_client()