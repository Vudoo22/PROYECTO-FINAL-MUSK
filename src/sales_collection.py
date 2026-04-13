import pandas as pd

class SalesCollection:
    def __init__(self, sales=None):
        if sales is not None:
            self.sales = sales 
        else:
            self.sales = []
    
    def add(self, sale):
        self.sales.append(sale)

    def sales_by_client(self, client_id):
        sales = []
        for sale in self.sales:
            if sale.client_id == client_id:
                sales.append(sale)
        return sales

    def total_amount_by_client(self, client_id):
        amount = 0
        for sale in self.sales:
            if sale.client_id == client_id:
                amount += sale.amount
        return amount

    def total_amount_by_category(self, df, category):
        return float(df.groupby("category")["amount"].sum().get(category, 0))

    def average_sale_by_client(self, client_id):
        if len(self.sales_by_client(client_id)) == 0:
            return 0
        else:
            averageSale = self.total_amount_by_client(client_id) / len(self.sales_by_client(client_id))
        return averageSale
