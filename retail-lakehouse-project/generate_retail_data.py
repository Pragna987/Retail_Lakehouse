"""
Generate Sample Retail Data
Creates synthetic POS, CRM, and Inventory datasets for the lakehouse project
"""

import pandas as pd
import numpy as np
import os
from datetime import datetime, timedelta


def generate_pos_data(n_records=10000):
    """Generate synthetic POS transaction data"""
    print(f"Generating {n_records} POS transaction records...")
    np.random.seed(42)
    
    # Generate random dates over the past year
    dates = [datetime.now() - timedelta(days=np.random.randint(0, 365)) 
             for _ in range(n_records)]
    
    data = {
        'transaction_id': range(1, n_records + 1),
        'date': dates,
        'store_id': np.random.randint(1, 11, n_records),
        'product_id': np.random.randint(1000, 2000, n_records),
        'quantity': np.random.randint(1, 10, n_records),
        'unit_price': np.random.uniform(10, 500, n_records).round(2),
        'total_amount': None  # Will calculate below
    }
    
    df = pd.DataFrame(data)
    df['total_amount'] = (df['quantity'] * df['unit_price']).round(2)
    
    return df


def generate_crm_data(n_customers=5000):
    """Generate synthetic CRM customer data"""
    print(f"Generating {n_customers} customer records...")
    np.random.seed(42)
    
    data = {
        'customer_id': range(1, n_customers + 1),
        'name': [f'Customer_{i}' for i in range(1, n_customers + 1)],
        'age': np.random.randint(18, 80, n_customers),
        'gender': np.random.choice(['M', 'F'], n_customers),
        'city': np.random.choice(['New York', 'Los Angeles', 'Chicago', 
                                  'Houston', 'Phoenix'], n_customers),
        'signup_date': [datetime.now() - timedelta(days=np.random.randint(0, 1000)) 
                       for _ in range(n_customers)],
        'loyalty_tier': np.random.choice(['Bronze', 'Silver', 'Gold'], n_customers)
    }
    
    return pd.DataFrame(data)


def generate_inventory_data(n_products=1000):
    """Generate synthetic inventory data"""
    print(f"Generating {n_products} product records...")
    np.random.seed(42)
    
    data = {
        'product_id': range(1000, 1000 + n_products),
        'product_name': [f'Product_{i}' for i in range(1000, 1000 + n_products)],
        'category': np.random.choice(['Electronics', 'Clothing', 'Food', 
                                     'Home', 'Sports'], n_products),
        'stock_level': np.random.randint(0, 500, n_products),
        'reorder_point': np.random.randint(50, 150, n_products),
        'unit_cost': np.random.uniform(5, 300, n_products).round(2)
    }
    
    return pd.DataFrame(data)


def generate_marketing_data(n_campaigns=50):
    """Generate synthetic marketing campaign data"""
    print(f"Generating {n_campaigns} marketing campaign records...")
    np.random.seed(42)
    
    campaign_types = ['Email', 'Social Media', 'Display Ads', 'Search Ads', 'Direct Mail']
    
    data = {
        'campaign_id': range(1, n_campaigns + 1),
        'campaign_name': [f'Campaign_{i}' for i in range(1, n_campaigns + 1)],
        'campaign_type': np.random.choice(campaign_types, n_campaigns),
        'start_date': [datetime.now() - timedelta(days=np.random.randint(30, 365)) 
                      for _ in range(n_campaigns)],
        'end_date': [datetime.now() - timedelta(days=np.random.randint(0, 30)) 
                    for _ in range(n_campaigns)],
        'budget': np.random.uniform(5000, 50000, n_campaigns).round(2),
        'impressions': np.random.randint(10000, 500000, n_campaigns),
        'clicks': np.random.randint(100, 5000, n_campaigns),
        'conversions': np.random.randint(10, 500, n_campaigns)
    }
    
    df = pd.DataFrame(data)
    
    # Calculate derived metrics
    df['click_rate'] = (df['clicks'] / df['impressions'] * 100).round(2)
    df['conversion_rate'] = (df['conversions'] / df['clicks'] * 100).round(2)
    df['cost_per_conversion'] = (df['budget'] / df['conversions']).round(2)
    
    return df


def main():
    """Generate and save all sample datasets"""
    
    print("=" * 60)
    print("RETAIL DATA GENERATION - Sample Dataset Creator")
    print("=" * 60)
    print()
    
    # Create raw_data directory if it doesn't exist
    os.makedirs('raw_data', exist_ok=True)
    
    # Generate POS data
    pos_df = generate_pos_data(n_records=10000)
    pos_df.to_csv('raw_data/pos_transactions.csv', index=False)
    print(f"✓ Created pos_transactions.csv ({len(pos_df)} records)")
    print(f"  Columns: {list(pos_df.columns)}")
    print()
    
    # Generate CRM data
    crm_df = generate_crm_data(n_customers=5000)
    crm_df.to_csv('raw_data/customers.csv', index=False)
    print(f"✓ Created customers.csv ({len(crm_df)} records)")
    print(f"  Columns: {list(crm_df.columns)}")
    print()
    
    # Generate inventory data
    inventory_df = generate_inventory_data(n_products=1000)
    inventory_df.to_csv('raw_data/products_inventory.csv', index=False)
    print(f"✓ Created products_inventory.csv ({len(inventory_df)} records)")
    print(f"  Columns: {list(inventory_df.columns)}")
    print()
    
    # Generate marketing data
    marketing_df = generate_marketing_data(n_campaigns=50)
    marketing_df.to_csv('raw_data/marketing_campaigns.csv', index=False)
    print(f"✓ Created marketing_campaigns.csv ({len(marketing_df)} records)")
    print(f"  Columns: {list(marketing_df.columns)}")
    print()
    
    print("=" * 60)
    print("✅ Sample data generation completed successfully!")
    print("=" * 60)
    print()
    print("Generated files:")
    print("  - raw_data/pos_transactions.csv (10,000 records)")
    print("  - raw_data/customers.csv (5,000 records)")
    print("  - raw_data/products_inventory.csv (1,000 records)")
    print("  - raw_data/marketing_campaigns.csv (50 records)")
    print()
    print("Sample statistics:")
    print(f"  Total transactions: {len(pos_df):,}")
    print(f"  Total revenue: ${pos_df['total_amount'].sum():,.2f}")
    print(f"  Average transaction value: ${pos_df['total_amount'].mean():.2f}")
    print(f"  Unique customers: {len(crm_df):,}")
    print(f"  Unique products: {len(inventory_df):,}")
    print()


if __name__ == "__main__":
    main()
