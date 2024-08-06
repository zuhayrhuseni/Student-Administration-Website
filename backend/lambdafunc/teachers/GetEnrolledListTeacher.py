""" Use case:   Automatically display list of enrolled courses to teachers.
    Users: Teachers
    Type: GET
    Endpoint: ./teacherhomepage/enrollment
    Provide in request:
        Query String:
            UserID=___
    TODO:
        Return list of courses teacher is assigned to
    Respons to 200: List of course-id-section
        [SUBJ 1234-1]
    Response otherwise:
        String detailing error
"""

import json
import boto3

client = boto3.client('dynamodb')

def lambda_handler(event, context):
    userid = event["UserID"]
    corsheaders = {
        "Access-Control-Allow-Headers": "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token",
        "Access-Control-Allow-Methods": "GET,OPTIONS",
        "Access-Control-Allow-Origin": "*",
        "Content-Type": "application/json"
    }

    #find user
    user_item = client.get_item(
        TableName='Users',
        Key={
            'Type': {
                'S': 'Teacher',
            },
            'UserID': {
                'S': userid        
            }
        }
    )
    if ('Item' in user_item):
        #get enrollment
        enrollment = user_item['Item'].get('Enrollment', {'L': []}).get('L', [])
        returnlist = []
        for cid in enrollment:
            returnlist.append(cid.get('S', ''))
        return {
            'statusCode': 200,
            'headers': corsheaders,
            'body': returnlist
        }
    else:
        return {
            #should not reach
            'statusCode': 400,
            'headers': corsheaders,
            'body': json.dumps(f'User not found')
        }