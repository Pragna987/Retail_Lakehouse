# Migration Guide: Local → Databricks Community Edition

This guide helps you migrate your local Instacart lakehouse project to Databricks Community Edition.

## Quick Migration Checklist

- [ ] Sign up for Databricks Community Edition
- [ ] Create a compute cluster
- [ ] Upload Instacart CSV files to DBFS
- [ ] Import Databricks notebooks
- [ ] Update file paths in notebooks
- [ ] Run the pipeline (Bronze → Silver → Gold)
- [ ] Explore results with analysis notebook

---

## 1. Sign Up and Setup

### Create Databricks Account

1. Go to https://community.cloud.databricks.com/login
2. Click **Sign up** (top right)
3. Enter email, create password
4. Verify email and log in

### Create a Cluster

1. In Databricks workspace, click **Compute** (left sidebar)
2. Click **Create Compute**
3. Community Edition settings are auto-configured:
   - Name: `Community Edition Cluster` (or custom name)
   - Runtime: Latest LTS (e.g., 13.3 LTS)
   - Node Type: Fixed (no choice in free tier)
   - Auto-termination: 120 minutes
4. Click **Create Compute**
5. Wait 2-5 minutes for cluster to start

**Note:** Clusters auto-sleep after 2 hours. Restart by clicking the cluster name → **Start**.

---

## 2. Upload Data to DBFS

### Option A: Upload via UI (Small Files)

1. Click **Data** (left sidebar)
2. Click **Create Table**
3. Click **Upload File**
4. Select your CSV file (e.g., `orders.csv`)
5. Upload to: `/FileStore/instacart/raw/`
6. Repeat for all 6 CSV files

**Recommended DBFS structure:**
```
/FileStore/instacart/
├── raw/
│   ├── orders.csv
│   ├── products.csv
│   ├── aisles.csv
│   ├── departments.csv
│   ├── order_products_train.csv
│   └── order_products_prior.csv
├── bronze/         (created by pipeline)
├── silver/         (created by pipeline)
└── gold/           (created by pipeline)
```

### Option B: Upload via Databricks CLI (Large Files)

For large files like `order_products_prior.csv` (2.5 GB):

```bash
# Install Databricks CLI
pip install databricks-cli

# Configure authentication
databricks configure --token

# Upload files
databricks fs cp order_products_prior.csv dbfs:/FileStore/instacart/raw/order_products_prior.csv
```

### Option C: Upload Sample Data

If you don't have the full dataset, generate sample data locally then upload:

```powershell
# Local: Generate sample data
python scripts\generate_sample_data.py

# Upload to Databricks via UI or CLI
```

---

## 3. Import Notebooks

### Via Databricks UI

1. Go to **Workspace** → **Users** → your email
2. Click **⋮** (menu) → **Import**
3. Choose **File** and upload `.ipynb` files from `retail-lakehouse-project/databricks/`:
   - `01_bronze_ingestion_databricks.ipynb`
   - `02_silver_transformation_databricks.ipynb`
   - `03_gold_aggregation_databricks.ipynb`
   - `instacart_analysis_databricks.ipynb`
4. Notebooks will appear in your workspace

### Via Databricks CLI

```bash
databricks workspace import databricks/01_bronze_ingestion_databricks.ipynb \
  /Users/your-email@domain.com/01_bronze_ingestion \
  --language PYTHON --format JUPYTER
```

---

## 4. Key Code Changes (Local → Databricks)

### A. Spark Session Creation

**Local (remove this):**
```python
from delta import configure_spark_with_delta_pip

builder = SparkSession.builder \
    .appName("InstacartBronzeIngestion") \
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
    .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")

spark = configure_spark_with_delta_pip(builder).getOrCreate()
```

**Databricks (use built-in):**
```python
# Spark session already available as 'spark'
# No need to create or configure

# Optional: Display Spark version
print(f"Spark version: {spark.version}")
```

### B. File Paths

**Local:**
```python
raw_path = "data/raw/orders.csv"
bronze_path = "data/bronze/orders"
silver_path = "data/silver/product_master"
gold_path = "data/gold/product_metrics"
```

**Databricks:**
```python
raw_path = "/FileStore/instacart/raw/orders.csv"
bronze_path = "/FileStore/instacart/bronze/orders"
silver_path = "/FileStore/instacart/silver/product_master"
gold_path = "/FileStore/instacart/gold/product_metrics"

# Or use dbfs:/ prefix
raw_path = "dbfs:/FileStore/instacart/raw/orders.csv"
```

### C. Delta Lake Operations

**No changes needed!** Delta Lake is built-in to Databricks.

```python
# Same code works in both environments
df.write.format("delta").mode("overwrite").save(bronze_path)
df = spark.read.format("delta").load(silver_path)
```

### D. Visualization (Databricks notebooks)

**Local (matplotlib):**
```python
import matplotlib.pyplot as plt
plt.bar(x, y)
plt.show()
```

**Databricks (built-in display):**
```python
# Option 1: Use display() for interactive charts
display(df)

# Option 2: Still use matplotlib
import matplotlib.pyplot as plt
plt.bar(x, y)
plt.show()  # Works in Databricks notebooks
```

### E. SQL Queries (Databricks-specific)

Databricks supports `%sql` magic commands:

```sql
%sql
CREATE OR REPLACE TEMP VIEW top_products AS
SELECT product_name, total_orders, reorder_rate
FROM delta.`/FileStore/instacart/gold/product_metrics`
ORDER BY total_orders DESC
LIMIT 10;

SELECT * FROM top_products;
```

