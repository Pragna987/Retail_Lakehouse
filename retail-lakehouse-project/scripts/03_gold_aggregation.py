"""
Gold Layer Aggregation - Instacart Dataset

This script creates business-ready aggregate tables for analytics and ML:
- Product reorder statistics
- Department performance metrics
- Basket analysis (product affinity)
- Customer segmentation features

Gold layer philosophy:
- Pre-aggregated metrics
- Optimized for BI tools
- ML feature tables
- Business KPIs
"""

from pyspark.sql import SparkSession, Window
from pyspark.sql.functions import col, count, sum as spark_sum, avg, countDistinct
from pyspark.sql.functions import current_timestamp, dense_rank, round as spark_round
from delta import configure_spark_with_delta_pip
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def create_spark_session():
    """Create Spark session with Delta Lake configuration"""
    builder = SparkSession.builder \
        .appName("InstacartGoldAggregation") \
        .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
        .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog") \
        .config("spark.driver.memory", "4g") \
        .config("spark.sql.shuffle.partitions", "8")
    
    spark = configure_spark_with_delta_pip(builder).getOrCreate()
    spark.sparkContext.setLogLevel("WARN")
    return spark


def create_product_metrics(spark):
    """
    Aggregate product-level metrics: order frequency, reorder rate, avg cart position
    Useful for: product recommendations, inventory optimization
    """
    logger.info("Creating product_metrics table...")
    
    # Read silver enriched data
    order_products_df = spark.read.format("delta").load("data/silver/order_products_prior_enriched")
    
    # Calculate product-level metrics
    product_metrics = order_products_df \
        .groupBy("product_id", "product_name", "aisle", "department") \
        .agg(
            count("order_id").alias("total_orders"),
            countDistinct("user_id").alias("unique_customers"),
            spark_sum("reordered").alias("reorder_count"),
            avg("reordered").alias("reorder_rate"),
            avg("add_to_cart_order").alias("avg_cart_position")
        ) \
        .withColumn("reorder_rate", spark_round(col("reorder_rate"), 4)) \
        .withColumn("avg_cart_position", spark_round(col("avg_cart_position"), 2)) \
        .orderBy(col("total_orders").desc()) \
        .withColumn("processing_timestamp", current_timestamp())
    
    # Write to Gold layer
    product_metrics.write \
        .format("delta") \
        .mode("overwrite") \
        .save("data/gold/product_metrics")
    
    count = product_metrics.count()
    logger.info(f"✓ Created product_metrics with {count:,} products")
    
    # Show top 10 most ordered products
    logger.info("\nTop 10 Most Ordered Products:")
    product_metrics.select("product_name", "total_orders", "reorder_rate").show(10, truncate=False)
    
    return product_metrics


def create_department_metrics(spark):
    """
    Aggregate department-level performance metrics
    Useful for: category management, business reporting
    """
    logger.info("Creating department_metrics table...")
    
    order_products_df = spark.read.format("delta").load("data/silver/order_products_prior_enriched")
    
    # Calculate department-level metrics
    department_metrics = order_products_df \
        .groupBy("department_id", "department") \
        .agg(
            count("order_id").alias("total_orders"),
            countDistinct("product_id").alias("unique_products"),
            countDistinct("user_id").alias("unique_customers"),
            spark_sum("reordered").alias("reorder_count"),
            avg("reordered").alias("avg_reorder_rate")
        ) \
        .withColumn("avg_reorder_rate", spark_round(col("avg_reorder_rate"), 4)) \
        .orderBy(col("total_orders").desc()) \
        .withColumn("processing_timestamp", current_timestamp())
    
    # Write to Gold layer
    department_metrics.write \
        .format("delta") \
        .mode("overwrite") \
        .save("data/gold/department_metrics")
    
    count = department_metrics.count()
    logger.info(f"✓ Created department_metrics with {count:,} departments")
    
    logger.info("\nDepartment Performance:")
    department_metrics.select("department", "total_orders", "unique_products", "avg_reorder_rate").show(truncate=False)
    
    return department_metrics


