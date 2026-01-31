The Cloud Waste Reaper
======================
# Introduction
The Cloud Waste Reaper is a Python CLI tool designed to detect and report on orphaned EBS volumes in AWS, helping you identify and eliminate cloud waste.

# Requirements
- Python 3.7+
- boto3
- tabulate
- argparse

# Installation
pip install -r requirements.txt

# Usage
python reaper.py --scan --region ap-south-1

# Options
- --scan        Scan for orphaned EBS volumes
- --dry-run     Dry run, do not delete volumes
- --region      Specify AWS region (default: ap-south-1)

# Example Output
The tool will print a table with the following columns:
- Volume ID
- Size (GB)
- Type
- Cost ($)
- Region
- Created

Followed by the total wasted cash.

# Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.