# The Cloud Waste Reaper [Built by K.R.A.T.O.S]

## Table of Contents
1. [Introduction](#introduction)
2. [Getting Started](#getting-started)
3. [Usage](#usage)
4. [Flags](#flags)
5. [Examples](#examples)
6. [Error Handling](#error-handling)
7. [Lambda Deployment](#lambda-deployment)
8. [Event Bridge Setup](#event-bridge-setup)
9. [SES Email Setup](#ses-email-setup)

## Introduction
The Cloud Waste Reaper is a Python CLI tool designed to detect and manage cloud waste in AWS. It uses the boto3 library to interact with AWS services and provides a range of flags for scanning and deleting unused resources.

## Getting Started
To get started with the Cloud Waste Reaper, follow these steps:
1. Install the required dependencies by running `pip install -r requirements.txt`
2. Configure your AWS credentials by running `aws configure`
3. Run the Cloud Waste Reaper using the command `python reaper.py`

## Usage
The Cloud Waste Reaper can be used to scan and delete unused resources in AWS. The following flags are available:
* `--scan-ebs`: List all EBS volumes in the specified region
* `--delete-ebs <id_of_ebs_vol>`: Delete an EBS volume by ID
* `--delete-all-ebs`: Delete all unused EBS volumes
* `--scan-ec2`: List all EC2 instances in the specified region
* `--delete-ec2 <id_of_ec2>`: Delete an EC2 instance by ID
* `--delete-all-ec2`: Delete all EC2 instances
* `--scan-s3`: List all S3 buckets in the specified region
* `--delete-s3 <id_of_s3>`: Delete an S3 bucket by ID
* `--scan-dynamo`: List all DynamoDB tables in the specified region
* `--delete-dynamo <id_of_dynamo>`: Delete a DynamoDB table by ID
* `--delete-all-dynamo`: Delete all DynamoDB tables
* `--scan-all`: List all resources in the specified region
* `--region`: Specify the AWS region to use (default: ap-south-1)

## Flags
The following flags are available:
* `--scan-ebs`
* `--delete-ebs <id_of_ebs_vol>`
* `--delete-all-ebs`
* `--scan-ec2`
* `--delete-ec2 <id_of_ec2>`
* `--delete-all-ec2`
* `--scan-s3`
* `--delete-s3 <id_of_s3>`
* `--scan-dynamo`
* `--delete-dynamo <id_of_dynamo>`
* `--delete-all-dynamo`
* `--scan-all`
* `--region`

## Examples
* `python reaper.py --scan-ebs --region us-west-2`
* `python reaper.py --delete-ebs vol-12345678 --region us-west-2`
* `python reaper.py --delete-all-ebs --region us-west-2`
* `python reaper.py --scan-ec2 --region us-west-2`
* `python reaper.py --delete-ec2 i-12345678 --region us-west-2`
* `python reaper.py --delete-all-ec2 --region us-west-2`
* `python reaper.py --scan-s3 --region us-west-2`
* `python reaper.py --delete-s3 my-bucket --region us-west-2`
* `python reaper.py --scan-dynamo --region us-west-2`
* `python reaper.py --delete-dynamo my-table --region us-west-2`
* `python reaper.py --delete-all-dynamo --region us-west-2`
* `python reaper.py --scan-all --region us-west-2`

## Error Handling
The Cloud Waste Reaper uses try/except blocks to handle errors. If an error occurs, the tool will print an error message and exit.

## Lambda Deployment
To deploy the Cloud Waste Reaper to AWS Lambda, follow these steps:
1. Create a new Lambda function
2. Set the runtime to Python 3.8
3. Set the handler to `reaper.py`
4. Set the environment variables to include your AWS credentials
5. Deploy the function

## Event Bridge Setup
To set up Event Bridge to trigger the Cloud Waste Reaper, follow these steps:
1. Create a new Event Bridge rule
2. Set the event pattern to trigger on a schedule (e.g. every Monday at 9:00am)
3. Set the target to the Lambda function
4. Deploy the rule

## SES Email Setup
To set up SES to send emails from the Cloud Waste Reaper, follow these steps:
1. Create a new SES email identity
2. Verify the email address
3. Set up an SES email template
4. Update the Cloud Waste Reaper to use the SES email template