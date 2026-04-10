from functional_utils import *
import json, pandas as pd
from client import Client
from sale import Sale
from client_collection import ClientCollection
from sales_collection import SalesCollection

#Lectura de datos
with open('data/clients.json', 'r') as datos:
    clients = json.load(datos)

sales_df = pd.read_csv('data/sales.csv')

#iteración de objetos en las clases collection
client_collection = ClientCollection()
for i in clients:
    new_client = Client(i['client_id'], i['name'], i['country'], i['signup_date'])
    client_collection.add(new_client)

sales_collection = SalesCollection()
for i, row in sales_df.iterrows():
    new_sale = Sale(sale_id = row['sale_id'], client_id = row['client_id'], product = row['product'], category = row['category'], amount = row['amount'], date = ['date'])
    sales_collection.add(new_sale)

#10 cálculos
#1º
num_client = 0
for i in client_collection.clients:
    num_client += 1
print(num_client)

#2º
num_sales = 0
for i in sales_collection.sales:
    num_sales += 1
print(num_sales)

#3º
for client in client_collection.clients:
    print('client id: {}, amount: {}'.format(client.client_id, sales_collection.total_amount_by_client(client.client_id)))

#4º
for client in client_collection.clients:
    print('client id: {}, total sales: {}'.format(client.client_id, sales_collection.sales_by_client(client.client_id)))

#5º
for client in client_collection.clients:
    print('client id: {}, average sale: {}'.format(client.client_id, sales_collection.average_sale_by_client(client.client_id)))