---

## 5. Run the Pipeline

### Attach Notebook to Cluster

1. Open a notebook (e.g., `01_bronze_ingestion_databricks`)
2. At the top, ensure cluster is selected
3. If "Detached", click and select your cluster

### Execute Notebooks in Order

**Step 1: Bronze Ingestion**
- Open `01_bronze_ingestion_databricks`
- Click **Run All** or run cells individually with **Shift+Enter**
- Verify 6 Delta tables created in `/FileStore/instacart/bronze/`

**Step 2: Silver Transformation**
- Open `02_silver_transformation_databricks`
- Run all cells
- Verify 4 tables in `/FileStore/instacart/silver/`

**Step 3: Gold Aggregation**
- Open `03_gold_aggregation_databricks`
- Run all cells
- Verify 4 metric tables in `/FileStore/instacart/gold/`

**Step 4: Analysis**
- Open `instacart_analysis_databricks`
- Run all cells to see insights and visualizations

---

## 6. Databricks-Specific Features

### A. Display DataFrame with Built-in Viz

```python
# Instead of df.show()
display(df)

# Interactive table with:
# - Sorting
# - Filtering
# - Charts (bar, line, scatter, map)
```

### B. Widgets (Parameters)

Add interactive parameters to notebooks:

```python
dbutils.widgets.text("min_support", "100", "Minimum Support")
min_support = int(dbutils.widgets.get("min_support"))
```

### C. Databricks SQL

Create SQL queries on Delta tables:

```sql
%sql
SELECT department, SUM(total_orders) as total
FROM delta.`/FileStore/instacart/gold/department_metrics`
GROUP BY department
ORDER BY total DESC
```

### D. Databricks Assistant (AI)

1. Click **Databricks Assistant** icon (bottom right)
2. Ask questions like:
   - "Explain this code"
   - "How do I join two DataFrames in PySpark?"
   - "Fix this error: [paste error]"
3. Get AI-powered suggestions

### E. Version Control

Databricks has built-in Git integration:

1. Go to **Repos** (left sidebar)
2. Click **Add Repo**
3. Connect to GitHub: `Pragna987/Retail_Lakehouse`
4. Pull/push changes directly from Databricks

---

## 7. Path Reference Table

| Local Path | Databricks DBFS Path | Description |
|------------|----------------------|-------------|
| `data/raw/orders.csv` | `/FileStore/instacart/raw/orders.csv` | Raw CSV files |
| `data/bronze/orders` | `/FileStore/instacart/bronze/orders` | Bronze Delta table |
| `data/silver/product_master` | `/FileStore/instacart/silver/product_master` | Silver table |
| `data/gold/product_metrics` | `/FileStore/instacart/gold/product_metrics` | Gold metrics |
| `scripts/01_bronze_ingestion.py` | `01_bronze_ingestion_databricks` notebook | Bronze notebook |

---

## 8. Troubleshooting

### Issue: "Cluster is not running"

**Solution:** Go to **Compute** → select cluster → **Start**

### Issue: "File not found: /FileStore/instacart/raw/orders.csv"

**Solution:** Upload CSV files to DBFS via **Data** → **Create Table** → **Upload File**

### Issue: "No module named 'delta'"

**Solution:** Delta Lake is built-in to Databricks; no installation needed. Remove `from delta import configure_spark_with_delta_pip`.

### Issue: Notebook won't run

**Solution:** 
1. Check cluster is attached (top of notebook)
2. Ensure cluster is running (not terminated)
3. Check file paths are updated to DBFS paths

### Issue: "Out of memory" errors

**Solution:** Community Edition has limited memory. Use sample data or reduce data size:
```python
# Sample 10% of data
df = spark.read.csv(...).sample(fraction=0.1)
```

---

## 9. Best Practices for Databricks

### A. Organize Notebooks

Create folders in Workspace:
```
/Users/your-email/
├── instacart-lakehouse/
│   ├── 01_bronze_ingestion
│   ├── 02_silver_transformation
│   ├── 03_gold_aggregation
│   └── analysis/
│       └── instacart_analysis
```

### B. Use Databricks Repos

Connect to Git for version control:
- **Repos** → **Add Repo** → paste GitHub URL
- Pull latest changes
- Commit and push from Databricks UI

### C. Schedule Notebooks

Databricks supports workflow scheduling (not in Community Edition, but available in paid tiers):
- **Workflows** → **Create Job**
- Schedule Bronze → Silver → Gold pipeline

### D. Document with Markdown

Use `%md` magic for markdown cells:

```markdown
%md
# Bronze Layer Ingestion
This notebook ingests raw CSV files into Delta Lake format.
```

### E. Monitor Spark Jobs

- Click **Spark UI** link at top of notebook
- View DAG, stages, tasks, and execution times
- Debug slow operations

---

## 10. Next Steps in Databricks

Once your pipeline is running:

1. **Create Dashboards**: Use Databricks SQL to create visualizations
2. **Build ML Models**: Use MLflow for experiment tracking
3. **Automate Workflows**: Schedule notebooks (requires paid tier)
4. **Optimize Delta Tables**: Use `OPTIMIZE` and `ZORDER BY`
5. **Collaborate**: Share notebooks with teammates

---

## Additional Resources

- **Databricks Docs**: https://docs.databricks.com/
- **Delta Lake Guide**: https://docs.databricks.com/delta/
- **Community Forums**: https://community.databricks.com/
- **Databricks Academy**: Free training courses

---

**You're ready to migrate! Start with uploading data and importing the Bronze ingestion notebook.** 🚀
