#!/usr/bin/env python3

import boto3
import secrets

AWS_REGION = "us-east-1"
EC2_RESOURCE = boto3.resource('ec2', region_name=AWS_REGION)
SSM_CLIENT = boto3.client('ssm', region_name=AWS_REGION)
KEY_PAIR_NAME = f'SDKClassDemo-{secrets.token_hex(4)}'
KEY_PAIR = EC2_RESOURCE.create_key_pair(KeyName=KEY_PAIR_NAME, KeyType='ed25519', KeyFormat='pem')
AMI_ID = SSM_CLIENT.get_parameter(Name='/aws/service/ami-amazon-linux-latest/amzn2-ami-hvm-x86_64-gp2')['Parameter']['Value']
SECURITY_GROUP = EC2_RESOURCE.create_security_group(Description='SDK Class Demo', GroupName=f'SDKClassDemo-{secrets.token_hex(4)}')
SECURITY_GROUP.authorize_ingress(CidrIp='0.0.0.0/0', FromPort=80, IpProtocol='tcp', ToPort=80)
SECURITY_GROUP.authorize_ingress(CidrIp='0.0.0.0/0', FromPort=22, IpProtocol='tcp', ToPort=22)
SECURITY_GROUP_ID = SECURITY_GROUP.id

# more info on create_instances: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.ServiceResource.create_instances
instances = EC2_RESOURCE.create_instances(
    MinCount = 1,
    MaxCount = 1,
    ImageId=AMI_ID,
    InstanceType='t3.micro',  # x86_64
    KeyName=KEY_PAIR_NAME,
    UserData=open('http-bin-userdata-example.sh', 'r').read(),
    SecurityGroupIds=[SECURITY_GROUP_ID],
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
    
input('press enter to delete the newly created resources')
KEY_PAIR.delete()
for instance in instances:
    instance.terminate()
    print(f'Waiting for instance {instance.id} to terminate')
    instance.wait_until_terminated()
SECURITY_GROUP.delete()

