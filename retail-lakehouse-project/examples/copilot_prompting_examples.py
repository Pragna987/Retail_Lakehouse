"""
Copilot Prompting Examples for Data Engineering with PySpark and Delta Lake

This file demonstrates effective prompting patterns for GitHub Copilot.
The comments below are examples of how to write inline prompts that help
Copilot generate accurate, context-aware code for data engineering tasks.

Best Practice: Write clear, specific comments describing what you want,
then let Copilot suggest the implementation. Press Tab to accept.
"""

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, sum, avg, count, when
from delta import configure_spark_with_delta_pip


# Example 1: Create a Spark session with Delta Lake configuration
# Include settings for: app name "RetailLakehouse", 
# Delta Lake extensions, and catalog configuration
def create_spark_session():
    """
    Copilot should suggest something like:
    
    builder = SparkSession.builder \\
        .appName("RetailLakehouse") \\
        .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \\
        .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")
    spark = configure_spark_with_delta_pip(builder).getOrCreate()
    return spark
    """
    pass


# Example 2: Read a CSV file from data/sales.csv into a Spark DataFrame with schema inference and header
def read_sales_data(spark):
    """
    Prompt: Read CSV with header=True, inferSchema=True from path 'data/sales.csv'
    
    Expected suggestion:
    sales_df = spark.read.csv('data/sales.csv', header=True, inferSchema=True)
    return sales_df
    """
    pass


# Example 3: Filter the DataFrame to include only records where quantity > 10 and status == 'COMPLETED'
def filter_completed_sales(sales_df):
    """
    Prompt in comment before line:
    # Filter to keep only rows where quantity > 10 and status is 'COMPLETED'
    
    Expected:
    filtered_df = sales_df.filter((col('quantity') > 10) & (col('status') == 'COMPLETED'))
    return filtered_df
    """
    pass


# Example 4: Group by product_id and calculate total revenue, average quantity, and count of transactions
def aggregate_sales_by_product(sales_df):
    """
    Prompt:
    # Group by product_id, then aggregate: sum of revenue as total_revenue, 
    # avg of quantity as avg_quantity, count of transactions as num_transactions
    
    Expected suggestion:
    agg_df = sales_df.groupBy('product_id').agg(
        sum('revenue').alias('total_revenue'),
        avg('quantity').alias('avg_quantity'),
        count('*').alias('num_transactions')
    )
    return agg_df
    """
    pass


# Example 5: Write the DataFrame to Delta Lake format at path 'delta/retail_sales' with overwrite mode
def write_to_delta(df, path='delta/retail_sales'):
    """
    Prompt:
    # Write df to Delta format at the given path using overwrite mode
    
    Expected:
    df.write.format('delta').mode('overwrite').save(path)
    """
    pass


# Example 6: Read from Delta table and add a new column 'discount_flag' 
# that is True when discount > 0, otherwise False
def add_discount_flag(spark, delta_path='delta/retail_sales'):
    """
    Prompt:
    # Read Delta table from delta_path
    # Add a column 'discount_flag': True if discount > 0, else False
    
    Expected:
    df = spark.read.format('delta').load(delta_path)
    df_with_flag = df.withColumn('discount_flag', when(col('discount') > 0, True).otherwise(False))
    return df_with_flag
    """
    pass


# Example 7: Upsert (merge) new data into an existing Delta table
# Match on transaction_id, update all columns if matched, insert if not matched
def upsert_sales_data(spark, new_data_df, target_table_path='delta/retail_sales'):
    """
    Prompt:
    # Perform Delta merge (upsert) on target_table_path
    # Match condition: target.transaction_id = source.transaction_id
    # When matched: update all columns
    # When not matched: insert new row
    
    Expected (pseudo-code, Copilot may suggest deltaTable.alias usage):
    from delta.tables import DeltaTable
    delta_table = DeltaTable.forPath(spark, target_table_path)
    delta_table.alias('target').merge(
        new_data_df.alias('source'),
        'target.transaction_id = source.transaction_id'
    ).whenMatchedUpdateAll().whenNotMatchedInsertAll().execute()
    """
    pass


# Example 8: Create a function to read JSON files from a folder, flatten nested schema, and write to Delta
def ingest_json_to_delta(spark, json_folder='data/raw_json', output_path='delta/ingested_data'):
    """
    Prompt:
    # Read all JSON files from json_folder with multiLine=True
    # Flatten any nested struct columns (example: explode arrays or select nested fields)
    # Write result to Delta at output_path in append mode
    
    Copilot might suggest:
    df = spark.read.option('multiLine', True).json(json_folder)
    # (manual flattening depends on schema; Copilot can help if you describe structure)
    df.write.format('delta').mode('append').save(output_path)
    """
    pass


# Example 9: Join two DataFrames on a key and select specific columns
def join_sales_and_customers(sales_df, customers_df):
    """
    Prompt:
    # Inner join sales_df and customers_df on customer_id
    # Select columns: transaction_id, customer_name, revenue, purchase_date from joined result
    
    Expected:
    joined_df = sales_df.join(customers_df, on='customer_id', how='inner') \\
        .select('transaction_id', 'customer_name', 'revenue', 'purchase_date')
    return joined_df
    """
    pass


# Example 10: Time-travel query in Delta Lake to read data as of a specific version
def read_delta_version(spark, table_path='delta/retail_sales', version=5):
    """
    Prompt:
    # Read Delta table at table_path as of version number 'version'
    
    Expected:
    df = spark.read.format('delta').option('versionAsOf', version).load(table_path)
    return df
    """
    pass


if __name__ == '__main__':
    print("This file contains example prompts for GitHub Copilot.")
    print("Open it in VS Code with Copilot enabled and try uncommenting the function bodies.")
    print("Write the comment prompts, then let Copilot suggest the implementation.")
