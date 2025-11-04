"""
Sample Data Generator for Instacart Dataset

This script creates small sample CSV files for testing the pipeline
without downloading the full 3GB Instacart dataset.

Use this for:
- Testing the pipeline locally
- Development and debugging
- Quick demos

Run: python scripts/generate_sample_data.py
"""

import pandas as pd
import numpy as np
from pathlib import Path
import random

# Set random seed for reproducibility
np.random.seed(42)
random.seed(42)

# Output directory
OUTPUT_DIR = Path("data/raw")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

print("=" * 80)
print("GENERATING SAMPLE INSTACART DATA")
print("=" * 80)

# 1. Generate Departments
departments = pd.DataFrame({
    'department_id': range(1, 22),
    'department': [
        'frozen', 'other', 'bakery', 'produce', 'alcohol', 'international',
        'beverages', 'pets', 'dry goods pasta', 'bulk', 'personal care',
        'meat seafood', 'pantry', 'breakfast', 'canned goods', 'dairy eggs',
        'household', 'babies', 'snacks', 'deli', 'missing'
    ]
})
departments.to_csv(OUTPUT_DIR / "departments.csv", index=False)
print(f"✓ Created departments.csv ({len(departments)} departments)")

# 2. Generate Aisles
aisles_data = [
    (1, 'prepared soups salads', 15), (2, 'specialty cheeses', 16),
    (3, 'energy granola bars', 19), (4, 'instant foods', 13),
    (5, 'marinades meat preparation', 13), (6, 'other', 2),
    (7, 'packaged meat', 12), (8, 'bakery desserts', 3),
    (9, 'pasta sauce', 9), (10, 'kitchen supplies', 17),
    (11, 'cold flu allergy', 11), (12, 'fresh pasta', 16),
    (13, 'prepared meals', 15), (14, 'tofu meat alternatives', 12),
    (15, 'packaged seafood', 12), (16, 'fresh herbs', 4),
    (17, 'baking ingredients', 13), (18, 'milk', 16),
    (19, 'refrigerated', 16), (20, 'ice cream ice', 1),
    (21, 'fresh vegetables', 4), (22, 'fresh fruits', 4),
    (23, 'yogurt', 16), (24, 'chips pretzels', 19),
    (25, 'cookies cakes', 19), (26, 'candy chocolate', 19),
    (27, 'crackers', 19), (28, 'water seltzer sparkling water', 7),
    (29, 'juice nectars', 7), (30, 'coffee', 7),
]

aisles = pd.DataFrame(aisles_data, columns=['aisle_id', 'aisle', 'department_id'])
aisles.to_csv(OUTPUT_DIR / "aisles.csv", index=False)
print(f"✓ Created aisles.csv ({len(aisles)} aisles)")

# 3. Generate Products (sample 500 products)
product_names = [
    'Banana', 'Bag of Organic Bananas', 'Organic Strawberries', 'Organic Baby Spinach',
    'Organic Hass Avocado', 'Organic Avocado', 'Large Lemon', 'Limes',
    'Strawberries', 'Organic Whole Milk', 'Organic Raspberries', 'Organic Blueberries',
    'Cucumber Kirby', 'Organic Fuji Apple', 'Organic Lemon', 'Apple Honeycrisp Organic',
    'Organic Zucchini', 'Organic Yellow Onion', 'Organic Garlic', 'Organic Grape Tomatoes',
]

# Extend to 500 products
products_data = []
for i in range(500):
    if i < len(product_names):
        name = product_names[i]
    else:
        name = f"Product {i}"
    
    aisle_id = random.randint(1, 30)
    dept_row = aisles[aisles['aisle_id'] == aisle_id].iloc[0]
    
    products_data.append({
        'product_id': i + 1,
        'product_name': name,
        'aisle_id': aisle_id,
        'department_id': dept_row['department_id']
    })

products = pd.DataFrame(products_data)
products.to_csv(OUTPUT_DIR / "products.csv", index=False)
print(f"✓ Created products.csv ({len(products)} products)")

# 4. Generate Orders (sample 10,000 orders)
num_users = 1000
num_orders = 10000

orders_data = []
for order_id in range(1, num_orders + 1):
    user_id = random.randint(1, num_users)
    eval_set = random.choice(['prior', 'train', 'test'])
    order_number = random.randint(1, 100)
    order_dow = random.randint(0, 6)  # day of week
    order_hour_of_day = random.randint(0, 23)
    days_since_prior = random.randint(1, 30) if order_number > 1 else None
    
    orders_data.append({
        'order_id': order_id,
        'user_id': user_id,
        'eval_set': eval_set,
        'order_number': order_number,
        'order_dow': order_dow,
        'order_hour_of_day': order_hour_of_day,
        'days_since_prior_order': days_since_prior
    })

orders = pd.DataFrame(orders_data)
orders.to_csv(OUTPUT_DIR / "orders.csv", index=False)
print(f"✓ Created orders.csv ({len(orders)} orders)")

# 5. Generate Order Products (prior and train)
# Average 10 products per order
order_products_data = []
for order_id in range(1, num_orders + 1):
    num_items = random.randint(3, 20)
    eval_set = orders[orders['order_id'] == order_id]['eval_set'].iloc[0]
    
    for position in range(1, num_items + 1):
        product_id = random.randint(1, 500)
        reordered = random.choice([0, 1]) if position > 1 else 0
        
        order_products_data.append({
            'order_id': order_id,
            'product_id': product_id,
            'add_to_cart_order': position,
            'reordered': reordered,
            'eval_set': eval_set
        })

order_products_df = pd.DataFrame(order_products_data)

# Split into prior and train
order_products_prior = order_products_df[order_products_df['eval_set'] == 'prior'].drop('eval_set', axis=1)
order_products_train = order_products_df[order_products_df['eval_set'] == 'train'].drop('eval_set', axis=1)

order_products_prior.to_csv(OUTPUT_DIR / "order_products_prior.csv", index=False)
order_products_train.to_csv(OUTPUT_DIR / "order_products_train.csv", index=False)

print(f"✓ Created order_products_prior.csv ({len(order_products_prior)} records)")
print(f"✓ Created order_products_train.csv ({len(order_products_train)} records)")

print("=" * 80)
print("✓ SAMPLE DATA GENERATION COMPLETE")
print("=" * 80)
print(f"\nFiles created in: {OUTPUT_DIR.absolute()}")
print("\nYou can now run the pipeline:")
print("  python scripts/01_bronze_ingestion.py")
print("  python scripts/02_silver_transformation.py")
print("  python scripts/03_gold_aggregation.py")
print("\nOr use the helper:")
print("  .\\run_pipeline.ps1")
