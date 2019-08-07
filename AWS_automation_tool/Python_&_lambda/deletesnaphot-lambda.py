import boto3
from datetime import datetime, timedelta

ec2 = boto3.client('ec2',region_name='ap-southeast-1')

# account owner snapshot
account_ids = ['845286826995']

def lambda_handler(event, context):
    days =457  # don't change date
    delete_time = datetime.strftime(datetime.utcnow() - timedelta(days=days),'%Y-%m-%dT%H:%M:%S.000Z')
    print 'Delete Snapshots Run Before %s' % delete_time

    print 'Deleting any snapshots older than {days} days'.format(days=days)

    #Pagination Size, Max is 1000
    MaxPageResults = 1000
    MinuteInSeconds = 60
    UnitConversionMultipler = 1000

    # Maximum execution of lambda is 5 minutes
    # We want our lambda function to stop when 
    # the execution time is greater than 4.5 minutes
    MaxExecutionTime = 5 * MinuteInSeconds * UnitConversionMultipler
    OurCodeExecutionTime = 4.5 * MinuteInSeconds * UnitConversionMultipler

    snapshot_response = ec2.describe_snapshots(OwnerIds=account_ids, MaxResults=MaxPageResults)

    #Infinite Loop
    while True :

        deletion_counter = 0
        size_counter = 0

        # delete variable should be moved
        # immediately after the for loop below because, 
        # each snapshot will have its own tags and this 
        # should be checked for each snapshot
        delete =True

        for snapshot in snapshot_response['Snapshots']:
            if 'Tags' in snapshot:
                for tag in snapshot['Tags']:
                    if (tag['Key'] == 'DoNotDelete') and (tag['Value'].lower() == 'yes'):
                        delete = False
            start_time = datetime.strftime(snapshot['StartTime'],'%Y-%m-%dT%H:%M:%S.000Z')
            if "ami-" not in snapshot['Description']: 
                if (start_time < delete_time) and (delete == True ):
                    print 'Deleting {id}'.format(id=snapshot['SnapshotId'])
                    deletion_counter = deletion_counter + 1
                    size_counter = size_counter + snapshot['VolumeSize']
                    try:
                        ec2.delete_snapshot(SnapshotId=snapshot['SnapshotId'])
                    except Exception, e:
                        print e

        # Currently this code prints deletion number and  size counter for every page
        print 'Deleted {number} snapshots totalling {size} GB'.format(
            number=deletion_counter,
            size=size_counter
        )

        # Break the loop and End the script if processing time in lambda 
        # has reached greater or equal to 4.5 minutes (MaxExecutionTime)
        if context.get_remaining_time_in_millis <= (MaxExecutionTime-OurCodeExecutionTime):
            print 'Our Execution time completed'
            break

        # Break the loop and End the script if there is next page of snapshots
        if 'NextToken' not in snapshot_response or snapshot_response['NextToken'] is None or snapshot_response['NextToken'] == '':
            print 'No next page found'
            break

        #Fetch snapshot descriptions for next token
        snapshot_response = ec2.describe_snapshots(
                OwnerIds = account_ids, 
                MaxResults = MaxPageResults, 
                NextToken = snapshot_response['NextToken']
            )