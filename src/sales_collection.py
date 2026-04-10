class SalesCollection:
    def __init__(self):
        self.sales = []
    
    def add(self, sale):
        self.sales.append(sale)

    def sales_by_client(self, client_id):
        sales = 0
        for sale in self.sales:
            if sale.client_id == client_id:
                sales += 1
        return sales

    def total_amount_by_client(self, client_id):
        amount = 0
        for sale in self.sales:
            if sale.client_id == client_id:
                amount += sale.amount
        return amount

    def total_amount_by_category(self, category):
        pass

    def average_sale_by_client(self, client_id):
        averageSale = self.total_amount_by_client(client_id) / self.sales_by_client(client_id)
        return averageSale