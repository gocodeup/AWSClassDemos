#!/bin/bash
yum update -y
yum install httpd -y
service httpd start
chkconfig httpd on
echo "<html><h1>Hello from `curl http://169.254.169.254/latest/meta-data/instance-id`</h1></html>" > /var/www/html/index.html