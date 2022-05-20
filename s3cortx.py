import boto3
from botocore.exceptions import ClientError
import sys
import os
import ipfshttpclient

#init
ACCESS_KEY = 'AKIAIAtG4lneTVy_ANcbXaqnvA'
S_ACCESS_KEY = 'CptRr3WhWbzzBBE0ihzokA4GK0SH2FQKZLthCXvb'

#create access to s3 resource
s3client = boto3.client(service_name = 's3',
endpoint_url = 'http://192.168.8.148',
aws_access_key_id = ACCESS_KEY,
aws_secret_access_key = S_ACCESS_KEY)

#ipfs client
ipfsclient = ipfshttpclient.connect('/ip4/127.0.0.1/tcp/5001')

def create_bucket(bucketName):
	try:
		s3client.create_bucket(Bucket = bucketName)
	except ClientError as e:
		return False
	return True
	
def list_buckets():
	bucketList = []
	response = s3client.list_buckets()
	for bucket in response['Buckets']:
		bucketList += {bucket['Name']}
	return bucketList

def upload_file(fileName, bucket, objectName = None):
	# fileName has to be a file-like object opened in binary mode
	if objectName is None:
		objectName = os.path.basename(fileName)
	try:
		resp = s3client.upload_file(fileName, bucket, objectName)
	except ClientError as e:
		return False
	return True

def upload_to_ipfs(fileName):
	newfile = ipfsclient.add(fileName)
	return newfile['Hash']
		
		
if len(sys.argv) > 1:
	if sys.argv[1] == '--create-bucket':
		retval = create_bucket(sys.argv[2])
		if retval is True:
			print('Created bucket: %s' % sys.argv[2])
		else:
			print('Error')
	elif sys.argv[1] == '--list-buckets':
		buckets = list_buckets()
		for i in buckets:
			print("Bucket Name: %s" % i)
	elif sys.argv[1] == '--upload-file':
		retval = upload_to_ipfs(sys.argv[2])
		print(retval)
