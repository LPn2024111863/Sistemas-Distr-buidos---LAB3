class ListaCliente:
    def __init__(self):
        self.clientes = []

    def connect(self, address):
        self.clientes.append(address)

    def disconnect(self, address):
        for cliente in self.clientes:
            if cliente == address:
                self.clientes.remove(address)