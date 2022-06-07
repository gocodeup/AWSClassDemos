#!/usr/bin/env python3
'''Delete any Security Groups in the account+region that aren't currently being used'''


import boto3
from botocore.exceptions import ClientError

AWS_REGION = "us-east-2"
# Create EC2 resource
ec2 = boto3.resource('ec2', region_name=AWS_REGION)

for sg in ec2.security_groups.all():
    # Delete security group
    try:
        sg.delete()
        print(f'Security Group {sg.id} deleted')
    except ClientError as error:
        if not error.response['Error']['Code'] in ['DependencyViolation', 'CannotDelete']:
            print('unexpected error during delete')
            raise error
        else:
            # the SG is in use
            print(f'Security Group {sg.id} NOT deleted')