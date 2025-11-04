"""
Create Unified Dashboard - Complete Retail Lakehouse Dashboard
Combines Business Analytics + ML Models (Customer Segmentation + Demand Forecasting)
"""

import pandas as pd
import base64
from pathlib import Path

def image_to_base64(image_path):
    """Convert image to base64 for embedding in HTML"""
    try:
        with open(image_path, 'rb') as img_file:
            return base64.b64encode(img_file.read()).decode('utf-8')
    except Exception as e:
        print(f"Warning: Could not load image {image_path}: {e}")
        return None

def create_unified_dashboard():
    """Create comprehensive unified dashboard with all components"""
    print("\n📊 Creating Unified Dashboard (Business + ML Models)...")
    
    # Load data
    transactions = pd.read_csv("raw_data/pos_transactions.csv") if Path("raw_data/pos_transactions.csv").exists() else None
    customers = pd.read_csv("raw_data/customers.csv") if Path("raw_data/customers.csv").exists() else None
    products = pd.read_csv("raw_data/products_inventory.csv") if Path("raw_data/products_inventory.csv").exists() else None
    
    # Business metrics
    total_revenue = f"${transactions['total_amount'].sum()/1e6:.2f}M" if transactions is not None else "N/A"
    total_transactions = f"{len(transactions):,}" if transactions is not None else "N/A"
    total_customers = f"{len(customers):,}" if customers is not None else "N/A"
    total_products = f"{len(products):,}" if products is not None else "N/A"
    avg_transaction = f"${transactions['total_amount'].mean():.2f}" if transactions is not None else "N/A"
    
    # ML Segmentation Data
    segment_file = Path("ml_models/outputs/segment_analysis.csv")
    segment_cards = ""
    if segment_file.exists():
        segments = pd.read_csv(segment_file, index_col=0)
        for idx, row in segments.iterrows():
            segment_cards += f"""
            <div class="segment-card">
                <h3>{row['segment_name']}</h3>
                <div class="metric-grid-small">
                    <div class="metric-small">
                        <div class="value">{int(row['customer_count']):,}</div>
                        <div class="label">Customers</div>
                    </div>
                    <div class="metric-small">
                        <div class="value">${row['total_revenue']/1e6:.1f}M</div>
                        <div class="label">Revenue</div>
                    </div>
                    <div class="metric-small">
                        <div class="value">${row['avg_total_spent']:,.0f}</div>
                        <div class="label">Avg Spend</div>
                    </div>
                    <div class="metric-small">
                        <div class="value">{row['avg_recency_days']:.0f}</div>
                        <div class="label">Days Recency</div>
                    </div>
                </div>
            </div>
            """
    
    # ML Forecast Data
    forecast_file = Path("ml_models/outputs/demand_forecast.csv")
    forecast_stats = ""
    forecast_table = ""
    if forecast_file.exists():
        forecast = pd.read_csv(forecast_file)
        urgency_counts = forecast['urgency'].value_counts()
        
        high = urgency_counts.get('HIGH', 0)
        medium = urgency_counts.get('MEDIUM', 0)
        low = urgency_counts.get('LOW', 0)
        total_units = int(forecast['recommended_order_qty'].sum())
        
        forecast_stats = f"""
        <div class="forecast-mini-stats">
            <div class="mini-stat high">
                <div class="mini-value">{high}</div>
                <div class="mini-label">High Priority</div>
            </div>
            <div class="mini-stat medium">
                <div class="mini-value">{medium}</div>
                <div class="mini-label">Medium</div>
            </div>
            <div class="mini-stat low">
                <div class="mini-value">{low}</div>
                <div class="mini-label">Low</div>
            </div>
            <div class="mini-stat total">
                <div class="mini-value">{total_units:,}</div>
                <div class="mini-label">Units to Order</div>
            </div>
        </div>
        """
        
        # Top 5 priority products
        top_5 = forecast.nlargest(5, 'recommended_order_qty')
        rows = ""
        for idx, row in top_5.iterrows():
            urgency_class = row['urgency'].lower()
            rows += f"""
            <tr class="urgency-{urgency_class}">
                <td>{row['product_id']}</td>
                <td>{row['category']}</td>
                <td>{int(row['current_stock'])}</td>
                <td><strong>{int(row['recommended_order_qty'])}</strong></td>
                <td><span class="badge badge-{urgency_class}">{row['urgency']}</span></td>
            </tr>
            """
        
        forecast_table = f"""
        <table class="compact-table">
            <thead>
                <tr>
                    <th>Product</th>
                    <th>Category</th>
                    <th>Stock</th>
                    <th>Order Qty</th>
                    <th>Priority</th>
                </tr>
            </thead>
            <tbody>{rows}</tbody>
        </table>
        """
    
    # Load all images
    images = {}
    image_paths = {
        # Business charts
        'revenue_store': 'visualizations/01_revenue_by_store.png',
        'sales_trend': 'visualizations/02_monthly_sales_trend.png',
        'customer_dist': 'visualizations/03_customer_distribution.png',
        'inventory': 'visualizations/04_inventory_analysis.png',
        'transaction_patterns': 'visualizations/05_transaction_patterns.png',
        'top_products': 'visualizations/06_top_products.png',
        'marketing': 'visualizations/07_marketing_performance.png',
        'gold_kpis': 'visualizations/08_gold_layer_kpis.png',
        # ML charts
        'seg_analysis': 'ml_models/outputs/customer_segmentation_analysis.png',
        'forecast_analysis': 'ml_models/outputs/demand_forecasting_analysis.png',
        'forecast_results': 'ml_models/outputs/demand_forecast_results.png'
    }
    
    for key, path in image_paths.items():
        if Path(path).exists():
            b64 = image_to_base64(path)
            if b64:
                images[key] = f"data:image/png;base64,{b64}"
    
    # Create HTML
    html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Retail Lakehouse - Complete Dashboard</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
            color: #333;
        }}
        
        .container {{
            max-width: 1600px;
            margin: 0 auto;
        }}
        
        .header {{
            background: white;
            padding: 40px;
            border-radius: 20px;
            box-shadow: 0 15px 40px rgba(0,0,0,0.3);
            margin-bottom: 30px;
            text-align: center;
        }}
        
        .header h1 {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-size: 3em;
            margin-bottom: 10px;
        }}
        
        .header .subtitle {{
            color: #666;
            font-size: 1.3em;
        }}
        
        .kpi-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}
        
        .kpi-card {{
            background: white;
            padding: 25px;
            border-radius: 15px;
            box-shadow: 0 10px 25px rgba(0,0,0,0.2);
            text-align: center;
            transition: transform 0.3s;
        }}
        
        .kpi-card:hover {{
            transform: translateY(-5px);
        }}
        
        .kpi-value {{
            font-size: 2.5em;
            font-weight: bold;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 5px;
        }}
        
        .kpi-label {{
            color: #666;
            font-size: 1.1em;
        }}
        
        .section {{
            background: white;
            padding: 35px;
            border-radius: 20px;
            box-shadow: 0 15px 40px rgba(0,0,0,0.3);
            margin-bottom: 30px;
        }}
        
        .section h2 {{
            color: #667eea;
            font-size: 2.2em;
            margin-bottom: 20px;
            padding-bottom: 15px;
            border-bottom: 4px solid #667eea;
            display: flex;
            align-items: center;
            gap: 15px;
        }}
        
        .tabs {{
            display: flex;
            gap: 10px;
            margin-bottom: 25px;
            border-bottom: 2px solid #e0e0e0;
        }}
        
        .tab {{
            padding: 12px 25px;
            background: #f5f5f5;
            border: none;
            border-radius: 8px 8px 0 0;
            cursor: pointer;
            font-size: 1.1em;
            font-weight: 600;
            color: #666;
            transition: all 0.3s;
        }}
        
        .tab:hover {{
            background: #e0e0e0;
        }}
        
        .tab.active {{
            background: #667eea;
            color: white;
        }}
        
        .tab-content {{
            display: none;
        }}
        
        .tab-content.active {{
            display: block;
        }}
        
        .viz-container {{
            margin: 20px 0;
        }}
        
        .viz-container img {{
            width: 100%;
            height: auto;
            border-radius: 12px;
            box-shadow: 0 8px 20px rgba(0,0,0,0.15);
        }}
        
        .two-col {{
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 25px;
        }}
        
        .segment-card {{
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            padding: 20px;
            border-radius: 12px;
            margin-bottom: 15px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }}
        
        .segment-card h3 {{
            color: #333;
            font-size: 1.5em;
            margin-bottom: 12px;
        }}
        
        .metric-grid-small {{
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 10px;
        }}
        
        .metric-small {{
            background: white;
            padding: 12px;
            border-radius: 8px;
            text-align: center;
        }}
        
        .metric-small .value {{
            font-size: 1.4em;
            font-weight: bold;
            color: #667eea;
        }}
        
        .metric-small .label {{
            font-size: 0.85em;
            color: #666;
            margin-top: 3px;
        }}
        
        .forecast-mini-stats {{
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 15px;
            margin-bottom: 20px;
        }}
        
        .mini-stat {{
            padding: 20px;
            border-radius: 10px;
            text-align: center;
            color: white;
        }}
        
        .mini-stat.high {{ background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); }}
        .mini-stat.medium {{ background: linear-gradient(135deg, #ffc837 0%, #ff8008 100%); }}
        .mini-stat.low {{ background: linear-gradient(135deg, #a8edea 0%, #6dd5ed 100%); }}
        .mini-stat.total {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); }}
        
        .mini-value {{
            font-size: 2em;
            font-weight: bold;
            margin-bottom: 5px;
        }}
        
        .mini-label {{
            font-size: 0.95em;
            opacity: 0.95;
        }}
        
        .compact-table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 15px;
        }}
        
        .compact-table thead {{
            background: #667eea;
            color: white;
        }}
        
        .compact-table th {{
            padding: 12px;
            text-align: left;
            font-weight: 600;
        }}
        
        .compact-table td {{
            padding: 10px 12px;
            border-bottom: 1px solid #e0e0e0;
        }}
        
        .compact-table tr:hover {{
            background: #f5f5f5;
        }}
        
        .urgency-high {{
            background: #ffe5e5;
        }}
        
        .badge {{
            padding: 4px 10px;
            border-radius: 15px;
            font-size: 0.85em;
            font-weight: bold;
        }}
        
        .badge-high {{ background: #f5576c; color: white; }}
        .badge-medium {{ background: #ff8008; color: white; }}
        .badge-low {{ background: #6dd5ed; color: white; }}
        
        .footer {{
            background: white;
            padding: 25px;
            border-radius: 20px;
            box-shadow: 0 15px 40px rgba(0,0,0,0.3);
            text-align: center;
            color: #666;
            margin-top: 30px;
        }}
        
        .footer strong {{
            color: #667eea;
        }}
        
        @media (max-width: 1200px) {{
            .two-col {{
                grid-template-columns: 1fr;
            }}
        }}
        
        @media (max-width: 768px) {{
            .kpi-grid {{
                grid-template-columns: repeat(2, 1fr);
            }}
            
            .metric-grid-small {{
                grid-template-columns: repeat(2, 1fr);
            }}
            
            .forecast-mini-stats {{
                grid-template-columns: repeat(2, 1fr);
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <!-- Header -->
        <div class="header">
            <h1>🏪 Retail Data Lakehouse</h1>
            <div class="subtitle">Complete Analytics Dashboard - Business Insights + Machine Learning Models</div>
        </div>
        
        <!-- KPI Overview -->
        <div class="kpi-grid">
            <div class="kpi-card">
                <div class="kpi-value">{total_revenue}</div>
                <div class="kpi-label">Total Revenue</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-value">{total_transactions}</div>
                <div class="kpi-label">Transactions</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-value">{total_customers}</div>
                <div class="kpi-label">Customers</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-value">{total_products}</div>
                <div class="kpi-label">Products</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-value">{avg_transaction}</div>
                <div class="kpi-label">Avg Transaction</div>
            </div>
        </div>
        
        <!-- Business Analytics Section -->
        <div class="section">
            <h2>📊 Business Analytics</h2>
            
            <div class="tabs">
                <button class="tab active" onclick="switchTab('revenue')">Revenue & Sales</button>
                <button class="tab" onclick="switchTab('customers')">Customers</button>
                <button class="tab" onclick="switchTab('inventory')">Inventory & Products</button>
                <button class="tab" onclick="switchTab('marketing')">Marketing</button>
            </div>
            
            <div id="revenue" class="tab-content active">
                <div class="two-col">
                    {f'<div class="viz-container"><img src="{images["revenue_store"]}" alt="Revenue by Store"></div>' if 'revenue_store' in images else ''}
                    {f'<div class="viz-container"><img src="{images["sales_trend"]}" alt="Sales Trend"></div>' if 'sales_trend' in images else ''}
                </div>
            </div>
            
            <div id="customers" class="tab-content">
                <div class="two-col">
                    {f'<div class="viz-container"><img src="{images["customer_dist"]}" alt="Customer Distribution"></div>' if 'customer_dist' in images else ''}
                    {f'<div class="viz-container"><img src="{images["gold_kpis"]}" alt="Customer KPIs"></div>' if 'gold_kpis' in images else ''}
                </div>
            </div>
            
            <div id="inventory" class="tab-content">
                <div class="two-col">
                    {f'<div class="viz-container"><img src="{images["inventory"]}" alt="Inventory Analysis"></div>' if 'inventory' in images else ''}
                    {f'<div class="viz-container"><img src="{images["top_products"]}" alt="Top Products"></div>' if 'top_products' in images else ''}
                </div>
            </div>
            
            <div id="marketing" class="tab-content">
                {f'<div class="viz-container"><img src="{images["marketing"]}" alt="Marketing Performance"></div>' if 'marketing' in images else ''}
            </div>
        </div>
        
        <!-- ML Models Section -->
        <div class="section">
            <h2>🤖 Machine Learning Models</h2>
            
            <div class="tabs">
                <button class="tab active" onclick="switchTab('segmentation')">Customer Segmentation</button>
                <button class="tab" onclick="switchTab('forecasting')">Demand Forecasting</button>
            </div>
            
            <div id="segmentation" class="tab-content active">
                <p style="color: #666; margin-bottom: 20px; font-size: 1.1em;">
                    K-Means clustering identified customer segments for targeted marketing strategies.
                </p>
                {segment_cards}
                {f'<div class="viz-container"><img src="{images["seg_analysis"]}" alt="Customer Segmentation"></div>' if 'seg_analysis' in images else ''}
            </div>
            
            <div id="forecasting" class="tab-content">
                <p style="color: #666; margin-bottom: 20px; font-size: 1.1em;">
                    Gradient Boosting model forecasts 30-day product demand for inventory optimization.
                </p>
                {forecast_stats}
                <h3 style="color: #333; margin: 25px 0 10px 0;">Top 5 Priority Orders</h3>
                {forecast_table}
                <div class="two-col" style="margin-top: 25px;">
                    {f'<div class="viz-container"><img src="{images["forecast_analysis"]}" alt="Forecast Analysis"></div>' if 'forecast_analysis' in images else ''}
                    {f'<div class="viz-container"><img src="{images["forecast_results"]}" alt="Forecast Results"></div>' if 'forecast_results' in images else ''}
                </div>
            </div>
        </div>
        
        <!-- Footer -->
        <div class="footer">
            <p><strong>Retail Data Lakehouse Project</strong> | Medallion Architecture Implementation</p>
            <p>Business Analytics + Machine Learning (Customer Segmentation + Demand Forecasting)</p>
            <p style="margin-top: 10px;">Generated: November 4, 2025 | Apache Spark + Delta Lake + Python + scikit-learn</p>
        </div>
    </div>
    
    <script>
        function switchTab(tabName) {{
            // Hide all tab contents
            const contents = document.querySelectorAll('.tab-content');
            contents.forEach(content => content.classList.remove('active'));
            
            // Remove active class from all tabs
            const tabs = document.querySelectorAll('.tab');
            tabs.forEach(tab => tab.classList.remove('active'));
            
            // Show selected tab content
            const selectedContent = document.getElementById(tabName);
            if (selectedContent) {{
                selectedContent.classList.add('active');
            }}
            
            // Add active class to clicked tab
            event.target.classList.add('active');
        }}
    </script>
</body>
</html>
    """
    
    # Save dashboard
    output_path = Path("complete_dashboard.html")
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"✅ Unified Dashboard created: {output_path.absolute()}")
    
    return output_path

def main():
    """Main execution"""
    print("\n" + "=" * 100)
    print("  📊 CREATING UNIFIED DASHBOARD (Business + ML Models)")
    print("=" * 100 + "\n")
    
    # Create dashboard
    dashboard_path = create_unified_dashboard()
    
    print("\n" + "=" * 100)
    print("  ✅ UNIFIED DASHBOARD CREATION COMPLETE!")
    print("=" * 100 + "\n")
    
    print(f"Dashboard saved to: {dashboard_path.absolute()}\n")
    print("This dashboard includes:")
    print("  ✓ Business Analytics (Revenue, Sales, Customers, Inventory, Marketing)")
    print("  ✓ ML Customer Segmentation (K-Means Clustering)")
    print("  ✓ ML Demand Forecasting (Gradient Boosting)")
    print("\nOpening dashboard in your default browser...")
    
    # Open dashboard
    try:
        import os
        os.startfile(str(dashboard_path.absolute()))
        print("✅ Dashboard opened!\n")
    except Exception as e:
        print(f"⚠️  Could not auto-open: {e}")
        print(f"Please manually open: {dashboard_path.absolute()}\n")

if __name__ == "__main__":
    main()
