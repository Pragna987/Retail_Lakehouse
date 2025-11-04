"""
Analytics Queries
Interactive analytics on Gold layer data
Provides reusable query functions and SQL capabilities
"""

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, desc
from delta import *
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def create_spark_session():
    """Create Spark session with Delta Lake support"""
    builder = SparkSession.builder \
        .appName("RetailLakehouse-Analytics") \
        .config("spark.sql.extensions", 
                "io.delta.sql.DeltaSparkSessionExtension") \
        .config("spark.sql.catalog.spark_catalog", 
                "org.apache.spark.sql.delta.catalog.DeltaCatalog")
    
    spark = configure_spark_with_delta_pip(builder).getOrCreate()
    return spark


def query_top_customers(spark, limit=10):
    """Query top customers by spending"""
    print(f"\n📊 Top {limit} Customers by Total Spending:")
    print("=" * 80)
    
    df = spark.read.format("delta").load("data/gold/customer_spending")
    
    top_customers = df.orderBy(col("total_spent").desc()).limit(limit)
    top_customers.show(truncate=False)
    
    return top_customers


def query_sales_trends(spark):
    """Query monthly sales trends"""
    print("\n📈 Monthly Sales Trends:")
    print("=" * 80)
    
    df = spark.read.format("delta").load("data/gold/sales_summary")
    
    df.orderBy("year", "month").show(20)
    
    return df


def query_inventory_alerts(spark):
    """Query products needing reorder"""
    print("\n⚠️  Products Needing Reorder:")
    print("=" * 80)
    
    df = spark.read.format("delta").load("data/silver/products")
    
    reorder_needed = df.filter(col("needs_reorder") == True)
    reorder_needed.select("product_id", "product_name", "category", 
                          "stock_level", "reorder_point").show()
    
    print(f"\nTotal products needing reorder: {reorder_needed.count()}")
    
    return reorder_needed


def query_category_performance(spark):
    """Query sales performance by product category"""
    print("\n🏆 Category Performance:")
    print("=" * 80)
    
    spark.read.format("delta").load("data/gold/inventory_metrics") \
        .createOrReplaceTempView("inventory_metrics")
    
    result = spark.sql("""
        SELECT 
            category,
            COUNT(*) as product_count,
            SUM(total_sold) as total_units_sold,
            ROUND(SUM(total_revenue), 2) as total_revenue,
            ROUND(AVG(total_revenue), 2) as avg_revenue_per_product
        FROM inventory_metrics
        GROUP BY category
        ORDER BY total_revenue DESC
    """)
    
    result.show(truncate=False)
    return result


def register_temp_views(spark):
    """Register Delta tables as SQL views for querying"""
    tables = {
        "customer_spending": "data/gold/customer_spending",
        "sales_summary": "data/gold/sales_summary",
        "inventory_metrics": "data/gold/inventory_metrics",
        "transactions": "data/silver/transactions",
        "customers": "data/silver/customers"
    }
    
    print("\n📋 Registering temp views for SQL queries...")
    for view_name, path in tables.items():
        spark.read.format("delta").load(path).createOrReplaceTempView(view_name)
        print(f"✓ Registered view: {view_name}")


def run_custom_sql_query(spark, query):
    """Execute custom SQL query on lakehouse data"""
    result = spark.sql(query)
    result.show()
    return result


def main():
    """Execute analytics queries"""
    logger.info("=" * 60)
    logger.info("ANALYTICS QUERIES - Running Interactive Analytics")
    logger.info("=" * 60)
    
    spark = create_spark_session()
    
    try:
        # Register all tables as views
        register_temp_views(spark)
        
        # Run analytics queries
        query_top_customers(spark)
        query_sales_trends(spark)
        query_inventory_alerts(spark)
        query_category_performance(spark)
        
        # Example custom SQL query
        print("\n📊 Average Transaction Value by Loyalty Tier:")
        print("=" * 80)
        query = """
        SELECT 
            loyalty_tier,
            ROUND(AVG(avg_transaction_value), 2) as avg_value,
            COUNT(*) as customer_count,
            ROUND(SUM(total_spent), 2) as total_revenue
        FROM customer_spending
        GROUP BY loyalty_tier
        ORDER BY avg_value DESC
        """
        run_custom_sql_query(spark, query)
        
        logger.info("\n✅ Analytics queries completed!")
        
    finally:
        spark.stop()


if __name__ == "__main__":
    main()
