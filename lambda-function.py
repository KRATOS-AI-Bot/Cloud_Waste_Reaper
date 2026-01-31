
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
    total_cost = 0
    for volume in volumes:
        size = volume['Size']
        volume_type = volume['VolumeType']
        cost = size * 0.10
        total_cost += cost
        data.append([volume['VolumeId'], size, volume_type, cost, volume['CreateTime']])
    return data, total_cost

def scan_ec2_instances():
    ec2_client = boto3.client('ec2')
    instances = ec2_client.describe_instances()
    data = []
    for reservation in instances['Reservations']:
        for instance in reservation['Instances']:
            data.append([instance['InstanceId'], instance['InstanceType'], instance['State']['Name']])
    return data

def scan_s3_buckets():
    s3_client = boto3.client('s3')
    buckets = s3_client.list_buckets()
    data = []
    for bucket in buckets['Buckets']:
        data.append([bucket['Name'], bucket['CreationDate']])
    return data

def scan_dynamodb_tables():
    dynamodb_client = boto3.client('dynamodb')
    tables = dynamodb_client.list_tables()
    data = []
    for table in tables['TableNames']:
        data.append([table])
    return data

def scan_all_resources():
    ebs_data, ebs_total_cost = scan_ebs_volumes()
    ec2_data = scan_ec2_instances()
    s3_data = scan_s3_buckets()
    dynamodb_data = scan_dynamodb_tables()
    report = ""
    report += "EBS Volumes:\n"
    report += print_table(["ID", "Size(GB)", "Type", "Cost($)", "Created"], ebs_data)
    report += "\nTOTAL WASTED CASH: **${:.2f}**\n\n".format(ebs_total_cost)
    report += "EC2 Instances:\n"
    report += print_table(["ID", "Type", "State"], ec2_data)
    report += "\n\n"
    report += "S3 Buckets:\n"
    report += print_table(["Name", "Created"], s3_data)
    report += "\n\n"
    report += "DynamoDB Tables:\n"
    report += print_table(["Name"], dynamodb_data)
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
            print("Error sending email: {}".format(e))

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
