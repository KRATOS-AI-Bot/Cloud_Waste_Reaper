
import os
import json
import boto3
import argparse
from datetime import datetime

def get_ebs_volumes(ec2, region):
    ebs_volumes = ec2.describe_volumes(
        Filters=[{'Name': 'status', 'Values': ['available']}]
    )['Volumes']
    return ebs_volumes

def get_ec2_instances(ec2, region):
    ec2_instances = ec2.describe_instances()
    return ec2_instances['Reservations']

def get_s3_buckets(s3, region):
    s3_buckets = s3.list_buckets()
    return s3_buckets['Buckets']

def get_dynamodb_tables(dynamodb, region):
    dynamodb_tables = dynamodb.list_tables()
    return dynamodb_tables['TableNames']

def calculate_savings(ebs_volumes):
    total_savings = 0
    for volume in ebs_volumes:
        size = volume['Size']
        total_savings += size * 0.10
    return total_savings

def lambda_handler(event, context):
    region = os.environ.get('AWS_REGION', 'ap-south-1')
    ec2 = boto3.client('ec2', region_name=region)
    s3 = boto3.client('s3', region_name=region)
    dynamodb = boto3.client('dynamodb', region_name=region)
    ses = boto3.client('ses', region_name=region)

    parser = argparse.ArgumentParser()
    parser.add_argument('--scan-ebs', action='store_true')
    parser.add_argument('--delete-ebs')
    parser.add_argument('--delete-all-ebs', action='store_true')
    parser.add_argument('--scan-ec2', action='store_true')
    parser.add_argument('--delete-ec2')
    parser.add_argument('--delete-all-ec2', action='store_true')
    parser.add_argument('--scan-s3', action='store_true')
    parser.add_argument('--delete-s3')
    parser.add_argument('--scan-dynamo', action='store_true')
    parser.add_argument('--delete-dynamo')
    parser.add_argument('--delete-all-dynamo', action='store_true')
    parser.add_argument('--scan-all', action='store_true')
    parser.add_argument('--region')
    args = parser.parse_args(['--scan-all'])

    report_body = ''
    if args.scan_all:
        ebs_volumes = get_ebs_volumes(ec2, region)
        ec2_instances = get_ec2_instances(ec2, region)
        s3_buckets = get_s3_buckets(s3, region)
        dynamodb_tables = get_dynamodb_tables(dynamodb, region)

        report_body += 'EBS Volumes:\n'
        report_body += 'ID | Size(GB) | Type | Cost($) | Created\n'
        for volume in ebs_volumes:
            size = volume['Size']
            volume_type = volume['VolumeType']
            created = volume['CreateTime']
            cost = size * 0.10
            report_body += f'{volume["VolumeId"]} | {size} | {volume_type} | {cost} | {created}\n'
        report_body += '\n'

        report_body += 'EC2 Instances:\n'
        report_body += 'ID | Type | State\n'
        for reservation in ec2_instances:
            for instance in reservation['Instances']:
                instance_id = instance['InstanceId']
                instance_type = instance['InstanceType']
                state = instance['State']['Name']
                report_body += f'{instance_id} | {instance_type} | {state}\n'
        report_body += '\n'

        report_body += 'S3 Buckets:\n'
        report_body += 'Name | Creation Date\n'
        for bucket in s3_buckets:
            bucket_name = bucket['Name']
            creation_date = bucket['CreationDate']
            report_body += f'{bucket_name} | {creation_date}\n'
        report_body += '\n'

        report_body += 'DynamoDB Tables:\n'
        report_body += 'Name\n'
        for table in dynamodb_tables:
            report_body += f'{table}\n'
        report_body += '\n'

        total_savings = calculate_savings(ebs_volumes)
        report_body += f'TOTAL WASTED CASH: ${total_savings:.2f}'

    ses_recipient = os.environ.get('SES_RECIPIENT')
    if ses_recipient:
        ses.send_email(
            Source='dakshsawhney2@gmail.com',
            Destination={'ToAddresses': [ses_recipient]},
            Message={
                'Body': {
                    'Text': {
                        'Data': report_body
                    }
                },
                'Subject': 'Cloud Waste Report'
            }
        )

    return {
        'statusCode': 200,
        'body': json.dumps({'report': report_body})
    }
