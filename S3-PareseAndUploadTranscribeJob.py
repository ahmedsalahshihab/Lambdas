import boto3
import os
import urllib.request
import tempfile
import json     #https://www.codegrepper.com/code-examples/javascript/byte+to+json+python

DESTINATION_BUCKET = os.environ['DESTINATION_BUCKET']

def lambda_handler(event, context):
    
    transjobname = event['detail']['TranscriptionJobName']
    
    transclient = boto3.client('transcribe')
    response = transclient.get_transcription_job(
        TranscriptionJobName = transjobname
    )
    transjoburl = response['TranscriptionJob']['Transcript']['TranscriptFileUri']
    print(transjoburl)
    
    http_response_object = urllib.request.urlopen(transjoburl)   #return an HTTPResponse object
    content = http_response_object.read()    #returns a byte array object
    my_json = content.decode('utf8')     #returns an str object
    data = json.loads(my_json)
    text = data['results']['transcripts'][0]['transcript']
    print(text)
    
    mytempfile = tempfile.NamedTemporaryFile()
    with open(mytempfile.name, 'w') as f:
        f.write(text)
        
    s3client = boto3.client('s3')
    outputfile = 'asr/asr' + transjobname[:-4] + '.txt'
    s3client.upload_file(mytempfile.name, DESTINATION_BUCKET, outputfile)
