import boto3 
from datetime import datetime

def lambda_handler(event, context):

    ec2client = boto3.client('ec2')

    response = ec2client.describe_regions()

    for i in response['Regions']:
        print(i['RegionName'])
        ec2 = boto3.resource('ec2', region_name=i['RegionName'])

        instances = ec2.instances.filter(
            Filters=[
                {
                    'Name': 'tag:backup',
                    'Values': [
                        'true',
                        ]
                },
            ],
        )

        for j in instances:
            for v in j.volumes.all():
                v.create_snapshot(
                    Description='instance {0}, volume {1}, {2}'.format(j.instance_id,v.volume_id,(datetime.today()).strftime('%d-%m-%YT%H-%M-%S.%f'))
                )
                print('Creating snapshot for volume {0}'.format(v.volume_id))
