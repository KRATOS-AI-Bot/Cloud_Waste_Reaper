
import boto3
import argparse
import json
import urllib
import tabulate
from datetime import datetime

def get_ebs_volumes(ec2, region):
    ebs_volumes = ec2.describe_volumes(
        Filters=[{'Name': 'status', 'Values': ['available']}]
    )['Volumes']
    return ebs_volumes

def calculate_ebs_cost(ebs_volumes):
    total_cost = 0
    table = []
    for volume in ebs_volumes:
        size = volume['Size']
        cost = size * 0.10
        total_cost += cost
        table.append([volume['VolumeId'], size, volume['VolumeType'], cost, volume['CreateTime']])
    return table, total_cost

def get_ec2_instances(ec2, region):
    instances = ec2.describe_instances(
        Filters=[{'Name': 'instance-state-name', 'Values': ['running', 'stopped', 'pending', 'shutting-down', 'stopping', 'stopped']}]
    )['Reservations']
    return instances

def get_s3_buckets(s3, region):
    buckets = s3.list_buckets()
    return buckets['Buckets']

def get_dynamodb_tables(dynamodb, region):
    tables = dynamodb.list_tables()
    return tables['TableNames']

def delete_ebs_volume(ec2, volume_id):
    ec2.delete_volume(VolumeId=volume_id)

def delete_ec2_instance(ec2, instance_id):
    ec2.terminate_instances(InstanceIds=[instance_id])

def delete_s3_bucket(s3, bucket_name):
    s3.delete_bucket(Bucket=bucket_name)

def delete_dynamodb_table(dynamodb, table_name):
    dynamodb.delete_table(TableName=table_name)

def send_email(ses, message):
    ses.send_email(
        Source='dakshsawhney2@gmail.com',
        Destination={
            'ToAddresses': ['dakshsawhney2@gmail.com']
        },
        Message={
            'Body': {
                'Text': {
                    'Data': message
                }
            },
            'Subject': 'Cloud Waste Report'
        }
    )

def lambda_handler(event, context):
    parser = argparse.ArgumentParser()
    parser.add_argument('--scan-ebs', action='store_true')
    parser.add_argument('--delete-ebs', type=str)
    parser.add_argument('--delete-all-ebs', action='store_true')
    parser.add_argument('--scan-ec2', action='store_true')
    parser.add_argument('--delete-ec2', type=str)
    parser.add_argument('--delete-all-ec2', action='store_true')
    parser.add_argument('--scan-s3', action='store_true')
    parser.add_argument('--delete-s3', type=str)
    parser.add_argument('--scan-dynamo', action='store_true')
    parser.add_argument('--delete-dynamo', type=str)
    parser.add_argument('--delete-all-dynamo', action='store_true')
    parser.add_argument('--scan-all', action='store_true')
    parser.add_argument('--region', type=str, default='ap-south-1')
    args = parser.parse_args()

    ec2 = boto3.client('ec2', region_name=args.region)
    s3 = boto3.client('s3', region_name=args.region)
    dynamodb = boto3.client('dynamodb', region_name=args.region)
    ses = boto3.client('ses', region_name='us-east-1')

    if args.scan_ebs:
        ebs_volumes = get_ebs_volumes(ec2, args.region)
        table, total_cost = calculate_ebs_cost(ebs_volumes)
        print(tabulate.tabulate(table, headers=['ID', 'Size(GB)', 'Type', 'Cost($)', 'Created'], tablefmt='grid'))
        print(f'\033[1m\033[91mTOTAL WASTED CASH: ${total_cost:.2f}\033[0m')

    if args.delete_ebs:
        delete_ebs_volume(ec2, args.delete_ebs)

    if args.delete_all_ebs:
        ebs_volumes = get_ebs_volumes(ec2, args.region)
        for volume in ebs_volumes:
            delete_ebs_volume(ec2, volume['VolumeId'])

    if args.scan_ec2:
        instances = get_ec2_instances(ec2, args.region)
        for instance in instances:
            print(instance)

    if args.delete_ec2:
        delete_ec2_instance(ec2, args.delete_ec2)

    if args.delete_all_ec2:
        instances = get_ec2_instances(ec2, args.region)
        for instance in instances:
            delete_ec2_instance(ec2, instance[0]['InstanceId'])

    if args.scan_s3:
        buckets = get_s3_buckets(s3, args.region)
        for bucket in buckets:
            print(bucket)

    if args.delete_s3:
        delete_s3_bucket(s3, args.delete_s3)

    if args.scan_dynamo:
        tables = get_dynamodb_tables(dynamodb, args.region)
        for table in tables:
            print(table)

    if args.delete_dynamo:
        delete_dynamodb_table(dynamodb, args.delete_dynamo)

    if args.delete_all_dynamo:
        tables = get_dynamodb_tables(dynamodb, args.region)
        for table in tables:
            delete_dynamodb_table(dynamodb, table)

    if args.scan_all:
        ebs_volumes = get_ebs_volumes(ec2, args.region)
        instances = get_ec2_instances(ec2, args.region)
        buckets = get_s3_buckets(s3, args.region)
        tables = get_dynamodb_tables(dynamodb, args.region)
        data = {
            'ebs_volumes': ebs_volumes,
            'ec2_instances': instances,
            's3_buckets': buckets,
            'dynamodb_tables': tables
        }
        send_email(ses, json.dumps(data))

    return {
        'statusCode': 200,
        'statusMessage': 'OK'
    }
