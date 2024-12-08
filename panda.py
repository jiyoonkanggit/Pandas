import random
import string
import csv
from datetime import datetime, timedelta

# Helper function to generate unique IDs
def generate_unique_id(prefix='', length=6):
    """Generates a unique ID with an optional prefix."""
    return prefix + ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

# Helper function to generate random dates
def random_date(start_date, end_date):
    """Generates a random datetime between start_date and end_date."""
    delta = end_date - start_date
    random_seconds = random.randint(0, int(delta.total_seconds()))
    return start_date + timedelta(seconds=random_seconds)

# Product class
class Product:
    def __init__(self, name, price):
        self.name = name
        self.price = price

# Order class
class Order:
    def __init__(self, customer_id, store_id, order_date):
        self.order_id = generate_unique_id('ORD_')
        self.customer_id = customer_id
        self.store_id = store_id
        self.order_date = order_date
        self.products = []

    def add_product(self, product):
        self.products.append(product)

# Customer class
class Customer:
    def __init__(self, customer_id):
        self.customer_id = customer_id
        self.orders = []

    def create_order(self, store_id, available_products, order_date):
        order = Order(self.customer_id, store_id, order_date)
        num_products = random.randint(1, 5)  # Each order contains 1 to 5 products
        for _ in range(num_products):
            product = random.choice(available_products)
            order.add_product(product)
        self.orders.append(order)
        return order

# Store class
class Store:
    def __init__(self, store_id, available_products):
        self.store_id = store_id
        self.available_products = available_products
        self.customers = []

    def get_or_create_customer(self, customer_id):
        """Retrieve an existing customer or create a new one."""
        for customer in self.customers:
            if customer.customer_id == customer_id:
                return customer
        new_customer = Customer(customer_id)
        self.customers.append(new_customer)
        return new_customer

# Corporation class
class Corporation:
    def __init__(self, name, num_stores, available_products):
        self.name = name
        self.stores = []
        self.available_products = available_products
        self.create_stores(num_stores)

    def create_stores(self, num_stores):
        """Initialize stores for the corporation."""
        for _ in range(num_stores):
            store_id = generate_unique_id('STR_')
            store = Store(store_id, self.available_products)
            self.stores.append(store)

    def generate_sales_data(self, start_date, end_date, customers_per_store):
        """Generate sales data for all stores."""
        sales_records = []
        for store in self.stores:
            for _ in range(customers_per_store):
                customer_id = generate_unique_id('CUST_')
                customer = store.get_or_create_customer(customer_id)
                num_orders = random.randint(1, 10)  # Each customer makes 1-10 orders
                for _ in range(num_orders):
                    order_date = random_date(start_date, end_date)
                    order = customer.create_order(store.store_id, store.available_products, order_date)
                    for product in order.products:
                        record = {
                            'Date': order.order_date.date(),
                            'Time': order.order_date.time(),
                            'StoreID': store.store_id,
                            'CustomerID': order.customer_id,
                            'OrderID': order.order_id,
                            'ProductName': product.name,
                            'Price': product.price
                        }
                        sales_records.append(record)
        return sales_records

# Function to write sales data to a CSV file
def write_sales_to_csv(sales_data, filename='sales_data.csv'):
    """Write sales data to a CSV file."""
    headers = ['Date', 'Time', 'StoreID', 'CustomerID', 'OrderID', 'ProductName', 'Price']
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        writer.writeheader()
        writer.writerows(sales_data)

# Example usage
if __name__ == "__main__":
    # Define available products
    product_names = [
        "Smartphone", "Laptop", "Tablet", "Smartwatch", 
        "Headphones", "Speaker", "Monitor", "Keyboard"
    ]
    available_products = [Product(name, round(random.uniform(50, 1000), 2)) for name in product_names]

    # Create a corporation with 10 stores
    corp = Corporation(name="TechCorp", num_stores=10, available_products=available_products)

    # Define simulation date range
    start_date = datetime(2023, 1, 1)
    end_date = datetime(2023, 12, 31)

    # Generate sales data
    sales_data = corp.generate_sales_data(start_date, end_date, customers_per_store=100)

    # Write data to a CSV file
    write_sales_to_csv(sales_data)
    print(f"Sales data for {len(sales_data)} transactions has been saved to 'sales_data.csv'.")

