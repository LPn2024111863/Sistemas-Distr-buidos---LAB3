import json
import servidor
import socket
import threading
from servidor.operacoes.somar import Somar
from servidor.dados.dados import Dados
class ProcessaCliente(threading.Thread):
    def __init__(self, connection, address, dados):
        super().__init__()
        self.connection = connection
        self.address = address
        self.sum = Somar()
        self.dados = dados
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
        print(self.address, "Thread iniciada")
        last_request = False
        while not last_request:
            request_type = self.receive_str(self.connection, servidor.COMMAND_SIZE)
            if request_type == servidor.ADD_OP:
                x = self.receive_int(self.connection, servidor.INT_SIZE)
                y = self.receive_int(self.connection, servidor.INT_SIZE)
                print(f"[{self.address}] Somar: {x} + {y}")
                result = self.sum.execute(x, y)
                self.send_int(self.connection, result, servidor.INT_SIZE)
                self.dados.registar_oper("+", x, y, result, self.address)
                for key in self.dados.operacoes:
                    print(key, self.dados.operacoes[key])
            elif request_type == servidor.SUB_OP:
                pass
            elif request_type == servidor.END_OP:
                last_request = True
                print(self.address, "Thread terminada")
                self.connection.close()
