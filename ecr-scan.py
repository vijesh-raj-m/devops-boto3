from datetime import datetime
from logging import getLogger, INFO
import json
import os
from botocore.exceptions import ClientError
import boto3
sns = boto3.client('sns')
ecr = boto3.client('ecr')
import pprint
snsTopicArn = os.environ['TopicArn']
def lambda_handler(event, context):
    scandetails = event['detail']
    ecrreponame = scandetails['repository-name']
    awsaccount = event['account']
    region = event['region']
    imagedigest = scandetails['image-digest']
    url = 'https://console.aws.amazon.com/ecr/repositories/{0}/image/{1}/scan-results?region={2}'.format(ecrreponame,imagedigest,region)
    scanreport = scandetails['finding-severity-counts']
    if all(key in scanreport for key in ('HIGH', 'CRITICAL', 'MEDIUM')):
        sns_response = sns.publish(
        TopicArn=snsTopicArn,
        Message="Vulnerabilities found in docker images scanned from ECR repository, please find more details below.\nRepository Name - {0}.\nAWS AccountID - {1}.\nScan findings - {2}.\nFor detailed scan report please visit {3}".format(ecrreponame,awsaccount,scanreport,url))
    else:
        sns_response = sns.publish(
        TopicArn=snsTopicArn,
        Message="No Critical Vulnerabilities found in docker images scanned from ECR repository, please find more details below.\nRepository Name - {0}.\nAWS AccountID - {1}.\nFor detailed scan report please visit {2}".format(ecrreponame,awsaccount,url))




