import boto3
import os

AMI = os.environ['AMI']
KEY_PAIR = os.environ['KEY_PAIR']

def lambda_handler(event, context):
    
    ec2 = boto3.resource('ec2')
    
    response = ec2.create_instances(
        ImageId = AMI,
        KeyName = KEY_PAIR,
        MaxCount = 1,
        MinCount = 1
    )
    
    for i in response:
        print("Creating EC2 instance " + i.instance_id)
