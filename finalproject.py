# Importing Libraries
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter

# Load the sales data
sales_data = pd.read_csv('sales_data.csv')

# **Data Preparation**
# Aggregate data by OrderID and ProductName
basket = sales_data.groupby(['StoreID', 'OrderID', 'ProductName'])['Price'].sum().unstack().fillna(0)
basket = (basket > 0).astype(int)  # Convert to binary format (1 if product was purchased, else 0)

# Helper: Identify top items and frequent combinations
def find_top_items(basket_df, top_n=10):
    """
    Finds the most frequently purchased individual items and combinations.
    """
    # Count individual product occurrences
    product_counts = basket_df.sum().sort_values(ascending=False)
    
    # Pairwise combination counts
    pair_counts = Counter()
    for row in basket_df.itertuples(index=False):
        items = [basket_df.columns[i] for i, val in enumerate(row) if val == 1]
        for i in range(len(items)):
            for j in range(i + 1, len(items)):
                pair_counts[(items[i], items[j])] += 1

    # Top products and pairs
    top_products = product_counts.head(top_n)
    top_pairs = Counter(dict(pair_counts)).most_common(top_n)
    return top_products, top_pairs

# Helper: Plot top items
def plot_top_items(item_counts, title="Top Items", xlabel="Items", ylabel="Frequency"):
    item_counts.plot(kind='bar', figsize=(10, 6), color='skyblue')
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# **1. Corporation-Wide Analysis**
print("Analyzing sales across the corporation...\n")

# Aggregate data across the corporation
corporate_basket = basket.groupby(level=1).max()

# Find top individual items and item pairs
corporate_top_products, corporate_top_pairs = find_top_items(corporate_basket)

# Print results
print("Top Individual Products Across the Corporation:")
print(corporate_top_products)

print("\nTop Product Pairs Across the Corporation:")
for pair, count in corporate_top_pairs:
    print(f"{pair}: {count} times")

# Plot top products
plot_top_items(corporate_top_products, title="Top Products Across the Corporation")

# **2. Store-Level Analysis**
print("\nAnalyzing sales per store...\n")

store_best_sellers = {}
for store_id, store_data in basket.groupby(level=0):
    print(f"Analyzing Store: {store_id}")
    
    # Remove store-level index for processing
    store_basket = store_data.droplevel(0)
    
    # Find top items for the store
    store_top_products, store_top_pairs = find_top_items(store_basket)
    
    # Store results
    store_best_sellers[store_id] = {
        'top_products': store_top_products,
        'top_pairs': store_top_pairs
    }
    
    # Print and plot results for the store
    print(f"\nTop Products in {store_id}:")
    print(store_top_products)
    
    print(f"\nTop Product Pairs in {store_id}:")
    for pair, count in store_top_pairs:
        print(f"{pair}: {count} times")
    
    plot_top_items(store_top_products, title=f"Top Products in {store_id}")

# **3. Save Results to CSV**
print("\nSaving results to CSV files...\n")
corporate_top_products.to_csv('corporate_top_products.csv', header=True)
pd.DataFrame(corporate_top_pairs, columns=['Product Pair', 'Frequency']).to_csv('corporate_top_pairs.csv', index=False)

for store_id, data in store_best_sellers.items():
    store_filename = f'{store_id}_top_products.csv'
    data['top_products'].to_csv(store_filename, header=True)
    print(f"Saved top products for {store_id} to {store_filename}.")
