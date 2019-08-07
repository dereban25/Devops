import boto3

def lambda_handler(event, context):

    # Extract Instance ID from event
    instance_id = event['detail']['instance-id']

    # Obtain information about the instance
    ec2_client = boto3.client('ec2')
    instance_info = ec2_client.describe_instances(InstanceIds=[instance_id])
    instance = instance_info['Reservations'][0]['Instances'][0]

    # Extract name tag
    name_tags = [t['Value'] for t in instance['Tags'] if t['Key']=='Name']
    name = name_tags[0] if name_tags is not None else ''

    # Send message to SNS
    MY_SNS_TOPIC_ARN = 'arn:aws:sns:us-east-1:803440774993:critical'
    sns_client = boto3.client('sns')
    sns_client.publish(
        TopicArn = MY_SNS_TOPIC_ARN,
        Subject = 'Instance Change State: ' + instance_id,
        Message = 'Instance: ' + instance_id + ' has changed state\n' +
                  'State: ' + instance['State']['Name'] + '\n' +
                  'IP Address: ' + instance['PublicIpAddress'] + '\n' +
                  'Name: ' + name)