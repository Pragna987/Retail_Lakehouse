"""
Bronze Layer Ingestion - Instacart Dataset

This script reads raw CSV files from data/raw/ and writes them to Delta Lake format
in data/bronze/ with minimal transformations (schema enforcement, timestamps).

Bronze layer philosophy:
- Raw data preservation
- Schema validation
- Ingestion timestamp tracking
- No business logic or cleaning
"""

from pyspark.sql import SparkSession
from pyspark.sql.functions import current_timestamp, lit
from delta import configure_spark_with_delta_pip
from pathlib import Path
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def create_spark_session():
    """
    Create a Spark session with Delta Lake configuration
    Include settings for: app name "InstacartBronzeIngestion",
    Delta Lake extensions, and catalog configuration
    """
    builder = SparkSession.builder \
        .appName("InstacartBronzeIngestion") \
        .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
        .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog") \
        .config("spark.driver.memory", "4g") \
        .config("spark.sql.shuffle.partitions", "8")
    
    spark = configure_spark_with_delta_pip(builder).getOrCreate()
    spark.sparkContext.setLogLevel("WARN")
    return spark


def ingest_csv_to_bronze(spark, csv_filename, table_name, bronze_path="data/bronze"):
    """
    Read a CSV file from data/raw and write to Bronze Delta Lake table
    
    Args:
        spark: SparkSession
        csv_filename: Name of CSV file (e.g., 'orders.csv')
        table_name: Name for the Bronze table (e.g., 'orders')
        bronze_path: Path to bronze layer folder
    """
    raw_path = f"data/raw/{csv_filename}"
    output_path = f"{bronze_path}/{table_name}"
    
    logger.info(f"Starting ingestion: {csv_filename} -> {output_path}")
    
    try:
        # Read CSV with header and schema inference
        df = spark.read.csv(raw_path, header=True, inferSchema=True)
        
        # Add metadata columns for tracking
        df_with_metadata = df \
            .withColumn("ingestion_timestamp", current_timestamp()) \
            .withColumn("source_file", lit(csv_filename))
        
        # Write to Delta Lake in overwrite mode
        df_with_metadata.write \
            .format("delta") \
            .mode("overwrite") \
            .save(output_path)
        
        record_count = df.count()
        logger.info(f"✓ Ingested {record_count:,} records from {csv_filename} to {output_path}")
        
        return True
        
    except Exception as e:
        logger.error(f"✗ Failed to ingest {csv_filename}: {str(e)}")
        return False


def verify_raw_files():
    """Check if required raw CSV files exist"""
    raw_dir = Path("data/raw")
    
    required_files = [
        "orders.csv",
        "products.csv",
        "aisles.csv",
        "departments.csv",
        "order_products_train.csv",
        "order_products_prior.csv"
    ]
    
    missing_files = []
    for file in required_files:
        if not (raw_dir / file).exists():
            missing_files.append(file)
    
    if missing_files:
        logger.warning(f"Missing raw files: {', '.join(missing_files)}")
        logger.warning("Some tables will not be ingested. Place CSV files in data/raw/")
    else:
        logger.info("✓ All required raw files found")
    
    return [f for f in required_files if (raw_dir / f).exists()]


def main():
    """Main ingestion pipeline"""
    logger.info("=" * 80)
    logger.info("BRONZE LAYER INGESTION - Instacart Dataset")
    logger.info("=" * 80)
    
    # Verify raw files exist
    available_files = verify_raw_files()
    
    if not available_files:
        logger.error("No raw CSV files found in data/raw/. Exiting.")
        return
    
    # Create Spark session
    spark = create_spark_session()
    
    # Define ingestion tasks (csv_filename, table_name)
    ingestion_tasks = [
        ("orders.csv", "orders"),
        ("products.csv", "products"),
        ("aisles.csv", "aisles"),
        ("departments.csv", "departments"),
        ("order_products_train.csv", "order_products_train"),
        ("order_products_prior.csv", "order_products_prior")
    ]
    
    # Filter to only available files
    tasks_to_run = [(csv, table) for csv, table in ingestion_tasks if csv in available_files]
    
    # Run ingestion for each file
    results = []
    for csv_file, table_name in tasks_to_run:
        success = ingest_csv_to_bronze(spark, csv_file, table_name)
        results.append((table_name, success))
    
    # Summary
    logger.info("=" * 80)
    logger.info("INGESTION SUMMARY")
    logger.info("=" * 80)
    
    successful = sum(1 for _, success in results if success)
    total = len(results)
    
    for table_name, success in results:
        status = "✓ SUCCESS" if success else "✗ FAILED"
        logger.info(f"{status}: {table_name}")
    
    logger.info(f"\nCompleted {successful}/{total} ingestions successfully")
    
    spark.stop()


if __name__ == "__main__":
    main()
