#!/usr/bin/bash
KEY_PAIR_NAME='AWSClassDemo'
AMI_ID='ami-0f19d220602031aed'
INSTANCE_TYPE='t3.micro'
SECURITY_GROUP='sg-020a716b47696a32f'

aws ec2 run-instances \
    --image-id $AMI_ID \
    --count 1 \
    --instance-type $INSTANCE_TYPE \
    --key-name $KEY_PAIR_NAME \
    --security-group-ids $SECURITY_GROUP \
    --user-data file://http-bin-userdata-example.sh \
    --tag-specifications 'ResourceType=instance,Tags=[{Key=Name,Value="CLI Class Demo"}]'