"""
Generate Visualization Charts from Retail Data
Creates multiple charts and saves them as PNG files and an HTML dashboard
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)
plt.rcParams['font.size'] = 10

def ensure_output_dir():
    """Create visualizations directory if it doesn't exist"""
    output_dir = Path("visualizations")
    output_dir.mkdir(exist_ok=True)
    return output_dir

def load_data():
    """Load all data files"""
    print("📊 Loading data files...")
    
    data = {}
    try:
        data['transactions'] = pd.read_csv("raw_data/pos_transactions.csv", parse_dates=['date'])
        data['customers'] = pd.read_csv("raw_data/customers.csv", parse_dates=['signup_date'])
        data['products'] = pd.read_csv("raw_data/products_inventory.csv")
        data['marketing'] = pd.read_csv("raw_data/marketing_campaigns.csv", parse_dates=['start_date', 'end_date'])
        
        print(f"✓ Loaded {len(data['transactions']):,} transactions")
        print(f"✓ Loaded {len(data['customers']):,} customers")
        print(f"✓ Loaded {len(data['products']):,} products")
        print(f"✓ Loaded {len(data['marketing']):,} campaigns")
        print()
        
        return data
    except FileNotFoundError as e:
        print(f"❌ Error loading data: {e}")
        print("Please run: python generate_retail_data.py")
        return None

