import threading

class ListaCliente:
    def __init__(self):
        self.clientes = {} # Dicionário {address: connection}
        self._lock = threading.Lock()

    def connect(self, connection, address):
        with self._lock:
            self.clientes[address] = connection

    def disconnect(self, address):
        with self._lock:
            if address in self.clientes:
                del self.clientes[address]