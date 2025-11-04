
"""
RUN COMPLETE PROJECT - Master Execution Script
Executes the entire Retail Lakehouse project including:
1. Data Generation
2. Business Analytics & Visualizations
3. Customer Segmentation ML Model
4. Demand Forecasting ML Model
5. Opens all dashboards and results
"""

import subprocess
import sys
from pathlib import Path
from datetime import datetime
import time

def print_header(text, char="="):
    """Print formatted header"""
    print("\n" + char * 100)
    print(f"  {text}")
    print(char * 100 + "\n")

def print_step(step_num, total_steps, description):
    """Print step information"""
    print(f"\n{'='*100}")
    print(f"  STEP {step_num}/{total_steps}: {description}")
    print(f"{'='*100}\n")

def run_script(script_name, description):
    """Run a Python script"""
    try:
        # Get the virtual environment Python executable
        venv_python = Path(".venv/Scripts/python.exe")
        
        if venv_python.exists():
            python_cmd = str(venv_python)
        else:
            python_cmd = sys.executable
        
        print(f"▶️  Running: {script_name}")
        print(f"   Description: {description}\n")
        
        # Run the script
        result = subprocess.run(
            [python_cmd, script_name],
            capture_output=False,
            text=True,
            check=True
        )
        
        print(f"\n✅ {description} - COMPLETED!")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Error running {script_name}")
        print(f"Error: {e}")
        return False
    except Exception as e:
        print(f"\n❌ Unexpected error running {script_name}")
        print(f"Error: {e}")
        return False

def open_visualizations():
    """Open all visualization dashboards"""
    print_header("OPENING DASHBOARDS", "~")
    
    try:
        import os
        
        # Open ML Dashboard (combined Customer Segmentation + Demand Forecasting)
        ml_dashboard = Path("ml_models/ml_dashboard.html")
        if ml_dashboard.exists():
            print("🤖 Opening ML Models Dashboard (Customer Segmentation + Demand Forecasting)...")
            os.startfile(str(ml_dashboard.absolute()))
            time.sleep(2)
            print("   ✓ Shows both ML models in one interactive dashboard!")
        else:
            print("⚠️  ML Dashboard not found. Creating it now...")
            # Create the ML dashboard
            result = subprocess.run(
                [sys.executable, "create_ml_dashboard.py"],
                capture_output=True,
                text=True
            )
            if ml_dashboard.exists():
                os.startfile(str(ml_dashboard.absolute()))
                print("   ✓ ML Dashboard created and opened!")
        
        time.sleep(1)
        
        # Open business dashboard
        dashboard = Path("visualizations/dashboard.html")
        if dashboard.exists():
            print("� Opening Business Analytics Dashboard...")
            os.startfile(str(dashboard.absolute()))
            print("   ✓ Shows business metrics and visualizations!")
        
        print("\n✅ All dashboards opened successfully!")
        print("\n📂 Dashboards opened:")
        print("   1. ML Models Dashboard (ml_models/ml_dashboard.html)")
        print("      → Customer Segmentation + Demand Forecasting")
        print("   2. Business Analytics Dashboard (visualizations/dashboard.html)")
        print("      → Revenue, Sales, Customers, Inventory, Marketing")
        
    except Exception as e:
        print(f"\n⚠️  Could not auto-open visualizations: {e}")
        print("Please manually open:")
        print("  • ml_models/ml_dashboard.html (ML Models)")
        print("  • visualizations/dashboard.html (Business Analytics)")

