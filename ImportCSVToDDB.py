import boto3
import tempfile
import os

SOURCE_BUCKET = os.environ['source-ashihab']

def read_csv(file):
    items = []
    with open(file) as csvfile:
        reader = csv.DictReader(csvfile)		#https://docs.python.org/3/library/csv.html
        for row in reader:
            data = {}
            data['Meta'] = {}
            data['Year'] = int(row['Year'])
            data['Title'] = row['Title'] or None
            data['Meta']['Length'] = int(row['Length'] or 0)
            data['Meta']['Subject'] = row['Subject'] or None
            data['Meta']['Actor'] = row['Actor'] or None
            data['Meta']['Actress'] = row['Actress'] or None
            data['Meta']['Director'] = row['Director'] or None
            data['Meta']['Popularity'] = row['Popularity'] or None
            data['Meta']['Awards'] = row['Awards'] == 'Yes'			#if equal Yes, return True(boolean). Otherwise, return False(boolean)			
            data['Meta']['Image'] = row['Image'] or None
            data['Meta'] = {k: v for k,
                            v in data['Meta'].items() if v is not None}
            items.append(data)
    return items

def lambda_handler(event, context):

	for record in event['Records']:

		key = record['s3']['object']['key']

		csvfile = tempfile.NamedTemporaryFile()
		
		s3client = boto3.client('s3')
		s3client.download_file(SOURCE_BUCKET, key, csvfile.name)
		
		items = read_csv(csvfile.name)

		dynamodb = boto3.resource('dynamodb')
		table = dynamodb.Table('MyMovies')
		with table.batch_writer() as batch:
			for item in items():
    			batch.put_item(Item=item)

#===============================================================#

#for testing

import boto3
import tempfile
import csv

def read_csv(file):
    items = []
    with open(file) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            data = {}
            data['Meta'] = {}
            data['Year'] = int(row['Year'])
            data['Title'] = row['Title'] or None
            data['Meta']['Length'] = int(row['Length'] or 0)
            data['Meta']['Subject'] = row['Subject'] or None
            data['Meta']['Actor'] = row['Actor'] or None
            data['Meta']['Actress'] = row['Actress'] or None
            data['Meta']['Director'] = row['Director'] or None
            data['Meta']['Popularity'] = row['Popularity'] or None
            data['Meta']['Awards'] = row['Awards'] == 'Yes'		#if equal Yes, return True(boolean). Otherwise, return False(boolean)
            data['Meta']['Image'] = row['Image'] or None
            items.append(data)
    return items

SOURCE_BUCKET = 'source-ashihab'
key = 'mymovies.csv'
csvfile = tempfile.NamedTemporaryFile()
s3client = boto3.client('s3')
s3client.download_file(SOURCE_BUCKET, key, csvfile.name)
items = read_csv(csvfile.name)
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('MyMovies')
with table.batch_writer() as batch:
	for item in items:
		batch.put_item(Item=item)

