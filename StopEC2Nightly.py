import boto3

def lambda_handler(event, context):

    ec2client = boto3.client('ec2')

    response = ec2client.describe_regions()

    for i in response['Regions']:
        print(i['RegionName'])
        ec2 = boto3.resource('ec2', region_name=i['RegionName'])
        instances = ec2.instances.all()
        for j in instances:
            if (j.state['Name'] == 'running'):
                print(j.instance_id)
                #Anything you do here will be applied on all running instances in all regions; so for example, you can stop all running instances.
