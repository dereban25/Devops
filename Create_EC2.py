

import boto3

#1.Create One EC2 INSTANCES
ec2 = boto3.resource('ec2',
                     aws_access_key_id = 'insert access key',
                     aws_secret_access_key = 'insert secret key',
                     region_name = 'us-east-1')

ec2.create_instances(

    ImageId='ami-b70554c8',
    MinCount=1,
    MaxCount=1)


instances = ec2.instances.filter(
    Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])
for instance in instances:
    print(instance.id, instance.instance_type)

    snapshot = ec2.create_snapshot(VolumeId='vol-09957c91e20572e43', Size=1, Description='Maksym')
    volume = ec2.create_volume(SnapshotId=snapshot.id, VolumeSize=1, VolumeType='magnetic', AvailabilityZone='us-east-1e')
    ec2.Instance('i-050aca272b384add6').attach_volume(VolumeId=volume.id, Device='/dev/sdy')
    snapshot.delete()

