# Retail Data Lakehouse Architecture

This repository contains a **comprehensive Retail Data Lakehouse** implementation using **Apache Spark**, **Delta Lake**, and **Python** for retail analytics, machine learning, and business intelligence.

## 🎯 Project Overview

This project demonstrates a complete **Medallion Architecture** (Bronze-Silver-Gold) implementation for retail data processing, featuring:

- **Dataset Options**:
  - 🛒 Instacart Market Basket Analysis (3M+ orders, 200K+ users)
  - 🏪 Synthetic Retail Data (POS, CRM, Inventory, Marketing)
- **Goal**: Build scalable lakehouse for retail analytics, ML, and real-time insights

### 🏗️ Lakehouse Architecture (Medallion)

```
raw_data/          → Source CSV files (POS, CRM, Inventory, Marketing)
data/bronze/       → Delta Lake tables (raw ingestion with metadata)
data/silver/       → Cleaned, validated, joined datasets
data/gold/         → Business-ready aggregates and ML features
```

### ✨ Key Features

- ✅ **Multi-source ingestion** (CSV to Delta Lake with ACID transactions)
- ✅ **3-layer Medallion Architecture** (Bronze/Silver/Gold)
- ✅ **Data quality framework** (validation, deduplication, standardization)
- ✅ **Analytics-ready tables** (customer spending, sales trends, inventory metrics)
- ✅ **ML capabilities** (demand forecasting, customer segmentation)
- ✅ **Interactive dashboards** (Plotly, Power BI, Tableau support)
- ✅ **Databricks migration** (local → cloud deployment path)
- ✅ **GitHub Copilot integration** (AI-assisted development)

---

## Quick Start

### 1. Download the Dataset

Get the Instacart dataset from Kaggle:  
https://www.kaggle.com/c/instacart-market-basket-analysis/data

Place all CSV files in: `retail-lakehouse-project/data/raw/`

Required files:
- `orders.csv`
- `products.csv`
- `aisles.csv`
- `departments.csv`
- `order_products_train.csv`
- `order_products_prior.csv`

### 2. Set Up Environment

```powershell
# Run the helper script to create venv and install packages
cd retail-lakehouse-project
.\setup_venv.ps1

# Or manually:
python -m venv .venv
. .venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### 3. Run the Lakehouse Pipeline

```powershell
# Activate venv
. .venv\Scripts\Activate.ps1

# Bronze: Ingest raw CSV → Delta
python scripts/01_bronze_ingestion.py

# Silver: Transform and enrich
python scripts/02_silver_transformation.py

