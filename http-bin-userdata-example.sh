#!/bin/bash
yum update -y
yum install python3 -y
amazon-linux-extras install docker -y
service docker start
chkconfig docker on
docker pull kennethreitz/httpbin
docker run -d -p 80:80 kennethreitz/httpbin