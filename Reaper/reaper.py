
import os
import json
import boto3
import argparse
from datetime import datetime
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
    ebs = boto3.client('ec2')
    volumes = ebs.describe_volumes(Filters=[{'Name': 'status', 'Values': ['available']}])
    data = []
    total_savings = 0
    for volume in volumes['Volumes']:
        size = volume['Size']
        cost = size * 0.10
        total_savings += cost
        data.append([volume['VolumeId'], size, volume['VolumeType'], cost, volume['CreateTime']])
    return data, total_savings

def scan_ec2_instances():
    ec2 = boto3.client('ec2')
    instances = ec2.describe_instances()
    data = []
    for reservation in instances['Reservations']:
        for instance in reservation['Instances']:
            data.append([instance['InstanceId'], instance['InstanceType'], instance['State']['Name']])
    return data

def scan_s3_buckets():
    s3 = boto3.client('s3')
    buckets = s3.list_buckets()
    data = []
    for bucket in buckets['Buckets']:
        data.append([bucket['Name'], bucket['CreationDate']])
    return data

def scan_dynamodb_tables():
    dynamodb = boto3.client('dynamodb')
    tables = dynamodb.list_tables()
    data = []
    for table in tables['TableNames']:
        data.append([table])
    return data

def scan_all_resources():
    ebs_data, total_savings = scan_ebs_volumes()
    ec2_data = scan_ec2_instances()
    s3_data = scan_s3_buckets()
    dynamodb_data = scan_dynamodb_tables()
    
    report = ""
    report += "EBS Volumes:\n"
    report += print_table(["ID", "Size(GB)", "Type", "Cost($)", "Created"], ebs_data)
    report += "\nTOTAL WASTED CASH: **${:.2f}**\n\n".format(total_savings)
    
    report += "EC2 Instances:\n"
    report += print_table(["ID", "Type", "State"], ec2_data)
    report += "\n\n"
    
    report += "S3 Buckets:\n"
    report += print_table(["Name", "Created"], s3_data)
    report += "\n\n"
    
    report += "DynamoDB Tables:\n"
    report += print_table(["Name"], dynamodb_data)
    report += "\n\n"
    
    return report

def send_email_report(body):
    recipient = os.environ.get('SES_RECIPIENT')
    if recipient:
        ses = boto3.client('ses')
        try:
            ses.send_email(
                Source='dakshsawhney2@gmail.com',
                Destination={'ToAddresses': [recipient]},
                Message={
                    'Body': {
                        'Text': {
                            'Data': body,
                            'Charset': 'utf-8'
                        }
                    },
                    'Subject': {
                        'Data': 'Cloud Waste Report',
                        'Charset': 'utf-8'
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
        'body': json.dumps('Report sent successfully')
    }

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Cloud Waste Reaper')
    parser.add_argument('--scan-all', action='store_true', help='Scan all resources')
    parser.add_argument('--scan-ebs', action='store_true', help='Scan EBS volumes')
    parser.add_argument('--scan-ec2', action='store_true', help='Scan EC2 instances')
    parser.add_argument('--scan-s3', action='store_true', help='Scan S3 buckets')
    parser.add_argument('--scan-dynamodb', action='store_true', help='Scan DynamoDB tables')
    args = parser.parse_args()
    
    if args.scan_all:
        print(scan_all_resources())
    elif args.scan_ebs:
        ebs_data, total_savings = scan_ebs_volumes()
        print(print_table(["ID", "Size(GB)", "Type", "Cost($)", "Created"], ebs_data))
        print("\nTOTAL WASTED CASH: **${:.2f}**".format(total_savings))
    elif args.scan_ec2:
        ec2_data = scan_ec2_instances()
        print(print_table(["ID", "Type", "State"], ec2_data))
    elif args.scan_s3:
        s3_data = scan_s3_buckets()
        print(print_table(["Name", "Created"], s3_data))
    elif args.scan_dynamodb:
        dynamodb_data = scan_dynamodb_tables()
        print(print_table(["Name"], dynamodb_data))
