import boto3
import os
import tempfile
from PIL import Image

SOURCE_BUCKET_NAME = os.environ['SOURCE_BUCKET_NAME']
DESTINATION_BUCKET_NAME = os.environ['DESTINATION_BUCKET_NAME']

SIZE = 128, 128

def generate_thumbnail(original_image):
    with Image.open(original_image.name) as im:			#https://pillow.readthedocs.io/en/stable/reference/Image.html	
        im.thumbnail(SIZE)
        im.save(original_image.name, 'JPEG')

def lambda_handler(event, context):
    
    s3client = boto3.client('s3')
    
    for record in event['Records']:
        source_key = record['s3']['object']['key']
        print(source_key)
        dest_key = 'thumb-' + source_key
        print(dest_key)
        
        original_image = tempfile.NamedTemporaryFile()		#https://www.tutorialspoint.com/generate-temporary-files-and-directories-using-python
        print(original_image.name)
        s3client.download_file(SOURCE_BUCKET_NAME, source_key, original_image.name)
        #thumbnail_image = tempfile.NamedTemporaryFile()
        #print(thumbnail_image.name)
        generate_thumbnail(original_image)
        thumbnail_image = original_image
        s3client.upload_file(thumbnail_image.name, DESTINATION_BUCKET_NAME, dest_key)

#========================================================#

#Run the below as administrator in Python for testing

import boto3
import os
import tempfile
from PIL import Image

SOURCE_BUCKET_NAME = 'source-ashihab'
DESTINATION_BUCKET_NAME = 'destination-ashihab'

SIZE = 128, 128

def generate_thumbnail(original_image):
    with Image.open(original_image.name) as im:
        im.thumbnail(SIZE)
        im.save(original_image.name, 'JPEG')

def lambda_handler(event, context):
    
    s3client = boto3.client('s3')
    source_key = 'earth.jpg'
    print(source_key)
    dest_key = 'thumb-' + source_key
    print(dest_key)
        
    original_image = tempfile.NamedTemporaryFile()
    print(original_image.name)
    s3client.download_file(SOURCE_BUCKET_NAME, source_key, original_image.name)
    #thumbnail_image = tempfile.NamedTemporaryFile()
    #print(thumbnail_image.name)
    #generate_thumbnail(download_image, thumbnail_image)
    generate_thumbnail(original_image)
    thumbnail_image = original_image
    s3client.upload_file(thumbnail_image.name, DESTINATION_BUCKET_NAME, dest_key)

if __name__ == '__main__':
	lambda_handler('1234', '1234')