def display_results_summary():
    """Display final results summary"""
    print_header("📊 PROJECT EXECUTION SUMMARY", "=")
    
    import pandas as pd
    
    # Customer Segmentation Results
    segment_file = Path("ml_models/outputs/segment_analysis.csv")
    if segment_file.exists():
        segments = pd.read_csv(segment_file, index_col=0)
        print("\n🎯 CUSTOMER SEGMENTATION:")
        print(f"   • Total Customers Analyzed: {int(segments['customer_count'].sum()):,}")
        print(f"   • Total Revenue: ${segments['total_revenue'].sum():,.2f}")
        print(f"   • Segments Identified: {len(segments)}")
        for idx, row in segments.iterrows():
            print(f"     - {row['segment_name']}: {int(row['customer_count']):,} customers, ${row['total_revenue']:,.2f}")
    
    # Demand Forecast Results
    forecast_file = Path("ml_models/outputs/demand_forecast.csv")
    if forecast_file.exists():
        forecast = pd.read_csv(forecast_file)
        urgency_counts = forecast['urgency'].value_counts()
        print(f"\n📈 DEMAND FORECASTING:")
        print(f"   • Total Products Forecasted: {len(forecast):,}")
        print(f"   • High Urgency (Immediate Reorder): {urgency_counts.get('HIGH', 0)}")
        print(f"   • Medium Urgency (Order Soon): {urgency_counts.get('MEDIUM', 0)}")
        print(f"   • Low Urgency (Stock Sufficient): {urgency_counts.get('LOW', 0)}")
        print(f"   • Total Units to Order (30 days): {int(forecast['recommended_order_qty'].sum()):,}")
    
    # Data Files
    print(f"\n📁 DATA GENERATED:")
    data_files = {
        'raw_data/pos_transactions.csv': 'POS Transactions',
        'raw_data/customers.csv': 'Customers',
        'raw_data/products_inventory.csv': 'Products',
        'raw_data/marketing_campaigns.csv': 'Marketing Campaigns'
    }
    
    total_records = 0
    for file_path, name in data_files.items():
        if Path(file_path).exists():
            df = pd.read_csv(file_path)
            print(f"   • {name}: {len(df):,} records")
            total_records += len(df)
    
    print(f"   • TOTAL: {total_records:,} records")
    
    # Visualizations
    viz_count = len(list(Path("visualizations").glob("*.png"))) if Path("visualizations").exists() else 0
    ml_viz_count = len(list(Path("ml_models/outputs").glob("*.png"))) if Path("ml_models/outputs").exists() else 0
    
    print(f"\n📊 VISUALIZATIONS CREATED:")
    print(f"   • Business Charts: {viz_count}")
    print(f"   • ML Model Charts: {ml_viz_count}")
    print(f"   • Dashboards: 2 (Business + ML)")
    print(f"   • TOTAL: {viz_count + ml_viz_count + 2} visualizations")

