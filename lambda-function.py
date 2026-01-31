
import os
import json
import boto3
import argparse
from datetime import datetime
import urllib.request
import urllib.parse

try:
    from tabulate import tabulate
    HAS_TABULATE = True
except ImportError:
    HAS_TABULATE = False

def print_table(headers, data):
    if HAS_TABULATE:
        return tabulate(data, headers, tablefmt="grid")
    else:
        table = ""
        table += "| " + " | ".join(headers) + " |\n"
        table += "| " + " | ".join(["---"] * len(headers)) + " |\n"
        for row in data:
            table += "| " + " | ".join(map(str, row)) + " |\n"
        return table

def scan_ebs_volumes():
    ebs_client = boto3.client('ec2')
    volumes = ebs_client.describe_volumes(
        Filters=[{'Name': 'status', 'Values': ['available']}]
    )['Volumes']
    data = []
    total_savings = 0
    for volume in volumes:
        size = volume['Size']
        volume_id = volume['VolumeId']
        volume_type = volume['VolumeType']
        created = volume['CreateTime']
        cost = size * 0.10
        total_savings += cost
        data.append([volume_id, size, volume_type, cost, created])
    return data, total_savings

def scan_ec2_instances():
    ec2_client = boto3.client('ec2')
    instances = ec2_client.describe_instances()
    data = []
    for reservation in instances['Reservations']:
        for instance in reservation['Instances']:
            instance_id = instance['InstanceId']
            instance_type = instance['InstanceType']
            data.append([instance_id, instance_type])
    return data

def scan_s3_buckets():
    s3_client = boto3.client('s3')
    buckets = s3_client.list_buckets()
    data = []
    for bucket in buckets['Buckets']:
        bucket_name = bucket['Name']
        created = bucket['CreationDate']
        data.append([bucket_name, created])
    return data

def scan_dynamodb_tables():
    dynamodb_client = boto3.client('dynamodb')
    tables = dynamodb_client.list_tables()
    data = []
    for table_name in tables['TableNames']:
        table = dynamodb_client.describe_table(TableName=table_name)
        created = table['Table']['CreationDateTime']
        data.append([table_name, created])
    return data

def scan_all_resources():
    ebs_data, total_savings = scan_ebs_volumes()
    ec2_data = scan_ec2_instances()
    s3_data = scan_s3_buckets()
    dynamodb_data = scan_dynamodb_tables()
    report = ""
    report += "EBS Volumes:\n"
    report += print_table(['ID', 'Size(GB)', 'Type', 'Cost($)', 'Created'], ebs_data) + "\n"
    report += f"TOTAL WASTED CASH: ${total_savings:.2f}\n\n"
    report += "EC2 Instances:\n"
    report += print_table(['ID', 'Type'], ec2_data) + "\n\n"
    report += "S3 Buckets:\n"
    report += print_table(['Name', 'Created'], s3_data) + "\n\n"
    report += "DynamoDB Tables:\n"
    report += print_table(['Name', 'Created'], dynamodb_data) + "\n"
    return report

def send_email_report(body):
    ses_client = boto3.client('ses')
    recipient = os.environ.get('SES_RECIPIENT')
    if recipient:
        try:
            ses_client.send_email(
                Source='dakshsawhney2@gmail.com',
                Destination={'ToAddresses': [recipient]},
                Message={
                    'Body': {
                        'Text': {
                            'Data': body
                        }
                    },
                    'Subject': {
                        'Data': 'Cloud Waste Report'
                    }
                }
            )
        except Exception as e:
            print(f"Error sending email: {e}")

def lambda_handler(event, context):
    report = scan_all_resources()
    send_email_report(report)
    return {
        'statusCode': 200,
        'body': json.dumps({'message': 'Report sent successfully'})
    }

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--scan-all', action='store_true')
    args = parser.parse_args()
    if args.scan_all:
        report = scan_all_resources()
        print(report)
