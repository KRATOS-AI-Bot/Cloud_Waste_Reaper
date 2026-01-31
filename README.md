python
import boto3
import argparse
from tabulate import tabulate
from datetime import datetime

def get_ebs_volumes(ec2):
    try:
        volumes = ec2.describe_volumes(
            Filters=[{'Name': 'status', 'Values': ['available']}]
        )['Volumes']
        return volumes
    except Exception as e:
        print(f"Error: {e}")
        return []

def calculate_savings(volumes):
    total_savings = 0
    table = []
    for volume in volumes:
        size = volume['Size']
        volume_id = volume['VolumeId']
        volume_type = volume['VolumeType']
        created = volume['CreateTime']
        cost = size * 0.10
        total_savings += cost
        table.append([volume_id, size, volume_type, round(cost, 2), 'ap-south-1', created])
    return table, total_savings

def print_table(table, total_savings):
    print(tabulate(table, headers=['Volume ID', 'Size(GB)', 'Type', 'Cost($)', 'Region', 'Created'], tablefmt='grid'))
    print(f"\033[1m\033[91mTOTAL WASTED CASH: ${round(total_savings, 2)}\033[0m")

def main():
    parser = argparse.ArgumentParser(description='Cloud Waste Reaper')
    parser.add_argument('--scan', action='store_true', help='Scan for orphaned EBS volumes')
    parser.add_argument('--dry-run', action='store_true', help='Dry run, do not print table')
    args = parser.parse_args()
    ec2 = boto3.client('ec2', region_name='ap-south-1')
    volumes = get_ebs_volumes(ec2)
    table, total_savings = calculate_savings(volumes)
    if not args.dry_run:
        print_table(table, total_savings)

if __name__ == '__main__':
    main()
