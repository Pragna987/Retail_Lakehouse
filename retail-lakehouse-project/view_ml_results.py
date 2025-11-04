"""
View ML Model Results - Quick Summary
Displays key findings from both ML models
"""

import pandas as pd
from pathlib import Path

def print_header(text):
    """Print formatted header"""
    print("\n" + "=" * 100)
    print(f"  {text}")
    print("=" * 100 + "\n")

def view_customer_segmentation():
    """Display customer segmentation results"""
    print_header("🎯 MODEL 1: CUSTOMER SEGMENTATION RESULTS")
    
    # Load segment analysis
    segment_file = Path("ml_models/outputs/segment_analysis.csv")
    if segment_file.exists():
        segments = pd.read_csv(segment_file, index_col=0)
        
        print("📊 CUSTOMER SEGMENTS IDENTIFIED:\n")
        print(segments.to_string())
        print("\n")
        
        print("💡 KEY INSIGHTS:")
        for idx in segments.index:
            segment = segments.loc[idx]
            print(f"\n   {segment['segment_name']}")
            print(f"   • Size: {int(segment['customer_count']):,} customers")
            print(f"   • Total Revenue: ${segment['total_revenue']:,.2f}")
            print(f"   • Avg Spending: ${segment['avg_total_spent']:.2f} per customer")
            print(f"   • Avg Recency: {segment['avg_recency_days']:.0f} days since last purchase")
            print(f"   • Avg Frequency: {segment['avg_frequency']:.1f} transactions")
        
        print("\n")
    else:
        print("❌ Segment analysis file not found")

def view_demand_forecast():
    """Display demand forecasting results"""
    print_header("📈 MODEL 2: DEMAND FORECASTING RESULTS")
    
    # Load forecast
    forecast_file = Path("ml_models/outputs/demand_forecast.csv")
    if forecast_file.exists():
        forecast = pd.read_csv(forecast_file)
        
        print("📊 FORECAST SUMMARY:\n")
        print(f"   Total Products Analyzed: {len(forecast):,}")
        
        # Urgency breakdown
        urgency_counts = forecast['urgency'].value_counts()
        print(f"\n   Urgency Breakdown:")
        for urgency in ['HIGH', 'MEDIUM', 'LOW']:
            if urgency in urgency_counts.index:
                count = urgency_counts[urgency]
                pct = (count / len(forecast)) * 100
                print(f"   • {urgency:6s}: {count:4d} products ({pct:5.1f}%)")
        
        # Top priority orders
        print(f"\n   🎯 TOP 10 PRIORITY ORDERS (Immediate Action Required):")
        print("   " + "-" * 96)
        print(f"   {'Product':<10} {'Category':<15} {'Current':<10} {'30-Day':<12} {'Recommended':<15} {'Urgency':<8}")
        print(f"   {'ID':<10} {'':<15} {'Stock':<10} {'Forecast':<12} {'Order Qty':<15} {'':<8}")
        print("   " + "-" * 96)
        
        top_10 = forecast.nlargest(10, 'recommended_order_qty')
        for idx, row in top_10.iterrows():
            print(f"   {row['product_id']:<10} {row['category']:<15} "
                  f"{int(row['current_stock']):<10} {int(row['30day_forecast']):<12} "
                  f"{int(row['recommended_order_qty']):<15} {row['urgency']:<8}")
        
        # Category summary
        print(f"\n   📦 FORECAST BY CATEGORY:")
        category_forecast = forecast.groupby('category').agg({
            '30day_forecast': 'sum',
            'recommended_order_qty': 'sum'
        }).sort_values('30day_forecast', ascending=False)
        
        for category, row in category_forecast.iterrows():
            print(f"   • {category:15s}: {int(row['30day_forecast']):5d} units forecasted, "
                  f"{int(row['recommended_order_qty']):5d} units to order")
        
        print("\n")
    else:
        print("❌ Demand forecast file not found")

