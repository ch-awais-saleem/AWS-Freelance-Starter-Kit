import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from pyspark.sql import SparkSession
from awsglue.context import GlueContext


# Arguments from job parameters
args = getResolvedOptions(sys.argv, ['FILE_PATH', 'TABLE_NAME'])
file_path = args['FILE_PATH']
target_database = 'posdb'
table_name = args['TABLE_NAME']


# Initialize Glue context
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session

# Use the Iceberg catalog configured with Glue Data Catalog
spark.conf.set("spark.sql.catalog.glue_catalog", "org.apache.iceberg.spark.SparkCatalog")
spark.conf.set("spark.sql.catalog.glue_catalog.catalog-impl", "org.apache.iceberg.aws.glue.GlueCatalog")
spark.conf.set("spark.sql.catalog.glue_catalog.warehouse", "s3://retail-pos-curated/iceberg-tables/")
spark.conf.set("spark.sql.catalog.glue_catalog.io-impl", "org.apache.iceberg.aws.s3.S3FileIO")
spark.conf.set("spark.sql.defaultCatalog", "glue_catalog")
# Create Iceberg table
# spark.sql("""
# create table if not exists glue_catalog.posdb.stores (
#         storeid INT,
#         storename STRING,
#         address STRING,
#         city STRING,
#         state STRING,
#         zipcode STRING
# )
# USING iceberg LOCATION 's3://retail-pos-curated/iceberg-tables/posdb/stores'
# ;""")

# Read Parquet data from S3
source_df = spark.read.parquet(file_path)

# Register DataFrame as a temporary view for SQL merge
source_df.createOrReplaceTempView("incoming_data")


# Define mapping of table names to their primary key columns
primary_keys = {
    "stores": "storeid",
    "products": "productid",
    "customers": "customerid",
    "transactions": "transactionid",
    "transactiondetails": "detailid",
    "pos_terminals": "terminalid",
    "pos_users": "userid",
    "pos_sales": "saleid",
    "pos_saledetails": "saledetailid"
}

# Get the appropriate ID column based on the table_name
id_column = primary_keys.get(table_name)

if id_column is None:
    raise ValueError(f"No primary key mapping found for table: {table_name}")

# Perform Iceberg MERGE (Upsert)
spark.sql(f"""
    MERGE INTO glue_catalog.posdb.curated_{table_name} AS target
    USING incoming_data AS source
    ON target.{id_column} = source.{id_column}
    WHEN MATCHED THEN
      UPDATE SET *
    WHEN NOT MATCHED THEN
      INSERT *
""")





# import sys
# from awsglue.context import GlueContext
# from awsglue.utils import getResolvedOptions
# from pyspark.context import SparkContext
# from pyspark.sql import functions as F

# # Arguments from job parameters
# args = getResolvedOptions(sys.argv, ['FILE_PATH', 'TABLE_NAME', 'PRIMARY_KEY'])
# source_file_path = args['FILE_PATH']
# target_database = 'posdb'
# target_table = args['TABLE_NAME']
# primary_key = args['PRIMARY_KEY']

# sc = SparkContext()
# glueContext = GlueContext(sc)
# spark = glueContext.spark_session

# # Load the new data file (e.g., JSON or CSV)
# df_new = spark.read.option("multiline", "true").json(source_file_path)

# # Register the new data as a temporary view
# df_new.createOrReplaceTempView("new_data")

# # Read the existing Iceberg table
# df_existing = spark.read.format("iceberg").load(f"{target_database}.{target_table}")
# df_existing.createOrReplaceTempView("existing_data")

# # Perform upsert using Spark SQL (can also use MERGE if Glue supports Iceberg Merge semantics)
# upserted_df = spark.sql(f"""
# SELECT * FROM new_data
# UNION ALL
# SELECT * FROM existing_data e
# WHERE NOT EXISTS (
#     SELECT 1 FROM new_data n
#     WHERE n.{primary_key} = e.{primary_key}
# )
# """)

# # Overwrite the Iceberg table in upsert mode
# (
#     upserted_df.writeTo(f"{target_database}.{target_table}")
#     .using("iceberg")
#     .option("overwrite-mode", "dynamic")  # Upsert behavior
#     .option("merge-schema", "true")
#     .tableProperty("write.format.default", "parquet")
#     .append()
# )


# Job parameters Info
# --TABLE_NAME

# Value
# customers

# Key
# --datalake-formats

# Value
# iceberg
