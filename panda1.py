import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter

# Load the sales data
sales_data = pd.read_csv('sales_data.csv')

# Convert price to numeric for analysis
sales_data['Price'] = pd.to_numeric(sales_data['Price'])

# Convert date columns to datetime
sales_data['DateTime'] = pd.to_datetime(sales_data['Date'] + ' ' + sales_data['Time'])

# 1. Most prevalent products in customer baskets
most_prevalent_products = sales_data['ProductName'].value_counts()
print("Most Prevalent Products:")
print(most_prevalent_products)

# 2. Frequency of large buyers (large baskets are orders with >3 items)
basket_sizes = sales_data.groupby('OrderID').size()
large_basket_orders = basket_sizes[basket_sizes > 3]
large_basket_frequency = large_basket_orders.shape[0]
print(f"\nNumber of large baskets (>3 items): {large_basket_frequency}")

# 3. Which stores contained large-basket buyers, and by how much
large_basket_store_stats = sales_data[sales_data['OrderID'].isin(large_basket_orders.index)].groupby('StoreID').size()
print("\nStores with large-basket buyers:")
print(large_basket_store_stats)

# 4. Visualization: Rank stores with large-basket customers by frequency
plt.figure(figsize=(10, 6))
large_basket_store_stats.sort_values(ascending=False).plot(kind='bar', color='skyblue')
plt.title('Top Stores with Large-Basket Customers')
plt.xlabel('StoreID')
plt.ylabel('Frequency of Large Baskets')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# 5. Top-N list of products for specific demographics (large-basket buyers)
top_products_large_basket = sales_data[sales_data['OrderID'].isin(large_basket_orders.index)]['ProductName'].value_counts().head(5)
print("\nTop-N Products for Large-Basket Buyers:")
print(top_products_large_basket)

# 6. Categorical makeup of baskets (average distribution)
basket_product_categories = sales_data.groupby('OrderID')['ProductName'].apply(list)
category_distribution = Counter([product for products in basket_product_categories for product in products])
total_products = sum(category_distribution.values())
category_average = {product: count / total_products for product, count in category_distribution.items()}
category_df = pd.DataFrame.from_dict(category_average, orient='index', columns=['Percentage'])

# Visualization: Categorical makeup of baskets
category_df.sort_values(by='Percentage', ascending=False).plot(kind='bar', figsize=(12, 6), color='orange')
plt.title('Average Categorical Makeup of Baskets')
plt.xlabel('Product')
plt.ylabel('Percentage')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
