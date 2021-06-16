import boto3
import datetime

def ami_age(creation_date):
    ami_creation_time = datetime.datetime.strptime(creation_date, '%Y-%m-%dT%H:%M:%S.%fZ')
    #print(ami_creation_time)   #for debugging purposes
    time_difference = datetime.datetime.now() - ami_creation_time
    #print(str(time_difference.days) + ' days')   #for debugging purposes
    return time_difference

def lambda_handler(event, context):
    
    ec2client = boto3.client('ec2')
    response = ec2client.describe_regions()

    for i in response['Regions']:
        print(i['RegionName'])
    
        ec2 = boto3.resource('ec2', region_name=i['RegionName'])
        
        my_images = ec2.images.filter(
            Owners=[
                'self',
            ],
        )
        
        for j in my_images:
            age = ami_age(j.creation_date)
            if age.days >= 2:       #removing AMIs created more than 2 days ago       
                print('Deregistering AMI {0}; creation time: {1}'.format(j.image_id, j.creation_date))
                j.deregister()
            else:
                print('AMI {0}; creation time: {1}'.format(j.image_id, j.creation_date)) 
                
    
