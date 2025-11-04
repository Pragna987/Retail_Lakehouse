# Instacart Dataset - Data Folders

This folder contains the Instacart Market Basket Analysis dataset organized in a **Medallion Architecture** (Bronze, Silver, Gold layers).

## Expected Raw Data Files

Place your Instacart CSV files in the `data/raw/` folder. The typical Instacart dataset includes:

### Core Files (place these in `data/raw/`)

1. **orders.csv** - Order information
   - `order_id`, `user_id`, `eval_set`, `order_number`, `order_dow`, `order_hour_of_day`, `days_since_prior_order`

2. **products.csv** - Product catalog
   - `product_id`, `product_name`, `aisle_id`, `department_id`

3. **aisles.csv** - Aisle information
   - `aisle_id`, `aisle`

4. **departments.csv** - Department information
   - `department_id`, `department`

5. **order_products_train.csv** - Training set order-product relationships
   - `order_id`, `product_id`, `add_to_cart_order`, `reordered`

6. **order_products_prior.csv** - Prior orders (largest file)
   - `order_id`, `product_id`, `add_to_cart_order`, `reordered`

## Lakehouse Layers

### Bronze Layer (`data/bronze/`)
Raw data from CSV files written to Delta Lake format with minimal transformation:
- Schema enforcement
- Data type casting
- Timestamp added for ingestion tracking
- **No business logic applied**

### Silver Layer (`data/silver/`)
Cleaned and enriched data:
- Joined tables (orders + products + aisles + departments)
- Data quality checks applied
- Deduplicated records
- **Business-ready analytical tables**

### Gold Layer (`data/gold/`)
Aggregated business metrics and KPIs:
- Basket analysis (frequently bought together)
- Product affinity matrices
- Customer segmentation
- Reorder prediction features
- **Optimized for BI and ML**

## How to Use

1. **Download the Instacart dataset** from Kaggle:
   https://www.kaggle.com/c/instacart-market-basket-analysis/data

2. **Place all CSV files** in `data/raw/`

3. **Run ingestion scripts** (in order):
   ```powershell
   # Activate venv first
   . .venv\Scripts\Activate.ps1
   
   # Bronze layer ingestion
   python scripts/01_bronze_ingestion.py
   
   # Silver layer transformation
   python scripts/02_silver_transformation.py
   
   # Gold layer aggregation
   python scripts/03_gold_aggregation.py
   ```

4. **Explore with Jupyter**:
   ```powershell
   jupyter notebook notebooks/instacart_analysis.ipynb
   ```

## File Size Notes

- `order_products_prior.csv` is the largest file (~2.5 GB uncompressed, ~400 MB compressed)
- Total dataset size: ~3.5 GB uncompressed
- Delta Lake will compress and optimize storage automatically

## Dataset Source

**Instacart Market Basket Analysis**  
Kaggle Competition: https://www.kaggle.com/c/instacart-market-basket-analysis

This dataset contains 3+ million grocery orders from 200,000+ Instacart users with product reorder information.
