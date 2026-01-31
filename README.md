# The Cloud Waste Reaper [Built by K.R.A.T.O.S]

The Cloud Waste Reaper is a Python CLI tool designed to detect and manage cloud waste in AWS. It provides a simple and efficient way to scan for unused resources, calculate potential savings, and delete unnecessary resources.

## Installation

To install the Cloud Waste Reaper, run the following command:
bash
pip install -r requirements.txt

## Usage

To use the Cloud Waste Reaper, run the following command:
bash
python reaper.py --help

This will display the available options and flags.

## Flags

The following flags are available:

* `--scan-ebs`: List all EBS volumes in the specified region.
* `--delete-ebs <id_of_ebs_vol>`: Delete the specified EBS volume.
* `--delete-all-ebs`: Delete all unused EBS volumes.
* `--scan-ec2`: List all EC2 instances in the specified region.
* `--delete-ec2 <id_of_ec2>`: Delete the specified EC2 instance.
* `--delete-all-ec2`: Delete all EC2 instances.
* `--scan-s3`: List all S3 buckets in the specified region.
* `--delete-s3 <id_of_s3>`: Delete the specified S3 bucket.
* `--scan-dynamo`: List all DynamoDB tables in the specified region.
* `--delete-dynamo <id_of_dynamo>`: Delete the specified DynamoDB table.
* `--delete-all-dynamo`: Delete all DynamoDB tables.
* `--scan-all`: List all resources in the specified region.
* `--region`: Specify the AWS region (default: ap-south-1).

## Examples

* Scan all EBS volumes in the ap-south-1 region:
bash
python reaper.py --scan-ebs --region ap-south-1

* Delete all unused EBS volumes in the ap-south-1 region:
bash
python reaper.py --delete-all-ebs --region ap-south-1

* Scan all EC2 instances in the ap-south-1 region:
bash
python reaper.py --scan-ec2 --region ap-south-1

* Delete the specified EC2 instance:
bash
python reaper.py --delete-ec2 i-0123456789abcdef0 --region ap-south-1

* Scan all S3 buckets in the ap-south-1 region:
bash
python reaper.py --scan-s3 --region ap-south-1

* Delete the specified S3 bucket:
bash
python reaper.py --delete-s3 my-bucket --region ap-south-1

* Scan all DynamoDB tables in the ap-south-1 region:
bash
python reaper.py --scan-dynamo --region ap-south-1

* Delete the specified DynamoDB table:
bash
python reaper.py --delete-dynamo my-table --region ap-south-1
