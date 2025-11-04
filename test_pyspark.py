from pyspark.sql import SparkSession

def main():
    spark = SparkSession.builder.master('local[*]').appName('health-check').getOrCreate()
    df = spark.createDataFrame([(1,'a'),(2,'b')], ['id','val'])
    df.show()
    spark.stop()

if __name__ == '__main__':
    main()
