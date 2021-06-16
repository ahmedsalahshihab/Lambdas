import boto3

def lambda_handler(event, context):

    ec2client = boto3.client('ec2')
    response = ec2client.describe_regions()

    for i in response['Regions']:
        print(i['RegionName'])

        ec2 = boto3.resource('ec2', region_name=i['RegionName'])
        volumes = ec2.volumes.filter(
            Filters=[
                {
                    'Name': 'status',
                    'Values': [
                        'available',
                    ]
                },
            ],
        )

        for v in volumes:
            v.delete()
            print('Deleting volume {0}'.format(v.volume_id))
