import boto3

def lambda_handler(event, context):
    glue = boto3.client('glue')
    
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']
    
    glue.start_job_run(
        JobName='json-to-csv-job',
        Arguments={
            '--SOURCE_PATH': f's3://{bucket}/{key}',
            '--TARGET_PATH': f's3://your-target-bucket/converted/'
        }
    )
    
    return {
        'statusCode': 200,
        'body': f'Started Glue job for file: {key}'
    }
