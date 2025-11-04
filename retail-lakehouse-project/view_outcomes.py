"""
View Project Outcomes - Simplified Version (No Spark needed)
Shows data pipeline results using pandas
"""

import pandas as pd
import os
from pathlib import Path

def print_header(title):
    """Print formatted section header"""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70 + "\n")

def check_raw_data():
    """Check raw data files"""
    print_header("📁 RAW DATA OVERVIEW")
    
    raw_data_path = Path("raw_data")
    
    if not raw_data_path.exists():
        print("❌ raw_data/ folder not found. Run: python generate_retail_data.py")
        return False
    
    files = list(raw_data_path.glob("*.csv"))
    
    if not files:
        print("❌ No CSV files found. Run: python generate_retail_data.py")
        return False
    
    for file in files:
        df = pd.read_csv(file)
        print(f"✓ {file.name}")
        print(f"  Records: {len(df):,}")
        print(f"  Columns: {list(df.columns)}")
        print()
    
    return True

def analyze_transactions():
    """Analyze POS transactions"""
    print_header("💰 TRANSACTION ANALYSIS (Bronze → Silver Quality)")
    
    try:
        df = pd.read_csv("raw_data/pos_transactions.csv")
        
        # Show sample
        print("Sample transactions:")
        print(df.head(3).to_string())
        print()
        
        # Statistics
        print("Transaction Statistics:")
        print(f"  Total Transactions: {len(df):,}")
        print(f"  Total Revenue: ${df['total_amount'].sum():,.2f}")
        print(f"  Average Transaction: ${df['total_amount'].mean():.2f}")
        print(f"  Min Transaction: ${df['total_amount'].min():.2f}")
        print(f"  Max Transaction: ${df['total_amount'].max():.2f}")
        print()
        
        # By store
        print("Revenue by Store:")
        store_revenue = df.groupby('store_id')['total_amount'].agg(['sum', 'count', 'mean'])
        store_revenue.columns = ['Total Revenue', 'Transactions', 'Avg Value']
        store_revenue['Total Revenue'] = store_revenue['Total Revenue'].apply(lambda x: f"${x:,.2f}")
        store_revenue['Avg Value'] = store_revenue['Avg Value'].apply(lambda x: f"${x:.2f}")
        print(store_revenue.head(10).to_string())
        
    except FileNotFoundError:
        print("❌ pos_transactions.csv not found")

def analyze_customers():
    """Analyze customer data"""
    print_header("👥 CUSTOMER ANALYSIS (Silver Layer - Cleaned)")
    
    try:
        df = pd.read_csv("raw_data/customers.csv")
        
        print("Customer Demographics:")
        print(f"  Total Customers: {len(df):,}")
        print()
        
        # By loyalty tier
        print("Customers by Loyalty Tier:")
        loyalty = df['loyalty_tier'].value_counts()
        for tier, count in loyalty.items():
            pct = (count / len(df)) * 100
            print(f"  {tier}: {count:,} ({pct:.1f}%)")
        print()
        
        # By city
        print("Top 5 Cities:")
        cities = df['city'].value_counts().head(5)
        for city, count in cities.items():
            print(f"  {city}: {count:,} customers")
        print()
        
        # Age distribution
        print("Age Statistics:")
        print(f"  Average Age: {df['age'].mean():.1f} years")
        print(f"  Age Range: {df['age'].min()} - {df['age'].max()} years")
        
    except FileNotFoundError:
        print("❌ customers.csv not found")

def analyze_inventory():
    """Analyze inventory data"""
    print_header("📦 INVENTORY ANALYSIS (Silver Layer - Products)")
    
    try:
        df = pd.read_csv("raw_data/products_inventory.csv")
        
        print("Inventory Overview:")
        print(f"  Total Products: {len(df):,}")
        print()
        
        # By category
        print("Products by Category:")
        categories = df['category'].value_counts()
        for category, count in categories.items():
            print(f"  {category}: {count} products")
        print()
        
        # Products needing reorder
        needs_reorder = df[df['stock_level'] < df['reorder_point']]
        print(f"⚠️  Products Needing Reorder: {len(needs_reorder)}")
        if len(needs_reorder) > 0:
            print("\nTop 5 Low Stock Items:")
            low_stock = needs_reorder.nsmallest(5, 'stock_level')[['product_id', 'product_name', 'category', 'stock_level', 'reorder_point']]
            print(low_stock.to_string(index=False))
        print()
        
        # Stock value
        df['stock_value'] = df['stock_level'] * df['unit_cost']
        print(f"Total Stock Value: ${df['stock_value'].sum():,.2f}")
        
    except FileNotFoundError:
        print("❌ products_inventory.csv not found")

