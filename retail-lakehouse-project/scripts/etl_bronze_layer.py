"""
Bronze Layer ETL Pipeline
Ingests raw data from CSV files into Delta Lake Bronze layer
Adds metadata columns for lineage tracking
"""

from pyspark.sql import SparkSession
from pyspark.sql.functions import current_timestamp, input_file_name
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
        .appName("RetailLakehouse-Bronze") \
        .config("spark.sql.extensions", 
                "io.delta.sql.DeltaSparkSessionExtension") \
        .config("spark.sql.catalog.spark_catalog", 
                "org.apache.spark.sql.delta.catalog.DeltaCatalog")
    
    spark = configure_spark_with_delta_pip(builder).getOrCreate()
    logger.info("✓ Spark session created successfully")
    return spark


def ingest_pos_data(spark, source_path, target_path):
    """
    Ingest POS transaction data into Bronze layer
    
    Args:
        spark: SparkSession object
        source_path: Path to source CSV file
        target_path: Path to Delta Lake target directory
    
    Returns:
        DataFrame with ingested data
    """
    logger.info(f"Ingesting POS data from {source_path}...")
    
    # Read CSV with schema inference
    df = spark.read \
        .option("header", "true") \
        .option("inferSchema", "true") \
        .csv(source_path)
    
    # Add metadata columns
    df = df.withColumn("ingestion_timestamp", current_timestamp()) \
           .withColumn("source_file", input_file_name())
    
    logger.info(f"Read {df.count()} records from source")
    
    # Write to Delta Lake in Bronze layer
    df.write \
        .format("delta") \
        .mode("overwrite") \
        .save(target_path)
    
    logger.info(f"✓ Ingested POS data to {target_path}")
    return df


def ingest_crm_data(spark, source_path, target_path):
    """
    Ingest CRM customer data into Bronze layer
    
    Args:
        spark: SparkSession object
        source_path: Path to source CSV file
        target_path: Path to Delta Lake target directory
    
    Returns:
        DataFrame with ingested data
    """
    logger.info(f"Ingesting CRM data from {source_path}...")
    
    df = spark.read \
        .option("header", "true") \
        .option("inferSchema", "true") \
        .csv(source_path)
    
    df = df.withColumn("ingestion_timestamp", current_timestamp()) \
           .withColumn("source_file", input_file_name())
    
    logger.info(f"Read {df.count()} records from source")
    
    df.write \
        .format("delta") \
        .mode("overwrite") \
        .save(target_path)
    
    logger.info(f"✓ Ingested CRM data to {target_path}")
    return df


def ingest_inventory_data(spark, source_path, target_path):
    """
    Ingest inventory data into Bronze layer
    
    Args:
        spark: SparkSession object
        source_path: Path to source CSV file
        target_path: Path to Delta Lake target directory
    
    Returns:
        DataFrame with ingested data
    """
    logger.info(f"Ingesting inventory data from {source_path}...")
    
    df = spark.read \
        .option("header", "true") \
        .option("inferSchema", "true") \
        .csv(source_path)
    
    df = df.withColumn("ingestion_timestamp", current_timestamp()) \
           .withColumn("source_file", input_file_name())
    
    logger.info(f"Read {df.count()} records from source")
    
    df.write \
        .format("delta") \
        .mode("overwrite") \
        .save(target_path)
    
    logger.info(f"✓ Ingested inventory data to {target_path}")
    return df


def ingest_marketing_data(spark, source_path, target_path):
    """
    Ingest marketing campaign data into Bronze layer
    
    Args:
        spark: SparkSession object
        source_path: Path to source CSV file
        target_path: Path to Delta Lake target directory
    
    Returns:
        DataFrame with ingested data
    """
    logger.info(f"Ingesting marketing data from {source_path}...")
    
    df = spark.read \
        .option("header", "true") \
        .option("inferSchema", "true") \
        .csv(source_path)
    
    df = df.withColumn("ingestion_timestamp", current_timestamp()) \
           .withColumn("source_file", input_file_name())
    
    logger.info(f"Read {df.count()} records from source")
    
    df.write \
        .format("delta") \
        .mode("overwrite") \
        .save(target_path)
    
    logger.info(f"✓ Ingested marketing data to {target_path}")
    return df


def main():
    """Main execution function for Bronze layer ingestion"""
    logger.info("=" * 60)
    logger.info("BRONZE LAYER INGESTION - Starting ETL Pipeline")
    logger.info("=" * 60)
    
    spark = create_spark_session()
    
    try:
        # Ingest all data sources to Bronze layer
        logger.info("\nIngesting data sources...")
        
        ingest_pos_data(
            spark, 
            "raw_data/pos_transactions.csv",
            "data/bronze/pos"
        )
        
        ingest_crm_data(
            spark,
            "raw_data/customers.csv",
            "data/bronze/crm"
        )
        
        ingest_inventory_data(
            spark,
            "raw_data/products_inventory.csv",
            "data/bronze/inventory"
        )
        
        ingest_marketing_data(
            spark,
            "raw_data/marketing_campaigns.csv",
            "data/bronze/marketing"
        )
        
        logger.info("\n" + "=" * 60)
        logger.info("✅ Bronze layer ingestion completed successfully!")
        logger.info("=" * 60)
        logger.info("\nBronze layer tables created:")
        logger.info("  - data/bronze/pos")
        logger.info("  - data/bronze/crm")
        logger.info("  - data/bronze/inventory")
        logger.info("  - data/bronze/marketing")
        
    except Exception as e:
        logger.error(f"❌ Error during ingestion: {str(e)}")
        raise
    finally:
        spark.stop()
        logger.info("\nSpark session stopped")


if __name__ == "__main__":
    main()
