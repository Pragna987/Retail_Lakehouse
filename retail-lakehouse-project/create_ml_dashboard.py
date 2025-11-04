"""
Create ML Models Dashboard - Combined Interactive HTML Dashboard
Shows Customer Segmentation and Demand Forecasting results in one page
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

def create_ml_dashboard():
    """Create comprehensive ML models dashboard"""
    print("\n📊 Creating ML Models Dashboard...")
    
    # Load data
    segment_file = Path("ml_models/outputs/segment_analysis.csv")
    forecast_file = Path("ml_models/outputs/demand_forecast.csv")
    
    # Get segment data
    segment_data = ""
    if segment_file.exists():
        segments = pd.read_csv(segment_file, index_col=0)
        
        segment_cards = ""
        for idx, row in segments.iterrows():
            segment_cards += f"""
            <div class="segment-card">
                <h3>{row['segment_name']}</h3>
                <div class="metric-grid">
                    <div class="metric">
                        <div class="metric-value">{int(row['customer_count']):,}</div>
                        <div class="metric-label">Customers</div>
                    </div>
                    <div class="metric">
                        <div class="metric-value">${row['total_revenue']/1e6:.2f}M</div>
                        <div class="metric-label">Revenue</div>
                    </div>
                    <div class="metric">
                        <div class="metric-value">${row['avg_total_spent']:,.0f}</div>
                        <div class="metric-label">Avg Spending</div>
                    </div>
                    <div class="metric">
                        <div class="metric-value">{row['avg_recency_days']:.0f}</div>
                        <div class="metric-label">Days Since Last Purchase</div>
                    </div>
                    <div class="metric">
                        <div class="metric-value">{row['avg_frequency']:.1f}</div>
                        <div class="metric-label">Avg Transactions</div>
                    </div>
                    <div class="metric">
                        <div class="metric-value">{row['avg_age']:.0f}</div>
                        <div class="metric-label">Avg Age</div>
                    </div>
                </div>
            </div>
            """
        
        segment_data = segment_cards
    
    # Get forecast summary
    forecast_summary = ""
    top_products_html = ""
    if forecast_file.exists():
        forecast = pd.read_csv(forecast_file)
        
        urgency_counts = forecast['urgency'].value_counts()
        high = urgency_counts.get('HIGH', 0)
        medium = urgency_counts.get('MEDIUM', 0)
        low = urgency_counts.get('LOW', 0)
        
        forecast_summary = f"""
        <div class="forecast-stats">
            <div class="stat-card high">
                <div class="stat-value">{high}</div>
                <div class="stat-label">High Priority</div>
                <div class="stat-desc">Below Reorder Point</div>
            </div>
            <div class="stat-card medium">
                <div class="stat-value">{medium}</div>
                <div class="stat-label">Medium Priority</div>
                <div class="stat-desc">Order Recommended</div>
            </div>
            <div class="stat-card low">
                <div class="stat-value">{low}</div>
                <div class="stat-label">Low Priority</div>
                <div class="stat-desc">Stock Sufficient</div>
            </div>
            <div class="stat-card total">
                <div class="stat-value">{int(forecast['recommended_order_qty'].sum()):,}</div>
                <div class="stat-label">Total Units to Order</div>
                <div class="stat-desc">30-Day Forecast</div>
            </div>
        </div>
        """
        
        # Top 10 priority products
        top_10 = forecast.nlargest(10, 'recommended_order_qty')
        products_rows = ""
        for idx, row in top_10.iterrows():
            urgency_class = row['urgency'].lower()
            products_rows += f"""
            <tr class="urgency-{urgency_class}">
                <td>{row['product_id']}</td>
                <td>{row['category']}</td>
                <td>{int(row['current_stock'])}</td>
                <td>{int(row['30day_forecast'])}</td>
                <td><strong>{int(row['recommended_order_qty'])}</strong></td>
                <td><span class="badge badge-{urgency_class}">{row['urgency']}</span></td>
            </tr>
            """
        
        top_products_html = f"""
        <div class="table-container">
            <table class="products-table">
                <thead>
                    <tr>
                        <th>Product ID</th>
                        <th>Category</th>
                        <th>Current Stock</th>
                        <th>30-Day Forecast</th>
                        <th>Order Qty</th>
                        <th>Urgency</th>
                    </tr>
                </thead>
                <tbody>
                    {products_rows}
                </tbody>
            </table>
        </div>
        """
    
    # Load images
    img_paths = {
        'seg_analysis': 'ml_models/outputs/customer_segmentation_analysis.png',
        'seg_elbow': 'ml_models/outputs/customer_segmentation_elbow.png',
        'forecast_analysis': 'ml_models/outputs/demand_forecasting_analysis.png',
        'forecast_results': 'ml_models/outputs/demand_forecast_results.png'
    }
    
    images = {}
    for key, path in img_paths.items():
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
    <title>ML Models Dashboard - Retail Lakehouse</title>
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
            max-width: 1400px;
            margin: 0 auto;
        }}
        
        .header {{
            background: white;
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            margin-bottom: 30px;
            text-align: center;
        }}
        
        .header h1 {{
            color: #667eea;
            font-size: 2.5em;
            margin-bottom: 10px;
        }}
        
        .header .subtitle {{
            color: #666;
            font-size: 1.2em;
        }}
        
        .section {{
            background: white;
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            margin-bottom: 30px;
        }}
        
        .section h2 {{
            color: #667eea;
            font-size: 2em;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 3px solid #667eea;
        }}
        
        .segment-card {{
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            padding: 25px;
            border-radius: 10px;
            margin-bottom: 20px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }}
        
        .segment-card h3 {{
            color: #333;
            font-size: 1.8em;
            margin-bottom: 15px;
        }}
        
        .metric-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 15px;
        }}
        
        .metric {{
            background: white;
            padding: 15px;
            border-radius: 8px;
            text-align: center;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }}
        
        .metric-value {{
            font-size: 1.8em;
            font-weight: bold;
            color: #667eea;
            margin-bottom: 5px;
        }}
        
        .metric-label {{
            font-size: 0.9em;
            color: #666;
        }}
        
        .forecast-stats {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}
        
        .stat-card {{
            padding: 25px;
            border-radius: 10px;
            text-align: center;
            color: white;
            box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        }}
        
        .stat-card.high {{
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        }}
        
        .stat-card.medium {{
            background: linear-gradient(135deg, #ffc837 0%, #ff8008 100%);
        }}
        
        .stat-card.low {{
            background: linear-gradient(135deg, #a8edea 0%, #6dd5ed 100%);
        }}
        
        .stat-card.total {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        }}
        
        .stat-value {{
            font-size: 2.5em;
            font-weight: bold;
            margin-bottom: 10px;
        }}
        
        .stat-label {{
            font-size: 1.2em;
            margin-bottom: 5px;
        }}
        
        .stat-desc {{
            font-size: 0.9em;
            opacity: 0.9;
        }}
        
        .table-container {{
            overflow-x: auto;
        }}
        
        .products-table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
        }}
        
        .products-table thead {{
            background: #667eea;
            color: white;
        }}
        
        .products-table th {{
            padding: 15px;
            text-align: left;
            font-weight: 600;
        }}
        
        .products-table td {{
            padding: 12px 15px;
            border-bottom: 1px solid #ddd;
        }}
        
        .products-table tr:hover {{
            background: #f5f5f5;
        }}
        
        .urgency-high {{
            background: #ffe5e5;
        }}
        
        .badge {{
            padding: 5px 12px;
            border-radius: 20px;
            font-size: 0.85em;
            font-weight: bold;
        }}
        
        .badge-high {{
            background: #f5576c;
            color: white;
        }}
        
        .badge-medium {{
            background: #ff8008;
            color: white;
        }}
        
        .badge-low {{
            background: #6dd5ed;
            color: white;
        }}
        
        .viz-container {{
            margin: 20px 0;
        }}
        
        .viz-container img {{
            width: 100%;
            height: auto;
            border-radius: 10px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }}
        
        .viz-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(500px, 1fr));
            gap: 20px;
            margin-top: 20px;
        }}
        
        .footer {{
            background: white;
            padding: 20px;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            text-align: center;
            color: #666;
            margin-top: 30px;
        }}
        
        .footer strong {{
            color: #667eea;
        }}
        
        @media (max-width: 768px) {{
            .viz-grid {{
                grid-template-columns: 1fr;
            }}
            
            .metric-grid {{
                grid-template-columns: repeat(2, 1fr);
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <!-- Header -->
        <div class="header">
            <h1>🤖 Machine Learning Models Dashboard</h1>
            <div class="subtitle">Customer Segmentation & Demand Forecasting | Retail Lakehouse Project</div>
        </div>
        
        <!-- Customer Segmentation Section -->
        <div class="section">
            <h2>🎯 Customer Segmentation Analysis</h2>
            <p style="margin-bottom: 20px; color: #666; font-size: 1.1em;">
                K-Means clustering identified distinct customer segments for targeted marketing strategies.
            </p>
            
            {segment_data}
            
            <div class="viz-grid">
                {f'<div class="viz-container"><img src="{images["seg_analysis"]}" alt="Customer Segmentation Analysis"></div>' if 'seg_analysis' in images else ''}
                {f'<div class="viz-container"><img src="{images["seg_elbow"]}" alt="Optimal Clusters"></div>' if 'seg_elbow' in images else ''}
            </div>
        </div>
        
        <!-- Demand Forecasting Section -->
        <div class="section">
            <h2>📈 Demand Forecasting & Inventory Optimization</h2>
            <p style="margin-bottom: 20px; color: #666; font-size: 1.1em;">
                Gradient Boosting model forecasts 30-day product demand for proactive inventory management.
            </p>
            
            {forecast_summary}
            
            <h3 style="color: #333; margin: 30px 0 15px 0;">🎯 Top 10 Priority Orders</h3>
            {top_products_html}
            
            <div class="viz-grid" style="margin-top: 30px;">
                {f'<div class="viz-container"><img src="{images["forecast_analysis"]}" alt="Demand Forecasting Analysis"></div>' if 'forecast_analysis' in images else ''}
                {f'<div class="viz-container"><img src="{images["forecast_results"]}" alt="Forecast Results"></div>' if 'forecast_results' in images else ''}
            </div>
        </div>
        
        <!-- Footer -->
        <div class="footer">
            <p><strong>Retail Data Lakehouse Project</strong> | Machine Learning Models Dashboard</p>
            <p>Customer Segmentation (K-Means) + Demand Forecasting (Gradient Boosting)</p>
            <p style="margin-top: 10px;">Generated: November 4, 2025</p>
        </div>
    </div>
</body>
</html>
    """
    
    # Save dashboard
    output_path = Path("ml_models/ml_dashboard.html")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"✅ ML Dashboard created: {output_path.absolute()}")
    
    return output_path

def main():
    """Main execution"""
    print("\n" + "=" * 100)
    print("  📊 CREATING ML MODELS DASHBOARD")
    print("=" * 100 + "\n")
    
    # Create dashboard
    dashboard_path = create_ml_dashboard()
    
    print("\n" + "=" * 100)
    print("  ✅ DASHBOARD CREATION COMPLETE!")
    print("=" * 100 + "\n")
    
    print(f"Dashboard saved to: {dashboard_path.absolute()}\n")
    print("Opening dashboard in your default browser...")
    
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
