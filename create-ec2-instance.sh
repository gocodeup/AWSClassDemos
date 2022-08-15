#!/usr/bin/env bash

KEY_PAIR_NAME="CLIClassDemo-`openssl rand -hex 4`"
KEY_PAIR=$(aws ec2 create-key-pair --key-name $KEY_PAIR_NAME)
AMI_ID=$(aws ssm get-parameters --names /aws/service/ami-amazon-linux-latest/amzn2-ami-hvm-x86_64-gp2 --query 'Parameters[0].[Value]' --output text)
INSTANCE_TYPE='t3.micro'
SECURITY_GROUP_NAME="CLIClassDemo-`openssl rand -hex 4`"
SECURITY_GROUP_ID=$(aws ec2 create-security-group --group-name $SECURITY_GROUP_NAME --description "CLI Class Demo" --output text --query 'GroupId')
INGRESS80=$(aws ec2 authorize-security-group-ingress --group-id $SECURITY_GROUP_ID --protocol tcp --port 80 --cidr 0.0.0.0/0)
INGRESS22=$(aws ec2 authorize-security-group-ingress --group-id $SECURITY_GROUP_ID --protocol tcp --port 22 --cidr 0.0.0.0/0)

INSTANCE_ID=$(aws ec2 run-instances \
    --image-id $AMI_ID \
    --count 1 \
    --instance-type $INSTANCE_TYPE \
    --key-name $KEY_PAIR_NAME \
    --security-group-ids $SECURITY_GROUP_ID \
    --user-data file://http-bin-userdata-example.sh \
    --tag-specifications 'ResourceType=instance,Tags=[{Key=Name,Value="CLI Class Demo"}]' \
    --output text \
    --query 'Instances[0].[InstanceId]')
echo "Created instance with id $INSTANCE_ID"
echo "Press enter to delete the newly created resources"
read PRESS_ENTER
aws ec2 delete-key-pair --key-name $KEY_PAIR_NAME --output text --no-cli-pager
aws ec2 terminate-instances --instance-ids $INSTANCE_ID --output text --no-cli-pager
echo "Waiting for instance to terminate"
aws ec2 wait instance-terminated --instance-ids $INSTANCE_ID --output text --no-cli-pager
aws ec2 delete-security-group --group-id $SECURITY_GROUP_ID --output text --no-cli-pager
