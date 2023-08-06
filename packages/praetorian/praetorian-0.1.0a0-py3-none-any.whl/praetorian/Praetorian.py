import socket
import threading


class SocketException(Exception):
    pass


class ServerException(Exception):
    pass


class TestingSocket:
    """
    Contains specifications for the creation of clients with a specific socket for testing purposes.
    
    Socket object defaults to port 80.

    Required:
        target_host
    
    Optional:
        target_port
    """
    def __init__(self, target_host, target_port=80):
        self.target_host = target_host
        self.target_port = target_port
    

    def create_socket(self, socket_type='TCP') -> socket.socket:
        """
        Create a socket of the specified type. Currently supports TCP and UDP. Defaults to TCP.

        Parameters
        ----------
        socket_type -> str: The type of socket to create

        Returns
        ----------
        client -> socket: A socket object created to specifications
        """
        socket_store = {'TCP': socket.SOCK_STREAM, 'UDP': socket.SOCK_DGRAM}

        if socket_type not in socket_store.keys():
            raise SocketException(
                f'Specified socket type {socket_type} does not exist or is not yet implemented.'
            )
        
        client = socket.socket(socket.AF_INET, socket_store[socket_type])

        return client
    

    def connect_socket(self, client: socket.socket):
        """
        Connects the specified socket to the host
        """
        client.connect((self.target_host, self.target_port))
    

    def send_receive(self, client: socket.socket, payload: str):
        client.send


class TestingServer:
    def __init__(self, bind_ip, bind_port=9999, max_backlog=5):
        self.bind_ip = bind_ip
        self.bind_port = bind_port
        self.max_backlog = max_backlog
    

    def initialize_server(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((self.bind_ip, self.bind_port))

        server.listen(self.max_backlog)
        print(f'[*] Listening on {self.bind_ip}:{self.bind_port}')

        return server
    

    def handle_client(self, client_socket: socket.socket):
        """
        Thread to handle client. Takes a socket object created from TestingSocket.
        """
        request = client_socket.recv(1024)
        print(f'[*] Received: {request}')

        client_socket.send('ACK')
        client_socket.close()


    def thread_client(self, server):
        while True:
            client, addr = server.accept()

            print(f'[*] Accepted connection from {addr[0]}:{addr[1]}')

            client_handler = threading.Thread(target=self.handle_client, args=(client,))
            client_handler.start()