def main():
    """Main execution"""
    start_time = datetime.now()
    
    print("\n" + "🚀" * 50)
    print_header("RETAIL LAKEHOUSE - COMPLETE PROJECT EXECUTION", "=")
    print("This script will execute your ENTIRE project including:")
    print("  ✓ Data Generation (16,050 records)")
    print("  ✓ Business Analytics & Visualizations (8 charts)")
    print("  ✓ Customer Segmentation ML Model (K-Means)")
    print("  ✓ Demand Forecasting ML Model (Gradient Boosting)")
    print("  ✓ Results Summary & ML Dashboard Creation")
    print("  ✓ Auto-open Interactive Dashboards")
    print("\n" + "🚀" * 50)
    
    input("\nPress ENTER to begin execution...")
    
    # Track results
    results = {}
    total_steps = 6
    
    # Step 1: Generate Data
    print_step(1, total_steps, "GENERATE RETAIL DATA")
    results['Data Generation'] = run_script(
        'generate_retail_data.py',
        'Generate 16,050 retail records'
    )
    
    if not results['Data Generation']:
        print("\n❌ Data generation failed. Cannot continue.")
        return
    
    # Step 2: Business Visualizations
    print_step(2, total_steps, "CREATE BUSINESS VISUALIZATIONS")
    results['Business Visualizations'] = run_script(
        'generate_visualizations.py',
        'Create 8 business charts + dashboard'
    )
    
    # Step 3: Customer Segmentation
    print_step(3, total_steps, "CUSTOMER SEGMENTATION ML MODEL")
    results['Customer Segmentation'] = run_script(
        'ml_customer_segmentation.py',
        'K-Means clustering on customer data'
    )
    
    # Step 4: Demand Forecasting
    print_step(4, total_steps, "DEMAND FORECASTING ML MODEL")
    results['Demand Forecasting'] = run_script(
        'ml_demand_forecasting.py',
        'Gradient Boosting for inventory prediction'
    )
    
    # Step 5: View Results
    print_step(5, total_steps, "VIEW RESULTS SUMMARY")
    results['View Results'] = run_script(
        'view_ml_results.py',
        'Display comprehensive results'
    )
    
    # Step 6: Create ML Dashboard
    print_step(6, total_steps, "CREATE ML DASHBOARD")
    results['ML Dashboard'] = run_script(
        'create_ml_dashboard.py',
        'Create combined ML dashboard (Segmentation + Forecasting)'
    )
    
    # Calculate execution time
    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()
    
    # Print execution summary
    print_header("✅ EXECUTION COMPLETE!", "=")
    
    print("\n📊 COMPONENT STATUS:")
    print("-" * 100)
    for component, success in results.items():
        status = "✅ SUCCESS" if success else "❌ FAILED"
        print(f"  {component:30s} {status}")
    print("-" * 100)
    
    successful = sum(results.values())
    total = len(results)
    
    print(f"\nTotal: {successful}/{total} components completed successfully")
    print(f"Execution Time: {duration:.1f} seconds ({duration/60:.1f} minutes)")
    
    if all(results.values()):
        print("\n" + "🎉" * 50)
        print_header("🎉 ALL COMPONENTS COMPLETED SUCCESSFULLY! 🎉", "=")
        print("🎉" * 50)
        
        # Display results summary
        display_results_summary()
        
        # Open visualizations
        print("\n")
        open_visualizations()
        
        print("\n" + "=" * 100)
        print("\n📂 YOUR COMPLETE PROJECT OUTPUT:")
        print("=" * 100)
        print("\n📊 Data Files:")
        print("   📁 raw_data/")
        print("      • pos_transactions.csv")
        print("      • customers.csv")
        print("      • products_inventory.csv")
        print("      • marketing_campaigns.csv")
        
        print("\n📈 Visualizations:")
        print("   📁 visualizations/")
        print("      • dashboard.html (Interactive Business Dashboard)")
        print("      • 01-08_*.png (8 Business Charts)")
        
        print("\n🤖 ML Model Outputs:")
        print("   📁 ml_models/outputs/")
        print("      • customer_segmentation_analysis.png")
        print("      • customer_segmentation_elbow.png")
        print("      • customer_segments.csv")
        print("      • segment_analysis.csv")
        print("      • demand_forecasting_analysis.png")
        print("      • demand_forecast_results.png")
        print("      • demand_forecast.csv")
        
        print("\n" + "=" * 100)
        print("\n🎓 YOUR PROJECT IS READY FOR:")
        print("   ✓ Academic submission")
        print("   ✓ Portfolio showcase")
        print("   ✓ Job interviews")
        print("   ✓ GitHub upload")
        
        print("\n📋 NEXT STEPS:")
        print("   1. Review all opened visualizations")
        print("   2. Check ml_models/outputs/ for detailed results")
        print("   3. Read OPTION_B_COMPLETE.md for full documentation")
        print("   4. Follow GITHUB_UPLOAD_GUIDE.md to share your project")
        
    else:
        print("\n⚠️  Some components failed. Please check the error messages above.")
        print("You can re-run individual scripts to troubleshoot:")
        for component, success in results.items():
            if not success:
                print(f"  • {component}")
    
    print("\n" + "=" * 100 + "\n")

if __name__ == "__main__":
    main()
