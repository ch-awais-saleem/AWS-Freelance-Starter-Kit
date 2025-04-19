import boto3
from datetime import date

def lambda_handler(event, context):
    client = boto3.client('athena')
    query = '''
    SELECT COUNT(*) AS files, SUM(size) AS total_bytes
    FROM processed_file_log
    WHERE date = current_date
    '''
    
    response = client.start_query_execution(
        QueryString=query,
        QueryExecutionContext={'Database': 'your_db'},
        ResultConfiguration={'OutputLocation': 's3://your-report-bucket/'}
    )
    
    return {'status': 'Query started', 'ExecutionId': response['QueryExecutionId']}
