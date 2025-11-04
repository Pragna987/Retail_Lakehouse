"""
Silver Layer Transformation - Instacart Dataset

This script reads Bronze Delta tables and creates cleaned, enriched Silver tables:
- Joins orders with products, aisles, and departments
- Data quality checks and cleaning
- Business-ready analytical tables

Silver layer philosophy:
- Clean, validated data
- Joined/enriched tables
- Business logic applied
- Ready for analytics
"""

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, count, sum as spark_sum, avg, max as spark_max, min as spark_min
from pyspark.sql.functions import current_timestamp, when, lit, concat_ws
from delta import configure_spark_with_delta_pip
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def create_spark_session():
    """Create Spark session with Delta Lake configuration"""
    builder = SparkSession.builder \
        .appName("InstacartSilverTransformation") \
        .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
        .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog") \
        .config("spark.driver.memory", "4g") \
        .config("spark.sql.shuffle.partitions", "8")
    
    spark = configure_spark_with_delta_pip(builder).getOrCreate()
    spark.sparkContext.setLogLevel("WARN")
    return spark


def create_product_master(spark):
    """
    Create enriched product master table by joining products, aisles, and departments
    Result: product catalog with full hierarchical information
    """
    logger.info("Creating product_master table...")
    
    # Read bronze tables
    products_df = spark.read.format("delta").load("data/bronze/products")
    aisles_df = spark.read.format("delta").load("data/bronze/aisles")
    departments_df = spark.read.format("delta").load("data/bronze/departments")
    
    # Join products with aisles and departments to create complete product catalog
    product_master = products_df \
        .join(aisles_df, "aisle_id", "left") \
        .join(departments_df, "department_id", "left") \
        .select(
            col("product_id"),
            col("product_name"),
            col("aisle_id"),
            col("aisle"),
            col("department_id"),
            col("department")
        ) \
        .withColumn("processing_timestamp", current_timestamp())
    
    # Write to Silver layer
    product_master.write \
        .format("delta") \
        .mode("overwrite") \
        .save("data/silver/product_master")
    
    count = product_master.count()
    logger.info(f"✓ Created product_master with {count:,} products")
    
    return product_master


def create_order_products_enriched(spark, order_type="prior"):
    """
    Create enriched order_products table with full product information
    
    Args:
        order_type: 'prior' or 'train'
    """
    table_name = f"order_products_{order_type}"
    logger.info(f"Creating {table_name}_enriched table...")
    
    # Read bronze tables
    order_products_df = spark.read.format("delta").load(f"data/bronze/{table_name}")
    orders_df = spark.read.format("delta").load("data/bronze/orders")
    product_master_df = spark.read.format("delta").load("data/silver/product_master")
    
    # Join order_products with orders and product information
    enriched_df = order_products_df \
        .join(orders_df, "order_id", "inner") \
        .join(product_master_df, "product_id", "inner") \
        .select(
            col("order_id"),
            col("user_id"),
            col("order_number"),
            col("order_dow"),
            col("order_hour_of_day"),
            col("days_since_prior_order"),
            col("product_id"),
            col("product_name"),
            col("aisle_id"),
            col("aisle"),
            col("department_id"),
            col("department"),
            col("add_to_cart_order"),
            col("reordered")
        ) \
        .withColumn("processing_timestamp", current_timestamp())
    
    # Write to Silver layer
    output_path = f"data/silver/{table_name}_enriched"
    enriched_df.write \
        .format("delta") \
        .mode("overwrite") \
        .partitionBy("department_id") \
        .save(output_path)
    
    count = enriched_df.count()
    logger.info(f"✓ Created {table_name}_enriched with {count:,} records")
    
    return enriched_df


def create_user_order_summary(spark):
    """
    Create user-level summary statistics from orders
    Aggregate: total orders, avg days between orders, preferred shopping times
    """
    logger.info("Creating user_order_summary table...")
    
    orders_df = spark.read.format("delta").load("data/bronze/orders")
    
    # Aggregate user statistics from orders
    user_summary = orders_df \
        .groupBy("user_id") \
        .agg(
            count("order_id").alias("total_orders"),
            spark_max("order_number").alias("max_order_number"),
            avg("order_dow").alias("avg_order_dow"),
            avg("order_hour_of_day").alias("avg_order_hour"),
            avg("days_since_prior_order").alias("avg_days_between_orders")
        ) \
        .withColumn("processing_timestamp", current_timestamp())
    
    # Write to Silver layer
    user_summary.write \
        .format("delta") \
        .mode("overwrite") \
        .save("data/silver/user_order_summary")
    
    count = user_summary.count()
    logger.info(f"✓ Created user_order_summary with {count:,} users")
    
    return user_summary


def main():
    """Main Silver layer transformation pipeline"""
    logger.info("=" * 80)
    logger.info("SILVER LAYER TRANSFORMATION - Instacart Dataset")
    logger.info("=" * 80)
    
    spark = create_spark_session()
    
    try:
        # Step 1: Create product master (dimension table)
        create_product_master(spark)
        
        # Step 2: Create enriched order_products tables (fact tables)
        create_order_products_enriched(spark, order_type="prior")
        create_order_products_enriched(spark, order_type="train")
        
        # Step 3: Create user summary (analytical table)
        create_user_order_summary(spark)
        
        logger.info("=" * 80)
        logger.info("✓ SILVER LAYER TRANSFORMATION COMPLETED SUCCESSFULLY")
        logger.info("=" * 80)
        
    except Exception as e:
        logger.error(f"✗ Silver transformation failed: {str(e)}")
        raise
    
    finally:
        spark.stop()


if __name__ == "__main__":
    main()
