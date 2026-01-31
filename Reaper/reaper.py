
import boto3
import argparse
from tabulate import tabulate
from datetime import datetime

def get_orphaned_volumes(ec2):
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
    table_data = []
    for volume in volumes:
        size = volume['Size']
        volume_id = volume['VolumeId']
        volume_type = volume['VolumeType']
        created = volume['CreateTime'].strftime('%Y-%m-%d %H:%M:%S')
        cost = size * 0.10
        total_savings += cost
        table_data.append([volume_id, size, volume_type, f"${cost:.2f}", 'ap-south-1', created])
    return table_data, total_savings

def main():
    parser = argparse.ArgumentParser(description='Cloud Waste Reaper')
    parser.add_argument('--scan', action='store_true', help='Scan for orphaned EBS volumes')
    parser.add_argument('--dry-run', action='store_true', help='Dry run, do not calculate savings')
    args = parser.parse_args()

    if args.scan:
        ec2 = boto3.client('ec2', region_name='ap-south-1')
        volumes = get_orphaned_volumes(ec2)
        table_data, total_savings = calculate_savings(volumes)
        print(tabulate(table_data, headers=['Volume ID', 'Size(GB)', 'Type', 'Cost($)', 'Region', 'Created'], tablefmt='grid'))
        if not args.dry_run:
            print(f"\033[1m\033[91mTOTAL WASTED CASH: ${total_savings:.2f}\033[0m")

if __name__ == '__main__':
    main()
