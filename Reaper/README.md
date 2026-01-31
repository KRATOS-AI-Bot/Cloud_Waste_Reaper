
import boto3
import argparse
from tabulate import tabulate
from datetime import datetime

def get_orphaned_volumes(ec2):
    volumes = ec2.describe_volumes(
        Filters=[{'Name': 'status', 'Values': ['available']}]
    )['Volumes']
    return [v for v in volumes if not v['Attachments']]

def calculate_savings(volumes):
    savings = 0
    table = []
    for v in volumes:
        size = v['Size']
        volume_type = v['VolumeType']
        cost = size * 0.10
        table.append([v['VolumeId'], size, volume_type, round(cost, 2), v['AvailabilityZone'], v['CreateTime'].strftime('%Y-%m-%d %H:%M:%S')])
        savings += cost
    return table, savings

def print_results(table, savings):
    print(tabulate(table, headers=['Volume ID', 'Size(GB)', 'Type', 'Cost($)', 'Region', 'Created'], tablefmt='grid'))
    print(f'\033[1m\033[91mTOTAL WASTED CASH: ${round(savings, 2)}\033[0m')

def main():
    parser = argparse.ArgumentParser(description='Cloud Waste Reaper')
    parser.add_argument('--scan', action='store_true', help='scan for orphaned volumes')
    parser.add_argument('--dry-run', action='store_true', help='dry run, do not print results')
    args = parser.parse_args()
    
    try:
        ec2 = boto3.client('ec2', region_name='ap-south-1')
        volumes = get_orphaned_volumes(ec2)
        table, savings = calculate_savings(volumes)
        if not args.dry_run:
            print_results(table, savings)
    except Exception as e:
        print(f'Error: {str(e)}')

if __name__ == '__main__':
    main()