# Gold: Create business metrics
python scripts/03_gold_aggregation.py
```

### 4. Explore with Jupyter

```powershell
jupyter notebook notebooks/instacart_analysis.ipynb
```

---

## This repository contains code and notes for the Retail Lakehouse project.

## Prerequisites (Windows-focused)

This guide walks through installing the main prerequisites for Apache Spark development on Windows:

- Java Development Kit (JDK) — Java 8, 11, or 17 (recommended 17)
- Python 3.8+ (recommend 3.11+)
- Visual Studio Code (with Python extension)
- Apache Spark 3.5.1 prebuilt for Hadoop 3.3+

Follow the steps below. Commands are for PowerShell (Windows).

---

## 1) Install JDK (Java 8 / 11 / 17)

1. Download a JDK (AdoptOpenJDK / Temurin or Oracle). Temurin (Eclipse Adoptium) is recommended:
	- https://adoptium.net/ or https://jdk.java.net/

2. Run the installer and note the install path (for example: `C:\Program Files\Java\jdk-17.0.x`).

3. Verify install in a new PowerShell window:

```powershell
java -version
javac -version
```

4. Set `JAVA_HOME` permanently (replace the path with your JDK path):

```powershell
#$jdkPath should be the actual installation folder you observed
$jdkPath = 'C:\Program Files\Java\jdk-17.0.2'
[Environment]::SetEnvironmentVariable('JAVA_HOME', $jdkPath, 'User')
# Add java bin to the user PATH
$old = [Environment]::GetEnvironmentVariable('Path','User')
[Environment]::SetEnvironmentVariable('Path', "$old;$jdkPath\bin", 'User')
```

Note: After updating User environment variables you may need to restart PowerShell, VS Code, or log out/in.

---

## 2) Install Python 3.8+ (recommend 3.11+)

1. Download the installer from https://www.python.org/downloads/windows/
	- During installation check "Add Python to PATH" and choose "Disable path length limit".

2. Verify install in PowerShell:

```powershell
python --version
pip --version
```

3. (Recommended) Create a project virtual environment and activate it:

```powershell
cd \path\to\Retail_Lakehouse
python -m venv .venv
# In PowerShell
. .venv\Scripts\Activate.ps1
pip install --upgrade pip
```

---

## 3) Install Visual Studio Code

1. Download and install VS Code: https://code.visualstudio.com/
2. Open VS Code and install the Python extension (ms-python.python) from the Extensions view.
3. Recommended: set the workspace interpreter to the virtual environment `.venv` you created.

---

## 4) Install Apache Spark 3.5.1 (prebuilt for Hadoop 3.3+)

1. Download Spark 3.5.1 prebuilt for Hadoop 3.3+ from https://spark.apache.org/downloads.html
	- Choose: Spark 3.5.1, Pre-built for Apache Hadoop 3.3 and later

2. Extract the archive to a folder, e.g. `C:\spark\spark-3.5.1-bin-hadoop3.3`.

3. Set `SPARK_HOME` and add Spark `bin` to PATH (PowerShell — persistent User variables):

```powershell
$sparkHome = 'C:\spark\spark-3.5.1-bin-hadoop3.3'
[Environment]::SetEnvironmentVariable('SPARK_HOME', $sparkHome, 'User')
$old = [Environment]::GetEnvironmentVariable('Path','User')
[Environment]::SetEnvironmentVariable('Path', "$old;$sparkHome\bin", 'User')
```

4. Set `PYSPARK_PYTHON` so PySpark uses the correct Python interpreter (recommended):

```powershell
[Environment]::SetEnvironmentVariable('PYSPARK_PYTHON', (Get-Command python).Source, 'User')
```

Note: On Windows, some Hadoop-related operations may require `winutils.exe`. If you see errors mentioning permissions or Hadoop binaries, see the Troubleshooting section below.

---

## 5) Install PySpark in your Python environment

With your venv activated:

```powershell
pip install pyspark
# Optional: install other libs and freeze
pip freeze > requirements.txt
```

Installing `pyspark` via pip installs the Python bindings. Spark itself is still provided by the Spark binaries you extracted.

---

## 6) Verify Spark / PySpark works

1. Verify `spark-shell` (Scala REPL) version:

```powershell
spark-shell --version
```

2. Verify `pyspark` CLI (should open REPL):

```powershell
pyspark --version
# or just 'pyspark' to open interactive shell
```

3. Run a tiny PySpark script to verify end-to-end. Save this as `test_pyspark.py` in the repo root and run `python test_pyspark.py`:

```python
from pyspark.sql import SparkSession

