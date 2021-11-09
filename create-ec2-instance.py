#!/usr/bin/env python3

import boto3

AWS_REGION = "us-east-2"
EC2_RESOURCE = boto3.resource('ec2', region_name=AWS_REGION)
KEY_PAIR_NAME = 'AWSClassDemo'
AMI_ID = 'ami-0f19d220602031aed' # Amazon Linux 2 - HVM - SSD - x86_64
SECURITY_GROUP = 'sg-020a716b47696a32f'

# more info on create_instances: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.ServiceResource.create_instances
instances = EC2_RESOURCE.create_instances(
    MinCount = 1,
    MaxCount = 1,
    ImageId=AMI_ID,
    InstanceType='t3.micro',  # x86_64
    KeyName=KEY_PAIR_NAME,
    UserData=open('http-bin-userdata-example.sh', 'r').read(),
    SecurityGroupIds=[SECURITY_GROUP],
    TagSpecifications=[
        {
            'ResourceType': 'instance',
            'Tags': [
                {
                    'Key': 'Name',
                    'Value': 'SDK Class Demo'
                },
            ]
        },
    ]
)

for instance in instances:
    print(f'EC2 instance "{instance.id}" has been launched')
    
    instance.wait_until_running()
    print(f'EC2 instance "{instance.id}" has been started')