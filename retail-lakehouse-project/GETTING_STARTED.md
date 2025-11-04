# Getting Started - Instacart Retail Lakehouse

Welcome! This guide walks you through setting up and running the Instacart Market Basket Analysis lakehouse project.

## Prerequisites Checklist

Before starting, ensure you have installed (see main README.md for details):

- ✅ **Java JDK 8/11/17** - `java -version`
- ✅ **Python 3.8+** - `python --version`
- ✅ **Apache Spark 3.5.1** - `spark-shell --version`
- ✅ **VS Code** with Python extension
- ✅ **Environment variables** set: `JAVA_HOME`, `SPARK_HOME`, `PYSPARK_PYTHON`

---

## Quick Start (5 Steps)

### Step 1: Set Up the Python Environment

```powershell
# Navigate to the project folder
cd retail-lakehouse-project

# Run the automated setup script (creates venv, installs packages)
.\setup_venv.ps1
```

**What this does:**
- Creates a `.venv` virtual environment
- Installs all required Python packages (PySpark, Delta Lake, pandas, etc.)
- Registers a Jupyter kernel for notebooks

### Step 2: Get the Data

**Option A: Use the Full Instacart Dataset**

1. Download from Kaggle: https://www.kaggle.com/c/instacart-market-basket-analysis/data
2. Extract all CSV files to `data/raw/`
3. Required files:
   - `orders.csv`
   - `products.csv`
   - `aisles.csv`
   - `departments.csv`
   - `order_products_train.csv`
   - `order_products_prior.csv`

**Option B: Generate Sample Data (for testing)**

```powershell
# Activate venv
. .venv\Scripts\Activate.ps1

# Generate small sample dataset
python scripts\generate_sample_data.py
```

This creates ~10,000 sample orders with 500 products - perfect for testing!

### Step 3: Run the Lakehouse Pipeline

**Option A: Run all layers at once (automated)**

```powershell
# Run the complete pipeline script
.\run_pipeline.ps1
```

**Option B: Run each layer manually**

```powershell
# Activate venv first
. .venv\Scripts\Activate.ps1

# Bronze: Ingest CSV → Delta Lake
python scripts\01_bronze_ingestion.py

# Silver: Clean and enrich
python scripts\02_silver_transformation.py

# Gold: Create business metrics
python scripts\03_gold_aggregation.py
```

**Expected output:**
- Bronze tables in `data/bronze/` (6 tables)
- Silver tables in `data/silver/` (4 tables)
- Gold tables in `data/gold/` (4 metric tables)

### Step 4: Explore with Jupyter

```powershell
# Start Jupyter
jupyter notebook

# Open: notebooks/instacart_analysis.ipynb
```

The notebook includes:
- Top products analysis
- Reorder rate insights
- Department performance
- Basket analysis (frequently bought together)
- Customer segmentation

### Step 5: Customize and Extend

Now you can:
- Modify the scripts for your own analysis
- Add new Gold layer metrics
- Build ML models (reorder prediction, recommendations)
- Connect BI tools to Gold tables

---

## Troubleshooting

### Issue: `java: command not found`

**Solution:** Install JDK and set `JAVA_HOME`. See main README Step 1.

```powershell
# Check Java is installed
java -version

# If not found, download from https://adoptium.net/
```

### Issue: `ModuleNotFoundError: No module named 'pyspark'`

**Solution:** Activate venv and install requirements

```powershell
. .venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### Issue: `FileNotFoundError: data/raw/orders.csv`

**Solution:** Download the dataset or generate sample data

```powershell
python scripts\generate_sample_data.py
```

### Issue: Spark errors about `winutils.exe` on Windows

**Solution:** This is common on Windows. For local development, you can often ignore it. If needed:
- Download winutils.exe from https://github.com/steveloughran/winutils
- Set `HADOOP_HOME` environment variable

### Issue: Pipeline runs slowly

**Tips to speed up:**
- Start with sample data (`generate_sample_data.py`)
- Increase Spark memory: Edit scripts and change `.config("spark.driver.memory", "8g")`
- Use fewer shuffle partitions for small data

---

## Project Structure Overview

```
retail-lakehouse-project/
├── data/
│   ├── raw/          ← Place CSV files here
│   ├── bronze/       ← Delta tables (raw)
│   ├── silver/       ← Clean tables
│   └── gold/         ← Business metrics
├── scripts/
│   ├── 01_bronze_ingestion.py
│   ├── 02_silver_transformation.py
│   ├── 03_gold_aggregation.py
│   └── generate_sample_data.py
├── notebooks/
│   └── instacart_analysis.ipynb
├── examples/
│   └── copilot_prompting_examples.py
├── setup_venv.ps1
└── run_pipeline.ps1
```

---

## What's Next?

### Learn the Data

- Read `data/README.md` for dataset schema
- Read `PROJECT_STRUCTURE.md` for architecture details
- Explore `notebooks/instacart_analysis.ipynb` for insights

### Build Something Cool

**Ideas:**
1. **Recommendation Engine**: Use product pairs affinity to recommend items
2. **Reorder Prediction**: Build an ML model to predict if a product will be reordered
3. **Customer Segmentation**: K-means clustering on user purchase features
4. **Time-Series Analysis**: Analyze shopping patterns by day/hour
5. **Dashboard**: Connect Power BI/Tableau to Gold tables

### Use GitHub Copilot

Open `examples/copilot_prompting_examples.py` to see effective prompting patterns for data engineering with Copilot.

**Example prompt:**
```python
# Read Delta table from 'data/gold/product_metrics'
# Filter to products with reorder_rate > 0.5
# Select product_name, total_orders, reorder_rate
# Show top 10
```

Copilot will suggest the PySpark code!

---

## Getting Help

- **Dataset docs**: `data/README.md`
- **Architecture**: `PROJECT_STRUCTURE.md`
- **Main setup**: `../README.md` (parent folder)
- **Instacart dataset info**: https://www.kaggle.com/c/instacart-market-basket-analysis

---

## Sample Commands Reference

```powershell
# Activate venv
. .venv\Scripts\Activate.ps1

# Generate sample data
python scripts\generate_sample_data.py

# Run Bronze
python scripts\01_bronze_ingestion.py

# Run Silver
python scripts\02_silver_transformation.py

# Run Gold
python scripts\03_gold_aggregation.py

# Run full pipeline
.\run_pipeline.ps1

# Start Jupyter
jupyter notebook

# Deactivate venv
deactivate
```

---

**Happy Data Engineering! 🚀**
