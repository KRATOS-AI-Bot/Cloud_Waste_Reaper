
# README.md
The Cloud Waste Reaper [Built by K.R.A.T.O.S]

This is a Python CLI tool designed to detect cloud waste in AWS. It scans for unattached EBS volumes, EC2 instances, S3 buckets, DynamoDB tables, ELB, and EIP.

## Requirements
- Python 3.8+
- boto3
- tabulate

## Installation
1. Clone the repository
2. Install the required packages: `pip install -r requirements.txt`
3. Configure your AWS credentials

## Usage
- Run the script using `python reaper.py --scan-all` to scan all resources
- Use the `--help` flag to see available options

## Deployment
- Deploy the script as a Lambda function
- Configure the Lambda function to run every Monday at 9:00am using Event Bridge
- Set up SES to send email notifications