spark = SparkSession.builder.master('local[*]').appName('health-check').getOrCreate()
df = spark.createDataFrame([(1,'a'),(2,'b')], ['id','val'])
df.show()
spark.stop()
```

You should see the DataFrame printed and no Java errors.

---

## Troubleshooting

- If `java` or `python` commands are not found, ensure you restarted the terminal after updating environment variables.
- If Spark fails with Windows/Hadoop errors, you may need a `winutils.exe` binary and set `HADOOP_HOME`. See: https://github.com/steveloughran/winutils
- If pyspark cannot find Python, set `PYSPARK_PYTHON` to the path of the Python executable you want to use.

---

## Next steps for this repo

- Create a `.venv` and install project dependencies (`pyspark`, data libs like `pandas` / `pyarrow` as needed).
- Add example notebooks or scripts under a `notebooks/` or `examples/` folder.
- Add CI checks or a quick test that runs the `test_pyspark.py` script.

If you want, I can:

- create a `.venv` and `requirements.txt` here,
- add the `test_pyspark.py` sample file to the repository,
- or produce a short PowerShell script that automates environment variable setup (you will still need to confirm paths).

---

## Step 2 — Set up VS Code Python environment (project folder)

Follow these steps to create a project directory, virtual environment, configure VS Code, and install the Python packages used by this project. Commands below are for PowerShell on Windows.

1) Create project directory and venv

```powershell
# from the repo root
mkdir retail-lakehouse-project
cd retail-lakehouse-project
python -m venv .venv
# Activate venv in PowerShell
. .venv\Scripts\Activate.ps1
```

2) Configure VS Code to use the virtual environment

```powershell
# Open VS Code in the project folder
code .
# In VS Code: Ctrl+Shift+P -> 'Python: Select Interpreter' -> choose the .venv interpreter
```

3) Install required Python packages

The repository includes a `requirements.txt` inside `retail-lakehouse-project/`. With the venv activated run:

```powershell
pip install --upgrade pip
pip install -r requirements.txt
```

Packages included (pinned where recommended):

- pyspark==3.5.1
- delta-spark==3.2.0
- pandas
- numpy
- matplotlib
- seaborn
- scikit-learn
- xgboost
- tensorflow
- plotly
- ipykernel
- jupyter

Notes:
- Some packages (TensorFlow, xgboost) may need specific wheels on Windows or GPU support; if installation fails, refer to the project's docs for platform-specific instructions.
- After installing `ipykernel`, you can register the venv as a Jupyter kernel:

```powershell
python -m ipykernel install --user --name retail-lakehouse-project --display-name "Retail Lakehouse (.venv)"
```

4) Verify: run the sample

```powershell
# With venv active
python ..\test_pyspark.py
```

If the sample runs and prints the DataFrame, your environment is ready.

---

## Step 3 — Configure GitHub Copilot in VS Code

GitHub Copilot accelerates data engineering development by suggesting code completions, functions, and entire workflows. Follow these steps to set it up and use it effectively.

### Install GitHub Copilot Extension

1. Open VS Code Extensions view: `Ctrl+Shift+X`
2. Search for "GitHub Copilot" and install it (extension ID: `GitHub.copilot`)
3. Sign in with your GitHub account (ensure you have Copilot access via subscription or trial)
4. Restart VS Code if prompted

The repository includes a `.vscode/extensions.json` file that recommends Copilot and the Python extension.

### Best Practices for Using Copilot with Data Engineering

**Break down complex tasks**  
Instead of asking Copilot to build entire pipelines, request specific components:
- ✅ "create a function to read CSV files into Spark DataFrame"
- ❌ "build a complete lakehouse ETL pipeline"

**Be specific**  
Provide context in comments about data schemas, expected outputs, and technologies:
```python
# Create a Spark session with Delta Lake configuration
# Include settings for: app name "RetailLakehouse", 
# Delta Lake extensions, and catalog configuration
```

**Use descriptive variable names**  
This helps Copilot understand your intent better:
- ✅ `retail_sales_df`, `customer_dim_table`
- ❌ `df1`, `temp`, `x`

**Iterate**  
Accept suggestions, test them, and refine with follow-up prompts. Use Copilot Chat to ask clarifying questions.

**Add inline comments**  
Describe what you want before writing code — Copilot will suggest implementations based on your comments.

### Example Prompting Patterns

See `retail-lakehouse-project/examples/copilot_prompting_examples.py` for sample comments that generate effective Spark/Delta Lake code.

Quick examples:

```python
# Read a CSV file from data/sales.csv into a Spark DataFrame with schema inference
# df = spark.read...

# Filter the DataFrame to include only records where quantity > 10 and status == 'COMPLETED'
# filtered_df = ...

