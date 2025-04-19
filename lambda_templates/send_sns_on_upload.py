import boto3

def lambda_handler(event, context):
    sns = boto3.client('sns')
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']

    message = f"A new file was uploaded to {bucket}/{key}"
    topic_arn = 'arn:aws:sns:your-region:your-account-id:your-topic-name'

    sns.publish(
        TopicArn=topic_arn,
        Subject='New S3 Upload Notification',
        Message=message
    )
    
    return {'status': 'Notification sent'}