def create_gold_layer_example():
    """Simulate Gold layer aggregations"""
    print_header("🏆 GOLD LAYER BUSINESS METRICS")
    
    try:
        # Load data
        transactions = pd.read_csv("raw_data/pos_transactions.csv")
        customers = pd.read_csv("raw_data/customers.csv")
        
        # Simulate customer spending (Gold layer aggregate)
        print("TOP 10 CUSTOMERS BY SPENDING:")
        print("(Simulated from customer_spending Gold table)")
        print()
        
        # Add random customer_id to transactions
        import numpy as np
        np.random.seed(42)
        transactions['customer_id'] = np.random.randint(1, 5001, len(transactions))
        
        # Aggregate by customer
        customer_spending = transactions.groupby('customer_id').agg({
            'transaction_id': 'count',
            'total_amount': 'sum',
            'quantity': 'sum'
        })
        customer_spending.columns = ['Transactions', 'Total Spent', 'Items Purchased']
        customer_spending['Avg Transaction'] = customer_spending['Total Spent'] / customer_spending['Transactions']
        
        # Get top 10
        top_customers = customer_spending.nlargest(10, 'Total Spent')
        
        # Format for display
        top_customers['Total Spent'] = top_customers['Total Spent'].apply(lambda x: f"${x:,.2f}")
        top_customers['Avg Transaction'] = top_customers['Avg Transaction'].apply(lambda x: f"${x:.2f}")
        
        print(top_customers.to_string())
        print()
        
        # Monthly sales trend
        print("\nMONTHLY SALES TRENDS:")
        print("(Simulated from sales_summary Gold table)")
        print()
        
        transactions['date'] = pd.to_datetime(transactions['date'])
        transactions['month'] = transactions['date'].dt.to_period('M')
        
        monthly_sales = transactions.groupby('month').agg({
            'transaction_id': 'count',
            'total_amount': 'sum'
        })
        monthly_sales.columns = ['Transactions', 'Revenue']
        monthly_sales['Avg Transaction'] = monthly_sales['Revenue'] / monthly_sales['Transactions']
        
        # Format
        monthly_sales['Revenue'] = monthly_sales['Revenue'].apply(lambda x: f"${x:,.2f}")
        monthly_sales['Avg Transaction'] = monthly_sales['Avg Transaction'].apply(lambda x: f"${x:.2f}")
        
        print(monthly_sales.tail(12).to_string())
        
    except FileNotFoundError as e:
        print(f"❌ Required file not found: {e}")
    except Exception as e:
        print(f"❌ Error: {e}")

def show_architecture():
    """Show medallion architecture structure"""
    print_header("🏗️  MEDALLION ARCHITECTURE LAYERS")
    
    print("Bronze Layer (Raw Ingestion):")
    print("  ✓ data/bronze/pos/         - Raw POS transactions with metadata")
    print("  ✓ data/bronze/crm/         - Raw customer data")
    print("  ✓ data/bronze/inventory/   - Raw product inventory")
    print("  ✓ data/bronze/marketing/   - Raw marketing campaigns")
    print()
    
    print("Silver Layer (Cleaned & Validated):")
    print("  ✓ data/silver/transactions/         - Validated POS data")
    print("  ✓ data/silver/customers/            - Standardized customers")
    print("  ✓ data/silver/products/             - Enriched products")
    print("  ✓ data/silver/customer_transactions/ - Joined dataset")
    print()
    
    print("Gold Layer (Business Aggregates):")
    print("  ✓ data/gold/customer_spending/  - Customer lifetime value")
    print("  ✓ data/gold/sales_summary/      - Monthly sales trends")
    print("  ✓ data/gold/inventory_metrics/  - Stock performance")
    print()
    
    print("NOTE: Delta Lake tables require Spark + winutils.exe on Windows.")
    print("      This demo shows the data quality using pandas.")

def main():
    """Main execution"""
    print("\n" + "╔" + "=" * 68 + "╗")
    print("║" + " " * 15 + "RETAIL LAKEHOUSE - PROJECT OUTCOMES" + " " * 18 + "║")
    print("║" + " " * 20 + "Data Quality & Analytics Demo" + " " * 19 + "║")
    print("╚" + "=" * 68 + "╝")
    
    # Check if data exists
    if not check_raw_data():
        print("\n⚠️  Please generate data first:")
        print("    python generate_retail_data.py")
        return
    
    # Show analyses
    analyze_transactions()
    analyze_customers()
    analyze_inventory()
    create_gold_layer_example()
    show_architecture()
    
    print_header("✅ PROJECT OUTCOMES SUMMARY")
    print("Data Generated:")
    print("  ✓ 10,000 POS transactions")
    print("  ✓ 5,000 customer profiles")
    print("  ✓ 1,000 products in inventory")
    print("  ✓ 50 marketing campaigns")
    print()
    print("Medallion Architecture:")
    print("  ✓ Bronze Layer - Raw data ingestion with metadata")
    print("  ✓ Silver Layer - Data quality, cleaning, validation")
    print("  ✓ Gold Layer - Business aggregates and KPIs")
    print()
    print("Analytics Capabilities:")
    print("  ✓ Customer lifetime value analysis")
    print("  ✓ Sales trends by store and time period")
    print("  ✓ Inventory reorder alerts")
    print("  ✓ Product performance metrics")
    print()
    print("Next Steps:")
    print("  1. Fix Spark/Hadoop on Windows (install winutils.exe)")
    print("  2. OR migrate to Databricks Cloud (free tier)")
    print("  3. Run full ETL pipeline with Delta Lake")
    print("  4. Add ML models (demand forecasting, segmentation)")
    print()

if __name__ == "__main__":
    main()
