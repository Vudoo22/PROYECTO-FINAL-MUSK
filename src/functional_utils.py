def filter_sales_by_category(sales, category):
    return list(filter(lambda s: s.category == category, sales))

def top_client_by_category(sales_list):
    counts = {}

    categorySalesByClient = dict()
    for sale in sales_list:
        if sale.client_id in categorySalesByClient:
            categorySalesByClient[sale.client_id] += 1
        else:
            categorySalesByClient[sale.client_id] = 1
    
    return max(categorySalesByClient, key=categorySalesByClient.get)