def create_user_purchase_features(spark):
    """
    Create user-level purchase features for ML and segmentation
    Features: basket size, favorite departments, reorder propensity
    """
    logger.info("Creating user_purchase_features table...")
    
    order_products_df = spark.read.format("delta").load("data/silver/order_products_prior_enriched")
    user_summary_df = spark.read.format("delta").load("data/silver/user_order_summary")
    
    # Calculate user purchase behavior features
    user_features = order_products_df \
        .groupBy("user_id") \
        .agg(
            countDistinct("order_id").alias("total_orders"),
            countDistinct("product_id").alias("unique_products_purchased"),
            count("product_id").alias("total_items_purchased"),
            avg("reordered").alias("reorder_propensity"),
            countDistinct("department").alias("departments_shopped")
        ) \
        .join(user_summary_df, "user_id", "left") \
        .withColumn("avg_basket_size", 
                    spark_round(col("total_items_purchased") / col("total_orders"), 2)) \
        .withColumn("reorder_propensity", spark_round(col("reorder_propensity"), 4)) \
        .select(
            "user_id",
            "total_orders",
            "unique_products_purchased",
            "total_items_purchased",
            "avg_basket_size",
            "reorder_propensity",
            "departments_shopped",
            "avg_order_dow",
            "avg_order_hour",
            "avg_days_between_orders"
        ) \
        .withColumn("processing_timestamp", current_timestamp())
    
    # Write to Gold layer
    user_features.write \
        .format("delta") \
        .mode("overwrite") \
        .save("data/gold/user_purchase_features")
    
    count = user_features.count()
    logger.info(f"✓ Created user_purchase_features with {count:,} users")
    
    # Show sample user features
    logger.info("\nSample User Features:")
    user_features.show(5)
    
    return user_features


def create_product_pairs_affinity(spark, min_support=100):
    """
    Create product-pair affinity matrix for basket analysis
    Shows which products are frequently bought together
    
    Args:
        min_support: Minimum number of times products must appear together
    """
    logger.info(f"Creating product_pairs_affinity table (min_support={min_support})...")
    
    order_products_df = spark.read.format("delta").load("data/silver/order_products_prior_enriched")
    
    # Self-join to find product pairs in same order
    product_pairs = order_products_df.alias("a") \
        .join(
            order_products_df.alias("b"),
            (col("a.order_id") == col("b.order_id")) & (col("a.product_id") < col("b.product_id")),
            "inner"
        ) \
        .select(
            col("a.product_id").alias("product_a_id"),
            col("a.product_name").alias("product_a_name"),
            col("b.product_id").alias("product_b_id"),
            col("b.product_name").alias("product_b_name")
        ) \
        .groupBy("product_a_id", "product_a_name", "product_b_id", "product_b_name") \
        .agg(count("*").alias("pair_count")) \
        .filter(col("pair_count") >= min_support) \
        .orderBy(col("pair_count").desc()) \
        .withColumn("processing_timestamp", current_timestamp())
    
    # Write to Gold layer
    product_pairs.write \
        .format("delta") \
        .mode("overwrite") \
        .save("data/gold/product_pairs_affinity")
    
    count = product_pairs.count()
    logger.info(f"✓ Created product_pairs_affinity with {count:,} product pairs")
    
    # Show top product pairs
    logger.info("\nTop 10 Product Pairs (Frequently Bought Together):")
    product_pairs.select("product_a_name", "product_b_name", "pair_count").show(10, truncate=False)
    
    return product_pairs


def main():
    """Main Gold layer aggregation pipeline"""
    logger.info("=" * 80)
    logger.info("GOLD LAYER AGGREGATION - Instacart Dataset")
    logger.info("=" * 80)
    
    spark = create_spark_session()
    
    try:
        # Create business metrics tables
        create_product_metrics(spark)
        create_department_metrics(spark)
        create_user_purchase_features(spark)
        create_product_pairs_affinity(spark, min_support=100)
        
        logger.info("=" * 80)
        logger.info("✓ GOLD LAYER AGGREGATION COMPLETED SUCCESSFULLY")
        logger.info("=" * 80)
        logger.info("\nGold tables created:")
        logger.info("  - data/gold/product_metrics")
        logger.info("  - data/gold/department_metrics")
        logger.info("  - data/gold/user_purchase_features")
        logger.info("  - data/gold/product_pairs_affinity")
        
    except Exception as e:
        logger.error(f"✗ Gold aggregation failed: {str(e)}")
        raise
    
    finally:
        spark.stop()


if __name__ == "__main__":
    main()
