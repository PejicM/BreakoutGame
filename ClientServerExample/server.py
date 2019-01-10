import socket,pickle
import threading


class Person:
    def __init__(self, firstname, lastname):
        self.firstname = firstname
        self.lastname = lastname

    def __str__(self):
        return self.firstname + " " + self.lastname


bind_ip = '127.0.0.1'
bind_port = 9999

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((bind_ip, bind_port))
server.listen(5)  # max backlog of connections

print('Listening on {}:{}'.format(bind_ip, bind_port))


def handle_client_connection(client_socket):
    request = client_socket.recv(1024)
    p = pickle.loads(request)
    print('Received '+p.__str__())
    client_socket.send(pickle.dumps(p))
    client_socket.close()

while True:
    client_sock, address = server.accept()
    print('Accepted connection from {}:{}'.format(address[0], address[1]))
    client_handler = threading.Thread(
        target=handle_client_connection,
        args=(client_sock,)  # without comma you'd get a... TypeError: handle_client_connection() argument after * must be a sequence, not _socketobject
    )
    client_handler.start()