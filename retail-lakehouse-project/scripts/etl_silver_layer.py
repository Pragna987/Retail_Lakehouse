"""
Silver Layer ETL Pipeline
Cleanses, validates, and joins data from Bronze layer
Creates enriched datasets for analytics
"""

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, when, isnan, count, sum as _sum
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
        .appName("RetailLakehouse-Silver") \
        .config("spark.sql.extensions", 
                "io.delta.sql.DeltaSparkSessionExtension") \
        .config("spark.sql.catalog.spark_catalog", 
                "org.apache.spark.sql.delta.catalog.DeltaCatalog")
    
    spark = configure_spark_with_delta_pip(builder).getOrCreate()
    logger.info("✓ Spark session created successfully")
    return spark


def clean_pos_data(spark, bronze_path, silver_path):
    """
    Clean and validate POS transaction data
    
    Args:
        spark: SparkSession object
        bronze_path: Path to Bronze layer data
        silver_path: Path to Silver layer output
    
    Returns:
        Cleaned DataFrame
    """
    logger.info("Cleaning POS data...")
    
    # Read from Bronze
    df = spark.read.format("delta").load(bronze_path)
    
    initial_count = df.count()
    logger.info(f"Bronze records: {initial_count}")
    
    # Data quality checks and cleaning
    df_clean = df \
        .filter(col("transaction_id").isNotNull()) \
        .filter(col("quantity") > 0) \
        .filter(col("unit_price") > 0) \
        .filter(col("total_amount") > 0) \
        .dropDuplicates(["transaction_id"])
    
    # Recalculate total_amount for consistency
    df_clean = df_clean.withColumn(
        "total_amount",
        (col("quantity") * col("unit_price")).cast("decimal(10,2)")
    )
    
    cleaned_count = df_clean.count()
    logger.info(f"Cleaned records: {cleaned_count}")
    logger.info(f"Records removed: {initial_count - cleaned_count}")
    
    # Write to Silver layer
    df_clean.write \
        .format("delta") \
        .mode("overwrite") \
        .save(silver_path)
    
    logger.info(f"✓ Cleaned POS data written to {silver_path}")
    return df_clean


def clean_crm_data(spark, bronze_path, silver_path):
    """
    Clean and standardize CRM customer data
    
    Args:
        spark: SparkSession object
        bronze_path: Path to Bronze layer data
        silver_path: Path to Silver layer output
    
    Returns:
        Cleaned DataFrame
    """
    logger.info("Cleaning CRM data...")
    
    df = spark.read.format("delta").load(bronze_path)
    
    initial_count = df.count()
    logger.info(f"Bronze records: {initial_count}")
    
    # Clean and validate
    df_clean = df \
        .filter(col("customer_id").isNotNull()) \
        .filter(col("age").between(18, 100)) \
        .filter(col("gender").isin(['M', 'F'])) \
        .dropDuplicates(["customer_id"])
    
    # Standardize gender values
    df_clean = df_clean.withColumn(
        "gender",
        when(col("gender") == "M", "Male")
        .when(col("gender") == "F", "Female")
        .otherwise(col("gender"))
    )
    
    cleaned_count = df_clean.count()
    logger.info(f"Cleaned records: {cleaned_count}")
    logger.info(f"Records removed: {initial_count - cleaned_count}")
    
    df_clean.write \
        .format("delta") \
        .mode("overwrite") \
        .save(silver_path)
    
    logger.info(f"✓ Cleaned customer data written to {silver_path}")
    return df_clean


def clean_inventory_data(spark, bronze_path, silver_path):
    """
    Clean and validate inventory data
    
    Args:
        spark: SparkSession object
        bronze_path: Path to Bronze layer data
        silver_path: Path to Silver layer output
    
    Returns:
        Cleaned DataFrame
    """
    logger.info("Cleaning inventory data...")
    
    df = spark.read.format("delta").load(bronze_path)
    
    initial_count = df.count()
    logger.info(f"Bronze records: {initial_count}")
    
    df_clean = df \
        .filter(col("product_id").isNotNull()) \
        .filter(col("stock_level") >= 0) \
        .filter(col("unit_cost") > 0) \
        .dropDuplicates(["product_id"])
    
    # Add stock status flag
    df_clean = df_clean.withColumn(
        "needs_reorder",
        when(col("stock_level") < col("reorder_point"), True)
        .otherwise(False)
    )
    
    cleaned_count = df_clean.count()
    logger.info(f"Cleaned records: {cleaned_count}")
    logger.info(f"Records removed: {initial_count - cleaned_count}")
    
    df_clean.write \
        .format("delta") \
        .mode("overwrite") \
        .save(silver_path)
    
    logger.info(f"✓ Cleaned inventory data written to {silver_path}")
    return df_clean


def create_customer_transactions(spark, pos_path, crm_path, output_path):
    """
    Join POS transactions with customer data
    
    Args:
        spark: SparkSession object
        pos_path: Path to cleaned transaction data
        crm_path: Path to cleaned customer data
        output_path: Path to output joined data
    
    Returns:
        Joined DataFrame
    """
    logger.info("Creating customer_transactions dataset...")
    
    pos_df = spark.read.format("delta").load(pos_path)
    crm_df = spark.read.format("delta").load(crm_path)
    
    # Add sample customer_id to transactions (in real scenario, this exists)
    from pyspark.sql.functions import expr
    pos_df = pos_df.withColumn("customer_id", 
                               expr("int(rand(42) * 5000) + 1"))
    
    # Join transactions with customer data
    joined_df = pos_df.join(
        crm_df.select("customer_id", "name", "age", "gender", "city", "loyalty_tier"),
        on="customer_id",
        how="left"
    )
    
    joined_count = joined_df.count()
    logger.info(f"Created {joined_count} joined records")
    
    joined_df.write \
        .format("delta") \
        .mode("overwrite") \
        .save(output_path)
    
    logger.info(f"✓ Created customer_transactions table at {output_path}")
    return joined_df


def main():
    """Main execution for Silver layer transformation"""
    logger.info("=" * 60)
    logger.info("SILVER LAYER TRANSFORMATION - Starting ETL Pipeline")
    logger.info("=" * 60)
    
    spark = create_spark_session()
    
    try:
        # Clean all Bronze datasets
        logger.info("\nCleaning Bronze layer data...")
        
        clean_pos_data(
            spark,
            "data/bronze/pos",
            "data/silver/transactions"
        )
        
        clean_crm_data(
            spark,
            "data/bronze/crm",
            "data/silver/customers"
        )
        
        clean_inventory_data(
            spark,
            "data/bronze/inventory",
            "data/silver/products"
        )
        
        # Create joined datasets
        logger.info("\nCreating enriched datasets...")
        
        create_customer_transactions(
            spark,
            "data/silver/transactions",
            "data/silver/customers",
            "data/silver/customer_transactions"
        )
        
        logger.info("\n" + "=" * 60)
        logger.info("✅ Silver layer transformation completed successfully!")
        logger.info("=" * 60)
        logger.info("\nSilver layer tables created:")
        logger.info("  - data/silver/transactions (cleaned POS data)")
        logger.info("  - data/silver/customers (cleaned CRM data)")
        logger.info("  - data/silver/products (cleaned inventory data)")
        logger.info("  - data/silver/customer_transactions (joined dataset)")
        
    except Exception as e:
        logger.error(f"❌ Error during transformation: {str(e)}")
        raise
    finally:
        spark.stop()
        logger.info("\nSpark session stopped")


if __name__ == "__main__":
    main()
