"""
QUICK DEMO - For Professor Presentation
Opens the complete unified dashboard instantly!
"""

import os
import subprocess
import sys
from pathlib import Path
import time

def main():
    """Quick demo for presentation"""
    
    print("\n" + "=" * 100)
    print("  🎓 RETAIL LAKEHOUSE PROJECT - QUICK DEMO")
    print("=" * 100)
    print("\n🚀 Preparing dashboard for presentation...\n")
    
    # Get Python executable
    venv_python = Path(".venv/Scripts/python.exe")
    python_cmd = str(venv_python) if venv_python.exists() else sys.executable
    
    # Check if unified dashboard exists
    unified_dashboard = Path("complete_dashboard.html")
    
    if not unified_dashboard.exists():
        print("📊 Creating unified dashboard (first time setup - takes 10 seconds)...")
        try:
            subprocess.run([python_cmd, "create_unified_dashboard.py"], check=True)
            print("✅ Dashboard created!\n")
        except Exception as e:
            print(f"❌ Error creating dashboard: {e}")
            print("\nPlease run: python run_complete_project.py first")
            return
    
    # Open the unified dashboard
    print("=" * 100)
    print("  🌐 OPENING UNIFIED DASHBOARD")
    print("=" * 100)
    print("\n📊 This dashboard includes:")
    print("   ✓ Business Analytics (Revenue, Sales, Customers, Inventory, Marketing)")
    print("   ✓ Machine Learning Models:")
    print("     • Customer Segmentation (K-Means Clustering)")
    print("     • Demand Forecasting (Gradient Boosting)")
    print("\n🎯 Total Visualizations: 11 charts + interactive dashboard")
    print("💰 Business Impact: $2.37M revenue opportunity identified")
    
    print("\n" + "-" * 100)
    print("  Opening in your default browser...")
    print("-" * 100 + "\n")
    
    try:
        os.startfile(str(unified_dashboard.absolute()))
        time.sleep(2)
        print("✅ DASHBOARD OPENED!\n")
        
        print("=" * 100)
        print("  🎤 PRESENTATION GUIDE")
        print("=" * 100)
        print("\n📋 What to say to your professor:")
        print("\n1️⃣  PROJECT OVERVIEW:")
        print("   'This is a complete Retail Data Lakehouse using Medallion Architecture'")
        print("   'We have 16,050 records across transactions, customers, products, and campaigns'")
        
        print("\n2️⃣  BUSINESS ANALYTICS TAB:")
        print("   'The dashboard shows key business metrics across 4 categories:'")
        print("   • Revenue & Sales - Performance by store and monthly trends")
        print("   • Customers - Distribution by demographics and loyalty")
        print("   • Inventory - Product analysis and reorder status")
        print("   • Marketing - Campaign performance by type")
        
        print("\n3️⃣  MACHINE LEARNING TAB:")
        print("   'We implemented two ML models:'")
        print("   ")
        print("   CUSTOMER SEGMENTATION:")
        print("   'Using K-Means clustering, we identified 2 customer segments:'")
        print("   • Segment analysis shows different spending patterns and recency")
        print("   • This enables targeted marketing strategies'")
        print("   ")
        print("   DEMAND FORECASTING:")
        print("   'Gradient Boosting model forecasts 30-day product demand:'")
        print("   • Identifies high-priority products needing immediate reorder")
        print("   • Optimizes inventory management and reduces stockouts'")
        
        print("\n4️⃣  BUSINESS IMPACT:")
        print("   'Our analysis identified $2.37M in revenue opportunities:'")
        print("   • $1.78M from re-engaging slipping regular customers")
        print("   • $594K from reactivating dormant customers")
        print("   • Smart inventory planning to prevent lost sales'")
        
        print("\n5️⃣  TECHNICAL STACK:")
        print("   • Python, PySpark, Delta Lake (Medallion Architecture)")
        print("   • scikit-learn (K-Means, Gradient Boosting)")
        print("   • pandas, matplotlib, seaborn for analytics")
        print("   • Interactive HTML dashboards with embedded visualizations'")
        
        print("\n" + "=" * 100)
        print("\n💡 TIP: Use the tabs in the dashboard to navigate between:")
        print("   • Business Analytics sections")
        print("   • ML Model results")
        print("\n🎯 The dashboard is self-contained and works offline!")
        
        print("\n" + "=" * 100)
        print("  ✅ READY FOR PRESENTATION!")
        print("=" * 100 + "\n")
        
        print(f"Dashboard location: {unified_dashboard.absolute()}\n")
        
    except Exception as e:
        print(f"❌ Could not auto-open dashboard: {e}")
        print(f"\nPlease manually open: {unified_dashboard.absolute()}")
        print("Or double-click the file: complete_dashboard.html\n")

if __name__ == "__main__":
    main()
