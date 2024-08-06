""" Use Case: Logging in.
    Users: All
    Type: POST
    Endpoint: ./login
    Provide in request:
        Query string:
        Header:
        Body:
        {
            "UserID": "",
            "Type": "",
            "Password": ""
        }
    TODO:
        Check if user exists
        Check password
        Check type
        Send success or failure message
    Response:
        String - message (check status code to see if logged in)

"""

import json
import boto3

client = boto3.client('dynamodb')

def lambda_handler(event, context):
    userid = event["UserID"]
    type = event["Type"]
    password = event["Password"]
    corsheaders = {
          "Access-Control-Allow-Credentials": "true",
          "Access-Control-Allow-Headers": "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token",
          "Access-Control-Allow-Methods": "OPTIONS,POST",
          "Access-Control-Allow-Origin": "*",
          "Content-Type": "application/json"
    }
    
    #look for user
    user_item = client.get_item(
        TableName='Users',
        Key={
            'Type': {
                'S': type,
            },
            'UserID': {
                'S': userid        
            }
        }
    )
    #if user found
    if ('Item' in user_item):
        #get password
        pw = user_item['Item'].get('Password', {'S': ''}).get('S', '')
        #if password matches
        if password == pw:
            return {
                'statusCode': 200,
                'headers': corsheaders,
                'body': json.dumps(f'Login success!')
            }
        #if password does not match
        else:
            return {
                'statusCode': 400,
                'headers': corsheaders,
                'body': json.dumps(f'Login failed: incorrect credentials')
            }
    #if user is not found with their chosen type
    else:
        return {
            #should not reach
            'statusCode': 400,
            'headers': corsheaders,
            'body': json.dumps(f'Login failed: user not found or authorized')
        }