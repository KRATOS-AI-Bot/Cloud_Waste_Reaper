
# README.md
The Cloud Waste Reaper [Built by K.R.A.T.O.S]

Table of Contents
=================
1. [Introduction](#introduction)
2. [Getting Started](#getting-started)
3. [Usage](#usage)
4. [Flags](#flags)
5. [Lambda Setup](#lambda-setup)
6. [Event Bridge Setup](#event-bridge-setup)
7. [SES Setup](#ses-setup)

## Introduction
The Cloud Waste Reaper is a Python CLI tool designed to detect cloud waste in AWS. It scans for unused resources such as EBS volumes, EC2 instances, S3 buckets, and DynamoDB tables, and provides a report of potential savings.

## Getting Started
To get started, clone the repository and install the required dependencies using pip:
bash
pip install -r requirements.txt

## Usage
To run the Cloud Waste Reaper, use the following command:
bash
python reaper.py --help

This will display the available flags and options.

## Flags
The following flags are available:
* `--scan-ebs`: Scan for unused EBS volumes
* `--delete-ebs <id_of_ebs_vol>`: Delete a specific EBS volume
* `--delete-all-ebs`: Delete all unused EBS volumes
* `--scan-ec2`: Scan for all EC2 instances
* `--delete-ec2 <id_of_ec2>`: Delete a specific EC2 instance
* `--delete-all-ec2`: Delete all EC2 instances
* `--scan-s3`: Scan for all S3 buckets
* `--delete-s3 <id_of_s3>`: Delete a specific S3 bucket
* `--scan-dynamo`: Scan for all DynamoDB tables
* `--delete-dynamo <id_of_dynamo>`: Delete a specific DynamoDB table
* `--delete-all-dynamo`: Delete all DynamoDB tables
* `--scan-all`: Scan for all resources in the specified region
* `--region`: Specify the AWS region (default: ap-south-1)

## Lambda Setup
To run the Cloud Waste Reaper in a Lambda function, create a new Lambda function with the following settings:
* Runtime: Python 3.8
* Handler: reaper.lambda_handler
* Environment variables:
	+ SES_RECIPIENT: dakshsawhney2@gmail.com
* Role: Attach the necessary permissions to the Lambda function

## Event Bridge Setup
To schedule the Lambda function to run every Monday at 9:00am, create a new Event Bridge rule with the following settings:
* Event pattern: Schedule
* Schedule: cron(0 9 ? * MON *)
* Target: Lambda function

## SES Setup
To send emails using SES, create a new SES configuration set with the following settings:
* Configuration set name: CloudWasteReaper
* Email address: dakshsawhney2@gmail.com