# Write the DataFrame to Delta Lake format at path 'delta/retail_sales' with overwrite mode
# filtered_df.write...
```

---

## Phase 2: Data Lakehouse Platform Setup

## Step 4 — Choose and Set Up Lakehouse Platform

You can run this project locally (Steps 1-3 above) or migrate to a cloud lakehouse platform for production workloads.

### Option A: Databricks Community Edition (Recommended for Learning)

Databricks provides a **free tier** perfect for prototyping and learning lakehouse architecture without cloud costs.

#### Benefits of Databricks Community Edition

- ✅ **Managed environment** - No infrastructure setup required
- ✅ **Built-in Delta Lake** - Native support, no configuration needed
- ✅ **Collaborative notebooks** - Share and version notebooks easily
- ✅ **Databricks Assistant** - AI-powered code suggestions and explanations
- ✅ **Auto-scaling clusters** - Compute resources managed automatically
- ✅ **Free tier** - 15 GB storage, community support

#### Setup Instructions

1. **Sign up for Databricks Community Edition**
   - Visit: https://community.cloud.databricks.com/login
   - Click "Sign up" and create a free account
   - Verify your email address

2. **Log in and create a cluster**
   - After login, go to **Compute** → **Create Compute**
   - Choose **Community Edition** cluster settings (auto-configured)
   - Click **Create Compute** (cluster will start automatically)
   - Note: Clusters auto-sleep after 2 hours of inactivity; restart as needed

3. **Upload your Instacart dataset**
   - Go to **Data** → **Create Table**
   - Choose **Upload File** and select your CSV files
   - Upload to **DBFS (Databricks File System)**: `/FileStore/instacart/`
   - Recommended path structure:
     ```
     /FileStore/instacart/raw/orders.csv
     /FileStore/instacart/raw/products.csv
     /FileStore/instacart/raw/aisles.csv
     /FileStore/instacart/raw/departments.csv
     /FileStore/instacart/raw/order_products_train.csv
     /FileStore/instacart/raw/order_products_prior.csv
     ```

4. **Import project notebooks**
   - Go to **Workspace** → **Users** → your email
   - Click **⋮** (menu) → **Import**
   - Upload notebooks from `retail-lakehouse-project/databricks/` (see below)
   - Or create new notebooks and copy code from local scripts

5. **Run the lakehouse pipeline**
   - Open the imported notebooks in order:
     - `01_bronze_ingestion` (Databricks notebook)
     - `02_silver_transformation`
     - `03_gold_aggregation`
   - Run each cell with **Shift+Enter** or click **Run All**

#### Differences: Local vs. Databricks

| Feature | Local Setup | Databricks Community |
|---------|-------------|---------------------|
| **Spark session** | Manual creation | Auto-created as `spark` |
| **Delta Lake** | Installed via pip | Built-in, no install needed |
| **File paths** | Windows paths (`C:\`, `data/`) | DBFS paths (`/FileStore/`, `dbfs:/`) |
| **Compute** | Your machine | Cloud cluster (managed) |
| **Storage** | Local disk | DBFS (15 GB free) |
| **Collaboration** | Git-based | Built-in sharing |
| **Cost** | Free (your hardware) | Free tier (limited) |

#### Migrating Local Scripts to Databricks

The repository includes Databricks-compatible notebooks in `retail-lakehouse-project/databricks/`:

- `01_bronze_ingestion_databricks.ipynb`
- `02_silver_transformation_databricks.ipynb`
- `03_gold_aggregation_databricks.ipynb`
- `instacart_analysis_databricks.ipynb`

**Key changes for Databricks:**
- Paths: `data/raw/` → `/FileStore/instacart/raw/`
- No Spark session creation (use built-in `spark`)
- Delta tables: `data/bronze/orders` → `/FileStore/instacart/bronze/orders`
- Use `%sql` magic for SQL queries
- Databricks widgets for parameters

See `retail-lakehouse-project/databricks/MIGRATION_GUIDE.md` for detailed conversion steps.

### Option B: Local Development (Current Setup)

Continue using your local environment (Steps 1-3). Best for:
- Learning Spark/Delta Lake fundamentals
- Offline development
- Full control over compute resources
- Prototyping before cloud migration

### Option C: Other Cloud Platforms (Advanced)

- **AWS**: Amazon EMR + AWS Glue + S3
- **Azure**: Azure Synapse Analytics + Azure Data Lake Storage
- **GCP**: Dataproc + BigQuery + Cloud Storage

Each requires cloud account setup, billing, and infrastructure configuration.

---

## Step 5: Implement Medallion Architecture Storage Structure

The Medallion Architecture organizes data into **Bronze** (raw), **Silver** (cleaned), and **Gold** (aggregated) layers.

### Create Directory Structure

Run the storage setup script:

```powershell
# Navigate to project directory
cd retail-lakehouse-project

