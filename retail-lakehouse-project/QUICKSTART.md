# Quick Start Guide - Running the Complete Pipeline

This guide walks you through executing the complete retail lakehouse pipeline in under 5 minutes.

---

## Prerequisites Check

Before running the pipeline, ensure:

- ✅ JDK 8/11/17 installed and `JAVA_HOME` set
- ✅ Apache Spark 3.5.1 installed and `SPARK_HOME` set
- ✅ Python 3.11+ installed
- ✅ Virtual environment created (`.venv`)
- ✅ Dependencies installed (`pip install -r requirements.txt`)

**Quick verification**:

```powershell
java -version
python --version
spark-shell --version  # Ctrl+C to exit
```

If any fail, see main [README.md](../README.md) Steps 1-3.

---

## Option 1: Automated Pipeline (Recommended)

### PowerShell Script (Windows)

```powershell
# Activate virtual environment and run pipeline
.\run_complete_pipeline.ps1
```

### Python Script (Cross-platform)

```powershell
# Activate virtual environment first
.\.venv\Scripts\Activate.ps1  # Windows
# source .venv/bin/activate    # macOS/Linux

# Run pipeline
python run_all.py
```

**Pipeline stages** (automatic execution):
1. ✅ Storage structure setup (~1 second)
2. ✅ Sample data generation (~3 seconds)
3. ✅ Bronze layer ingestion (~10 seconds)
4. ✅ Silver layer transformation (~12 seconds)
5. ✅ Gold layer aggregation (~8 seconds)
6. ✅ Analytics queries (~5 seconds)

**Total runtime**: ~40-50 seconds

---

## Option 2: Step-by-Step Manual Execution

Run each stage individually for learning or debugging:

### Step 1: Setup Storage Structure

```powershell
python setup_storage.py
```

**Output**: Creates `data/bronze/`, `data/silver/`, `data/gold/`, `raw_data/` directories.

---

### Step 2: Generate Sample Data

```powershell
python generate_retail_data.py
```

**Output**: Creates 4 CSV files in `raw_data/`:
- `pos_transactions.csv` (10,000 records)
- `customers.csv` (5,000 records)
- `products_inventory.csv` (1,000 records)
- `marketing_campaigns.csv` (50 records)

---

### Step 3: Bronze Layer Ingestion

```powershell
python scripts\etl_bronze_layer.py
```

**Output**: Delta Lake tables in `data/bronze/`:
- `pos/` - Raw transactions with metadata
- `crm/` - Raw customer data
- `inventory/` - Raw product data
- `marketing/` - Raw campaign data

**Verification**:
```powershell
ls data\bronze\pos
# Should show _delta_log/ directory and parquet files
```

---

### Step 4: Silver Layer Transformation

```powershell
python scripts\etl_silver_layer.py
```

**Output**: Cleaned Delta tables in `data/silver/`:
- `transactions/` - Validated POS data
- `customers/` - Standardized customer profiles
- `products/` - Enriched product catalog
- `customer_transactions/` - Joined dataset

**Data quality improvements**:
- Removed invalid records (negative prices, null IDs)
- Deduplicated by primary keys
- Standardized gender values (M/F → Male/Female)

---

### Step 5: Gold Layer Aggregation

```powershell
python scripts\etl_gold_layer.py
```

**Output**: Business aggregates in `data/gold/`:
- `customer_spending/` - Customer lifetime value metrics
- `sales_summary/` - Monthly sales trends by store
- `inventory_metrics/` - Product performance metrics

---

### Step 6: Analytics Queries

```powershell
python scripts\analytics_queries.py
```

**Output**: Printed reports showing:
- 📊 Top 10 customers by spending
- 📈 Monthly sales trends
- ⚠️ Products needing reorder
- 🏆 Category performance analysis
- 💎 Loyalty tier comparison

---

## Viewing Results

### Delta Lake Tables

Use PySpark shell to explore:

```python
from pyspark.sql import SparkSession
from delta import *

builder = SparkSession.builder.appName("Explore")
spark = configure_spark_with_delta_pip(builder).getOrCreate()

# Read any table
df = spark.read.format("delta").load("data/gold/customer_spending")
df.show()
df.printSchema()

# SQL queries
df.createOrReplaceTempView("spending")
spark.sql("SELECT * FROM spending WHERE total_spent > 1000").show()
```

### Export to CSV

```python
# Export Gold layer for Power BI/Tableau
df = spark.read.format("delta").load("data/gold/sales_summary")
df.toPandas().to_csv("sales_summary.csv", index=False)
```

---

## Troubleshooting

### Issue: "java: command not found"

**Solution**: Set `JAVA_HOME` and restart terminal

```powershell
# Run environment setup script
python setup_env.ps1
# Restart terminal
```

### Issue: "ModuleNotFoundError: No module named 'pyspark'"

**Solution**: Activate virtual environment and install dependencies

```powershell
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### Issue: "Py4JJavaError: java.lang.OutOfMemoryError"

**Solution**: Increase Spark driver memory

```python
# Add to Spark config in scripts
.config("spark.driver.memory", "4g")
```

### Issue: "Path does not exist: data/bronze/pos"

**Solution**: Run Bronze layer ingestion first

```powershell
python scripts\etl_bronze_layer.py
```

### Issue: "Permission denied" on PowerShell script

**Solution**: Change execution policy

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

---

## Next Steps After Successful Run

1. **Explore the data**:
   - Use `analytics_queries.py` to run custom SQL
   - Open Jupyter notebooks for interactive analysis

2. **Run ML models** (optional):
   ```powershell
   python scripts\ml_demand_forecasting.py
   python scripts\ml_customer_segmentation.py
   ```

3. **Create dashboards** (optional):
   ```powershell
   python scripts\dashboard_visualization.py
   ```

4. **Run tests**:
   ```powershell
   python scripts\test_lakehouse.py
   ```

5. **Migrate to Databricks**:
   - See `databricks/MIGRATION_GUIDE.md`
   - Upload data to DBFS
   - Run Databricks notebooks

---

## Performance Benchmarks

Expected execution times (on typical laptop):

| Stage | Sample Data (16K records) | Instacart Data (3M+ records) |
|-------|---------------------------|-------------------------------|
| Bronze Ingestion | ~10 seconds | ~2-5 minutes |
| Silver Transformation | ~12 seconds | ~5-10 minutes |
| Gold Aggregation | ~8 seconds | ~3-7 minutes |
| **Total Pipeline** | **~40 seconds** | **~15-25 minutes** |

*Benchmarks: Intel i5, 8GB RAM, SSD*

---

## Need Help?

- **Documentation**: See main [README.md](../README.md)
- **Architecture**: See [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md)
- **Results**: See [PROJECT_REPORT.md](PROJECT_REPORT.md)
- **Databricks**: See [databricks/MIGRATION_GUIDE.md](databricks/MIGRATION_GUIDE.md)
- **GitHub Copilot**: See [examples/copilot_prompting_examples.py](examples/copilot_prompting_examples.py)

---

**Ready to run? Execute**: `.\run_complete_pipeline.ps1` or `python run_all.py`
