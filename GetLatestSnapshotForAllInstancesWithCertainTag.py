import boto3

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
                for s in v.snapshots.all():
                    print(', '.join((j.instance_id, s.id, s.volume_id, s.start_time.strftime("%c"), s.state, s.progress)))
                    if (s.state == "completed"):
                        break
