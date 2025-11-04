"""
Gold Layer ETL Pipeline
Creates business-ready aggregated datasets and metrics
Produces analytics-ready tables for reporting and ML
"""

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, sum as _sum, avg, count, month, year, max as _max, min as _min, when
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
    logger.info("Creating Spark session with Delta Lake configuration...")
    
    builder = SparkSession.builder \
        .appName("RetailLakehouse-Gold") \
        .config("spark.sql.extensions", 
                "io.delta.sql.DeltaSparkSessionExtension") \
        .config("spark.sql.catalog.spark_catalog", 
                "org.apache.spark.sql.delta.catalog.DeltaCatalog")
    
    spark = configure_spark_with_delta_pip(builder).getOrCreate()
    logger.info("✓ Spark session created successfully")
    return spark


def create_customer_spending(spark, source_path, target_path):
    """
    Aggregate customer spending metrics
    
    Args:
        spark: SparkSession object
        source_path: Path to customer_transactions Silver table
        target_path: Path to output Gold table
    
    Returns:
        Aggregated DataFrame
    """
    logger.info("Creating customer spending aggregates...")
    
    df = spark.read.format("delta").load(source_path)
    
    # Aggregate by customer
    customer_spending = df.groupBy("customer_id", "name", "loyalty_tier") \
        .agg(
            count("transaction_id").alias("total_transactions"),
            _sum("total_amount").alias("total_spent"),
            avg("total_amount").alias("avg_transaction_value"),
            _sum("quantity").alias("total_items_purchased")
        )
    
    # Round decimal values
    customer_spending = customer_spending \
        .withColumn("total_spent", col("total_spent").cast("decimal(10,2)")) \
        .withColumn("avg_transaction_value", col("avg_transaction_value").cast("decimal(10,2)"))
    
    record_count = customer_spending.count()
    logger.info(f"Created {record_count} customer spending records")
    
    customer_spending.write \
        .format("delta") \
        .mode("overwrite") \
        .save(target_path)
    
    logger.info(f"✓ Created customer_spending at {target_path}")
    return customer_spending


def create_sales_summary(spark, source_path, target_path):
    """
    Create daily/monthly sales summary
    
    Args:
        spark: SparkSession object
        source_path: Path to transactions Silver table
        target_path: Path to output Gold table
    
    Returns:
        Aggregated DataFrame
    """
    logger.info("Creating sales summary...")
    
    df = spark.read.format("delta").load(source_path)
    
    # Add date components
    df = df.withColumn("year", year(col("date"))) \
           .withColumn("month", month(col("date")))
    
    # Aggregate by store and time period
    sales_summary = df.groupBy("store_id", "year", "month") \
        .agg(
            count("transaction_id").alias("total_transactions"),
            _sum("total_amount").alias("total_revenue"),
            avg("total_amount").alias("avg_transaction_value"),
            _sum("quantity").alias("total_units_sold")
        ) \
        .orderBy("year", "month", "store_id")
    
    # Round decimal values
    sales_summary = sales_summary \
        .withColumn("total_revenue", col("total_revenue").cast("decimal(10,2)")) \
        .withColumn("avg_transaction_value", col("avg_transaction_value").cast("decimal(10,2)"))
    
    record_count = sales_summary.count()
    logger.info(f"Created {record_count} sales summary records")
    
    sales_summary.write \
        .format("delta") \
        .mode("overwrite") \
        .save(target_path)
    
    logger.info(f"✓ Created sales_summary at {target_path}")
    return sales_summary


def create_inventory_metrics(spark, product_path, transaction_path, target_path):
    """
    Create inventory performance metrics
    
    Args:
        spark: SparkSession object
        product_path: Path to products Silver table
        transaction_path: Path to transactions Silver table
        target_path: Path to output Gold table
    
    Returns:
        Inventory metrics DataFrame
    """
    logger.info("Creating inventory metrics...")
    
    products_df = spark.read.format("delta").load(product_path)
    transactions_df = spark.read.format("delta").load(transaction_path)
    
    # Calculate product sales velocity
    product_sales = transactions_df.groupBy("product_id") \
        .agg(
            _sum("quantity").alias("total_sold"),
            count("transaction_id").alias("num_transactions"),
            _sum("total_amount").alias("total_revenue")
        )
    
    # Join with inventory
    inventory_metrics = products_df.join(
        product_sales,
        on="product_id",
        how="left"
    ).fillna(0, subset=["total_sold", "num_transactions", "total_revenue"])
    
    # Add calculated fields
    inventory_metrics = inventory_metrics.withColumn(
        "stock_coverage_days",
        when(col("total_sold") > 0, 
             (col("stock_level") / (col("total_sold") / 365)).cast("decimal(10,2)"))
        .otherwise(999)
    )
    
    # Cast revenue to decimal
    inventory_metrics = inventory_metrics \
        .withColumn("total_revenue", col("total_revenue").cast("decimal(10,2)"))
    
    record_count = inventory_metrics.count()
    logger.info(f"Created {record_count} inventory metric records")
    
    inventory_metrics.write \
        .format("delta") \
        .mode("overwrite") \
        .save(target_path)
    
    logger.info(f"✓ Created inventory_metrics at {target_path}")
    return inventory_metrics


def main():
    """Main execution for Gold layer aggregation"""
    logger.info("=" * 60)
    logger.info("GOLD LAYER AGGREGATION - Starting ETL Pipeline")
    logger.info("=" * 60)
    
    spark = create_spark_session()
    
    try:
        # Create business-level aggregates
        logger.info("\nCreating Gold layer aggregates...")
        
        create_customer_spending(
            spark,
            "data/silver/customer_transactions",
            "data/gold/customer_spending"
        )
        
        create_sales_summary(
            spark,
            "data/silver/transactions",
            "data/gold/sales_summary"
        )
        
        create_inventory_metrics(
            spark,
            "data/silver/products",
            "data/silver/transactions",
            "data/gold/inventory_metrics"
        )
        
        logger.info("\n" + "=" * 60)
        logger.info("✅ Gold layer aggregation completed successfully!")
        logger.info("=" * 60)
        logger.info("\nGold layer tables created:")
        logger.info("  - data/gold/customer_spending (customer metrics)")
        logger.info("  - data/gold/sales_summary (sales trends)")
        logger.info("  - data/gold/inventory_metrics (inventory performance)")
        logger.info("\nThese tables are ready for:")
        logger.info("  • Business intelligence dashboards")
        logger.info("  • Machine learning model training")
        logger.info("  • Executive reporting")
        
    except Exception as e:
        logger.error(f"❌ Error during aggregation: {str(e)}")
        raise
    finally:
        spark.stop()
        logger.info("\nSpark session stopped")


if __name__ == "__main__":
    main()
