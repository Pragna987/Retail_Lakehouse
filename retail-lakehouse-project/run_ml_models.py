"""
Master Script: Run All Machine Learning Models
Executes customer segmentation and demand forecasting models
"""

import subprocess
import sys
from pathlib import Path
from datetime import datetime

def print_header(text):
    """Print formatted header"""
    print("\n" + "=" * 100)
    print(f"  {text}")
    print("=" * 100 + "\n")

def run_ml_model(script_name, description):
    """Run a machine learning model script"""
    print_header(f"Running: {description}")
    
    try:
        # Get the virtual environment Python executable
        venv_python = Path(".venv/Scripts/python.exe")
        
        if venv_python.exists():
            python_cmd = str(venv_python)
        else:
            python_cmd = sys.executable
        
        # Run the script
        result = subprocess.run(
            [python_cmd, script_name],
            capture_output=False,
            text=True,
            check=True
        )
        
        print(f"\n✅ {description} completed successfully!")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Error running {description}")
        print(f"Error: {e}")
        return False
    except Exception as e:
        print(f"\n❌ Unexpected error running {description}")
        print(f"Error: {e}")
        return False

def main():
    """Main execution"""
    start_time = datetime.now()
    
    print("\n" + "🤖" * 50)
    print_header("RETAIL LAKEHOUSE - MACHINE LEARNING PIPELINE")
    print("🤖" * 50)
    
    print("This script will run all machine learning models:")
    print("  1. Customer Segmentation (K-Means Clustering)")
    print("  2. Demand Forecasting (Gradient Boosting Regressor)")
    print()
    
    # Track results
    results = {}
    
    # Model 1: Customer Segmentation
    results['Customer Segmentation'] = run_ml_model(
        'ml_customer_segmentation.py',
        'MODEL 1: Customer Segmentation'
    )
    
    # Model 2: Demand Forecasting
    results['Demand Forecasting'] = run_ml_model(
        'ml_demand_forecasting.py',
        'MODEL 2: Demand Forecasting'
    )
    
    # Print summary
    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()
    
    print_header("EXECUTION SUMMARY")
    
    print("Model Results:")
    for model_name, success in results.items():
        status = "✅ SUCCESS" if success else "❌ FAILED"
        print(f"  • {model_name:30s} {status}")
    
    print(f"\nExecution Time: {duration:.1f} seconds")
    
    successful = sum(results.values())
    total = len(results)
    
    print(f"\nTotal: {successful}/{total} models completed successfully")
    
    if all(results.values()):
        print("\n🎉 All ML models completed successfully!")
        print("\nOutputs saved to: ml_models/outputs/")
        print("  • customer_segmentation_analysis.png")
        print("  • customer_segmentation_elbow.png")
        print("  • customer_segments.csv")
        print("  • segment_analysis.csv")
        print("  • demand_forecasting_analysis.png")
        print("  • demand_forecast_results.png")
        print("  • demand_forecast.csv")
    else:
        print("\n⚠️  Some models failed. Please check the error messages above.")
    
    print("\n" + "=" * 100 + "\n")

if __name__ == "__main__":
    main()
