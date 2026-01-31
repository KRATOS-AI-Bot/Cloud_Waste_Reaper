
import boto3
import argparse
from tabulate import tabulate
from datetime import datetime

def get_orphaned_volumes(ec2):
    volumes = ec2.describe_volumes(
        Filters=[{'Name': 'status', 'Values': ['available']}]
    )['Volumes']
    return [volume for volume in volumes if not volume['Attachments']]

def calculate_savings(volumes):
    total_savings = 0
    table = []
    for volume in volumes:
        size = volume['Size']
        volume_type = volume['VolumeType']
        cost = size * 0.10
        total_savings += cost
        table.append([
            volume['VolumeId'],
            size,
            volume_type,
            round(cost, 2),
            volume['AvailabilityZone'],
            volume['CreateTime'].strftime('%Y-%m-%d %H:%M:%S')
        ])
    return table, total_savings

def main():
    parser = argparse.ArgumentParser(description='Cloud Waste Reaper')
    parser.add_argument('--scan', action='store_true', help='Scan for orphaned EBS volumes')
    parser.add_argument('--dry-run', action='store_true', help='Dry run, do not delete volumes')
    args = parser.parse_args()

    if args.scan:
        ec2 = boto3.client('ec2', region_name='ap-south-1')
        try:
            volumes = get_orphaned_volumes(ec2)
            table, total_savings = calculate_savings(volumes)
            print(tabulate(table, headers=['Volume ID', 'Size(GB)', 'Type', 'Cost($)', 'Region', 'Created'], tablefmt='grid'))
            print(f'\033[1m\033[91mTOTAL WASTED CASH: ${round(total_savings, 2)}\033[0m')
        except Exception as e:
            print(f'Error: {str(e)}')

if __name__ == '__main__':
    main()
