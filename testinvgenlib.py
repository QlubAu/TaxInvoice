import pandas
import boto3
access_key = 'AKIAR5SVE56T5QHE5G6W'
secret_key = 'Td7BXuawWp8L0dT/MBJ6qZajD6DXDqRBucR0whnt'
client = boto3.client('quicksight',
                      region_name='us-east-1',
                      aws_access_key_id='YOUR_ACCESS_KEY',
                      aws_secret_access_key='YOUR_SECRET_KEY',
                      aws_session_token='YOUR_SESSION_TOKEN')






