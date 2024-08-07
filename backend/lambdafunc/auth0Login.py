""" Use Case: After the user has signedup with Auth0, their information should be added to the database.
    Users: All
    Type: POST
    Endpoint: ./auth0Login
    Provide in request:
        Query string:
        Header:
        Body:
        {
            "UserID": "",       //this is username - could be anything now
            "Type": "",
            "Name": "",
        }
    TODO:
        Check if user exists in DB
        If they do not exist, add them
    Response:
        String - message (User found, user created, error)
"""

import json
import boto3

client = boto3.client('dynamodb')

def lambda_handler(event, context):
    try:
        UserID = event["UserID"]
        Type = event["Type"]
        Name = event["Name"]
        corsheaders = {
            "Access-Control-Allow-Headers": "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token",
            "Access-Control-Allow-Methods": "OPTIONS,POST",
            "Access-Control-Allow-Origin": "*",
            "Content-Type": "application/json"
        }

        #Check if the user already exists in the database
        user_item = client.get_item(
            TableName='Users',
            Key={
                'Type': {
                    'S': Type,
                },
                'UserID': {
                    'S': UserID        
                }
            }
        )
        existing_user = user_item.get('Item')

        #If the user does not exist, insert them into the database
        if not existing_user:
            client.put_item(
            TableName='Users',
            Item={
                'Type': {
                    'S': Type,
                },
                'UserID': {
                    'S': UserID      
                },
                'Name': {
                    'S': Name,        
                },
            }
            )
            return {
                'statusCode': 200,
                'headers': corsheaders,
                'body': json.dumps(f'New user: {UserID}'),
            }
        #If the user already exists, do not update the information
        return {
            'statusCode': 200,
            'headers': corsheaders,
            'body': json.dumps(f"User found: {UserID}"),
        }
    #catch errors
    except Exception as e:
        print(f'Error: {e}')
        return {
            'statusCode': 500,
            'headers': corsheaders,
            'body': json.dumps({'message': 'Internal Server Error'}),
        }