def view_files_created():
    """Show all output files created"""
    print_header("📁 OUTPUT FILES CREATED")
    
    output_dir = Path("ml_models/outputs")
    if output_dir.exists():
        files = list(output_dir.glob("*"))
        
        print("Visualizations:")
        for f in sorted(files):
            if f.suffix == '.png':
                size_kb = f.stat().st_size / 1024
                print(f"   ✅ {f.name:<45} ({size_kb:,.0f} KB)")
        
        print("\nData Files:")
        for f in sorted(files):
            if f.suffix == '.csv':
                size_kb = f.stat().st_size / 1024
                df = pd.read_csv(f)
                print(f"   ✅ {f.name:<45} ({size_kb:,.0f} KB, {len(df):,} records)")
        
        print(f"\nTotal Files: {len(files)}")
        total_size_mb = sum(f.stat().st_size for f in files) / (1024 * 1024)
        print(f"Total Size: {total_size_mb:.2f} MB")
        print(f"\nLocation: {output_dir.absolute()}")
        print("\n")
    else:
        print("❌ Output directory not found")

def view_business_impact():
    """Calculate and display business impact"""
    print_header("💰 BUSINESS IMPACT ANALYSIS")
    
    segment_file = Path("ml_models/outputs/segment_analysis.csv")
    forecast_file = Path("ml_models/outputs/demand_forecast.csv")
    
    if segment_file.exists():
        segments = pd.read_csv(segment_file, index_col=0)
        total_revenue = segments['total_revenue'].sum()
        
        print("Customer Segmentation Impact:")
        print(f"   • Total Revenue Analyzed: ${total_revenue:,.2f}")
        print(f"   • Number of Segments: {len(segments)}")
        
        # Calculate opportunity
        slipping = segments[segments['segment_name'].str.contains('Slipping', na=False)]
        if len(slipping) > 0:
            slipping_revenue = slipping['total_revenue'].iloc[0]
            print(f"   • 'Slipping Regulars' Revenue at Risk: ${slipping_revenue:,.2f}")
            print(f"   • Potential Win-Back (20% improvement): ${slipping_revenue * 0.20:,.2f}")
        
        dormant = segments[segments['segment_name'].str.contains('Dormant', na=False)]
        if len(dormant) > 0:
            dormant_revenue = dormant['total_revenue'].iloc[0]
            print(f"   • 'Dormant Customers' Reactivation Potential: ${dormant_revenue * 0.15:,.2f}")
    
    if forecast_file.exists():
        forecast = pd.read_csv(forecast_file)
        high_urgency = forecast[forecast['urgency'] == 'HIGH']
        
        print(f"\nDemand Forecasting Impact:")
        print(f"   • Products Analyzed: {len(forecast):,}")
        print(f"   • High-Priority Reorders Needed: {len(high_urgency)}")
        print(f"   • Potential Stockout Prevention: {len(high_urgency)} product lines")
        
        # Estimate inventory optimization
        total_recommended = forecast['recommended_order_qty'].sum()
        print(f"   • Total Units to Order (30 days): {int(total_recommended):,}")
        
        # Estimate cost savings
        avg_unit_cost = 50  # Approximate
        inventory_value = total_recommended * avg_unit_cost
        print(f"   • Estimated Inventory Investment: ${inventory_value:,.2f}")
    
    print("\n")

def main():
    """Main execution"""
    print("\n" + "🎉" * 50)
    print_header("MACHINE LEARNING MODELS - RESULTS SUMMARY")
    print("🎉" * 50)
    
    # Display results
    view_customer_segmentation()
    view_demand_forecast()
    view_business_impact()
    view_files_created()
    
    print_header("✅ RESULTS REVIEW COMPLETE")
    
    print("To view visualizations:")
    print("   1. Navigate to: ml_models/outputs/")
    print("   2. Open PNG files to see charts")
    print("   3. Open CSV files for detailed data")
    print("\nKey Files:")
    print("   • customer_segmentation_analysis.png - Complete segmentation dashboard")
    print("   • demand_forecasting_analysis.png - Model performance metrics")
    print("   • demand_forecast_results.png - Forecast visualizations")
    print("   • customer_segments.csv - Individual customer assignments")
    print("   • demand_forecast.csv - Product-level forecasts")
    print("\n" + "=" * 100 + "\n")

if __name__ == "__main__":
    main()
