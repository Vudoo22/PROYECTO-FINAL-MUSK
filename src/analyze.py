import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.functional_utils import *
from src.client import Client
from src.sale import Sale
from src.client_collection import ClientCollection
from src.sales_collection import SalesCollection
from datetime import datetime
import json, pandas as pd

def generate_report():
    #Lectura de datos
    with open('data/clients.json', 'r') as datos:
        c = json.load(datos)

    sales_df = pd.read_csv('data/sales.csv')

    #iteración de objetos en las clases collection
    client_collection = ClientCollection()
    for i in c:
        new_client = Client(i['client_id'], i['name'], i['country'], i['signup_date'])
        client_collection.add(new_client)

    sales_collection = SalesCollection()
    for i, row in sales_df.iterrows():
        new_sale = Sale(sale_id = row['sale_id'], client_id = row['client_id'], product = row['product'], category = row['category'], amount = row['amount'], date = row['date'])
        sales_collection.add(new_sale)

    #10 cálculos
    #1º
    total_clients = 0
    for i in client_collection.clients:
        total_clients += 1

    #2º
    total_sales = 0
    for i in sales_collection.sales:
        total_sales += 1

    #3º
    total_spent = dict()
    for client in client_collection.clients:
        total_spent[client.client_id] = sales_collection.total_amount_by_client(client.client_id)

    #4º
    sale_count = dict()
    for client in client_collection.clients:
        sale_count[client.client_id] = len(sales_collection.sales_by_client(client.client_id))

    #5º
    average_sale = dict()
    for client in client_collection.clients:
        average_sale[client.client_id] = round(sales_collection.average_sale_by_client(client.client_id), 2)

    #6º
    #Conseguimo clientes por país
    ClientsByCountry = dict()
    for i in client_collection.clients:
        if i.country not in ClientsByCountry:
            ClientsByCountry[i.country] = client_collection.clients_by_country(i.country)

    topClientByCountry = dict()
    for country, clients_list in ClientsByCountry.items():
        AmountByClient = dict()
        for i in clients_list:
            AmountByClient[i.client_id] = sales_collection.total_amount_by_client(i.client_id)      #Hacemos diccionario para cada país con id de cliente y total de gasto

        topClientByCountry[country] = client_collection.get_client_by_id(max(AmountByClient, key = AmountByClient.get)).name           #Con el diccionario previamente creado, comparamos sus valores y guardamos la llave del cliente con mayor gasto en un diccionario país: id

    #7º
    total_electronics = sales_collection.total_amount_by_category(sales_df, "Electronics")
    total_accessories = sales_collection.total_amount_by_category(sales_df, "Accessories")

    #8º
    sales_electronics = filter_sales_by_category(sales_collection.sales, "Electronics")
    sales_accessories = filter_sales_by_category(sales_collection.sales, "Accessories")

    top_client_electronics_id = top_client_by_category(sales_electronics)
    top_client_accessories_id = top_client_by_category(sales_accessories)

    top_client_electronics_name = client_collection.get_client_by_id(top_client_electronics_id).name
    top_client_accessories_name = client_collection.get_client_by_id(top_client_accessories_id).name

    #9º
    MINIMUM_AMOUNT = 500
    high_spenders = list()
    for client in client_collection.clients:
        if sales_collection.total_amount_by_client(client.client_id) > MINIMUM_AMOUNT:
            high_spenders.append(client.name)

    #10º
    sales_df["date"] = pd.to_datetime(sales_df["date"])
    total_revenue = sales_df.groupby(sales_df["date"].dt.to_period("M"))["amount"].sum()
    monthly_sales = {str(k): float(v) for k, v in total_revenue.to_dict().items()}


    #Creación informe
    summary = {"total_clients": total_clients,
    "total_sales": total_sales,
    "total_revenue": float(sales_df['amount'].sum())
    }

    clients = []
    for i in client_collection.clients:
        clients.append(
            {
                "client_id": i.client_id,
                "name": i.name,
                "total_spent": total_spent[i.client_id],
                "sale_count": sale_count[i.client_id],
                "average_sale": average_sale[i.client_id]
            }
        )

    top_client_by_country = topClientByCountry

    sales_by_category = {
        "Electronics": total_electronics,
        "Accessories": total_accessories
    }

    high_spending_clients = high_spenders

    report_data = {
        "summary": summary,
        "clients": clients,
        "top_client_by_country": top_client_by_country,
        "sales_by_category": sales_by_category,
        "high_spending_clients": high_spending_clients,
        "monthly_sales": monthly_sales
    }

    return report_data

with open("data/report.json", "w") as f:
    json.dump(generate_report(), f, indent=4)