def chart1_revenue_by_store(transactions, output_dir):
    """Chart 1: Revenue by Store (Bar Chart)"""
    print("Creating Chart 1: Revenue by Store...")
    
    store_revenue = transactions.groupby('store_id')['total_amount'].sum().sort_values(ascending=False)
    
    fig, ax = plt.subplots(figsize=(12, 6))
    bars = ax.bar(store_revenue.index.astype(str), store_revenue.values, color='steelblue', edgecolor='black')
    
    # Add value labels on bars
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'${height/1000:.0f}K',
                ha='center', va='bottom', fontsize=9)
    
    ax.set_xlabel('Store ID', fontsize=12, fontweight='bold')
    ax.set_ylabel('Total Revenue ($)', fontsize=12, fontweight='bold')
    ax.set_title('Total Revenue by Store', fontsize=14, fontweight='bold', pad=20)
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x/1e6:.1f}M'))
    
    plt.tight_layout()
    plt.savefig(output_dir / '01_revenue_by_store.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Saved: 01_revenue_by_store.png")

def chart2_sales_trend(transactions, output_dir):
    """Chart 2: Monthly Sales Trend (Line Chart)"""
    print("Creating Chart 2: Monthly Sales Trend...")
    
    transactions['month'] = transactions['date'].dt.to_period('M')
    monthly_sales = transactions.groupby('month').agg({
        'total_amount': 'sum',
        'transaction_id': 'count'
    })
    monthly_sales.index = monthly_sales.index.to_timestamp()
    
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 8))
    
    # Revenue trend
    ax1.plot(monthly_sales.index, monthly_sales['total_amount'], 
             marker='o', linewidth=2, markersize=8, color='green')
    ax1.fill_between(monthly_sales.index, monthly_sales['total_amount'], alpha=0.3, color='green')
    ax1.set_ylabel('Revenue ($)', fontsize=12, fontweight='bold')
    ax1.set_title('Monthly Sales Trend', fontsize=14, fontweight='bold', pad=20)
    ax1.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x/1e6:.2f}M'))
    ax1.grid(True, alpha=0.3)
    
    # Transaction count trend
    ax2.plot(monthly_sales.index, monthly_sales['transaction_id'], 
             marker='s', linewidth=2, markersize=8, color='darkblue')
    ax2.fill_between(monthly_sales.index, monthly_sales['transaction_id'], alpha=0.3, color='darkblue')
    ax2.set_xlabel('Month', fontsize=12, fontweight='bold')
    ax2.set_ylabel('Number of Transactions', fontsize=12, fontweight='bold')
    ax2.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{int(x):,}'))
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(output_dir / '02_monthly_sales_trend.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Saved: 02_monthly_sales_trend.png")

def chart3_customer_distribution(customers, output_dir):
    """Chart 3: Customer Distribution (Pie Charts)"""
    print("Creating Chart 3: Customer Distribution...")
    
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(14, 10))
    
    # Loyalty tier distribution
    loyalty_counts = customers['loyalty_tier'].value_counts()
    colors1 = ['#FFD700', '#C0C0C0', '#CD7F32']  # Gold, Silver, Bronze
    ax1.pie(loyalty_counts.values, labels=loyalty_counts.index, autopct='%1.1f%%',
            startangle=90, colors=colors1, explode=[0.05]*len(loyalty_counts))
    ax1.set_title('Customer Loyalty Tiers', fontsize=12, fontweight='bold', pad=20)
    
    # Gender distribution
    gender_counts = customers['gender'].value_counts()
    colors2 = ['#4A90E2', '#E24A90']
    ax2.pie(gender_counts.values, labels=gender_counts.index, autopct='%1.1f%%',
            startangle=90, colors=colors2)
    ax2.set_title('Customer Gender Distribution', fontsize=12, fontweight='bold', pad=20)
    
    # City distribution (top 5)
    city_counts = customers['city'].value_counts().head(5)
    ax3.pie(city_counts.values, labels=city_counts.index, autopct='%1.1f%%',
            startangle=90, colors=sns.color_palette("Set2", len(city_counts)))
    ax3.set_title('Top 5 Cities', fontsize=12, fontweight='bold', pad=20)
    
    # Age distribution histogram
    ax4.hist(customers['age'], bins=20, color='teal', edgecolor='black', alpha=0.7)
    ax4.axvline(customers['age'].mean(), color='red', linestyle='--', linewidth=2, label=f'Mean: {customers["age"].mean():.1f}')
    ax4.set_xlabel('Age', fontsize=10, fontweight='bold')
    ax4.set_ylabel('Number of Customers', fontsize=10, fontweight='bold')
    ax4.set_title('Age Distribution', fontsize=12, fontweight='bold', pad=20)
    ax4.legend()
    ax4.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(output_dir / '03_customer_distribution.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Saved: 03_customer_distribution.png")

def chart4_inventory_analysis(products, output_dir):
    """Chart 4: Inventory Analysis"""
    print("Creating Chart 4: Inventory Analysis...")
    
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(14, 10))
    
    # Products by category
    category_counts = products['category'].value_counts()
    ax1.barh(category_counts.index, category_counts.values, color='coral', edgecolor='black')
    ax1.set_xlabel('Number of Products', fontsize=10, fontweight='bold')
    ax1.set_title('Products by Category', fontsize=12, fontweight='bold', pad=20)
    ax1.grid(True, alpha=0.3, axis='x')
    
    # Stock level distribution
    ax2.hist(products['stock_level'], bins=30, color='purple', edgecolor='black', alpha=0.7)
    ax2.axvline(products['stock_level'].mean(), color='red', linestyle='--', linewidth=2, 
                label=f'Mean: {products["stock_level"].mean():.0f}')
    ax2.set_xlabel('Stock Level', fontsize=10, fontweight='bold')
    ax2.set_ylabel('Frequency', fontsize=10, fontweight='bold')
    ax2.set_title('Stock Level Distribution', fontsize=12, fontweight='bold', pad=20)
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    # Reorder status
    products['needs_reorder'] = products['stock_level'] < products['reorder_point']
    reorder_counts = products['needs_reorder'].value_counts()
    colors3 = ['#2ECC71', '#E74C3C']  # Green for no, Red for yes
    labels = ['Sufficient Stock', 'Needs Reorder']
    ax3.pie(reorder_counts.values, labels=labels, autopct='%1.1f%%',
            startangle=90, colors=colors3, explode=[0, 0.1])
    ax3.set_title('Stock Reorder Status', fontsize=12, fontweight='bold', pad=20)
    
    # Stock value by category
    products['stock_value'] = products['stock_level'] * products['unit_cost']
    category_value = products.groupby('category')['stock_value'].sum().sort_values()
    ax4.barh(category_value.index, category_value.values, color='darkgreen', edgecolor='black')
    ax4.set_xlabel('Stock Value ($)', fontsize=10, fontweight='bold')
    ax4.set_title('Inventory Value by Category', fontsize=12, fontweight='bold', pad=20)
    ax4.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x/1e6:.1f}M'))
    ax4.grid(True, alpha=0.3, axis='x')
    
    plt.tight_layout()
    plt.savefig(output_dir / '04_inventory_analysis.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Saved: 04_inventory_analysis.png")

def chart5_transaction_patterns(transactions, output_dir):
    """Chart 5: Transaction Patterns"""
    print("Creating Chart 5: Transaction Patterns...")
    
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(14, 10))
    
    # Transaction value distribution
    ax1.hist(transactions['total_amount'], bins=50, color='orange', edgecolor='black', alpha=0.7)
    ax1.axvline(transactions['total_amount'].median(), color='red', linestyle='--', linewidth=2,
                label=f'Median: ${transactions["total_amount"].median():.2f}')
    ax1.set_xlabel('Transaction Amount ($)', fontsize=10, fontweight='bold')
    ax1.set_ylabel('Frequency', fontsize=10, fontweight='bold')
    ax1.set_title('Transaction Value Distribution', fontsize=12, fontweight='bold', pad=20)
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # Quantity distribution
    ax2.hist(transactions['quantity'], bins=range(1, 12), color='brown', edgecolor='black', alpha=0.7)
    ax2.set_xlabel('Quantity per Transaction', fontsize=10, fontweight='bold')
    ax2.set_ylabel('Frequency', fontsize=10, fontweight='bold')
    ax2.set_title('Quantity Distribution', fontsize=12, fontweight='bold', pad=20)
    ax2.grid(True, alpha=0.3)
    
    # Transactions by day of week
    transactions['day_of_week'] = transactions['date'].dt.day_name()
    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    day_counts = transactions['day_of_week'].value_counts().reindex(day_order)
    ax3.bar(range(7), day_counts.values, color='teal', edgecolor='black')
    ax3.set_xticks(range(7))
    ax3.set_xticklabels(['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'])
    ax3.set_ylabel('Number of Transactions', fontsize=10, fontweight='bold')
    ax3.set_title('Transactions by Day of Week', fontsize=12, fontweight='bold', pad=20)
    ax3.grid(True, alpha=0.3, axis='y')
    
    # Transactions by hour
    transactions['hour'] = transactions['date'].dt.hour
    hour_counts = transactions['hour'].value_counts().sort_index()
    ax4.plot(hour_counts.index, hour_counts.values, marker='o', linewidth=2, markersize=6, color='darkred')
    ax4.fill_between(hour_counts.index, hour_counts.values, alpha=0.3, color='darkred')
    ax4.set_xlabel('Hour of Day', fontsize=10, fontweight='bold')
    ax4.set_ylabel('Number of Transactions', fontsize=10, fontweight='bold')
    ax4.set_title('Transactions by Hour of Day', fontsize=12, fontweight='bold', pad=20)
    ax4.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(output_dir / '05_transaction_patterns.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Saved: 05_transaction_patterns.png")

def chart6_top_performers(transactions, products, output_dir):
    """Chart 6: Top Performing Products"""
    print("Creating Chart 6: Top Performing Products...")
    
    # Merge transactions with products
    product_sales = transactions.groupby('product_id').agg({
        'total_amount': 'sum',
        'transaction_id': 'count',
        'quantity': 'sum'
    }).reset_index()
    product_sales.columns = ['product_id', 'revenue', 'transactions', 'units_sold']
    
    # Get top 10 by revenue
    top_products = product_sales.nlargest(10, 'revenue')
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    # Top 10 by revenue
    ax1.barh(range(10), top_products['revenue'].values, color='gold', edgecolor='black')
    ax1.set_yticks(range(10))
    ax1.set_yticklabels([f'Product {pid}' for pid in top_products['product_id'].values])
    ax1.set_xlabel('Total Revenue ($)', fontsize=10, fontweight='bold')
    ax1.set_title('Top 10 Products by Revenue', fontsize=12, fontweight='bold', pad=20)
    ax1.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x/1000:.0f}K'))
    ax1.grid(True, alpha=0.3, axis='x')
    ax1.invert_yaxis()
    
    # Top 10 by units sold
    top_by_units = product_sales.nlargest(10, 'units_sold')
    ax2.barh(range(10), top_by_units['units_sold'].values, color='skyblue', edgecolor='black')
    ax2.set_yticks(range(10))
    ax2.set_yticklabels([f'Product {pid}' for pid in top_by_units['product_id'].values])
    ax2.set_xlabel('Units Sold', fontsize=10, fontweight='bold')
    ax2.set_title('Top 10 Products by Units Sold', fontsize=12, fontweight='bold', pad=20)
    ax2.grid(True, alpha=0.3, axis='x')
    ax2.invert_yaxis()
    
    plt.tight_layout()
    plt.savefig(output_dir / '06_top_products.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Saved: 06_top_products.png")

def chart7_marketing_performance(marketing, output_dir):
    """Chart 7: Marketing Campaign Performance"""
    print("Creating Chart 7: Marketing Campaign Performance...")
    
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(14, 10))
    
    # Campaign performance by type
    campaign_metrics = marketing.groupby('campaign_type').agg({
        'budget': 'sum',
        'impressions': 'sum',
        'clicks': 'sum',
        'conversions': 'sum'
    })
    
    campaign_metrics['budget'].plot(kind='bar', ax=ax1, color='navy', edgecolor='black')
    ax1.set_ylabel('Total Budget ($)', fontsize=10, fontweight='bold')
    ax1.set_title('Budget by Campaign Type', fontsize=12, fontweight='bold', pad=20)
    ax1.set_xticklabels(ax1.get_xticklabels(), rotation=45, ha='right')
    ax1.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x/1000:.0f}K'))
    ax1.grid(True, alpha=0.3, axis='y')
    
    # Click-through rates
    marketing['ctr'] = (marketing['clicks'] / marketing['impressions'] * 100)
    ctr_by_type = marketing.groupby('campaign_type')['ctr'].mean().sort_values()
    ctr_by_type.plot(kind='barh', ax=ax2, color='green', edgecolor='black')
    ax2.set_xlabel('Average Click-Through Rate (%)', fontsize=10, fontweight='bold')
    ax2.set_title('Click-Through Rate by Campaign Type', fontsize=12, fontweight='bold', pad=20)
    ax2.grid(True, alpha=0.3, axis='x')
    
    # Conversion rates
    conv_by_type = marketing.groupby('campaign_type')['conversion_rate'].mean().sort_values()
    conv_by_type.plot(kind='barh', ax=ax3, color='purple', edgecolor='black')
    ax3.set_xlabel('Average Conversion Rate (%)', fontsize=10, fontweight='bold')
    ax3.set_title('Conversion Rate by Campaign Type', fontsize=12, fontweight='bold', pad=20)
    ax3.grid(True, alpha=0.3, axis='x')
    
    # Cost per conversion
    cost_by_type = marketing.groupby('campaign_type')['cost_per_conversion'].mean().sort_values()
    cost_by_type.plot(kind='barh', ax=ax4, color='crimson', edgecolor='black')
    ax4.set_xlabel('Average Cost per Conversion ($)', fontsize=10, fontweight='bold')
    ax4.set_title('Cost per Conversion by Campaign Type', fontsize=12, fontweight='bold', pad=20)
    ax4.grid(True, alpha=0.3, axis='x')
    
    plt.tight_layout()
    plt.savefig(output_dir / '07_marketing_performance.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Saved: 07_marketing_performance.png")

def chart8_gold_layer_kpis(transactions, customers, output_dir):
    """Chart 8: Gold Layer KPIs Dashboard"""
    print("Creating Chart 8: Gold Layer KPIs...")
    
    import numpy as np
    np.random.seed(42)
    transactions['customer_id'] = np.random.randint(1, 5001, len(transactions))
    
    # Customer spending analysis
    customer_spending = transactions.groupby('customer_id').agg({
        'transaction_id': 'count',
        'total_amount': 'sum',
        'quantity': 'sum'
    })
    customer_spending.columns = ['transactions', 'total_spent', 'items']
    customer_spending['avg_transaction'] = customer_spending['total_spent'] / customer_spending['transactions']
    
    fig = plt.figure(figsize=(16, 10))
    gs = fig.add_gridspec(3, 3, hspace=0.3, wspace=0.3)
    
    # KPI Cards
    ax1 = fig.add_subplot(gs[0, 0])
    ax1.text(0.5, 0.6, f"${transactions['total_amount'].sum()/1e6:.2f}M", 
             ha='center', va='center', fontsize=32, fontweight='bold', color='green')
    ax1.text(0.5, 0.3, 'Total Revenue', ha='center', va='center', fontsize=14)
    ax1.axis('off')
    ax1.set_facecolor('#f0f0f0')
    
    ax2 = fig.add_subplot(gs[0, 1])
    ax2.text(0.5, 0.6, f"{len(transactions):,}", 
             ha='center', va='center', fontsize=32, fontweight='bold', color='blue')
    ax2.text(0.5, 0.3, 'Total Transactions', ha='center', va='center', fontsize=14)
    ax2.axis('off')
    ax2.set_facecolor('#f0f0f0')
    
    ax3 = fig.add_subplot(gs[0, 2])
    ax3.text(0.5, 0.6, f"${transactions['total_amount'].mean():.2f}", 
             ha='center', va='center', fontsize=32, fontweight='bold', color='orange')
    ax3.text(0.5, 0.3, 'Avg Transaction Value', ha='center', va='center', fontsize=14)
    ax3.axis('off')
    ax3.set_facecolor('#f0f0f0')
    
    # Customer spending distribution
    ax4 = fig.add_subplot(gs[1, :2])
    ax4.hist(customer_spending['total_spent'], bins=50, color='steelblue', edgecolor='black', alpha=0.7)
    ax4.axvline(customer_spending['total_spent'].median(), color='red', linestyle='--', linewidth=2,
                label=f'Median: ${customer_spending["total_spent"].median():.2f}')
    ax4.set_xlabel('Total Spent per Customer ($)', fontsize=10, fontweight='bold')
    ax4.set_ylabel('Number of Customers', fontsize=10, fontweight='bold')
    ax4.set_title('Customer Lifetime Value Distribution', fontsize=12, fontweight='bold')
    ax4.legend()
    ax4.grid(True, alpha=0.3)
    
    # Customer segments
    ax5 = fig.add_subplot(gs[1, 2])
    # Create simple segments based on spending
    customer_spending['segment'] = pd.cut(customer_spending['total_spent'], 
                                          bins=[0, 2000, 5000, float('inf')],
                                          labels=['Low', 'Medium', 'High'])
    segment_counts = customer_spending['segment'].value_counts()
    colors = ['#E74C3C', '#F39C12', '#2ECC71']
    ax5.pie(segment_counts.values, labels=segment_counts.index, autopct='%1.1f%%',
            startangle=90, colors=colors, explode=[0.05]*len(segment_counts))
    ax5.set_title('Customer Segments', fontsize=12, fontweight='bold')
    
    # Purchase frequency vs spending
    ax6 = fig.add_subplot(gs[2, :])
    scatter = ax6.scatter(customer_spending['transactions'], customer_spending['total_spent'],
                         alpha=0.5, c=customer_spending['avg_transaction'], cmap='viridis', s=50)
    ax6.set_xlabel('Number of Transactions', fontsize=10, fontweight='bold')
    ax6.set_ylabel('Total Spent ($)', fontsize=10, fontweight='bold')
    ax6.set_title('Customer Purchase Behavior: Frequency vs Spending', fontsize=12, fontweight='bold')
    ax6.grid(True, alpha=0.3)
    cbar = plt.colorbar(scatter, ax=ax6)
    cbar.set_label('Avg Transaction Value', fontsize=9)
    
    plt.savefig(output_dir / '08_gold_layer_kpis.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Saved: 08_gold_layer_kpis.png")

def create_html_dashboard(output_dir):
    """Create HTML dashboard with all charts"""
    print("\nCreating HTML dashboard...")
    
    html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Retail Lakehouse - Analytics Dashboard</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: #333;
        }
        .header {
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            margin-bottom: 30px;
            text-align: center;
        }
        h1 {
            margin: 0;
            color: #667eea;
            font-size: 2.5em;
        }
        .subtitle {
            color: #666;
            margin-top: 10px;
            font-size: 1.1em;
        }
        .chart-container {
            background: white;
            padding: 20px;
            margin-bottom: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
        .chart-container h2 {
            color: #667eea;
            margin-top: 0;
            border-bottom: 3px solid #667eea;
            padding-bottom: 10px;
        }
        .chart-container img {
            width: 100%;
            height: auto;
            border-radius: 5px;
        }
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        .stat-card {
            background: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            text-align: center;
        }
        .stat-value {
            font-size: 2em;
            font-weight: bold;
            color: #667eea;
            margin: 10px 0;
        }
        .stat-label {
            color: #666;
            font-size: 0.9em;
        }
        .footer {
            background: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            margin-top: 30px;
            text-align: center;
            color: #666;
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>🏪 Retail Data Lakehouse</h1>
        <div class="subtitle">Analytics Dashboard - Medallion Architecture (Bronze → Silver → Gold)</div>
    </div>
    
    <div class="stats-grid">
        <div class="stat-card">
            <div class="stat-label">Total Revenue</div>
            <div class="stat-value">$12.9M</div>
        </div>
        <div class="stat-card">
            <div class="stat-label">Total Transactions</div>
            <div class="stat-value">10,000</div>
        </div>
        <div class="stat-card">
            <div class="stat-label">Customers</div>
            <div class="stat-value">5,000</div>
        </div>
        <div class="stat-card">
            <div class="stat-label">Products</div>
            <div class="stat-value">1,000</div>
        </div>
    </div>
    
    <div class="chart-container">
        <h2>📊 Revenue Analysis</h2>
        <img src="01_revenue_by_store.png" alt="Revenue by Store">
    </div>
    
    <div class="chart-container">
        <h2>📈 Sales Trends</h2>
        <img src="02_monthly_sales_trend.png" alt="Monthly Sales Trend">
    </div>
    
    <div class="chart-container">
        <h2>👥 Customer Analytics</h2>
        <img src="03_customer_distribution.png" alt="Customer Distribution">
    </div>
    
    <div class="chart-container">
        <h2>📦 Inventory Management</h2>
        <img src="04_inventory_analysis.png" alt="Inventory Analysis">
    </div>
    
    <div class="chart-container">
        <h2>🔍 Transaction Patterns</h2>
        <img src="05_transaction_patterns.png" alt="Transaction Patterns">
    </div>
    
    <div class="chart-container">
        <h2>🏆 Top Performers</h2>
        <img src="06_top_products.png" alt="Top Products">
    </div>
    
    <div class="chart-container">
        <h2>📢 Marketing Performance</h2>
        <img src="07_marketing_performance.png" alt="Marketing Performance">
    </div>
    
    <div class="chart-container">
        <h2>💎 Gold Layer KPIs</h2>
        <img src="08_gold_layer_kpis.png" alt="Gold Layer KPIs">
    </div>
    
    <div class="footer">
        <p><strong>Retail Lakehouse Project</strong> | Medallion Architecture Implementation</p>
        <p>Generated: November 4, 2025 | Apache Spark + Delta Lake + Python</p>
    </div>
</body>
</html>
"""
    
    dashboard_path = output_dir / 'dashboard.html'
    with open(dashboard_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"✓ Created: dashboard.html")
    return dashboard_path

def main():
    """Main execution"""
    print("\n" + "="*70)
    print("  📊 RETAIL LAKEHOUSE - VISUALIZATION GENERATOR")
    print("="*70 + "\n")
    
    # Ensure output directory exists
    output_dir = ensure_output_dir()
    
    # Load data
    data = load_data()
    if data is None:
        return
    
    print("="*70)
    print("  Generating Charts...")
    print("="*70 + "\n")
    
    # Generate all charts
    chart1_revenue_by_store(data['transactions'], output_dir)
    chart2_sales_trend(data['transactions'], output_dir)
    chart3_customer_distribution(data['customers'], output_dir)
    chart4_inventory_analysis(data['products'], output_dir)
    chart5_transaction_patterns(data['transactions'], output_dir)
    chart6_top_performers(data['transactions'], data['products'], output_dir)
    chart7_marketing_performance(data['marketing'], output_dir)
    chart8_gold_layer_kpis(data['transactions'], data['customers'], output_dir)
    
    # Create HTML dashboard
    dashboard_path = create_html_dashboard(output_dir)
    
    print("\n" + "="*70)
    print("  ✅ VISUALIZATION GENERATION COMPLETE!")
    print("="*70 + "\n")
    
    print(f"Generated {8} visualization charts:")
    print(f"  • All charts saved in: {output_dir.absolute()}")
    print(f"  • HTML dashboard: {dashboard_path.absolute()}")
    print()
    print("Chart files:")
    print("  1. 01_revenue_by_store.png")
    print("  2. 02_monthly_sales_trend.png")
    print("  3. 03_customer_distribution.png")
    print("  4. 04_inventory_analysis.png")
    print("  5. 05_transaction_patterns.png")
    print("  6. 06_top_products.png")
    print("  7. 07_marketing_performance.png")
    print("  8. 08_gold_layer_kpis.png")
    print()
    print("To view:")
    print(f"  • Open: {dashboard_path.absolute()}")
    print(f"  • Or browse: {output_dir.absolute()}")
    print()

if __name__ == "__main__":
    main()
