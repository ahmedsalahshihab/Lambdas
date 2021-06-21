import boto3
import os

SOURCE_BUCKET = os.environ['SOURCE_BUCKET']

def lambda_handler(event, context):
    
    for record in event['Records']:
        key = record['s3']['object']['key']
        filename = key[6:]
        print(filename)
        
        transclient = boto3.client('transcribe')
        response = transclient.start_transcription_job(
            TranscriptionJobName=filename,
            LanguageCode='en-US',
            Media={
                'MediaFileUri':'s3://{0}/{1}'.format(SOURCE_BUCKET, key)
            },
        )
        print(response)
