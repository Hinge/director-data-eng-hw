#!/usr/bin/env python

import boto3
import os
import config

#AWS S3 details
s3 = boto3.resource('s3', aws_access_key_id = config.AWS_CONFIG['AWS_ACCESS_KEY'], aws_secret_access_key = config.AWS_CONFIG["AWS_SECRET_KEY"])
s3_client = boto3.client('s3', aws_access_key_id=config.AWS_CONFIG['AWS_ACCESS_KEY'], aws_secret_access_key=config.AWS_CONFIG["AWS_SECRET_KEY"])


def getfilelist(bucket, files_to_process, subfolder = ''):
	'''
		This function returns a list with files in S3 folder
	'''

	try:
		#Get list of objects in s3 bucket
		#Copy files to local server that don't end with '/'. Basically keys associated with folders end with '/'
		if (subfolder.strip()):
			s3bucketcontents = [obj['Key'] for obj in s3_client.list_objects_v2(Bucket = bucket, Prefix = subfolder)['Contents'] if(not obj['Key'].endswith("/"))]
		else:
			s3bucketcontents = [obj['Key'] for obj in s3_client.list_objects_v2(Bucket = bucket)['Contents'] if(not obj['Key'].endswith("/"))]
			
		# print(s3bucketcontents)


		# Fils to download
		files_to_download = []

		filesprocessed = 0
		totalfiles = 0

		# Set total files to process
		if (files_to_process.strip().lower() == 'all'):
			totalfiles = len(s3bucketcontents)
		else:
			totalfiles = files_to_process

	
		for file in s3bucketcontents:
			# Set the basename of each file since S3 sends the entire path back
			basename = os.path.basename(file)
			# print(basename			
			# print(file)
			files_to_download.append(basename)

			filesprocessed	+= 1

			if (filesprocessed == totalfiles):
				break


		# print(len(files_to_download))

		return files_to_download


	except Exception as e:
		# print(e.__doc__)
		#Send failure code
		return []

if __name__ == "__main__":
	print('Running tests')
	
