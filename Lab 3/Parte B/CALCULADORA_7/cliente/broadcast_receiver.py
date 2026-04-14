import json
import servidor
import socket
import threading
from time import sleep
from servidor.lista_clientes.lista_clientes import ListaCliente
class BroadcastReceiver(threading.Thread):
    def __init__(self, connection):
        super().__init__()
        self.connection = connection
#----------interaction with sockets ---------------
    def receive_str(self, connect, n_bytes: int) -> str:
        """
        :param n_bytes: The number of bytes to read from the current connection
        :return: The next string read from the current connection
        """
        data = connect.recv(n_bytes)
        return data.decode()

    def send_str(self, connect, value: str) -> None:

        connect.send(value.encode())

    def send_int(self, connect: socket.socket, value: int, n_bytes: int) -> None:

        connect.send(value.to_bytes(n_bytes, byteorder="big", signed=True))

    def receive_int(self, connect: socket.socket, n_bytes: int) -> int:

        data = connect.recv(n_bytes)
        return int.from_bytes(data, byteorder='big', signed=True)

    # TODO
    # Implement a method that sends and object and returns an object.
    # ...
    def send_object(self, connection, obj):
        """1º: envia tamanho, 2º: envia dados."""
        data = json.dumps(obj).encode('utf-8')
        size = len(data)
        self.send_int(connection, size, servidor.INT_SIZE)  # Envio do tamanho
        connection.send(data)  # Envio do objeto

    def receive_object(self, connection):
        """1º: lê tamanho, 2º: lê dados."""
        size = self.receive_int(connection, servidor.INT_SIZE)  # Recebe o tamanho
        data = connection.recv(size)  # Recebe o objeto
        return json.loads(data.decode('utf-8'))


    def run(self):
        while True:
            try:
                dados = self.receive_object(self.connection)
                print(dados)
            except Exception as e:
                print("Loading broadcast data...")