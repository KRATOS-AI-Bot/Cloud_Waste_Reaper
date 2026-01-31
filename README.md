
# README.md
The Cloud Waste Reaper [Built by K.R.A.T.O.S]
==============================================

Introduction
------------

The Cloud Waste Reaper is a Python CLI tool designed to detect cloud waste in AWS. It scans for unused resources such as EBS volumes, EC2 instances, S3 buckets, DynamoDB tables, ELB, and EIP, and provides a detailed report on potential cost savings.

Usage
-----

To run the Cloud Waste Reaper, follow these steps:

1. Install the required dependencies by running `pip install -r requirements.txt`
2. Configure your AWS credentials by setting the `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` environment variables
3. Run the tool using the command `python reaper.py --scan-all`

Flags
-----

The following flags are available:

* `--scan-all`: Scan all resources (EBS, EC2, S3, DynamoDB, ELB, EIP)
* `--scan-ebs`: Scan only EBS volumes
* `--scan-ec2`: Scan only EC2 instances
* `--scan-s3`: Scan only S3 buckets
* `--scan-dynamodb`: Scan only DynamoDB tables
* `--scan-elb`: Scan only ELB
* `--scan-eip`: Scan only EIP

Lambda Configuration
-------------------

To run the Cloud Waste Reaper inside a Lambda function, follow these steps:

1. Create a new Lambda function with the name `kratos-lambda`
2. Set the runtime to Python 3.8
3. Set the handler to `reaper.lambda_handler`
4. Set the environment variables `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY`
5. Configure the event trigger to run every Monday at 9:00am using Event Bridge

SES Configuration
----------------

To send email reports using SES, follow these steps:

1. Configure your SES credentials by setting the `SES_RECIPIENT` environment variable
2. Set up an SES email client using the `boto3` library

Requirements
------------

* Python 3.8
* `boto3` library
* `tabulate` library

