import csv
from woocommerce import API
import pandas as pd

wcapi = API(
    url="https://brew-hq.com",  # your store url
    consumer_key="ck_327ba843bf58f0c1694b0ed1d1807ced27ee0943",  # your consumer key
    consumer_secret="cs_901a004df48fe4ed1837462c6f430d18a89b12de",  # your consumer secret
    version="wc/v3"
)

def get_processing_invoices():
    page = 1
    while True:
        # Retrieve a batch of orders
        data = wcapi.get(f"orders?page={page}&per_page=100").json()
        if not data:
            break  # No more orders
        for order in data:
            # Check if the order is processing
            if order['status'] == 'processing':
                # Retrieve ordered products
                products = [item['name'] for item in order['line_items']]
                # Retrieve customer email and address
                email = order['billing']['email']
                address = f"{order['billing']['address_1']}, {order['billing']['address_2']}, {order['billing']['city']}, {order['billing']['state']}, {order['billing']['postcode']}, {order['billing']['country']}"
                yield order, products, email, address
        page += 1

# Prepare the CSV file
with open('invoices.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Invoice ID", "Date Created", "Total", "Currency", "Customer ID", "Products Ordered", "Email", "Address"])
    for order, products, email, address in get_processing_invoices():
        writer.writerow([
            order['id'],
            order['date_created'],
            order['total'],
            order['currency'],
            order['customer_id'],
            ", ".join(products),
            email,
            address
        ])

