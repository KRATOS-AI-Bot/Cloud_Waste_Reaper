
import os
import json
import argparse
import boto3
from botocore.exceptions import ClientError
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

def calculate_ebs_cost(ebs_volumes):
    total_cost = 0
    ebs_report = []
    for volume in ebs_volumes:
        size = volume['Size']
        cost = size * 0.10
        total_cost += cost
        ebs_report.append({
            'ID': volume['VolumeId'],
            'Size(GB)': size,
            'Type': volume['VolumeType'],
            'Cost($)': cost,
            'Created': volume['CreateTime']
        })
    return ebs_report, total_cost

def lambda_handler(event, context):
    region = os.environ.get('AWS_REGION', 'ap-south-1')
    ec2 = boto3.client('ec2', region_name=region)
    s3 = boto3.client('s3', region_name=region)
    dynamodb = boto3.client('dynamodb', region_name=region)
    ses = boto3.client('ses', region_name=region)
    report_body = ''
    if event.get('scan_all'):
        ebs_volumes = get_ebs_volumes(ec2, region)
        ebs_report, total_ebs_cost = calculate_ebs_cost(ebs_volumes)
        ec2_instances = get_ec2_instances(ec2, region)
        s3_buckets = get_s3_buckets(s3, region)
        dynamodb_tables = get_dynamodb_tables(dynamodb, region)
        report_body += 'EBS Volumes:\n'
        for ebs in ebs_report:
            report_body += f"ID: {ebs['ID']}, Size(GB): {ebs['Size(GB)']}, Type: {ebs['Type']}, Cost($): {ebs['Cost($)']}, Created: {ebs['Created']}\n"
        report_body += f'Total EBS Cost: ${total_ebs_cost:.2f}\n\n'
        report_body += 'EC2 Instances:\n'
        for instance in ec2_instances:
            report_body += f"ID: {instance['Instances'][0]['InstanceId']}\n"
        report_body += '\n'
        report_body += 'S3 Buckets:\n'
        for bucket in s3_buckets:
            report_body += f"Name: {bucket['Name']}\n"
        report_body += '\n'
        report_body += 'DynamoDB Tables:\n'
        for table in dynamodb_tables:
            report_body += f"Name: {table}\n"
        report_body += '\n'
        ses_recipient = os.environ.get('SES_RECIPIENT')
        if ses_recipient:
            try:
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
            except ClientError as e:
                print(e)
    return {
        'statusCode': 200,
        'body': report_body
    }

def main():
    parser = argparse.ArgumentParser(description='Cloud Waste Reaper')
    parser.add_argument('--scan-ebs', action='store_true', help='Scan for EBS volumes')
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
    parser.add_argument('--scan-all', action='store_true', help='Scan all resources')
    parser.add_argument('--region', default='ap-south-1', help='AWS region')
    args = parser.parse_args()
    region = args.region
    ec2 = boto3.client('ec2', region_name=region)
    s3 = boto3.client('s3', region_name=region)
    dynamodb = boto3.client('dynamodb', region_name=region)
    if args.scan_ebs:
        ebs_volumes = get_ebs_volumes(ec2, region)
        ebs_report, total_ebs_cost = calculate_ebs_cost(ebs_volumes)
        print('EBS Volumes:')
        from tabulate import tabulate
        print(tabulate(ebs_report, headers='keys', tablefmt='psql'))
        print(f'Total EBS Cost: ${total_ebs_cost:.2f}')
    elif args.scan_ec2:
        ec2_instances = get_ec2_instances(ec2, region)
        print('EC2 Instances:')
        for instance in ec2_instances:
            print(instance['Instances'][0]['InstanceId'])
    elif args.scan_s3:
        s3_buckets = get_s3_buckets(s3, region)
        print('S3 Buckets:')
        for bucket in s3_buckets:
            print(bucket['Name'])
    elif args.scan_dynamo:
        dynamodb_tables = get_dynamodb_tables(dynamodb, region)
        print('DynamoDB Tables:')
        for table in dynamodb_tables:
            print(table)
    elif args.scan_all:
        ebs_volumes = get_ebs_volumes(ec2, region)
        ebs_report, total_ebs_cost = calculate_ebs_cost(ebs_volumes)
        ec2_instances = get_ec2_instances(ec2, region)
        s3_buckets = get_s3_buckets(s3, region)
        dynamodb_tables = get_dynamodb_tables(dynamodb, region)
        print('EBS Volumes:')
        from tabulate import tabulate
        print(tabulate(ebs_report, headers='keys', tablefmt='psql'))
        print(f'Total EBS Cost: ${total_ebs_cost:.2f}\n')
        print('EC2 Instances:')
        for instance in ec2_instances:
            print(instance['Instances'][0]['InstanceId'])
        print('\n')
        print('S3 Buckets:')
        for bucket in s3_buckets:
            print(bucket['Name'])
        print('\n')
        print('DynamoDB Tables:')
        for table in dynamodb_tables:
            print(table)

if __name__ == '__main__':
    main()
