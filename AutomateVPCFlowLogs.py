import boto3
import os

ACCOUNT = os.environ['ACCOUNT']

def lambda_handler(event, context):
    vpc_id = event['detail']['responseElements']['vpc']['vpcId']
    
    ec2client = boto3.client('ec2')
    
    DELIVERLOGSPERMISSIONARN = 'arn:aws:iam::' + ACCOUNT + ':role/lambda-'
    LOGGROUPNAME = 'arn:aws:logs:eu-west-1:' + ACCOUNT + ':log-group:flowlogs' + vpc_id 
    
    response = ec2client.create_flow_logs(
        ResourceIds = [
            vpc_id,
            ],
        DeliverLogsPermissionArn = DELIVERLOGSPERMISSIONARN,
        #LogGroupName = LOGGROUPNAME,
        ResourceType = 'VPC',
        TrafficType = 'ALL',
        LogDestinationType = 'cloud-watch-logs',
        LogDestination = LOGGROUPNAME
    )
    
    print(response)
    print('Enabling flow logs for VPC ' + vpc_id)
  
