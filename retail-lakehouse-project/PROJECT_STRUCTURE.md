# Project Structure - Instacart Retail Lakehouse

```
retail-lakehouse-project/
│
├── .venv/                          # Python virtual environment
├── .vscode/                        
│   ├── settings.json               # VS Code Python interpreter config
│   └── extensions.json             # Recommended extensions (Copilot, Python)
│
├── data/                           # Data lakehouse layers
│   ├── README.md                   # Dataset documentation
│   ├── raw/                        # Place Instacart CSV files here
│   │   ├── orders.csv
│   │   ├── products.csv
│   │   ├── aisles.csv
│   │   ├── departments.csv
│   │   ├── order_products_train.csv
│   │   └── order_products_prior.csv
│   │
│   ├── bronze/                     # Raw Delta tables (ingested from CSV)
│   │   ├── orders/
│   │   ├── products/
│   │   ├── aisles/
│   │   ├── departments/
│   │   ├── order_products_train/
│   │   └── order_products_prior/
│   │
│   ├── silver/                     # Cleaned, enriched tables
│   │   ├── product_master/
│   │   ├── order_products_prior_enriched/
│   │   ├── order_products_train_enriched/
│   │   └── user_order_summary/
│   │
│   └── gold/                       # Business metrics & ML features
│       ├── product_metrics/
│       ├── department_metrics/
│       ├── user_purchase_features/
│       └── product_pairs_affinity/
│
├── scripts/                        # Data pipeline scripts
│   ├── 01_bronze_ingestion.py      # CSV → Delta (Bronze layer)
│   ├── 02_silver_transformation.py # Clean & join (Silver layer)
│   └── 03_gold_aggregation.py      # Business metrics (Gold layer)
│
├── notebooks/                      # Jupyter notebooks
│   └── instacart_analysis.ipynb    # EDA and visualization
│
├── examples/                       # Code examples
│   └── copilot_prompting_examples.py  # GitHub Copilot patterns
│
├── databricks/                     # Databricks-compatible notebooks
│   ├── README.md                   # Databricks setup guide
│   ├── MIGRATION_GUIDE.md          # Local → Databricks conversion
│   ├── 01_bronze_ingestion_databricks.ipynb
│   ├── 02_silver_transformation_databricks.ipynb
│   ├── 03_gold_aggregation_databricks.ipynb
│   └── instacart_analysis_databricks.ipynb
│
├── requirements.txt                # Python dependencies
├── setup_venv.ps1                  # Helper: create venv & install
└── README.md                       # Project documentation

```

## Workflow

### 1. Data Ingestion (Bronze Layer)
```powershell
python scripts/01_bronze_ingestion.py
```
- Reads CSV files from `data/raw/`
- Writes to Delta Lake in `data/bronze/`
- Adds ingestion timestamp and source tracking
- **No business logic** - raw data preservation

### 2. Data Transformation (Silver Layer)
```powershell
python scripts/02_silver_transformation.py
```
- Joins products with aisles and departments
- Creates enriched order-product tables
- Generates user summary statistics
- **Clean, validated, analytical tables**

### 3. Business Aggregation (Gold Layer)
```powershell
python scripts/03_gold_aggregation.py
```
- Product metrics (order frequency, reorder rates)
- Department performance
- Customer purchase features
- Product affinity (basket analysis)
- **Pre-aggregated for BI and ML**

### 4. Analysis & Visualization
```powershell
jupyter notebook notebooks/instacart_analysis.ipynb
```
- Interactive exploratory analysis
- Visualizations with matplotlib/seaborn
- Business insights and recommendations

## Key Delta Tables

### Bronze Layer (Raw)
- `orders` - All customer orders
- `products` - Product catalog
- `aisles` - Aisle metadata
- `departments` - Department metadata
- `order_products_prior` - Historical purchases
- `order_products_train` - Training set

### Silver Layer (Cleaned)
- `product_master` - Complete product catalog with hierarchy
- `order_products_*_enriched` - Orders joined with product info
- `user_order_summary` - User-level aggregates

### Gold Layer (Metrics)
- `product_metrics` - Order counts, reorder rates, cart position
- `department_metrics` - Department performance KPIs
- `user_purchase_features` - Customer segmentation features
- `product_pairs_affinity` - Frequently bought together analysis

## Technologies

- **Apache Spark 3.5.1** - Distributed data processing
- **Delta Lake 3.2.0** - ACID transactions, time travel
- **Python 3.11+** - Data engineering and ML
- **Jupyter** - Interactive analysis
- **Pandas, Matplotlib, Seaborn** - Visualization
- **scikit-learn, XGBoost, TensorFlow** - ML (optional)

## Next Steps

1. **ML Models**: Build reorder prediction, recommendation engine
2. **Time-Series**: Analyze shopping patterns by time
3. **Advanced Clustering**: Customer segmentation with K-means
4. **Real-time**: Stream processing with Structured Streaming
5. **BI Integration**: Connect Tableau/Power BI to Gold tables