# Create medallion directory structure
python setup_storage.py
```

This creates:
```
data/
├── bronze/    # Raw data (POS, CRM, Inventory, Marketing)
├── silver/    # Cleaned and validated data
├── gold/      # Business aggregates and ML features
└── checkpoints/  # For streaming pipelines
raw_data/      # Source CSV files
```

---

## Step 6: Acquire and Generate Sample Retail Data

### Option A: Generate Synthetic Data (Recommended for Testing)

```powershell
# Generate sample POS, CRM, Inventory, and Marketing data
python generate_retail_data.py
```

This creates:
- `raw_data/pos_transactions.csv` (10,000 records)
- `raw_data/customers.csv` (5,000 records)
- `raw_data/products_inventory.csv` (1,000 records)
- `raw_data/marketing_campaigns.csv` (50 records)

### Option B: Use Instacart Dataset

1. Download from [Kaggle Instacart Competition](https://www.kaggle.com/c/instacart-market-basket-analysis/data)
2. Place files in `retail-lakehouse-project/data/raw/`
3. Use existing Instacart-specific scripts in `scripts/` folder

---

## Step 7: Execute ETL Pipelines - Bronze Layer (Data Ingestion)

The Bronze layer stores raw, unmodified data from source systems with metadata.

```powershell
# Ingest CSV files to Delta Lake Bronze layer
python scripts\etl_bronze_layer.py
```

**What it does**:
- Reads raw CSV files
- Adds metadata columns (`ingestion_timestamp`, `source_file`)
- Writes to Delta Lake format in `data/bronze/`
- Maintains full data lineage

---

## Step 8: Execute ETL Pipelines - Silver Layer (Data Transformation)

The Silver layer cleanses, validates, and joins data from Bronze.

```powershell
# Transform and clean Bronze data
python scripts\etl_silver_layer.py
```

**What it does**:
- Data quality validation (null checks, range validation)
- Deduplication by primary keys
- Value standardization (e.g., gender M/F → Male/Female)
- Creates joined datasets (transactions + customers)
- Writes clean data to `data/silver/`

---

## Step 9: Execute ETL Pipelines - Gold Layer (Business Aggregates)

The Gold layer contains business-ready aggregated datasets.

```powershell
# Create business aggregates
python scripts\etl_gold_layer.py
```

**What it does**:
- Creates `customer_spending` table (customer metrics)
- Creates `sales_summary` table (monthly sales trends)
- Creates `inventory_metrics` table (stock performance)
- Optimizes for analytics and ML use cases

---

## Step 10: Run Analytics Queries

Execute interactive analytics on Gold layer data.

```powershell
# Run predefined analytics queries
python scripts\analytics_queries.py
```

**Sample queries**:
- Top customers by spending
- Monthly sales trends by store
- Products needing reorder
- Category performance analysis
- Loyalty tier comparison

**Custom SQL queries**: The script registers Delta tables as SQL views for ad-hoc querying.

---

## Step 11-12: Machine Learning Models (Optional)

### Demand Forecasting

```powershell
python scripts\ml_demand_forecasting.py
```

- Uses Random Forest and XGBoost
- Predicts product demand for inventory optimization
- Features: store_id, product_id, day_of_week, month, price

### Customer Segmentation

```powershell
python scripts\ml_customer_segmentation.py
```

- K-Means clustering to identify customer segments
- Segments: High Value, Frequent Buyers, Low Engagement
- Saves segments to Gold layer for targeted marketing

---

## Step 13: Create Dashboards and Visualizations (Optional)

### Option A: Python Dashboards with Plotly

```powershell
python scripts\dashboard_visualization.py
```

Generates interactive HTML dashboards with:
- Sales trends line charts
- Customer segment pie charts
- Top customers bar charts

### Option B: Power BI / Tableau

1. Export Gold layer tables to CSV:
   ```python
   df = spark.read.format("delta").load("data/gold/customer_spending")
   df.toPandas().to_csv("customer_spending.csv", index=False)
   ```
2. Import CSV into Power BI or Tableau
3. Create visualizations and publish

---

## Step 14: Run Complete Pipeline (Automated)

Execute the entire lakehouse pipeline in one command:

```powershell
# PowerShell script (recommended)
.\run_complete_pipeline.ps1

# OR Python script
python run_all.py
```

**Pipeline stages**:
1. Storage structure setup
2. Sample data generation
3. Bronze layer ingestion
4. Silver layer transformation
5. Gold layer aggregation
6. Analytics queries execution

**Average runtime**: ~30-45 seconds (with sample data)

---

## Step 15: Testing and Validation (Optional)

Run automated tests to validate lakehouse implementation:

```powershell
# Run unit tests
python scripts\test_lakehouse.py

# Run performance benchmarks
python scripts\performance_test.py
```

**Tests include**:
- Data existence checks (Bronze/Silver/Gold layers)
- Data quality validation (null checks, valid ranges)
- Referential integrity (foreign key relationships)
- No duplicate records
- Performance benchmarking

---

## Step 16: Upload Project to GitHub

### Initialize Git Repository

```powershell
# Initialize git (if not already done)
git init

