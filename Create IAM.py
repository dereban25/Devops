

import boto3

iam = boto3.client('iam')

#Create user

response = iam.create_user(
    UserName='Dereban-test-user'
)

print(response)

