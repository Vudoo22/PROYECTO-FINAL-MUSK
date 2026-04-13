class ClientCollection:
    def __init__(self):
        self.clients = []
    
    def add(self, client):
        self.clients.append(client)

    def get_client_by_id(self, id):
        for i in self.clients:
            if i.client_id == id:
                return i

    def clients_by_country(self, country):
        clientes = []
        for i in self.clients:
            if i.country == country:
                clientes.append(i)
        return clientes