# Add remote repository
git remote add origin https://github.com/Pragna987/Retail_Lakehouse.git
```

### Stage and Commit Files

```powershell
# Stage all files
git add .

# Commit with message
git commit -m "Complete lakehouse implementation with Steps 5-16"
```

### Push to GitHub

```powershell
# Push to main branch
git branch -M main
git push -u origin main
```

### Verify on GitHub

1. Go to https://github.com/Pragna987/Retail_Lakehouse
2. Verify all files are uploaded
3. Check that README.md displays correctly

---

## 📊 Project Results Summary

See [PROJECT_REPORT.md](retail-lakehouse-project/PROJECT_REPORT.md) for comprehensive results including:
- Architecture diagrams
- Performance metrics
- Data quality results
- Machine learning outcomes
- Business value delivered

---

## 🎓 GitHub Copilot Usage Tips

Throughout this project, use GitHub Copilot effectively:

1. **Descriptive comments**: Write clear comments before code blocks
   ```python
   # Create a function to calculate customer lifetime value
   # based on total spending and transaction frequency
   ```

2. **Function signatures**: Start with function names and Copilot suggests implementation
   ```python
   def aggregate_sales_by_month(df):
       # Copilot will suggest groupBy and agg logic
   ```

3. **Ask Copilot Chat**: For explanations, debugging, or optimization
   - "Why is this PySpark query slow?"
   - "How to optimize Delta Lake table partitioning?"
   - "Explain this error: AnalysisException"

4. **Review suggestions**: Always validate Copilot's code for correctness

See `retail-lakehouse-project/examples/copilot_prompting_examples.py` for more examples.

---

## 📁 Complete Repository Structure

```
Retail_Lakehouse/
├── retail-lakehouse-project/
│   ├── data/                 # Lakehouse data (Bronze/Silver/Gold)
│   ├── raw_data/             # Source CSV files
│   ├── scripts/              # ETL and analytics scripts
│   │   ├── etl_bronze_layer.py
│   │   ├── etl_silver_layer.py
│   │   ├── etl_gold_layer.py
│   │   ├── analytics_queries.py
│   │   ├── ml_demand_forecasting.py (optional)
│   │   ├── ml_customer_segmentation.py (optional)
│   │   └── test_lakehouse.py (optional)
│   ├── databricks/           # Databricks migration notebooks
│   ├── notebooks/            # Jupyter analysis notebooks
│   ├── examples/             # GitHub Copilot examples
│   ├── .venv/                # Python virtual environment
│   ├── .vscode/              # VS Code settings
│   ├── setup_storage.py      # Storage structure setup
│   ├── generate_retail_data.py  # Sample data generator
│   ├── run_all.py            # Master pipeline executor
│   ├── run_complete_pipeline.ps1  # PowerShell runner
│   ├── requirements.txt      # Python dependencies
│   ├── GETTING_STARTED.md    # Quick start guide
│   ├── PROJECT_STRUCTURE.md  # Architecture docs
│   └── PROJECT_REPORT.md     # Results and metrics
├── README.md                 # This file
└── test_pyspark.py           # Environment health check
```

---

## 🚀 Next Steps After Implementation

1. **Optimize Performance**
   - Implement Z-ordering on frequently queried columns
   - Add table partitioning (by date, store_id, etc.)
   - Enable Delta Lake caching

2. **Add Real-Time Streaming**
   - Integrate Apache Kafka for real-time data ingestion
   - Use Structured Streaming for continuous processing
   - Update dashboards in real-time

3. **Deploy to Production**
   - Migrate to Databricks or AWS EMR
   - Set up CI/CD pipelines (GitHub Actions)
   - Implement data quality monitoring

4. **Advanced Analytics**
   - Build product recommendation engine
   - Implement customer churn prediction
   - Create price optimization models

---

## 📚 Additional Resources

- **Apache Spark**: https://spark.apache.org/docs/latest/
- **Delta Lake**: https://docs.delta.io/
- **PySpark Tutorial**: https://spark.apache.org/docs/latest/api/python/
- **Databricks Lakehouse**: https://www.databricks.com/product/data-lakehouse
- **GitHub Copilot Docs**: https://docs.github.com/en/copilot

---

## 📝 License

This project is for educational purposes. Data sources may have their own licenses.

---

Last updated: 2025-11-04