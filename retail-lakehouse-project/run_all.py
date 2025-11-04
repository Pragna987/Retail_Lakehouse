"""
Master Pipeline Executor
Runs the complete Data Lakehouse pipeline from setup to analytics
"""

import subprocess
import sys
import os


def run_script(script_name, description):
    """Run a Python script and report status"""
    print(f"\n{'='*70}")
    print(f"🔄 {description}")
    print(f"{'='*70}\n")
    
    try:
        result = subprocess.run(
            [sys.executable, script_name],
            check=True,
            capture_output=False
        )
        print(f"\n✅ {description} completed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n❌ {description} failed with error code: {e.returncode}")
        return False
    except FileNotFoundError:
        print(f"\n❌ Script not found: {script_name}")
        return False


def main():
    """Execute all pipeline stages in sequence"""
    
    print("""
╔══════════════════════════════════════════════════════════════════╗
║                                                                  ║
║   DATA LAKEHOUSE ARCHITECTURE - COMPLETE PIPELINE EXECUTION      ║
║   Retail Company Implementation                                 ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝
    """)
    
    # Define pipeline stages
    pipeline_stages = [
        ("setup_storage.py", "Storage Structure Setup"),
        ("generate_retail_data.py", "Sample Data Generation"),
        ("scripts/etl_bronze_layer.py", "Bronze Layer Ingestion"),
        ("scripts/etl_silver_layer.py", "Silver Layer Transformation"),
        ("scripts/etl_gold_layer.py", "Gold Layer Aggregation"),
        ("scripts/analytics_queries.py", "Analytics Queries Execution"),
    ]
    
    results = []
    
    # Execute each stage
    for script, description in pipeline_stages:
        success = run_script(script, description)
        results.append((description, success))
        
        if not success:
            print(f"\n⚠️  Pipeline stopped at: {description}")
            user_input = input("\nContinue anyway? (y/n): ")
            if user_input.lower() != 'y':
                print("\n❌ Pipeline execution aborted by user")
                break
    
    # Print summary
    print(f"\n\n{'='*70}")
    print("📊 PIPELINE EXECUTION SUMMARY")
    print(f"{'='*70}\n")
    
    for description, success in results:
        status = "✅ SUCCESS" if success else "❌ FAILED"
        print(f"{status}: {description}")
    
    success_count = sum(1 for _, s in results if s)
    total_count = len(results)
    
    print(f"\n🎯 Completion Rate: {success_count}/{total_count} stages completed")
    
    if success_count == total_count:
        print("\n" + "="*70)
        print("🎉 Congratulations! Lakehouse implementation completed successfully!")
        print("="*70)
        print("\n📁 Check the following outputs:")
        print("   • data/bronze/ - Raw data in Delta Lake format")
        print("   • data/silver/ - Cleaned and enriched data")
        print("   • data/gold/ - Business-ready analytics tables")
        print("\n📊 Next steps:")
        print("   1. Run ML models: python scripts/ml_demand_forecasting.py")
        print("   2. Run customer segmentation: python scripts/ml_customer_segmentation.py")
        print("   3. Create dashboards: python scripts/dashboard_visualization.py")
        print("   4. Run tests: python scripts/test_lakehouse.py")
    else:
        print("\n⚠️  Some stages failed. Please check the errors above.")
        print("You can re-run individual scripts to troubleshoot:")
        for description, success in results:
            if not success:
                script_name = next((s for s, d in pipeline_stages if d == description), "unknown")
                print(f"   python {script_name}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ Pipeline execution interrupted by user (Ctrl+C)")
        sys.exit(1)
