
import argparse
import boto3
from tabulate import tabulate
from datetime import datetime

def get_orphaned_volumes(ec2, region):
    try:
        volumes = ec2.describe_volumes(
            Filters=[{'Name': 'status', 'Values': ['available']}]
        )['Volumes']
        orphaned_volumes = []
        for volume in volumes:
            if not volume['Attachments']:
                orphaned_volumes.append({
                    'VolumeId': volume['VolumeId'],
                    'Size': volume['Size'],
                    'VolumeType': volume['VolumeType'],
                    'Cost': volume['Size'] * 0.10,
                    'Created': volume['CreateTime']
                })
        return orphaned_volumes
    except Exception as e:
        print(f"Error: {e}")
        return []

def delete_volume(ec2, volume_id):
    try:
        ec2.delete_volume(VolumeId=volume_id)
        print(f"Volume {volume_id} deleted successfully")
    except Exception as e:
        print(f"Error: {e}")

def main():
    parser = argparse.ArgumentParser(description='The Cloud Waste Reaper')
    parser.add_argument('--scan', action='store_true', help='Scan for orphaned EBS volumes')
    parser.add_argument('--region', default='ap-south-1', help='AWS region')
    parser.add_argument('--delete', help='Delete a specific EBS volume')
    parser.add_argument('--delete-all', action='store_true', help='Delete all orphaned EBS volumes')
    args = parser.parse_args()

    ec2 = boto3.client('ec2', region_name=args.region)

    if args.scan:
        orphaned_volumes = get_orphaned_volumes(ec2, args.region)
        if orphaned_volumes:
            table = [[volume['VolumeId'], volume['Size'], volume['VolumeType'], f"${volume['Cost']:.2f}", volume['Created']] for volume in orphaned_volumes]
            print(tabulate(table, headers=['Volume ID', 'Size(GB)', 'Type', 'Cost($)', 'Created'], tablefmt='grid'))
            total_cost = sum(volume['Cost'] for volume in orphaned_volumes)
            print(f"\033[1m\033[91mTOTAL WASTED CASH: ${total_cost:.2f}\033[0m")
        else:
            print("No orphaned EBS volumes found")

    if args.delete:
        delete_volume(ec2, args.delete)

    if args.delete_all:
        orphaned_volumes = get_orphaned_volumes(ec2, args.region)
        for volume in orphaned_volumes:
            delete_volume(ec2, volume['VolumeId'])

if __name__ == '__main__':
    main()
