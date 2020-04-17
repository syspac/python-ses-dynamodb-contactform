import boto3
from botocore.exceptions import ClientError
import json
import os
import time
import uuid
import decimal

client = boto3.client('ses', region_name=os.environ['SES_REGION'])
sender = os.environ['SENDER_EMAIL']
subject = os.environ['EMAIL_SUBJECT']
configset = os.environ['CONFIG_SET']
charset = 'UTF-8'

dynamodb = boto3.resource('dynamodb')

BASE_HEADERS = {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Credentials": True,
    "Access-Control-Allow-Methods": 'GET, OPTIONS',
    "Access-Control-Allow-Headers": 'Content-Type, Authorization, Accept',
    "Cache-Control": 'private, max-age=3600'
}

def sendMail(event, context):

    try:
        #print(event)
        data = event['body']
        # {
        #     "firstname": "Chris",
        #     "lastname": "Belfield",
        #     "email": "chris@belfield.org",
        #     "message": "sdfsdff"
        # }
        # Broke needs to be fixed
        #content = 'Sender Email: ' + data['email'] + ',<br> FullName: ' + data['firstname'] + ',<br> Form Type: ' + data['type'] + ',<br> Message Contents: ' + data['message']
        # saveToDynamoDB(data)
        # response = sendMailToUser(data, content)
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        print("Email sent! Message Id:"),
        #print(response['MessageId'])
    
    return {
        "statusCode": 200,
        "body": "saved",
        'headers': BASE_HEADERS
    }


def list(event, context):
    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])

    # fetch all records from database
    result = table.scan()

    #return response
    return {
        "statusCode": 200,
        "body": result['Items']
    }

def saveToDynamoDB(data):
    timestamp = int(time.time() * 1000)
    # Insert details into DynamoDB Table
    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])
    item = {
        'id': str(uuid.uuid1()),
        'fullname': data['fullname'],
        'email': data['email'],
        'type': data['type'],
        'message': data['message'],
        'createdAt': timestamp,
        'updatedAt': timestamp
    }
    table.put_item(Item=item)
    return

def sendMailToUser(data, content):
    # Send Email using SES
    return client.send_email(
        Source=sender,
        Destination={
            'ToAddresses': [
                sender,
            ],
        },
        Message={
            'Subject': {
                'Charset': charset,
                'Data': subject
            },
            'Body': {
                'Html': {
                    'Charset': charset,
                    'Data': content
                }
            }
        }
    )
