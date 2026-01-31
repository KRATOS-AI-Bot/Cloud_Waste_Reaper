# The Cloud Waste Reaper

The Cloud Waste Reaper is a Python CLI tool designed to detect and manage cloud waste, specifically orphaned EBS volumes in AWS. This tool uses the boto3 library to interact with AWS services and the tabulate library to print clean tables.

## Installation

To use the Cloud Waste Reaper, you will need to install the required libraries. You can do this by running the following command:

pip install -r requirements.txt

## Usage

The Cloud Waste Reaper can be used to scan for unused EBS volumes, calculate potential savings, and delete unused volumes. The following flags are available:

* --scan: List all unused EBS volumes
* --region: Specify the AWS region to scan (default: ap-south-1)
* --delete <id_of_ebs_vol>: Delete a specific unused EBS volume
* --delete-all: Delete all unused EBS volumes

Example usage:

python reaper.py --scan --region ap-south-1
python reaper.py --delete vol-12345678 --region ap-south-1
python reaper.py --delete-all --region ap-south-1

## Requirements

* Python 3.7+
* boto3
* tabulate
* argparse

## Notes

* The Cloud Waste Reaper assumes that the cost of an EBS volume is $0.10 per GB/month.
* The tool uses the AWS CLI credentials to authenticate with AWS services.
* The tool will only delete EBS volumes that are in the 'available' state and are not attached to any EC2 instance.