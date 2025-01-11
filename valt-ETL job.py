import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from awsgluedq.transforms import EvaluateDataQuality

args = getResolvedOptions(sys.argv, ['JOB_NAME'])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# Default ruleset used by all target nodes with data quality enabled
DEFAULT_DATA_QUALITY_RULESET = """
    Rules = [
        ColumnCount > 0
    ]
"""

# Script generated for node Amazon S3
AmazonS3_node1736042286045 = glueContext.create_dynamic_frame.from_catalog(database="valt-machine-learning", table_name="valt_cat_bucket_01", transformation_ctx="AmazonS3_node1736042286045")

# Script generated for node Change Schema
ChangeSchema_node1736043663717 = ApplyMapping.apply(frame=AmazonS3_node1736042286045, mappings=[("index", "long", "index", "long"), ("customer id", "string", "customer id", "string"), ("first name", "string", "first name", "string"), ("last name", "string", "last name", "string"), ("company", "string", "company", "string"), ("city", "string", "city", "string"), ("country", "string", "country", "string"), ("phone 1", "string", "phone 1", "string"), ("phone 2", "string", "phone 2", "string"), ("email", "string", "email", "string"), ("subscription date", "string", "subscription date", "date"), ("website", "string", "website", "string")], transformation_ctx="ChangeSchema_node1736043663717")

# Script generated for node Amazon S3
EvaluateDataQuality().process_rows(frame=ChangeSchema_node1736043663717, ruleset=DEFAULT_DATA_QUALITY_RULESET, publishing_options={"dataQualityEvaluationContext": "EvaluateDataQuality_node1736042222389", "enableDataQualityResultsPublishing": True}, additional_options={"dataQualityResultsPublishing.strategy": "BEST_EFFORT", "observations.scope": "ALL"})
AmazonS3_node1736044309776 = glueContext.write_dynamic_frame.from_options(frame=ChangeSchema_node1736043663717, connection_type="s3", format="csv", connection_options={"path": "s3://valt-etl-target-bucket-01", "partitionKeys": []}, transformation_ctx="AmazonS3_node1736044309776")

job.commit()