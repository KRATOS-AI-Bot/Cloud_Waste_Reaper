
import argparse
import boto3
import json
import urllib.request
import urllib.parse
from tabulate import tabulate
from datetime import datetime

def get_ebs_volumes(ec2, region):
    ebs_volumes = ec2.describe_volumes(
        Filters=[{'Name': 'status', 'Values': ['available']}]
    )['Volumes']
    return ebs_volumes

def calculate_ebs_cost(ebs_volumes):
    total_cost = 0
    ebs_data = []
    for volume in ebs_volumes:
        size = volume['Size']
        cost = size * 0.10
        total_cost += cost
        ebs_data.append([volume['VolumeId'], size, volume['VolumeType'], cost, volume['CreateTime']])
    return ebs_data, total_cost

def get_ec2_instances(ec2, region):
    ec2_instances = ec2.describe_instances(
        Filters=[{'Name': 'instance-state-name', 'Values': ['running', 'stopped', 'pending', 'shutting-down', 'stopping', 'stopped']}]
    )['Reservations']
    return ec2_instances

def get_s3_buckets(s3, region):
    s3_buckets = s3.list_buckets()
    return s3_buckets['Buckets']

def get_dynamodb_tables(dynamodb, region):
    dynamodb_tables = dynamodb.list_tables()
    return dynamodb_tables['TableNames']

def delete_ebs_volume(ec2, volume_id):
    ec2.delete_volume(VolumeId=volume_id)

def delete_ec2_instance(ec2, instance_id):
    ec2.terminate_instances(InstanceIds=[instance_id])

def delete_s3_bucket(s3, bucket_name):
    s3.delete_bucket(Bucket=bucket_name)

def delete_dynamodb_table(dynamodb, table_name):
    dynamodb.delete_table(TableName=table_name)

def send_email(ses, to, subject, body):
    ses.send_email(
        Source='dakshsawhney2@gmail.com',
        Destination={'ToAddresses': [to]},
        Message={
            'Subject': {'Data': subject},
            'Body': {'Text': {'Data': body}}
        }
    )

def main():
    parser = argparse.ArgumentParser(description='Cloud Waste Reaper')
    parser.add_argument('--scan-ebs', action='store_true', help='Scan for unused EBS volumes')
    parser.add_argument('--delete-ebs', help='Delete EBS volume by ID')
    parser.add_argument('--delete-all-ebs', action='store_true', help='Delete all unused EBS volumes')
    parser.add_argument('--scan-ec2', action='store_true', help='Scan for EC2 instances')
    parser.add_argument('--delete-ec2', help='Delete EC2 instance by ID')
    parser.add_argument('--delete-all-ec2', action='store_true', help='Delete all EC2 instances')
    parser.add_argument('--scan-s3', action='store_true', help='Scan for S3 buckets')
    parser.add_argument('--delete-s3', help='Delete S3 bucket by name')
    parser.add_argument('--scan-dynamo', action='store_true', help='Scan for DynamoDB tables')
    parser.add_argument('--delete-dynamo', help='Delete DynamoDB table by name')
    parser.add_argument('--delete-all-dynamo', action='store_true', help='Delete all DynamoDB tables')
    parser.add_argument('--scan-all', action='store_true', help='Scan for all resources')
    parser.add_argument('--region', default='ap-south-1', help='AWS region')
    args = parser.parse_args()

    ec2 = boto3.client('ec2', region_name=args.region)
    s3 = boto3.client('s3', region_name=args.region)
    dynamodb = boto3.client('dynamodb', region_name=args.region)
    ses = boto3.client('ses', region_name=args.region)

    if args.scan_ebs:
        ebs_volumes = get_ebs_volumes(ec2, args.region)
        ebs_data, total_cost = calculate_ebs_cost(ebs_volumes)
        print(tabulate(ebs_data, headers=['ID', 'Size(GB)', 'Type', 'Cost($)', 'Created'], tablefmt='grid'))
        print(f'\033[1m\033[91mTOTAL WASTED CASH: ${total_cost:.2f}\033[0m')

    if args.delete_ebs:
        delete_ebs_volume(ec2, args.delete_ebs)

    if args.delete_all_ebs:
        ebs_volumes = get_ebs_volumes(ec2, args.region)
        for volume in ebs_volumes:
            delete_ebs_volume(ec2, volume['VolumeId'])

    if args.scan_ec2:
        ec2_instances = get_ec2_instances(ec2, args.region)
        for instance in ec2_instances:
            print(instance['Instances'][0]['InstanceId'])

    if args.delete_ec2:
        delete_ec2_instance(ec2, args.delete_ec2)

    if args.delete_all_ec2:
        ec2_instances = get_ec2_instances(ec2, args.region)
        for instance in ec2_instances:
            delete_ec2_instance(ec2, instance['Instances'][0]['InstanceId'])

    if args.scan_s3:
        s3_buckets = get_s3_buckets(s3, args.region)
        for bucket in s3_buckets:
            print(bucket['Name'])

    if args.delete_s3:
        delete_s3_bucket(s3, args.delete_s3)

    if args.scan_dynamo:
        dynamodb_tables = get_dynamodb_tables(dynamodb, args.region)
        for table in dynamodb_tables:
            print(table)

    if args.delete_dynamo:
        delete_dynamodb_table(dynamodb, args.delete_dynamo)

    if args.delete_all_dynamo:
        dynamodb_tables = get_dynamodb_tables(dynamodb, args.region)
        for table in dynamodb_tables:
            delete_dynamodb_table(dynamodb, table)

    if args.scan_all:
        ebs_volumes = get_ebs_volumes(ec2, args.region)
        ec2_instances = get_ec2_instances(ec2, args.region)
        s3_buckets = get_s3_buckets(s3, args.region)
        dynamodb_tables = get_dynamodb_tables(dynamodb, args.region)
        data = {
            'EBS Volumes': ebs_volumes,
            'EC2 Instances': ec2_instances,
            'S3 Buckets': s3_buckets,
            'DynamoDB Tables': dynamodb_tables
        }
        print(json.dumps(data, indent=4))
        send_email(ses, 'dakshsawhney2@gmail.com', 'Cloud Waste Reaper Scan', json.dumps(data, indent=4))

if __name__ == '__main__':
    main()
