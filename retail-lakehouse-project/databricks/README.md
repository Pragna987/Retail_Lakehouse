# Databricks Notebooks - Instacart Lakehouse

This folder contains Databricks-compatible notebooks for running the Instacart lakehouse pipeline in **Databricks Community Edition**.

## 📚 Notebooks

| Notebook | Description | Output |
|----------|-------------|--------|
| `01_bronze_ingestion_databricks.ipynb` | Ingest CSV → Delta Bronze | 6 Bronze tables |
| `02_silver_transformation_databricks.ipynb` | Clean & enrich → Silver | 4 Silver tables |
| `03_gold_aggregation_databricks.ipynb` | Business metrics → Gold | 4 Gold tables |
| `instacart_analysis_databricks.ipynb` | Interactive EDA & insights | Visualizations |

## 🚀 Quick Start

### 1. Setup Databricks

1. Sign up: https://community.cloud.databricks.com/login
2. Create a compute cluster (Community Edition)
3. Upload CSV files to `/FileStore/instacart/raw/`

### 2. Import Notebooks

**Option A: Via UI**
- Workspace → Import → Upload `.ipynb` files from this folder

**Option B: Via CLI**
```bash
databricks workspace import 01_bronze_ingestion_databricks.ipynb \
  /Users/your-email@domain.com/instacart/01_bronze_ingestion \
  --format JUPYTER
```

### 3. Run Pipeline

Run notebooks in order:
1. `01_bronze_ingestion_databricks` (CSV → Delta)
2. `02_silver_transformation_databricks` (Clean & enrich)
3. `03_gold_aggregation_databricks` (Business metrics)
4. `instacart_analysis_databricks` (Explore insights)

## 📂 Expected DBFS Structure

```
/FileStore/instacart/
├── raw/                          # Upload CSV files here
│   ├── orders.csv
│   ├── products.csv
│   ├── aisles.csv
│   ├── departments.csv
│   ├── order_products_train.csv
│   └── order_products_prior.csv
│
├── bronze/                       # Created by 01_bronze_ingestion
│   ├── orders/
│   ├── products/
│   ├── aisles/
│   ├── departments/
│   ├── order_products_train/
│   └── order_products_prior/
│
├── silver/                       # Created by 02_silver_transformation
│   ├── product_master/
│   ├── order_products_prior_enriched/
│   ├── order_products_train_enriched/
│   └── user_order_summary/
│
└── gold/                         # Created by 03_gold_aggregation
    ├── product_metrics/
    ├── department_metrics/
    ├── user_purchase_features/
    └── product_pairs_affinity/
```

## 🔄 Local vs Databricks Differences

| Aspect | Local | Databricks |
|--------|-------|------------|
| **Spark session** | Manual creation | Auto-created (`spark`) |
| **Delta Lake** | Install via pip | Built-in |
| **File paths** | `data/raw/` | `/FileStore/instacart/raw/` |
| **Visualization** | `plt.show()` | `display(df)` |
| **SQL** | Not supported | `%sql` magic |
| **Widgets** | N/A | `dbutils.widgets` |

## 📖 Key Features

### Databricks-Specific Enhancements

1. **Built-in Spark**: No need to create SparkSession
2. **Interactive visualizations**: Use `display(df)` for charts
3. **SQL support**: Run SQL queries with `%sql` magic
4. **Widgets**: Add parameters with `dbutils.widgets`
5. **Auto-scaling**: Clusters scale automatically
6. **Collaboration**: Share notebooks with team

### Example: SQL Query in Notebook

```sql
%sql
SELECT product_name, total_orders, reorder_rate
FROM delta.`/FileStore/instacart/gold/product_metrics`
ORDER BY total_orders DESC
LIMIT 10
```

### Example: Widget for Parameters

```python
dbutils.widgets.text("min_support", "100", "Minimum Support")
min_support = int(dbutils.widgets.get("min_support"))
```

## 🛠️ Migration from Local

See `MIGRATION_GUIDE.md` for detailed instructions on converting local scripts to Databricks notebooks.

**Main changes:**
- Remove Spark session creation
- Update file paths (`data/` → `/FileStore/instacart/`)
- Remove `configure_spark_with_delta_pip` (Delta is built-in)
- Use `display()` instead of `df.show()` for better viz

## 📊 Output Tables

### Bronze (6 tables)
Raw data with ingestion timestamps:
- `orders`, `products`, `aisles`, `departments`
- `order_products_train`, `order_products_prior`

### Silver (4 tables)
Cleaned, joined, enriched:
- `product_master` - Full product catalog
- `order_products_*_enriched` - Orders with product details
- `user_order_summary` - User aggregates

### Gold (4 tables)
Business-ready metrics:
- `product_metrics` - Product performance KPIs
- `department_metrics` - Category analytics
- `user_purchase_features` - Customer segmentation (ML-ready)
- `product_pairs_affinity` - Basket analysis

## 🎯 Next Steps After Running Pipeline

1. **Create Dashboards**
   - Databricks SQL → Create queries and visualizations
   - Share dashboards with stakeholders

2. **Build ML Models**
   - Use `user_purchase_features` for customer segmentation
   - Train reorder prediction models with MLflow

3. **Schedule Jobs** (Paid tier required)
   - Automate Bronze → Silver → Gold pipeline
   - Run on a schedule (daily, weekly)

4. **Connect BI Tools**
   - Tableau, Power BI can query Databricks Delta tables
   - Use Gold tables as data source

## 📚 Resources

- **Databricks Community**: https://community.databricks.com/
- **Delta Lake Docs**: https://docs.databricks.com/delta/
- **MLflow Guide**: https://docs.databricks.com/mlflow/
- **Databricks SQL**: https://docs.databricks.com/sql/

## ⚠️ Limitations (Community Edition)

- **Storage**: 15 GB limit
- **Compute**: Single node cluster (no distributed processing)
- **Auto-termination**: Clusters stop after 2 hours
- **Jobs/Scheduling**: Not available
- **Collaboration**: Limited sharing features

For production workloads, consider upgrading to Databricks Standard or Premium tier.

---

**Happy Databricks exploration! 🚀**
