# Folder: glue_jobs/json_to_csv.py
import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job

args = getResolvedOptions(sys.argv, ['JOB_NAME', 'SOURCE_PATH', 'TARGET_PATH'])

sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

source_path = args['SOURCE_PATH']
target_path = args['TARGET_PATH']

dyframe = glueContext.create_dynamic_frame.from_options(
    connection_type="s3",
    connection_options={"paths": [source_path]},
    format="json"
)

# Flatten if nested and convert to DataFrame
df = dyframe.toDF()
df.write.mode("overwrite").csv(target_path, header=True)

job.commit()

