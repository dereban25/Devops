import boto3

s3 = boto3.client('s3')
response=s3.list_buckets()
#print(response)
buckets = [bucket['Name'] for bucket in response['Buckets']]
print("Buckets Name: %s" % buckets)
filename = 'Office.png'
bucket_name='dereban.test'
s3.upload_file(filename,bucket_name,filename)